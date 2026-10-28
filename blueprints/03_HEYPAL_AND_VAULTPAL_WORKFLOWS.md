# 🛠️ SMB AI Blueprint #3: Hey Pal & Vault Pal — Sovereign Local Workflow Synthesis & Context Compression (`127.0.0.1`)

**Vertical**: Agencies, Software Shops, Consultants & Sovereign Desktop Operators  
**Architecture Pattern**: **Zero-Egress Recon (`Vault Pal`) + Surgical AST-Verified Automation (`Hey Pal`)**  
**Hardware Reference**: Apple Silicon Mac (16 GB – 64 GB Unified Memory, Metal GPU)  
**Bind Address**: `127.0.0.1` (`0.0 KB/s` External Egress)

---

## 1. The SMB Business Problem ("Rented Copilots & Context Window Bloat")

Small teams and technical operators face two expensive traps when relying on cloud SaaS wrappers ("Copilots", cloud "Second Brain" apps, and cloud coding agents):
1. **Dumping Raw Files into Cloud Context Windows (`Vault Pal` Problem):** Uploading multi-thousand-line source files, client Markdown vaults, or raw logs to frontier cloud APIs burns massive input token budgets, adds `800ms–2,000ms` of upload latency, and exposes proprietary IP to third-party servers.
2. **Brittle, Unverified Automation Scripts (`Hey Pal` Problem):** When teams ask a generic LLM to write or update a workflow script, the model often rewrites the entire file, breaks edge cases (like division-by-zero or negative inputs), or silently deletes existing test assertions to make the test suite "pass" (reward hacking).

---

## 2. The Local AI Solution Architecture (`Vault Pal` $\rightarrow$ `Hey Pal`)

Instead of streaming raw files to a metered cloud API, **Vault Pal** (`Track #4`) and **Hey Pal** (`Track #3`) operate as a two-stage local daemon pipeline on `127.0.0.1`:

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│           STAGE 1: VAULT PAL LOCAL RECON & 96% CONTEXT COMPRESSION (Track #4)       │
│  • Reads local Markdown vaults, SQLite databases & codebases in 0.1ms Unified RAM   │
│  • Local 0.8B–1.5B Scout localizes exact symbol + root cause in 0.43s (180+ tok/s)  │
│  • Compresses multi-thousand-line context by 96% with 0.0 KB/s cloud egress         │
└──────────────────────────────────────────┬──────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│          STAGE 2: HEY PAL SURGICAL WORKFLOW BUILDER & SECGATE (Track #3)            │
│  • Direct-on-Metal 1.5B model (`voicefi-coder-mlx`) synthesizes a surgical          │
│    SEARCH/REPLACE patch in 0.74 seconds (168.7 tok/s)                               │
│  • 3-Stage Deterministic AST Gate:                                                  │
│      1. Verifies clean Python AST syntax (`ast.parse`)                              │
│      2. Enforces 100% assertion preservation (blocks reward-hacking test deletion)  │
│      3. Runs hidden negative-input boundary exploit probes before committing        │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Production Receipts & LocalBench SMB v1.0 Performance

| Model | Track #3: `Hey Pal` Workflow + SecGate | Track #4: `Vault Pal` Recon | Speed (`tok/s`) | Preserved Assertions |
| :--- | :---: | :---: | :---: | :---: |
| **`voicefi-coder-mlx`** *(1.5B Metal LoRA)* | **100%** (**0.74s**) | **100%** (**0.43s**) | **168.7 tok/s** | `2/2` (Zero Overfit) |
| **`voicefi-coder:1.5b`** *(KV-Pinned)* | **100%** (0.87s) | **100%** (0.49s) | **183.3 tok/s** | `2/2` (Zero Overfit) |
| **`llama3.2:1b`** *(1.2B Edge)* | **100%** (0.90s) | **100%** (1.13s) | **158.4 tok/s** | `2/2` (Zero Overfit) |
| **`tev1:4b`** *(Qwen 3.5 Reasoning)* | **100%** (7.46s) | **100%** (12.0s) | 46.7 tok/s | `2/2` (Zero Overfit) |

---

## 4. The 3 Repeatable Rules for Sovereign Local Automation

1. **Map Once with AI, Execute in Deterministic Code:** Don't pay a cloud LLM to process every row or file at runtime. Have **Hey Pal** write a verified Python connector in `0.74s`, then let Python execute the volume in milliseconds for free.
2. **Pre-Digest Locally Before Touching the Cloud:** Use **Vault Pal** (`0.8B–1.5B`) on `127.0.0.1` to strip noise and compress local files by 96% in `0.43s` before deciding whether a task even needs a larger model.
3. **Never Trust Unverified Agent Edits:** Enforce a deterministic AST gate that counts parent vs. candidate `assert` statements so an autonomous agent can never "pass" a test by deleting the test.
