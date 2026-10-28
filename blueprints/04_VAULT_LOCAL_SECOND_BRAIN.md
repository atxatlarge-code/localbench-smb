# SMB AI Blueprint #4: Vault - Local Markdown & SQLite FTS5 Second-Brain Q&A (`127.0.0.1`)

**Vertical**: Law Firms, Agencies, Consultancies, Medical Practices & Executive Operations  
**Architecture Pattern**: **Plain-Text Markdown (`.md`) + In-Memory `SQLite FTS5` + Local JSON Extraction**  
**Hardware Reference**: Apple Silicon Mac (8 GB - 64 GB Unified Memory)  
**Fires Cloud Tax**: $30/seat/mo Cloud "Second Brain" & Knowledge Base SaaS Wrappers (Notion AI, Mem, Reflect Cloud)

---

## 1. The SMB Business Problem ("Locked Silos & Superseded Document Hallucinations")

Every SMB accumulates critical institutional knowledge across client agreements, SOWs, pricing addendums, and meeting notes. Yet cloud "Second Brain" SaaS wrappers create two problems:
1. **Proprietary Silos & Monthly Rent**: Cloud platforms lock company notes inside proprietary databases and charge $30/seat/month just to run an AI wrapper over your own files.
2. **Draft vs. Signed Hallucinations**: In a real business folder, there is almost always an older *Draft Proposal* sitting next to the *Signed Master Agreement*. Naive RAG pipelines retrieve both and hallucinate outdated pricing or SLA terms.

---

## 2. The Local AI Solution Architecture (`Vault` Track #4)

**Vault** (`Track #4`, based on `Hey Pal Mafia` Pal #02) keeps all company knowledge in open, portable `.md` files on disk, indexes them in milliseconds using **`SQLite FTS5`**, and resolves active vs. superseded facts locally on `127.0.0.1`:

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│               LOCAL MARKDOWN VAULT (Plain .md Files on Local Disk)                  │
│   • clients/apex_draft_sep2026.md (DRAFT - SUPERSEDED: $3,200/mo, 60m SLA)          │
│   • clients/apex_sla_oct2026_signed.md (SIGNED & ACTIVE: $4,800/mo, 15m SLA)        │
│   • ops/hardware_inventory.md (Unrelated office inventory note)                     │
└──────────────────────────────────────────┬──────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│             STAGE 1: EPHEMERAL SQLITE FTS5 INDEXING (<2ms, 0.0 KB/s Egress)         │
│  • CREATE VIRTUAL TABLE notes_fts USING fts5(rel_path, title, content)              │
│  • Instant BM25 ranked retrieval across thousands of local Markdown notes           │
└──────────────────────────────────────────┬──────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│           STAGE 2: LOCAL FACT EXTRACTION & DRAFT RESOLUTION (0.38s-0.42s)           │
│  • Local 1.5B-8B model reads top FTS5 matches, discards superseded September draft  │
│  • Emits verified JSON: {"active_note": "...signed.md", "monthly_retainer_usd":     │
│    4800, "response_sla_minutes": 15, "contact": "Sarah Chen"}                       │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Production Receipts & LocalBench SMB v1.0 Performance

Across the **LocalBench SMB v1.0** `04_vault_qa` track (resolving a signed October SLA against a superseded September draft via `SQLite FTS5`):

| Local Model | Vault Q&A Accuracy | End-to-End Latency | Speed (`tok/s`) | Cloud Data Egress |
| :--- | :---: | :---: | :---: | :---: |
| **`voicefi-coder:1.5b`** *(KV-Pinned)* | **100%** | **0.38s** | **183+ tok/s** | `0.0 KB/s` |
| **`voicefi-coder-mlx`** *(1.5B Metal LoRA)* | **100%** | **0.42s** | **168+ tok/s** | `0.0 KB/s` |
| **`qwen2.5-coder:1.5b`** *(1.5B Base)* | **100%** | **0.39s** | **182+ tok/s** | `0.0 KB/s` |
| **`gemma2:2b`** *(2.6B Edge)* | **100%** | **0.66s** | **119+ tok/s** | `0.0 KB/s` |

---

## 4. The 3 Repeatable Rules for Local Company Knowledge Bases

1. **Own Your Formats (`Markdown` + `SQLite`)**: Never lock company SOPs and client notes inside a proprietary cloud database. Plain `.md` files indexed into `SQLite FTS5` search in `<2ms` and will still be readable 20 years from now.
2. **Tag Document Status Explicitly in Markdown Headers**: Adding `Status: ACTIVE` vs. `Status: SUPERSEDED` in the top 5 lines of your Markdown templates allows even a compact `1.5B` local model to achieve **100% zero-hallucination accuracy** in `0.38 seconds`.
3. **Zero-Egress Compliance by Default**: Because `SQLite FTS5` and local inference bind strictly to `127.0.0.1`, sensitive client contracts and retainer figures never touch an external network socket.
