# Blueprint #10: Local vs. Cloud Shootout: 100-Run Speed & Cost Comparison

**Pillar Reference**: Cross-Pillar Shootout (`LocalBench SMB v1.2`)  
**Hardware Reference**: Apple Silicon Mac (64 GB Unified Memory, Metal GPU)  
**Workload**: 100 Consecutive Business Workflow Runs (Invoicing, Lead Extraction, File Delivery, Code Self-Healing)

---

## 1. Executive Summary

When running business automations repeatedly, compiling the task into a local script runs **faster than calling a cloud coding agent (1.8s to 3.8s local compile vs. 14.5s cloud)** because there is zero network transit overhead.

Once compiled, **every subsequent run executes in 0.1s to 1.9s at $0.00 marginal cost and 0 cloud tokens**.

---

## 2. 100-Run Production Economics Matrix

Comparing four common ways businesses run desktop automations across 100 runs:

| Architecture | One-Time Setup / Compile | Per-Run Time | 100-Run Total Time | 100-Run Cloud Cost | Screen Data Sent to Cloud | Survives Layout Drift / Window Movement? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Screen-Coordinate Click Macro** | 0.1s | 18.5s | 30.8 min | **$0.00** | 0 MB | **No** (~38% survival; breaks if window moves 20px) |
| **2. Cloud Vision Browser Agent** (18 screenshot turns/run) | 0.0s (no compile) | 62.0s | 103.3 min | **$235.69** (35.8M tokens) | 2,580 MB (2.58 GB screenshots) | **Partial** (~82% survival; slow and leaks private screens) |
| **3. Cloud Coding Agent Compile -> Local Replay** | 14.5s ($0.19 once) | 1.9s | 3.2 min | **$0.19** | 0 MB during replay | **Yes** (~99% survival; requires cloud API access) |
| **4. 100% Local Specialist Stack** (`1.5B` to `14B` on Metal) | **1.8s to 3.8s** ($0.00) | **0.1s to 1.9s** | **3.2 min** | **$0.00** (0 cloud tokens) | **0 MB (100% on-device)** | **Yes** (~99% survival; self-heals locally in ~4.9s) |

---

## 3. How Each Local Model Tier Operates in the Stack

| Stage | Engine / Model | RAM Size | What It Does in Plain English | Verified Latency |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 0: Fast Python Filter** | Regex / AST | 0 MB | Throws away 95% of browser noise (static images, CSS, fonts, tracking analytics) before any model reads it. | **< 1.0 ms** |
| **Stage 1: Intent & Voice Router** | `0.8B` to `1.2B` | 0.8 GB | Picks the real business API endpoint and extracts spoken parameters (county, date, client name). | **141 ms** |
| **Stage 2: Fast Surgical Editor** | `1.5B` Metal Coder | 0.84 GB | Applies instant edits and repairs broken field names when a partner website updates. | **4.1 ms to 4.9s** |
| **Stage 3: Rule Induction** | `14B` Coder | 8.5 GB | Generalizes string patterns from a single before/after example and writes standalone Python scripts. | **2.15 s** |
| **Stage 4: AST Safety Check** | Python `ast` Gate | 0 MB | Verifies every generated script parses cleanly, contains zero unsafe system calls, and preserves all unit test assertions. | **< 0.5 ms** |

---

## 4. Key Takeaways for Business Operators

1. **Avoid Paying Per-Screenshot Cloud Taxes**: Streaming thousands of desktop screenshots to cloud vision models is slow and expensive ($235+ per 100 runs).
2. **Compile Once into Headless Code**: Using local AI models to inspect network traffic and write a clean script once lets you run future tasks in under 2 seconds for free.
3. **Keep All Business Data On-Device**: Running on Apple Silicon Metal GPU means customer records, financial figures, and billing credentials never leave the building.
