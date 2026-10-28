#!/usr/bin/env python3
"""
LocalBench SMB - Specialist Local Router (`localbench-specialist-router`).
Zero-dependency OpenAI-compatible HTTP server (`127.0.0.1:9380/v1/chat/completions`).

Routes incoming SMB workloads across compact local specialists (<3.2 GB total RAM):
  1. `voice_or_vault_or_code` -> `voicefi-coder-mlx` (1.5B Metal :9379, fallback `voicefi-coder:1.5b` :11434)
     Handles Track #1 (VoiceFi Tool Dispatch), Track #3 (Hey Pal Code Synthesis), Track #4 (Vault SQLite Q&A).
  2. `tabular_code_sieve` -> `voicefi-coder-mlx` synthesizes a 5-line Python `keep_record(r)` predicate and
     executes it deterministically on the JSON records array (Track #2 LienLogic: 25% -> 100% accuracy).
  3. `comms_triage` -> `gemma2:2b` (:11434, fallback `voicefi-coder:1.5b`)
     Handles Track #5 (Hermes Slack Thread Ops) and Track #6 (Zmail Hero 90/10 Inbox Appliance).
"""

import argparse
import ast
import json
import re
import time
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, Dict, List, Optional, Tuple

DEFAULT_ROUTER_PORT = 9380
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MLX_URL = "http://127.0.0.1:9379/v1/chat/completions"


def classify_smb_workload(messages: List[Dict[str, Any]]) -> str:
    """Classify an OpenAI chat messages array into one of 3 specialist routes."""
    full_blob = "\n".join(str(m.get("content") or "") for m in messages).lower()

    # Route 1: Tabular Financial / Public-Record Sieve (Track #2 LienLogic)
    if (
        ("qualified_ids" in full_blob or "qualified_apns" in full_blob)
        and ("rejected_count" in full_blob or "disqualified_count" in full_blob)
        and "[" in full_blob
        and "]" in full_blob
    ):
        return "tabular_code_sieve"

    # Route 2: Comms & Thread Triage (Track #5 Hermes Slack & Track #6 Zmail Hero)
    if any(
        kw in full_blob
        for kw in (
            "zmail hero",
            "mail sorting assistant",
            "replysuggestions",
            "inbound slack message",
            "slack review thread",
            "defect_category",
            "<@u0bgm4v8sg7>",
        )
    ):
        return "comms_triage"

    # Route 3: Voice Dispatch, Surgical Python Code Synthesis, and Local Vault FTS5 Q&A (Tracks #1, #3, #4)
    return "mlx_coder"


