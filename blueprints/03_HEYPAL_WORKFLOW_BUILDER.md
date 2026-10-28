# SMB AI Blueprint #3: Hey Pal - Recording & Automating Multi-App File Delivery (Slack, Local Files, Google Drive & Sheets)

**Vertical**: B2B Data Providers, Operations Teams, Agencies & Sovereign Desktop Operators  
**Architecture Pattern**: **"Record Process Once, Automate in Deterministic Code" + 3-Stage AST SecGate**  
**Hardware Reference**: Apple Silicon Mac (16 GB - 64 GB Unified Memory, Metal GPU)  
**Bind Address**: `127.0.0.1` (`0.0 KB/s` External Egress for Code Synthesis)

---

## 1. The SMB Business Problem ("Manual Multi-App File Delivery vs. Fragile Browser Agents")

In real SMB operations, delivering a completed client order requires touching four different systems in sequence:
1. Checking **Slack** for QA approval (`QA decision: APPROVED`).
2. Locating and renaming the approved local deliverable file (`APPROVED <OrderID> - <Client> - <County>.csv`) on **local disk**.
3. Uploading the clean CSV into the client's shared folder on **Google Drive**.
4. Finding the matching order row in the operations tracker on **Google Sheets**, writing the delivered filename to the completion column, and marking the database registry `DELIVERED`.

When teams try to automate this with cloud browser-use agents, the agent costs tokens on every single run, takes 3-5 minutes clicking UI buttons, and breaks whenever a window loses focus.

---

## 2. The Local AI Solution Architecture (`Hey Pal` Track #3)

With **Hey Pal**, we recorded the manual LienLogic file delivery process once and used our local coding stack to synthesize and maintain a 100% deterministic, headless Python delivery pipeline (`deliver_dfpb.py` + `autonomous_delivery_handoff.py`):

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│        PHASE 1: RECORD PROCESS ONCE -> SYNTHESIZE IN CODE (Hey Pal Track #3)        │
│  * Operator records the manual Slack -> Finder -> Drive -> Sheets delivery workflow │
│  * Direct-on-Metal 1.5B (`voicefi-coder-mlx`) synthesizes and patches surgical      │
│    Python automation in 0.74s (verified by 3-Stage AST & Assertion SecGate)         │
└──────────────────────────────────────────┬──────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│          PHASE 2: HEADLESS 2-SECOND EXECUTION ACROSS 4 SYSTEMS ($0.00/RUN)          │
│  1. Slack Gate (`autonomous_delivery_handoff.py`):                                  │
│     Detects `QA decision: APPROVED` in the order's Slack review thread              │
│  2. Local File Resolution (`deliver_dfpb.py`):                                      │
│     Resolves `APPROVED <ID>.csv` on local disk and normalizes client filename       │
│  3. Google Drive REST API v3 (`upload_file_to_drive`):                              │
│     Uploads/updates the CSV directly into the Shared Drive folder (0 UI clicks)     │
│  4. Google Sheets REST API v4 + PostgreSQL Registry:                                │
│     Writes the delivered filename stem to Column J / Completed tab & logs DB        │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Production Receipts & LocalBench SMB v1.0 Performance

| Metric / Model | Manual / Cloud Browser Agent | Hey Pal Local Code Pipeline | Business Impact |
| :--- | :---: | :---: | :--- |
| **End-to-End Order Delivery Time** | 5 - 10 Minutes (Manual / UI Clicking) | **~2.0 Seconds** (`deliver_dfpb.py`) | **150x Faster Order Fulfillment** |
| **Per-Delivery Cloud AI Token Cost** | $0.50 - $2.00 per browser agent run | **$0.00** (Headless REST APIs) | **100% Margin Retention** |
| **`voicefi-coder-mlx` (1.5B Metal)** | N/A | **100% Track #3 Score (`0.74s`)** | `2/2` AST assertions preserved |
| **`voicefi-coder:1.5b` (KV-Pinned)** | N/A | **100% Track #3 Score (`0.87s`)** | `2/2` AST assertions preserved |

---

## 4. The 3 Repeatable Rules for Multi-App SMB Automation

1. **Record the Workflow Once, Run It in Headless REST**: Never pay a cloud vision model to click Google Drive and Google Sheets buttons 50 times a week. Record the workflow once, synthesize a direct Python REST script (`Drive v3` + `Sheets v4` + `Slack REST`), and execute it in 2 seconds for $0.00.
2. **Use Surgical `SEARCH/REPLACE` Diffs for Workflow Updates**: When a sheet column or filename rule changes, a local `1.5B` model (`voicefi-coder-mlx`) updates the exact function in `0.74 seconds` without rewriting the rest of the script.
3. **Enforce a 3-Stage AST SecGate on All Code Edits**: Before any automated workflow change is committed, verify `ast.parse()`, confirm `candidate_assertions >= parent_assertions` (`2/2`), and run negative-input boundary probes so the pipeline never silently breaks.
