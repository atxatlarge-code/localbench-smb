# SMB AI Blueprint #5: Hermes - Zero-MCP Slack Thread Ops & Pre-Flight Policy Gate

**Vertical**: B2B Data Delivery, Client Services, Underwriting Ops & Engineering Agencies  
**Architecture Pattern**: **Zero-MCP REST Thread Mapping (`thread_ts`) + Defect Taxonomy Triage + Deterministic Outbound Policy Gate**  
**Hardware Reference**: Apple Silicon Mac (16 GB - 64 GB Unified Memory, Metal GPU)  
**Replaces Cloud Tax**: Bloated 30-Tool Slack MCP Context Overhead + Manual Client Review Triage

---

## 1. The SMB Business Problem ("Slack Thread Chaos & Outbound Policy Slips")

While Email (`Zmail Hero`) handles external vendors and asynchronous correspondence, high-velocity B2B client delivery and internal operations happen inside **Slack threads**. Yet connecting cloud AI agents to Slack creates three major operational failures:
1. **The 30-Tool MCP Token Tax**: Injecting a standard Slack MCP server (with 25-40 tool schemas for channels, users, reactions, canvases, and search) into an LLM prompt burns **4,000 to 8,000 input tokens on every single turn** before the model even reads a message.
2. **Thread Drift & Lost Action Items**: When a client reviewer or QA bot posts a `HOLD` or `SWAP_REQUESTED` inside a project thread (flagging specific record IDs or data discrepancies), standard chat bots lose track of which `thread_ts` maps to which client order.
3. **Outbound Policy & Typography Violations**: Left unchecked, LLMs reply in client Slack channels using telltale AI punctuation (em-dashes ` - `), unverified legal/marketing claims (`"high equity"`, `"fast close"`), or broken `@username` strings that fail to trigger real Slack `<@U...>` notifications.

---

## 2. The Local AI Solution Architecture (`Hermes` Track #5)

**Hermes** (`Track #5`) bypasses MCP schema bloat entirely using a lean out-of-band REST bridge paired with local Apple Silicon inference and a deterministic **8-Gate Pre-Flight Policy Auditor**:

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│          STAGE 1: ZERO-MCP SLACK THREAD REGISTRY (hermes_slack_bridge.py)           │
│  • Maps 1 Slack `thread_ts` per client order / county project (`slack_config.json`) │
│  • Polls thread replies via pure Python REST (`0` MCP tool schema tokens injected)  │
└──────────────────────────────────────────┬──────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│         STAGE 2: LOCAL DEFECT TAXONOMY & TRIAGE (<1.0s on 1.5B-8B Metal)            │
│  • Parses inbound QA review message into structured JSON:                           │
│      - `decision`: "HOLD" | "SWAP_REQUESTED" | "APPROVED"                           │
│      - `defect_category`: "DRIFT" | "ENTITY_USE" | "SITUS_GEOMETRY" | "FORMULA"     │
│      - `flagged_apns`: ["R104821", "R109932"]                                       │
└──────────────────────────────────────────┬──────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│       STAGE 3: PRE-FLIGHT POLICY & MENTION HYGIENE GATE (hermes_nfe_auditor.py)     │
│  • Rewrites plain `@Reviewer` strings into active `<@U0BGM4V8SG7>` Slack IDs        │
│  • Blocks outbound message if it contains prohibited em-dashes (` - ` / `-`) or       │
│    unverified marketing claims (`"high equity"`, `"fast close"`, `"zero lawsuits"`) │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Production Receipts & LocalBench SMB v1.0 Performance

Across the **LocalBench SMB v1.0** `05_hermes_slack` track (parsing a Denton County `HOLD` thread, classifying the `SITUS_GEOMETRY` mailing-vs-situs city leak, extracting both flagged APNs, and passing the outbound policy/mention gate):

| Local Model | Hermes Slack Score | Latency per Thread | Speed (`tok/s`) | MCP Schema Tokens Saved |
| :--- | :---: | :---: | :---: | :---: |
| **`dolphin-llama3:8b`** *(Llama 3 8B)* | **100%** | **1.52s** | 51.4 tok/s | **~6,000 tokens/turn** |
| **`gemma2:2b`** *(Google Gemma 2)* | **100%** | **0.81s** | 114.5 tok/s | **~6,000 tokens/turn** |
| **`voicefi-coder-mlx`** *(1.5B Metal LoRA)* | **80%-100%** | **0.88s** | **158.1 tok/s** | **~6,000 tokens/turn** |
| **`voicefi-coder:1.5b`** *(KV-Pinned)* | **80%-100%** | **0.94s** | **176.5 tok/s** | **~6,000 tokens/turn** |

---

## 4. The 3 Repeatable Rules for Local Slack Agents

1. **Don't Inject 30 MCP Tools When You Only Need a `thread_ts` Map**: Keep a lightweight local JSON registry mapping project IDs to Slack `thread_ts` timestamps. Fetch the thread text in Python and pass *only* the message body to your local model.
2. **Force Structured Defect Taxonomies Before Taking Action**: Never let an agent "frantically patch" a client complaint. Have the local model classify the objection into a fixed taxonomy (`DRIFT`, `ENTITY_USE`, `SITUS_GEOMETRY`, `FORMULA_CACHE`) first so the root cause is fixed in code.
3. **Run a Deterministic Regex Policy Gate on Outbound Replies**: Small models occasionally forget negative stylistic constraints (like *"don't use em-dashes"* or *"format `<@U...>` user IDs"*). Enforce mention formatting (`format_slack_bot_mention`) and prohibited-phrase stripping in deterministic Python before calling `chat.postMessage`.
