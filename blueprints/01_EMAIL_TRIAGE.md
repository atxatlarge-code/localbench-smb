# Blueprint #1: Email Triage - Sorting the Inbox Locally for $0.00

**Pillar**: `#1. Email Triage` (`01_email_triage`)  
**Vertical**: Horizontal Business Operations (Agencies, Legal/Accounting Practices, Executive Teams, Property Management)  
**Hardware Reference**: Apple Silicon Mac (16 GB to 64 GB Unified Memory)  
**Replaces Cloud Cost**: $30/seat/month AI email copilots & cloud inbox privacy leaks

---

## 1. The Business Problem: Inbox Overload vs. Cloud Privacy & Token Costs

Every small business drowns in email: vendor invoices, client status checks, scheduling threads, newsletters, and contract redlines. Yet businesses hit three roadblocks with cloud-only AI email tools:
1. **High Per-Seat SaaS & Token Costs**: Paying $30/user/month, or burning cloud API tokens on every newsletter, receipt, and 2-line status email across a 25-person company, costs $9,000+/year mostly to sort noise.
2. **Confidentiality & PII Exposure**: Law firms, medical offices, financial advisors, and dealmakers cannot stream their historical mail archive of client threads to third-party cloud APIs without risking client confidentiality.
3. **Rate-Limit Throttling on Backlogs**: Cloud email workers require artificial sleep delays between emails to avoid `HTTP 429` rate limits, turning an inbox backlog sync into a multi-hour crawl.

---

## 2. How the Local Solution Works

Every incoming email is **sorted 100% locally on `127.0.0.1` for $0.00**, separating routine operational threads from high-stakes legal/contract escalations:

```text
+-----------------------------------------------------------------------------------+
|                     INCOMING EMAIL / LOCAL SQLITE MAIL ARCHIVE                    |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                 STAGE 1: 100% LOCAL INBOX SORTING (127.0.0.1)                     |
|  * Model: gemma4-2b / gemma2:2b / llama3.2:1b                                     |
|  * Speed: 76-166 tok/s (~0.5s/email) | Cost: $0.00 | Zero External Egress         |
|  * Output: Strict JSON (summary, category, urgency, replySuggestions)             |
|  * Guardrail: Demotes fake-urgent cold outreach ("opt out"/"reply stop") to Low   |
+--------------------+----------------------------------------------+---------------+
                     | Routine Operational Mail                     | High-Stakes Legal / Billing
                     v                                              v
+--------------------------------------------+   +----------------------------------+
|     ROUTINE QUEUE (Fast One-Click Action)  |   |   HIGH-RISK ESCALATION QUEUE     |
|  * Vendor receipts, scheduling updates,    |   |  * Contract indemnification      |
|    inbound quote requests & newsletters    |   |    redlines & overdue disputes   |
|  * Surfaces 2-3 short next-step actions    |   |  * Flags High urgency for immediate|
|    (or hands off to Pillar #2 for full     |   |    human review before acting    |
|    outbound email drafting)                |   +----------------------------------+
+--------------------------------------------+
```

---

## 3. Benchmark Results (`01_email_triage`)

Across all 5 inbox scenarios (overdue vendor invoice, legal contract redline, warm 25-seat quote request, routine check-in reschedule, and cold marketing spam):

| Local Model | Email Triage Score | Latency per Email | Speed (`tok/s`) | 10,000-Email Backlog Cost |
| :--- | :---: | :---: | :---: | :---: |
| **`gemma2:2b`** | **100%** (5/5) | **~0.55s** | **120+ tok/s** | **$0.00** |
| **`gemma4-2b`** | **100%** (5/5) | **~0.62s** | **68+ tok/s** | **$0.00** |
| **`llama3.2:1b`** | **96%** (5/5) | **~0.42s** | **166+ tok/s** | **$0.00** |
| **`qwen2.5-coder:1.5b`** | **92%** (4/5) | **~0.48s** | **131+ tok/s** | **$0.00** |

---

## 4. Three Practical Rules for Business Email Triage

1. **Don't Use a Massive Cloud Model to Sort the Mail**: Most of a business inbox consists of invoices, calendar updates, receipts, and short questions. A `1.2B` to `2.6B` local model in JSON mode (`format: "json"`) hits **96% to 100% accuracy** in under a second at **$0.00 cost**.
2. **Demote Fake-Urgent Cold Outreach Automatically**: Cold sales pitches often stuff `"URGENT"` or exclamation marks into the subject line. A single guardrail rule checking for `"opt out"` or `"reply stop"` keeps marketing spam locked at `Newsletter` / `Low` urgency.
3. **Separate Triage (Pillar #1) from Full Outbound Drafting (Pillar #2)**: Let Pillar #1 sort the entire inbox and surface 1-sentence quick actions in ~0.5 seconds, then hand off threads that need a full multi-paragraph quote or SOW response to [Blueprint #2: Business Writing](02_BUSINESS_WRITING.md).
