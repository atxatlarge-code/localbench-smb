# SMB AI Blueprint #8: The Demonstration-to-Deterministic Compiler (PbD + Tier 1 API)

**Vertical**: B2B Accounts Receivable, SaaS Invoicing, Lead Fulfillment, Back-Office Data Operations  
**Architecture Pattern**: **Multimodal PbD (Hey Pal Teach Mode + Screenpipe OCR + Quartz AX) ➔ Semantic IR ➔ Tier 1 REST API Lowering ➔ SuperAgent Slack Review**  
**Hardware Reference**: Apple Silicon Mac (Metal GPU, M-Series Unified Memory)  
**Replaces Cloud Tax**: Fragile coordinate UI clickers (~45s execution, 100% session failure rate on MFA/timeouts) + Cloud Computer-Use token burn (~80,000 vision tokens/run @ $0.40/invoice) with a deterministic, zero-token Tier 1 REST program (<1s execution, $0.00 token cost).

---

## 1. The Vision: From Showing Once to Never Doing It Again

Small and medium businesses bleed hours every week performing repetitive GUI rituals:
* Logging into SaaS portals (Bill.com, QuickBooks, Stripe, Google Drive, Keap).
* Reading IDs and customer names from internal sheets/databases.
* Typing counts, line items, and descriptions across multiple tabs.

Traditional solutions fail:
1. **Robotic Process Automation (RPA) / GUI Replayers:** Fragile screen coordinates drift when browser windows resize or web app DOM updates, and session expiration / MFA challenges cause 100% failure rates on unattended cron jobs.
2. **Cloud Vision Agents (VLM Computer-Use):** Stream 1 screenshot per action into expensive frontier models, consuming **~80,000 tokens per invoice** ($0.40/run), while exposing raw passwords and session tokens in model prompts.

**Blueprint #8 solves this with Programming by Demonstration (PbD) + Multi-Tier Strength-Reduction Lowering**:
The user demonstrates the task *once* in their browser while speaking their intent. The compiler synthesizes a deterministic **Tier 1 Headless REST API program** that runs silently, headlessly, and for free.

---

## 2. System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. DEMONSTRATION & MULTIMODAL CAPTURE (Hey Pal Teach Mode + Screenpipe OCR)                     │
│ • Crimson Screen Border (#FF2A2A) & Live Floating Granola Card (localhost:5141/training)       │
│ • AXFocusedUIElement Probe: Automatically extracts `AXSelectedText` on mouse drag/highlight     │
│ • Auth-Pause Boundary: Redacts keystrokes and OCR frames during login/2FA challenges            │
│ • Spoken Voice Anchors: Binds semantic intent to UI inputs (e.g. "$quantity = unbilled_count")   │
└────────────────────────────────┬────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 2. COMPILATION & LOWERING PASS (PalCompiler Semantic Decompiler)                                │
│ • Denoises redundant scrolls and misclicks (125 UI steps ➔ 1 declarative batch specification)   │
│ • Lifts coordinate clicks into parameterized registers ($order_ids, $rate, $customer_id)       │
│ • Lowering Pass: Lowers Tier 3 Coordinate GUI ➔ Tier 1 Headless API (`/crud/Invoice.json`)      │
└────────────────────────────────┬────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 3. DETERMINISTIC ENGINE ROOM (LienLogic `scripts/billcom_client.py` & `scripts/billing.py`)     │
│ • Precondition Gate {P}: Validates credentials and non-empty unbilled batch                      │
│ • Automatic Sequencing: Computes next invoice series (e.g. `QQTDAABP-0018`)                     │
│ • Execution C: Emits HTTPS POST to Bill.com API with executive memo & itemized audit trail       │
│ • Reconciliation {Q}: Updates local `orders_registry.json` marking orders INVOICED              │
└────────────────────────────────┬────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 4. AUTONOMOUS FRONT-OFFICE SUPERVISION (Hermes + DeepSeek Super-Agent Slack OS)                 │
│ • Scheduled Trigger: Friday 4:00 PM cron inspects unbilled order queue                           │
│ • Hermes Slack Gate: Posts staged draft summary card to Slack `#accounting` thread              │
│ • Person-Stage Gate (`awaiting_review`): Holds execution until authorized human replies "approve"│
│ • Auto-Unblock: Worker issues invoice via Tier 1 API and posts confirmation reference to Slack  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Production Proof: The LienLogic Invoicing Batch

During the initial deployment of Blueprint #8 on November 2, 2026:
1. **The Demonstration:** User demonstrated creating a Bill.com invoice for 8 delivered tax delinquency orders ($3,160.00) while narrating field requirements.
2. **The Selection Fix:** VoiceFi captured the `select_text` event on the invoice UID `QQTDAABP-0017` via `AXSelectedText`.
3. **The Tier 1 Engine:** Synthesized [`LienLogic/scripts/billcom_client.py`](file:///Users/jaketrigg/Projects/LienLogic/scripts/billcom_client.py) and integrated `scripts/billing.py create-invoice`.
4. **The Ledger Synchronization:** 8 orders (UIDs 72–79) reconciled from `UNBILLED` ➔ `INVOICED` under `QQTDAABP-0017`.

---

## 4. CLI & Verification

```bash
# 1. Verify Environment Daemons (VoiceFi :5141, Screenpipe :3030, macOS AX)
python3 .agents/skills/automate-workflow/scripts/verify_environment.py

# 2. Run Tier 1 Dry-Run Simulation in LienLogic
cd /Users/jaketrigg/Projects/LienLogic && .venv/bin/python scripts/billing.py create-invoice --dry-run

# 3. Test SuperAgent Person-Stage Routing in Local Models
cd "/Users/jaketrigg/Projects/Local Models" && .venv/bin/python -c "
from workflows.dsh_superagent import DSHSuperAgentEngine
e = DSHSuperAgentEngine()
route, stage, q = e.classify_route('hermes_slack', 'Generate weekly Bill.com batch for Friday.')
assert stage == 'awaiting_review'
print('✓ SuperAgent AR Review Gate Verified!')
"
```
