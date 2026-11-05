# Blueprint #8: Process Automation: Turning Browser Demonstrations into Fast API Scripts

**Pillar**: `#8. Process Automation` (`08_process_automation`)  
**Vertical**: Accounts Receivable, Invoicing, Lead Fulfillment & Operations  
**Hardware Reference**: Apple Silicon Mac (Metal GPU, M-Series Unified Memory)  
**Replaces Cloud Cost**: Fragile browser-click macros & cloud computer-use token burn (~80,000 vision tokens/run @ $0.40/invoice)

---

## 1. The Business Problem: Repetitive Browser Clicking vs. Expensive Cloud Vision

Small and mid-sized businesses spend hours every week on repetitive browser routines:
* Logging into billing or vendor portals.
* Reading IDs and customer names from sheets or tables.
* Typing counts, line items, and invoice amounts across multiple tabs.

Traditional approaches fail:
1. **Coordinate UI Macros (RPA)**: Fragile screen coordinates break whenever a window moves 20 pixels or a website updates its layout.
2. **Cloud Vision Agents (VLM Computer-Use)**: Taking screenshots for every action burns ~80,000 vision tokens per run ($0.40/invoice) while exposing company passwords and customer data in cloud prompts.

---

## 2. How the Local Solution Works: Record Once, Lower to Headless Code

The user demonstrates the task once in their browser while speaking their intent. A local compiler synthesizes a clean, deterministic script that runs headlessly for $0.00:

```text
+-----------------------------------------------------------------------------------+
| 1. DEMONSTRATION & SCREEN CAPTURE                                                 |
| * Captures UI actions and text selection without coordinates                      |
| * Auth-Pause Boundary: Automatically redacts passwords and pauses during 2FA       |
| * Spoken Voice Anchors: Binds spoken intent to fields (e.g. "batch of 45 items")  |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 2. LOCAL COMPILER & LOWERING PASS                                                 |
| * Cleans out redundant clicks and scrolls                                         |
| * Lowers slow browser UI steps into a fast, headless REST API call                |
| * Induces clean regex cleanup rules from before/after examples                    |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 3. DETERMINISTIC BACKGROUND EXECUTION                                             |
| * Precondition check: Confirms valid credentials and non-empty batch              |
| * Direct API call: Runs in <2 seconds for $0.00 marginal cost                     |
| * Reconciliation: Updates local records and logs completion                       |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 4. CHAT APPROVAL GATE                                                             |
| * Posts staged draft summary card to the team chat review thread                  |
| * Holds execution until an authorized human replies "approve"                     |
+-----------------------------------------------------------------------------------+
```

---

## 3. Benchmark Results (`08_process_automation`)

Across all 5 process automation cases (batch invoicing lowering, directory lead loop induction, mistake undo, password auth-pause boundary, and filename cleanup regex induction):

| Local Model | Process Automation Score | Execution Tier Selected | Cloud Vision Token Cost |
| :--- | :---: | :---: | :---: |
| **`gemma4-2b`** | **100%** (5/5) | Headless API & Local Code | **$0.00** |
| **`gemma4-2b + qwen2.5-coder:1.5b` (`--router`)** | **100%** (5/5) | Headless API & Local Code | **$0.00** |
| **`gemma2:2b`** | **88%** (4/5) | Headless API & Local Code | **$0.00** |
| **`dolphin-llama3:8b`** | **84%** (4/5) | Headless API & Local Code | **$0.00** |
| **`qwen2.5-coder:1.5b`** | **80%** (4/5) | Headless API & Local Code | **$0.00** |

---

## 4. Three Practical Rules for Automating Business Chores

1. **Lower Browser UI Clicks to Direct API Calls**: Never let an AI bot endlessly click web buttons for routine chores. Lower the steps into a clean Python API call (`/crud/Invoice.json`) that executes headlessly in under 2 seconds.
2. **Always Pause During Passwords and 2FA**: The automation pipeline must detect password fields (`AXSecureTextField`) and voice prompts like *"pause for authentication"*, redacting keystrokes and stopping screen capture until the human is safely logged in.
3. **Turn Spoken Intent into Batch Loops**: When a user demonstrates one row and says *"for all 45 contractors"*, the compiler should generate a batch loop with duplicate-prevention checks instead of replaying single clicks 45 times.
