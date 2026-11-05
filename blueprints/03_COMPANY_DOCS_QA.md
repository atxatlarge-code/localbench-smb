# Blueprint #3: Company Docs Q&A: Local Markdown & SQLite Search Without Cloud Silos

**Pillar**: `#3. Company Docs Q&A` (`03_company_docs`)  
**Vertical**: Law Firms, Agencies, Consultancies, Medical Practices & Operations Teams  
**Hardware Reference**: Apple Silicon Mac (8 GB to 64 GB Unified Memory)  
**Replaces Cloud Cost**: $30/seat/month Cloud "Second Brain" & Knowledge Base SaaS Wrappers (Notion AI, Mem)

---

## 1. The Business Problem: Locked Silos & Outdated Draft Hallucinations

Every business builds up critical knowledge across client contracts, SOWs, pricing sheets, and employee handbooks. Yet cloud "Second Brain" SaaS wrappers create two headaches:
1. **Proprietary Silos & Monthly Rent**: Cloud platforms lock company notes inside proprietary databases and charge $30/seat/month just to run an AI search box over your own files.
2. **Draft vs. Signed Confusion**: In a real company folder, there is almost always an older *Draft Proposal* sitting next to the *Signed Master Agreement*. Basic RAG pipelines pull both files and give the wrong, outdated numbers.

---

## 2. How the Local Solution Works

All company knowledge stays in plain `.md` files on local disk, indexed in under 2 milliseconds using **`SQLite FTS5`**, and resolved locally on `127.0.0.1`:

```text
+-----------------------------------------------------------------------------------+
|               LOCAL MARKDOWN FOLDER (Plain .md Files on Local Disk)               |
|  * clients/apex_draft_sep2026.md (DRAFT - SUPERSEDED: $3,200/mo, 60m SLA)         |
|  * clients/apex_sla_oct2026_signed.md (SIGNED & ACTIVE: $4,800/mo, 15m SLA)       |
|  * ops/inventory.md (Unrelated office hardware note)                              |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|             STAGE 1: INSTANT SQLITE FTS5 SEARCH (<2ms, 0.0 KB/s Egress)           |
|  * CREATE VIRTUAL TABLE notes_fts USING fts5(rel_path, title, content)            |
|  * Instant keyword & phrase ranking across thousands of local Markdown notes      |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|           STAGE 2: LOCAL FACT EXTRACTION & DRAFT FILTERING (0.38s-0.66s)          |
|  * Local 1.2B to 2.6B model reads top matches and ignores superseded drafts       |
|  * Emits clean JSON: {"active_note": "...signed.md", "monthly_retainer_usd":      |
|    4800, "response_sla_minutes": 15, "contact": "Sarah Chen"}                     |
+-----------------------------------------------------------------------------------+
```

---

## 3. Benchmark Results (`03_company_docs`)

Across all 5 document lookup cases (signed client SLA vs. draft, active 2026 refund SOP vs. archived 2024 SOP, active PTO policy vs. old handbook, approved migration budget vs. rejected pitch, and active v2 DB runbook vs. deprecated v1):

| Local Model | Company Docs Score | End-to-End Latency | Speed (`tok/s`) | Cloud Data Egress |
| :--- | :---: | :---: | :---: | :---: |
| **`qwen2.5-coder:1.5b`** | **100%** (5/5) | **0.39s** | **131+ tok/s** | `0.0 KB/s` |
| **`llama3.2:1b`** | **100%** (5/5) | **0.36s** | **166+ tok/s** | `0.0 KB/s` |
| **`gemma2:2b`** | **100%** (5/5) | **0.66s** | **120+ tok/s** | `0.0 KB/s` |
| **`dolphin-llama3:8b`** | **100%** (5/5) | **0.95s** | **49+ tok/s** | `0.0 KB/s` |

---

## 4. Three Practical Rules for Company Knowledge Bases

1. **Own Your File Formats (`Markdown` + `SQLite`)**: Never lock company SOPs and contracts inside a proprietary cloud database. Plain `.md` files indexed into `SQLite FTS5` search in under 2 milliseconds and will still be readable 20 years from now.
2. **Mark Document Status at the Top of Every File**: Adding `Status: ACTIVE` vs. `Status: SUPERSEDED` in the top 5 lines of your Markdown files lets even a tiny `1B` local model hit **100% accuracy** in `0.38 seconds`.
3. **Zero Cloud Egress by Default**: Because `SQLite FTS5` and local inference run strictly on `127.0.0.1`, private client contracts and retainer numbers never leave your machine.
