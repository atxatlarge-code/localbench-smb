# SMB AI Blueprint #1: LienLogic — The Zero-Marginal-Cost Public Record & Lead Factory

**Vertical**: Real Estate Investment, Title Intelligence, PropTech & B2B Lead Agencies  
**Architecture Pattern**: **The Centaur Protocol ("Cloud Finds, Local Builds") + 4-Tier Apple Silicon Metal Pipeline**  
**Hardware Reference**: Apple Silicon Mac (M-Series Pro/Max/Ultra, 64 GB Unified Memory)  
**Primary Repo**: `LienLogic`

---

## 1. The SMB Business Problem ("The Per-Row Token & Latency Trap")

Small and mid-sized data businesses, boutique real estate funds, and B2B lead agencies ingest messy public records across 3,143 US counties (tax collector portals, fixed-width assessment rolls, GIS endpoints, and PDF notices).

When teams build these pipelines using standard cloud AI APIs:
1. **Per-Row API Burn Destroys Gross Margins**: Sending 50,000 county rows through frontier cloud LLMs to normalize parcel IDs (`APN`), classify property use codes, or disambiguate owner entities (Living Homeowner vs. LLC/Trust/Estate) costs hundreds of dollars per county run.
2. **The 15-Hour Latency Tax**: Across **25,420 daily autonomous micro-decisions** (pre-screening network HAR/JS bundles, checking schema types, validating AST syntax, auditing row quality), a `1,800ms` cloud round-trip introduces **14.2+ hours of pure network wait time and HTTP 429 rate-limit stalls per day**.
3. **Zero-QA Gamble**: Because running a second cloud LLM pass to audit 50,000 rows doubles the API bill, cloud-dependent teams only spot-check a tiny sample—leading to bad data deliveries (e.g., cured `$0.00` balances or statutory Over-65 deferrals).

---

## 2. The Local AI Solution Architecture

LienLogic replaces per-row cloud API dependency with the **Centaur Protocol** and a **4-Tier On-Device Apple Silicon Stack**:

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                   PHASE 0: CLOUD PATHFINDER (One-Time Discovery)                    │
│  Unstructured portal exploration ──► Emits County Interface Contract (<county>.json) │
└──────────────────────────────────────────┬──────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                 PHASE 1: LOCAL METAL BUILDER & PRODUCTION FACTORY                   │
├──────────────────────┬───────────────────────────────────┬──────────────────────────┤
│ Tier 0: Traffic Cop  │ Tier 1: Workhorse (:9379/:9380)   │ Tier 2: Specialist (:8085)│
│ • lienlogic-tev1:0.8b│ • voicefi-coder-mlx (180+ tok/s)  │ • Qwen 2.5-Coder 14B     │
│ • voicefi-coder:1.5b │ • Gemma 4 26B LiteRT (27 tok/s)   │   (17.8 tok/s w/ Draft)  │
│ • <100ms HAR/JSON    │ • Synthesizes format_apn() &      │ • 3-table PostgreSQL     │
│   endpoint triage    │   self-heals YAML configs         │   schema & quant math    │
└──────────────────────┴─────────────────┬─────────────────┴──────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│               DETERMINISTIC PYTHON EXECUTION + 100% LOCAL ROW QA                    │
│  • Polars / DuckDB vectorized demographic sieve (<30s for 500k parcels)             │
│  • AIMD Pacing REST Harvester (10–16 req/s, $0 proxy cost, <100ms/parcel)           │
│  • 100% Row-Level Local Audit: Purges LLCs, § 33.06 Over-65 deferrals & <$3.5k debt │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Production Receipts & Verified Unit Economics

| Metric | Legacy Cloud / Browser Stack | LienLogic Local Metal Stack | Business Impact |
| :--- | :--- | :--- | :--- |
| **County Onboarding Time** | 2 – 3 Days (Manual + Playwright) | **9 – 12 Minutes** (`./onboard`) | **100x Faster Market Expansion** |
| **Per-Parcel Query Speed** | 3,000 – 5,000 ms (Headless Browser) | **48 – 100 ms** (Direct REST API) | **5,000 Parcels in ~7 Minutes** |
| **Marginal AI Token Cost** | \$150 – \$450 per 100k rows | **\$0.00** (85–95% initial, ~100% repeat) | **Near-100% Gross Margin on Repeat Orders** |
| **Daily Autonomy Stalls** | 12.5 hrs wait / 25,000 decisions | **1.6 hrs** (`<235ms` avg local turn) | **14.2 Hours Reclaimed Daily** |
| **Row-Level QA Coverage** | <1% Spot-Check Sample | **100% Full-Delivery Audit** | **Zero Cured Leads, 100% Statutory Precision** |

### Empirical Case Study: The Texas Wave 4 Shootout (`LOCAL_AI_ORCHESTRATION_AND_MODELS.md`)
* **Bexar County (`bexar.acttax.com`)**: On-device `Gemma 4-26b` reverse-engineered the live ACT portal in **82 seconds**, synthesized a fault-tolerant async scraper, and queried 20 live single-family parcels in **0.97 seconds (`48ms/parcel`)**, uncovering **\$47,074.73 in verified delinquent debt** on the first run.
* **Cameron County (`tx_cameron`)**: Local `Gemma 4 2B Scout + 26B Builder` generated a 602-line $O(1)$ streaming ZIP parser and 48 unit tests (**48/48 passed in `0.05s`**) at **\$0.00 marginal API cost**.

---

## 4. The 3 Repeatable Rules for Any Data SMB

1. **Map Once with AI, Execute in Deterministic Code**: Never pay a cloud LLM to parse the same county or vendor format 50,000 times. Use local models (`voicefi-coder-mlx` / `Gemma 4 26B`) to write and self-heal the Python parser once; let vectorized Python (`polars`/`duckdb`) run the volume for free.
2. **Speculative Decoding on Unified Memory**: Pairing a `14B` or `32B` model with a `1.5B` draft model on Apple Silicon MLX delivers a **1.85x to 2.70x speedup** (`17.83 tok/s` on 14B) using only `~9.5 GB` of Unified RAM.
3. **Audit 100% of Deliverables Locally**: When inference is free on your own metal, run an adversarial local QA gate across every single row before the client ever sees the CSV.
