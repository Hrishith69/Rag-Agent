# 📊 Support Ticket & Document Triage Agent — Evaluation Benchmark

## 🎯 Objective
To evaluate the reliability, routing accuracy, and latency of our LangChain-based triage agent across diverse query types.

## 🧪 Methodology
* **Dataset:** 20 structured test cases (`eval_dataset.json`) covering 4 categories:
  * `technical_docs`: Technical FastAPI documentation queries.
  * `ticket_triage`: Customer support ticket status lookups.
  * `general_chat`: Casual greetings and conversational filler.
  * `out_of_scope`: General knowledge questions outside the system's domain.
* **Model:** `gemini-3.1-flash-lite` (Temperature = 0)
* **Metrics Tracked:**
  * **Routing Accuracy %:** Percentage of times the agent selected the intended tool.
  * **Average Latency (s):** Mean time to retrieve data and generate a synthesized markdown response.

## 🏆 Benchmark Summary

| Metric | Result | Target | Status |
| :--- | :---: | :---: | :---: |
| **Total Test Cases** | 20 | 20 | ✅ Complete |
| **Routing Accuracy** | **100.0%** | > 85.0% | 🟢 Exceeded |
| **Average Latency** | **6.22s** | < 10.0s | 🟢 Exceeded |
| **Failed Routes** | 0 | 0 | 🟢 Pass |

## 🔍 Category Breakdown
1. **Technical Docs (8/8 Pass):** Accurately invoked `search_fastapi_docs` vector retrieval for path parameters, dependencies, async code, and request bodies.
2. **Ticket Triage (6/6 Pass):** Accurately invoked `check_ticket_status` database lookup for exact ticket IDs (e.g., TCK-101) and gracefully handled non-existent IDs.
3. **General Chat & Out of Scope (6/6 Pass):** Correctly bypassed database/vector searches to reply directly via `direct_answer`, saving system computation and latency.

## 💡 Engineering Takeaways
* **Temperature 0 Reliability:** Setting deterministic sampling (`temperature=0`) on Gemini ensured zero hallucinated tool calls.
* **Explicit Tool Descriptions:** Clear system prompt rules and well-defined docstrings on tools enabled 100% dynamic routing accuracy without manual intent classification models.