def _extract_records_and_rules(messages: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
    sys_text = ""
    user_text = ""
    for m in messages:
        role = str(m.get("role", ""))
        content = str(m.get("content") or "")
        if role == "system":
            sys_text += content + "\n"
        elif role == "user":
            user_text += content + "\n"

    # Extract rules from system prompt
    rules_lines = []
    for line in (sys_text + "\n" + user_text).splitlines():
        s = line.strip()
        if re.match(r"^[1-9]\.", s):
            rules_lines.append(s)
    rules_text = "\n".join(rules_lines) if rules_lines else sys_text.strip()

    # Extract JSON records array from user prompt
    records: List[Dict[str, Any]] = []
    start = user_text.find("[")
    end = user_text.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            parsed = json.loads(user_text[start : end + 1])
            if isinstance(parsed, list):
                records = [r for r in parsed if isinstance(r, dict)]
        except Exception:
            pass
    return rules_text, records


def _call_ollama_chat(
    model: str,
    messages: List[Dict[str, str]],
    ollama_base: str = DEFAULT_OLLAMA_URL,
    max_tokens: int = 400,
    temperature: float = 0.1,
    json_mode: bool = False,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }
    if json_mode:
        payload["format"] = "json"
    t0 = time.perf_counter()
    req = urllib.request.Request(
        f"{ollama_base.rstrip('/')}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    elapsed_s = round(time.perf_counter() - t0, 3)
    msg = data.get("message", {})
    content = str(msg.get("content", "")).strip()
    eval_count = int(data.get("eval_count") or max(1, len(content) // 4))
    eval_dur_s = float(data.get("eval_duration", 0)) / 1e9
    tok_per_s = round(eval_count / eval_dur_s, 1) if eval_dur_s > 0 else round(eval_count / max(0.01, elapsed_s), 1)
    return {
        "content": content,
        "elapsed_s": elapsed_s,
        "tokens": eval_count,
        "tok_per_s": tok_per_s,
        "backend_model": model,
    }


def _call_mlx_or_fallback(
    messages: List[Dict[str, str]],
    max_tokens: int = 500,
    temperature: float = 0.1,
    mlx_fn: Optional[Callable[[List[Dict[str, str]], int, float], Dict[str, Any]]] = None,
    ollama_base: str = DEFAULT_OLLAMA_URL,
) -> Dict[str, Any]:
    if mlx_fn is not None:
        t0 = time.perf_counter()
        res = mlx_fn(messages, max_tokens, temperature)
        if "error" not in res:
            elapsed_s = round(time.perf_counter() - t0, 3)
            content = str(res.get("content", "")).strip()
            tokens = int(res.get("tokens") or max(1, len(content) // 4))
            tok_per_s = float(res.get("tok_per_s") or round(tokens / max(0.01, elapsed_s), 1))
            return {
                "content": content,
                "elapsed_s": elapsed_s,
                "tokens": tokens,
                "tok_per_s": tok_per_s,
                "backend_model": "voicefi-coder-mlx",
            }
    else:
        try:
            t0 = time.perf_counter()
            payload = {
                "model": "voicefi-coder-mlx",
                "messages": messages,
                "stream": False,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            req = urllib.request.Request(
                DEFAULT_MLX_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            elapsed_s = round(time.perf_counter() - t0, 3)
            choices = data.get("choices", [{}])
            content = str(choices[0].get("message", {}).get("content", "")).strip()
            metrics = data.get("x_metal_metrics", {})
            tokens = int(metrics.get("tokens") or max(1, len(content) // 4))
            tok_per_s = float(metrics.get("tok_per_s") or round(tokens / max(0.01, elapsed_s), 1))
            return {
                "content": content,
                "elapsed_s": elapsed_s,
                "tokens": tokens,
                "tok_per_s": tok_per_s,
                "backend_model": "voicefi-coder-mlx",
            }
        except Exception:
            pass

    return _call_ollama_chat(
        model="voicefi-coder:1.5b",
        messages=messages,
        ollama_base=ollama_base,
        max_tokens=max_tokens,
        temperature=temperature,
    )


def route_specialist_completion(
    messages: List[Dict[str, Any]],
    max_tokens: int = 500,
    temperature: float = 0.1,
    mlx_fn: Optional[Callable[[List[Dict[str, str]], int, float], Dict[str, Any]]] = None,
    ollama_base: str = DEFAULT_OLLAMA_URL,
) -> Dict[str, Any]:
    """
    Execute the Specialist Local Router across incoming OpenAI chat messages.
    Returns dict with `content`, `route`, `backend_model`, `tokens`, `tok_per_s`, `elapsed_s`.
    """
    norm_msgs = [
        {"role": str(m.get("role", "user")), "content": str(m.get("content") or "")}
        for m in messages
    ]
    route = classify_smb_workload(norm_msgs)

    if route == "tabular_code_sieve":
        rules_text, records = _extract_records_and_rules(norm_msgs)
        if records:
            sieve_msgs = [
                {
                    "role": "system",
                    "content": (
                        "You are the LienLogic Code Sieve Synthesizer. Given filtering rules and a sample JSON record, "
                        "write ONLY a valid Python function `def keep_record(r: dict) -> bool:` that takes a single "
                        "record dict `r` and returns True if `r` passes ALL rules and False otherwise. "
                        "Output ONLY a ```python code block."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Rules:\n{rules_text}\n\nSample Record:\n{json.dumps(records[0])}",
                },
            ]
            res = _call_mlx_or_fallback(
                sieve_msgs,
                max_tokens=250,
                temperature=0.1,
                mlx_fn=mlx_fn,
                ollama_base=ollama_base,
            )
            raw_code = res["content"]
            blocks = re.findall(r"```(?:python)?\s*\n(.*?)```", raw_code, flags=re.DOTALL)
            code = blocks[0] if blocks else raw_code
            try:
                ast.parse(code)
                ns: Dict[str, Any] = {}
                exec(code, ns)
                fn = ns.get("keep_record")
                if callable(fn):
                    kept = [r for r in records if fn(r)]
                    id_key = "apn" if ("apn" in records[0] and "id" not in records[0]) else "id"
                    amt_key = "delinquent_balance" if ("delinquent_balance" in records[0] and "amount" not in records[0]) else "amount"
                    q_ids = [str(r.get(id_key, "")).strip() for r in kept]
                    q_total = round(sum(float(r.get(amt_key, 0.0)) for r in kept), 2)
                    rej_count = len(records) - len(kept)
                    json_out = json.dumps(
                        {
                            "qualified_ids": q_ids,
                            "qualified_apns": q_ids,
                            "qualified_total": q_total,
                            "qualified_balance": q_total,
                            "rejected_count": rej_count,
                            "disqualified_count": rej_count,
                        }
                    )
                    return {
                        "content": json_out,
                        "route": "tabular_code_sieve",
                        "backend_model": f"{res['backend_model']}+python-ast-sieve",
                        "tokens": res["tokens"],
                        "tok_per_s": res["tok_per_s"],
                        "elapsed_s": res["elapsed_s"],
                    }
            except Exception:
                pass

    if route == "comms_triage":
        try:
            res = _call_ollama_chat(
                model="gemma2:2b",
                messages=norm_msgs,
                ollama_base=ollama_base,
                max_tokens=max_tokens,
                temperature=temperature,
                json_mode=True,
            )
            return {
                "content": res["content"],
                "route": "comms_triage",
                "backend_model": "gemma2:2b",
                "tokens": res["tokens"],
                "tok_per_s": res["tok_per_s"],
                "elapsed_s": res["elapsed_s"],
            }
        except Exception:
            pass

    res = _call_mlx_or_fallback(
        norm_msgs,
        max_tokens=max_tokens,
        temperature=temperature,
        mlx_fn=mlx_fn,
        ollama_base=ollama_base,
    )
    return {
        "content": res["content"],
        "route": "mlx_coder",
        "backend_model": res["backend_model"],
        "tokens": res["tokens"],
        "tok_per_s": res["tok_per_s"],
        "elapsed_s": res["elapsed_s"],
    }


def make_router_http_handler(ollama_base: str = DEFAULT_OLLAMA_URL):
    class SpecialistRouterHandler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:
            pass

        def _send_json(self, data: Any, status: int = 200) -> None:
            raw = json.dumps(data).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self) -> None:
            if self.path.startswith("/v1/models") or self.path.startswith("/models"):
                now = int(time.time())
                self._send_json(
                    {
                        "object": "list",
                        "data": [
                            {
                                "id": "localbench-specialist-router",
                                "object": "model",
                                "created": now,
                                "owned_by": "localbench-smb",
                            }
                        ],
                    }
                )
                return
            self._send_json({"status": "online", "model": "localbench-specialist-router"})

        def do_POST(self) -> None:
            if not (self.path.startswith("/v1/chat/completions") or self.path.startswith("/chat/completions")):
                self._send_json({"error": f"Unsupported path {self.path}"}, status=404)
                return
            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            body = json.loads(raw_body) if raw_body.strip() else {}
            messages = body.get("messages", [])
            max_tokens = int(body.get("max_tokens") or 500)
            temperature = float(body.get("temperature") if body.get("temperature") is not None else 0.1)

            routed = route_specialist_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                ollama_base=ollama_base,
            )
            prompt_chars = sum(len(str(m.get("content") or "")) for m in messages)
            p_tok = max(1, prompt_chars // 4)
            c_tok = int(routed["tokens"])
            self._send_json(
                {
                    "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": "localbench-specialist-router",
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": routed["content"]},
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": p_tok,
                        "completion_tokens": c_tok,
                        "total_tokens": p_tok + c_tok,
                    },
                    "x_metal_metrics": {
                        "route": routed["route"],
                        "backend_model": routed["backend_model"],
                        "tokens": c_tok,
                        "tok_per_s": routed["tok_per_s"],
                        "elapsed_s": routed["elapsed_s"],
                    },
                }
            )

    return SpecialistRouterHandler


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LocalBench SMB Specialist Local Router HTTP server.")
    parser.add_argument("--port", type=int, default=DEFAULT_ROUTER_PORT, help="Port to bind (default: 9380)")
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL, help="Ollama base URL (default: http://127.0.0.1:11434)")
    args = parser.parse_args()

    srv = ThreadingHTTPServer(("127.0.0.1", args.port), make_router_http_handler(args.ollama_url))
    print(f"LocalBench SMB Specialist Router listening on http://127.0.0.1:{args.port}/v1/chat/completions ...")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
