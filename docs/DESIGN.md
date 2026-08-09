# Design: Live Chat UI

**Project:** `live-chat-ui`  
**Parent system design:** [02 — Streaming Token Delivery](../02-streaming-token-delivery.md)

## 1. What this POC demonstrates

SSE token stream with `generation_id` + seq and a resume buffer for reconnects.

## 2. Architecture (POC)

```text
POST /stream → SSE meta/token/done
GET /resume/{id}?after_seq= → replay buffer
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| SSE event stream | HTTP-friendly one-way token delivery for chat UIs. | `EventSourceResponse` + `format_sse`. |
| generation_id + monotonic seq | Enables reconnect without duplicates/gaps. | In-memory `generations` map. |
| Short-lived resume buffer | Balances UX vs GPU/state cost. | `/resume` 410 when expired. |

## 4. Key endpoints

`GET /health`, `POST /stream`, `GET /resume/{generation_id}`

## 5. Tradeoffs / POC limits

Buffer is process-local; multi-instance needs Redis/shared log.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

> **Watch on YouTube:** [Live Chat Ui — System Design #Shorts](https://youtu.be/H9afr17REVc)
>
> Direct link: **https://youtu.be/H9afr17REVc**

Also available in-repo:
- GIF preview: [`video/design-overview.gif`](./video/design-overview.gif)
- MP4 download: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Narration script: [`video/narration.txt`](./video/narration.txt)

---

**Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.**  
Unauthorized copying or redistribution of this material is prohibited.  
GitHub: [Debashis2007](https://github.com/Debashis2007)

