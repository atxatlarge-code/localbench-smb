# Blueprint #9: Task Routing - Running Background Helpers with Chat Approval Gates

**Pillar**: `#9. Task Routing` (`09_task_routing`)  
**Vertical**: Operations, Customer Fulfillment, Engineering & Agency Teams  
**Hardware Reference**: Apple Silicon Mac (16 GB to 64 GB Unified Memory)  
**Replaces Cloud Cost**: Babysitting multiple agent windows & cloud multi-worker token burn (~23M tokens/run)

---

## 1. The Business Problem: Agent Window Sprawl & Lack of Human Sign-Off

Most business teams do not want to manage 5 terminal windows, 4 dashboards, and 3 different coding copilots. Teams already communicate in chat threads.

Yet automating tasks through chat creates two risks:
1. **Uncontrolled Background Actions**: If a bot immediately commits code or sends invoices without staging them for review, errors slip into production.
2. **Infinite Loops & Memory Starvation**: If a background worker gets stuck running the same broken test command repeatedly, it burns system memory and locks up machine resources.

---

## 2. How the Local Solution Works: Sender Firewall + Person Stage + Watchdog

A resident local router pairs with background workers, an allowlist firewall, and an external watchdog:

```text
               [ Team Chat Review Channel (#operations, #client-orders) ]
                                             |
                                             v
+-----------------------------------------------------------------------------------+
| 1. SENDER ALLOWLIST FIREWALL                                                      |
| * Checks incoming sender against authorized list (ops-lead, qa-reviewer, etc.)    |
| * Immediately blocks unknown or spoofed external webhooks                         |
+------------------------------------+----------------------------------------------+
                                     |
                                     v
+-----------------------------------------------------------------------------------+
| 2. RESIDENT TASK ROUTER & PERSON STAGES                                           |
| * Awaiting Answer: Pauses if scope or branch is missing; asks team lead in chat   |
| * Awaiting Review: Stages completed deliverables in chat; waits for "approve"     |
| * Auto-Unblock: When team lead replies "LGTM, ship it", the task finishes safely  |
+------------------------------------+----------------------------------------------+
                                     |
                                     v
+-----------------------------------------------------------------------------------+
| 3. ISOLATED LOCAL WORKERS (Copy-on-Write Sandbox)                                 |
| * Background workers run tasks in isolated local directories                      |
| * Runs 100% silently with zero chat spam until the deliverable is ready           |
+------------------------------------+----------------------------------------------+
                                     ^
                                     |
+------------------------------------+----------------------------------------------+
| 4. OUT-OF-BAND IMMUNE LOOP: EXTERNAL WATCHDOG                                     |
| * Monitors Mac thermals and memory usage                                          |
| * Detects stuck loops (e.g. running pytest 4x consecutively with 0 file changes)  |
| * Halts the loop, recovers state, and alerts the team                             |
+-----------------------------------------------------------------------------------+
```

---

## 3. Benchmark Results (`09_task_routing`)

Across all 5 task routing cases (unauthorized webhook firewall block, ambiguous deploy paused in `awaiting_answer`, QA hold staged in `awaiting_review`, in-thread `"LGTM, ship it"` auto-unblock, and stuck-worker loop recovery):

| Local Model | Task Routing Score | Firewall Block | Human "Approve" Gating | Watchdog Loop Recovery |
| :--- | :---: | :---: | :---: | :---: |
| **`gemma4-2b`** | **82%** (4/5) | **Pass** | **Pass** | **Pass** |
| **`gemma4-2b + qwen2.5-coder:1.5b` (`--router`)** | **82%** (4/5) | **Pass** | **Pass** | **Pass** |
| **`dolphin-llama3:8b`** | **80%** (4/5) | **Pass** | **Pass** | **Pass** |
| **`qwen2.5-coder:1.5b`** | **76%** (4/5) | **Pass** | **Pass** | **Pass** |
| **`gemma2:2b`** | **74%** (3/5) | **Pass** | Partial | Partial |

---

## 4. Three Practical Rules for Running Background Helpers

1. **Lock Down Senders with an Allowlist Firewall**: Never let an AI agent accept arbitrary commands from untrusted webhooks. Check the sender ID before processing any task.
2. **Never Execute Risky Actions Without an "Approve" Gate**: Put tasks into a paused stage (`awaiting_review`) whenever they touch production data or client files, auto-resuming only when an authorized human replies in the thread.
3. **Use an External Watchdog to Kill Stuck Loops**: AI workers can get stuck in loops when encountering unexpected errors. Run an independent watchdog process that counts repeated commands and resets stuck tasks.
