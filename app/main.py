# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""Live Chat UI — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "Live Chat UI"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(USE_CASE)


import uuid
from sse_starlette.sse import EventSourceResponse
from poc_core.sse import format_sse

generations: dict[str, list[str]] = {}

class StreamIn(BaseModel):
    prompt: str

@app.post("/stream")
async def stream(body: StreamIn):
    gid = f"g_{uuid.uuid4().hex[:8]}"
    generations[gid] = []

    async def gen():
        yield format_sse("meta", {"generation_id": gid})
        seq = 0
        async for tok in llm.stream(body.prompt, max_tokens=20):
            seq += 1
            generations[gid].append(tok)
            yield format_sse("token", {"seq": seq, "text": tok}, str(seq))
        yield format_sse("done", {"generation_id": gid, "finish_reason": "stop"})

    return EventSourceResponse(gen())

@app.get("/resume/{generation_id}")
def resume(generation_id: str, after_seq: int = 0):
    toks = generations.get(generation_id)
    if toks is None:
        raise HTTPException(410, detail="generation expired")
    return {"generation_id": generation_id, "tokens": toks[after_seq:]}
