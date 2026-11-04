# Blueprint #5: Team Chat - Lean Slack/Chat Triage & Outbound Style Guards

**Pillar**: `#5. Team Chat` (`05_team_chat`)  
**Vertical**: B2B Operations, Client Delivery, QA Teams & Agencies  
**Hardware Reference**: Apple Silicon Mac (16 GB to 64 GB Unified Memory, Metal GPU)  
**Replaces Cloud Cost**: Bloated 30-Tool Chat MCP Token Overhead (~6,000 tokens/turn) & Manual QA Triage

---

## 1. The Business Problem: Chat Thread Chaos & AI Tone Slips

High-velocity client delivery and internal QA happen inside **Slack and team chat threads**. Yet connecting standard cloud AI bots to team chat causes three problems:
1. **The 30-Tool MCP Token Tax**: Loading a full Slack MCP server (with 30+ tool schemas for channels, users, reactions, and search) into an LLM prompt burns **4,000 to 8,000 input tokens on every single message** before the model even reads the thread.
2. **Lost Action Items in Review Threads**: When a reviewer posts a `HOLD` or `SWAP_REQUESTED` flagging specific record IDs or spreadsheet cells, generic chat bots fail to extract the exact IDs and root cause.
3. **AI Punctuation & Broken Mentions**: Left unchecked, LLMs reply in team channels using robotic AI punctuation (em dashes), unverified marketing hype, or plain `@username` text that fails to trigger real `<@U...>` notifications.

---

## 2. How the Local Solution Works

Instead of injecting 30 MCP tools on every turn, a lightweight Python bridge maps each thread (`thread_ts`), classifies the message locally in under a second, and runs a strict outbound style check before posting:

```text
+-----------------------------------------------------------------------------------+
|               STAGE 1: LEAN THREAD REGISTRY (0 MCP Schema Tokens)                 |
|  * Maps 1 chat thread (`thread_ts`) per client order or project                   |
|  * Fetches thread replies via simple REST call (saves ~6,000 tokens/turn)         |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|         STAGE 2: LOCAL REVIEW TRIAGE (<1.0s on 1.5B to 2.6B Local Model)          |
|  * Parses inbound QA review message into clean JSON:                              |
|      - `decision`: "HOLD" | "SWAP_REQUESTED" | "APPROVED"                         |
|      - `defect_category`: "DRIFT" | "ENTITY_USE" | "SITUS_GEOMETRY" | "FORMULA"   |
|      - `flagged_ids`: ["R104821", "R109932"]                                      |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|              STAGE 3: OUTBOUND MENTION & STYLE CHECK (Deterministic)              |
|  * Converts plain `@QA-Lead` strings into active `<@U01QA_LEAD>` user tags        |
|  * Blocks or cleans any reply containing em/en dashes or banned hype phrases      |
+-----------------------------------------------------------------------------------+
```

---

## 3. Benchmark Results (`05_team_chat`)

Across all 5 team review scenarios (address mismatch hold, settled account swap request, corporate LLC filter hold, blank spreadsheet formula cell hold, and clean 300-record approval):

| Local Model | Team Chat Score | Latency per Thread | Speed (`tok/s`) | MCP Tokens Saved |
| :--- | :---: | :---: | :---: | :---: |
| **`gemma2:2b`** | **96%** (5/5) | **0.81s** | **120+ tok/s** | **~6,000 tokens/turn** |
| **`qwen2.5-coder:1.5b`** | **96%** (5/5) | **0.94s** | **131+ tok/s** | **~6,000 tokens/turn** |
| **`dolphin-llama3:8b`** | **96%** (5/5) | **1.52s** | **49+ tok/s** | **~6,000 tokens/turn** |
| **`localbench-router`** *(with Style Gate)* | **100%** (5/5) | **0.82s** | **153+ tok/s** | **~6,000 tokens/turn** |

---

## 4. Three Practical Rules for Local Team Chat Bots

1. **Skip the 30-Tool MCP Schema When You Only Need a Thread Map**: Keep a simple JSON table mapping project IDs to chat `thread_ts` timestamps. Fetch the thread text in Python and pass *only* the message to your local model.
2. **Classify the Problem Category Before Acting**: Have the local model bucket every QA issue into a clear category (`DRIFT`, `ENTITY_USE`, `SITUS_GEOMETRY`, `FORMULA_CACHE`) and list the exact flagged IDs so nothing gets missed.
3. **Check Mentions and Punctuation in Python Before Sending**: Small models occasionally slip up on negative formatting rules. Run a 5-line Python check to format `<@U...>` mentions and strip em dashes before posting to chat.
