# Blueprint #1: Email Triage - Sorting 90% of the Inbox Locally for $0.00

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

A **90/10 Local-First Hybrid Router** keeps 90% of routine email 100% on-device while escalating only high-stakes legal/contract threads:

```text
+-----------------------------------------------------------------------------------+
|                     INCOMING EMAIL / LOCAL SQLITE MAIL ARCHIVE                    |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                             COMPLEXITY HEURISTIC CHECK                            |
|  Is bodyText > 8,000 chars OR replies > 10 OR subject contains "legal"/"contract"?|
+--------------------+----------------------------------------------+---------------+
                     | NO (90% of Inbox Volume)                     | YES (10% High-Stakes)
                     v                                              v
+--------------------------------------------+   +----------------------------------+
|     TIER 1: 100% LOCAL METAL INFERENCE     |   |   TIER 2: OPTIONAL ESCALATION    |
|  * Model: gemma2:2b / llama3.2:1b          |   |  * Handles multi-page contracts  |
|  * Speed: 120-166 tok/s (~0.5s/email)      |   |    & 15-message legal redlines   |
|  * Output: Strict JSON (summary, category, |   |  * Cost: Only 10% of volume      |
|    urgency, replySuggestions)              |   +----------------------------------+
|  * Cost: $0.00 | Zero External Egress      |
+--------------------+-----------------------+
                     |
                     v
+-----------------------------------------------------------------------------------+
|                        HUMAN-IN-THE-LOOP APPROVAL STAGING                         |
|  * Pre-stages 2 to 3 short, ready-to-send reply options                           |
|  * Waits for human one-click or spoken "approve" before sending                   |
+-----------------------------------------------------------------------------------+
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

## 4. Three Practical Rules for Business Email AI

1. **Don't Use a Massive Cloud Model to Sort the Mail**: 90% of a business inbox consists of invoices, calendar updates, receipts, and short questions. A `1.2B` to `2.6B` local model in JSON mode (`format: "json"`) hits **96% to 100% accuracy** in under a second at **$0.00 cost**.
2. **Use a Simple Rule for High-Stakes Escalation**: A 5-line check (`bodyText.length > 8000 || subject.includes('legal') || subject.includes('contract')`) flags complex legal redlines while keeping 90% of routine company email private on local disk.
3. **Never Auto-Send Without Human Sign-Off**: Let the local model pre-draft the reply options in the background so a human can review and send in one click.
