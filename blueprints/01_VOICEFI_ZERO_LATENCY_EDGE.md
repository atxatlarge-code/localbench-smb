# SMB AI Blueprint #1: VoiceFi - Zero-Latency Offline Voice & Sub-100ms MCP Tool Dispatch

**Vertical**: Software Agencies, Executive Operations, Healthcare/Legal Dictation & Multi-Agent Engineering Teams  
**Architecture Pattern**: **0ms Offline Neural Audio + Direct-on-Metal MLX (`:9379`) + Universal MCP Stdio Bridge**  
**Hardware Reference**: Apple Silicon Mac (Unified Memory + Metal GPU + Neural Engine)  
**Fires Cloud Tax**: $20/mo Cloud Dictation Wrappers (Wispr Flow, Superwhisper Cloud) & Per-Minute Cloud Voice APIs

---

## 1. The SMB Business Problem ("Cloud Voice Lag & Audio Privacy Leaks")

When businesses deploy voice interfaces or spoken command workflows using cloud-only APIs, they hit three walls:
1. **Per-Seat & Per-Minute Cloud Voice Rent**: Cloud TTS/ASR wrappers charge $20/seat/month or $0.05-$0.15/minute while streaming private office audio, client calls, and spoken prompts to third-party servers.
2. **Round-Trip Voice-to-Tool Latency**: Waiting `1,500ms to 2,500ms` for a cloud voice API to transcribe audio and emit a structured tool call breaks natural human-computer cadence.
3. **Unreliable Tool JSON Formatting**: Many compact local models fail to emit clean JSON tool calls without wrapping them in conversational filler.

---

## 2. The Local AI Solution Architecture (`VoiceFi` Track #1)

VoiceFi eliminates network transit entirely via Apple Silicon Neural Engine speech synthesis, local `faster-whisper` ASR, and Direct-on-Metal MLX tool dispatch:

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                  VOICEFI MULTIMODAL EDGE LAYER (100% Offline Audio)                 │
│  * 0ms Instant Neural TTS (Apple Neural Engine / Qwen3-TTS / F5-TTS on MLX)         │
│  * On-Device faster-whisper ASR  *  155x34px Glassmorphic Cocoa Dynamic Island HUD  │
└──────────────────────────────────────────┬──────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│              HYBRID ROUTER & THERMAL SUPERVISOR (Port :9379 / :9380 / :11434)       │
├───────────────────────────┬───────────────────────────┬─────────────────────────────┤
│ Reflex Arbiter (42ms TTFB)│ Direct Metal Coder (65ms) │ Deep Reasoner (9B-26B)      │
│ * tev1:0.8b / llama3.2:1b │ * voicefi-coder-mlx       │ * gemma4-26b / nimble:9b    │
│ * Instant intent & routing│ * 168+ tok/s surgical     │ * Architectural & complex   │
│   at 158-174 tok/s        │   tool JSON dispatch      │   multi-step planning       │
└───────────────────────────┴─────────────┬─────────────┴─────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                     UNIVERSAL MCP STDIO & UNIX SOCKET BRIDGE                        │
│  * Dispatches verified JSON tool calls (`read_slice`, `find_symbol`, `search_code`) │
│  * Binds strictly to `127.0.0.1` and `/tmp/vifi.sock` with 0.0 KB/s cloud egress    │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Production Receipts & LocalBench SMB v1.0 Performance

Across **Track #1 (`VoiceFi`)**, **all 10 tested local models (`0.8B` to `9B`) scored 100%** on structured JSON tool-call dispatch:

| Model Tier | Operational Role | Local TTFB | Cloud Baseline | Speedup Factor | Track #1 Score |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`tev1:0.8b`** | Tier-0 Reflex Arbiter | **42 ms** | 1,800 ms | **42.8x Faster** | **100%** (0.77s) |
| **`voicefi-coder-mlx`** | Direct-on-Metal LoRA (`:9379`) | **65 ms** | 1,800 ms | **27.7x Faster** | **100%** (0.66s) |
| **`voicefi-coder:1.5b`** | KV-Pinned Ollama (`:11434`) | **118 ms** | 1,800 ms | **15.2x Faster** | **100%** (0.50s) |
| **`gemma2:2b`** | Voice Intent & Triage Router | **140 ms** | 1,800 ms | **12.8x Faster** | **100%** (0.51s) |

---

## 4. The 3 Repeatable Rules for Local Voice-to-Action Systems

1. **Pin Your KV Cache (`num_keep -1`)**: In SMB production, model cold-start time is the silent killer. Keep your `1.5B` tool-dispatch model resident in Unified Memory (`mlx_metal_worker.py`) for `65ms` time-to-first-byte.
2. **Constrain Tool Schemas to 3-5 Core Primitives**: Even an `800MB` local model (`tev1:0.8b`) achieves **100% tool-calling accuracy** when given a clean, focused tool schema instead of 40 overlapping endpoints.
3. **Keep Audio 100% On-Device**: Combining `faster-whisper` ASR with Apple Neural Engine / MLX TTS gives every employee a private voice interface at **$0.00/minute**.
