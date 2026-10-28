# SMB AI Blueprint #3: Hey Pal — Local Workflow Builder & Verified Code Synthesis (`127.0.0.1`)

**Vertical**: Agencies, Software Shops, Consultants & Sovereign Desktop Operators  
**Architecture Pattern**: **"Map Once with AI, Execute in Code" + 3-Stage Deterministic AST SecGate**  
**Hardware Reference**: Apple Silicon Mac (16 GB – 64 GB Unified Memory, Metal GPU)  
**Bind Address**: `127.0.0.1` (`0.0 KB/s` External Egress)

---

## 1. The SMB Business Problem ("Rented Copilots & Unverified Agent Edits")

When small teams and operators automate repetitive business workflows (parsing vendor CSVs, calculating commissions, syncing databases), they hit two walls with cloud AI coding wrappers:
1. **Per-Seat SaaS Rent & IP Exposure**: Paying $20–$200/seat/month for cloud coding wrappers that stream proprietary business logic and internal schemas to third-party servers.
2. **Brittle Edits & "Reward Hacking"**: Generic LLMs frequently rewrite entire files, fail on edge-case inputs (such as division-by-zero or negative balances), or silently delete existing unit test assertions so the test suite appears to pass.

---

## 2. The Local AI Solution Architecture (`Hey Pal` Track #3)

**Hey Pal** (`Track #3`) runs 100% locally on `127.0.0.1`, pairing a KV-pinned or Direct-on-Metal `1.5B` coding model with a **3-Stage Deterministic AST Security Gate**:

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│             STAGE 1: SURGICAL SEARCH/REPLACE SYNTHESIS (127.0.0.1)                  │
│  • Direct-on-Metal 1.5B model (`voicefi-coder-mlx`) or KV-pinned `1.5B` Ollama      │
│  • Emits exact SEARCH/REPLACE diff blocks in 0.74s–0.87s at 168–183 tok/s           │
└──────────────────────────────────────────┬──────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│               STAGE 2: 3-STAGE ZERO-LLM AST & BOUNDARY SECGATE                      │
│  1. Syntax & Patch Gate: Applies diff cleanly and verifies `ast.parse()`            │
│  2. Anti-Reward-Hacking Gate: Counts parent vs. candidate AST `assert` nodes        │
│     (`2/2` preserved) so an agent can never pass tests by deleting assertions       │
│  3. Hidden Boundary Oracle: Executes unit tests + negative/zero edge-case probes    │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Production Receipts & LocalBench SMB v1.0 Performance

| Model | Track #3: `Hey Pal` Score | Synthesis Latency | Throughput | Assertions Preserved |
| :--- | :---: | :---: | :---: | :---: |
| **`voicefi-coder-mlx`** *(1.5B Metal LoRA)* | **100%** | **0.74s** | **168.7 tok/s** | `2/2` (`100%` SecGate) |
| **`voicefi-coder:1.5b`** *(KV-Pinned)* | **100%** | **0.87s** | **183.3 tok/s** | `2/2` (`100%` SecGate) |
| **`llama3.2:1b`** *(1.2B Edge)* | **100%** | **0.90s** | **158.4 tok/s** | `2/2` (`100%` SecGate) |

---

## 4. The 3 Repeatable Rules for Local Workflow Automation

1. **Map Once with AI, Execute in Deterministic Code**: Never pay an LLM to filter 50,000 rows inside a prompt. Have **Hey Pal** write a verified Python function in `0.74s`, and let Python process the 50,000 rows in milliseconds for $0.00.
2. **Use Surgical `SEARCH/REPLACE` Blocks, Not Full-File Rewrites**: Constraining a `1.5B` local model to surgical diff blocks cuts generation latency under 1 second and prevents accidental code deletion.
3. **Enforce AST Assertion Counting**: Always verify `candidate_assertions >= parent_assertions` via Python's `ast` module before accepting any autonomous code edit.
