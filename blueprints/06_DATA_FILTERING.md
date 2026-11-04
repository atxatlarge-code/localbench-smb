# Blueprint #6: Data Filtering - Replacing Per-Row Cloud API Bills with Local Code Filters

**Pillar**: `#6. Data Filtering` (`06_data_filtering`)  
**Vertical**: Finance, Accounting, B2B Lead Ops, Real Estate & Back-Office Data Teams  
**Hardware Reference**: Apple Silicon Mac (16 GB to 64 GB Unified Memory)  
**Replaces Cloud Cost**: $150 to $450 per 100k rows in cloud LLM parsing bills & 14+ hours/day of API wait time

---

## 1. The Business Problem: The Per-Row Token & Latency Trap

Businesses regularly filter thousands of rows across vendor bills, CRM lead lists, aged accounts receivable, customer records, and weekly contractor timesheets.

When teams run these filters by sending every row to a cloud LLM:
1. **Per-Row API Bills Destroy Margins**: Sending 50,000 rows through a cloud API to check business rules and sum up dollar totals costs hundreds of dollars per run.
2. **The 14-Hour Wait Time**: Across 25,000+ daily row checks, a `1,800ms` cloud API round-trip adds **over 14 hours of network wait time and HTTP 429 rate-limit stalls per day**.
3. **Why Small Models Fail at Raw JSON Math**: Asking a non-thinking `1B` to `2.6B` model to output `{"qualified_ids": [...], "qualified_total": ...}` directly in JSON scores only **`25%`** because the model guesses the IDs before checking Rules #2 and #3.

---

## 2. How the Local Solution Works: Have the Model Write a 5-Line Python Filter

Instead of asking a small model to do mental math across JSON rows, the **Specialist Router (`tabular_code_sieve`)** asks a local `1.5B` code model to write a 5-line Python function (`def keep_record(r):`) from the business rules and executes that function in Python:

```text
+-----------------------------------------------------------------------------------+
|                        BUSINESS RULES + SAMPLE JSON RECORD                        |
|  1. Keep ONLY invoices where is_duplicate == false.                               |
|  2. Purge any invoice where billed_hourly_rate > contracted_hourly_rate.          |
|  3. Keep ONLY invoices with status == 'UNPAID'.                                   |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|            STAGE 1: LOCAL 1.5B WRITES PYTHON FILTER FUNCTION (~0.6s)              |
|    def keep_record(r: dict) -> bool:                                              |
|        return (                                                                   |
|            not r.get("is_duplicate")                                              |
|            and r.get("billed_hourly_rate", 0) <= r.get("contracted_hourly_rate",0)|
|            and r.get("status") == "UNPAID"                                        |
|        )                                                                          |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|               STAGE 2: EXACT PYTHON EXECUTION & DOLLAR SUM (<1ms)                 |
|  * Filters all rows in Python with 100% mathematical precision                    |
|  * Computes exact `qualified_ids`, `qualified_total`, and `rejected_count`        |
+-----------------------------------------------------------------------------------+
```

---

## 3. Benchmark Results (`06_data_filtering`)

Across all 5 spreadsheet filtering cases (residential account exemption filter, AP duplicate/overbilling audit, CRM lead DNC & personal-email purge, aged AR collections filter, and contractor timesheet overtime filter):

| Approach / Model | Data Filtering Score | Avg Speed | Dollar Math Precision | Cost per 100k Rows |
| :--- | :---: | :---: | :---: | :---: |
| **`localbench-router` (Code Filter)** | **100%** (5/5) | **148+ tok/s** | **100% (`+/- $0.00`)** | **$0.00** |
| **`gemma4-2b` (`<think>` Reasoning Mode)** | **100%** (5/5) | **68+ tok/s** | **100% (`+/- $0.00`)** | **$0.00** |
| **`dolphin-llama3:8b` (Raw JSON Prompting)** | 52% (2/5) | 49 tok/s | Fails multi-rule sums | $0.00 |
| **`qwen2.5-coder:1.5b` (Raw JSON Prompting)** | 25% (0/5) | 131 tok/s | Fails multi-rule sums | $0.00 |

---

## 4. Three Practical Rules for Spreadsheet & Record Filtering

1. **Write the Filter Once in Code, Run the Rows in Python**: Never ask an LLM to mentally filter and sum 10,000 rows in JSON. Have a `1.5B` local coder write `def keep_record(r):` once and let Python filter the rows in milliseconds for free.
2. **Or Use a `<think>` Model for Small Batches**: If you want direct JSON output on a small batch without running Python, use a model with a `<think>` scratchpad (`gemma4-2b`) so it evaluates every rule before emitting the final JSON.
3. **Audit 100% of Rows Locally**: Because local execution costs `$0.00`, you can check every single row before sending a report or paying a vendor batch.
