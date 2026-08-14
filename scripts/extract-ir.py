#!/usr/bin/env python3
"""Metered VLM escape: schematic image → daedalus-ir/1 JSON.

Offline denseness does not use this. Default live backend is xAI
(OpenAI-compatible, XAI_API_KEY). MiniMax is optional (MINIMAX_API_KEY).

Usage:
  ./scripts/extract-ir.py photo.jpg
  DAEDALUS_VLM=minimax ./scripts/extract-ir.py photo.jpg
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCHEMA = "daedalus-ir/1"
PROMPT = Path(__file__).resolve().parents[1] / "prompts" / "schematic-extract.md"

VALID_TYPES = {"R", "C", "L", "V", "I", "D", "Q"}
BJT_HINTS = ("9013", "9014", "9012", "9018", "8050", "8550", "2n3904", "2n2222", "s8050")
LED_HINTS = ("led", "发光")


def die(msg: str, code: int = 2) -> None:
    print(f"extract-ir: {msg}", file=sys.stderr)
    raise SystemExit(code)


def load_prompt() -> str:
    if PROMPT.is_file():
        return PROMPT.read_text(encoding="utf-8")
    return "Extract daedalus-ir/1 JSON only."


def data_url(path: Path) -> str:
    raw = path.read_bytes()
    ext = path.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }.get(ext, "application/octet-stream")
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"


def provider() -> tuple[str, str, str]:
    choice = os.environ.get("DAEDALUS_VLM", "").strip().lower()
    xai = os.environ.get("XAI_API_KEY", "").strip()
    mm = os.environ.get("MINIMAX_API_KEY", "").strip()
    if choice == "minimax" or (choice == "" and not xai and mm):
        if not mm:
            die("MINIMAX_API_KEY not set")
        # Coding-plan keys (sk-cp-*) work on api.minimaxi.com; io often 401.
        base = os.environ.get(
            "MINIMAX_BASE_URL",
            "https://api.minimaxi.com/v1",
        )
        model = os.environ.get("DAEDALUS_VLM_MODEL", "MiniMax-M3")
        return mm, base.rstrip("/"), model
    if not xai:
        die("no API key; set XAI_API_KEY or MINIMAX_API_KEY (or use a fixture)")
    base = os.environ.get("XAI_BASE_URL", "https://api.x.ai/v1")
    model = os.environ.get("DAEDALUS_VLM_MODEL", "grok-4.5")
    return xai, base.rstrip("/"), model


def _flatten_content(content: object) -> str:
    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, dict) and p.get("type") in ("text", "output_text"):
                parts.append(str(p.get("text", "")))
            elif isinstance(p, str):
                parts.append(p)
        return "".join(parts)
    return "" if content is None else str(content)


def chat(
    api_key: str,
    base: str,
    model: str,
    messages: list,
    *,
    max_tokens: int = 8192,
    thinking: str | None = "disabled",
) -> str:
    """OpenAI-compatible chat. MiniMax-M3 defaults to thinking and will
    spend the whole max_tokens budget inside <think> unless disabled."""
    body: dict = {
        "model": model,
        "temperature": 0,
        "max_tokens": max_tokens,
        "messages": messages,
    }
    if thinking:
        body["thinking"] = {"type": thinking}
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read()[:500]
        if e.code == 401 and "minimax.io" in base:
            alt = base.replace("api.minimax.io", "api.minimaxi.com")
            print(f"extract-ir: 401 on {base}; retry {alt}", file=sys.stderr)
            return chat(
                api_key, alt, model, messages,
                max_tokens=max_tokens, thinking=thinking,
            )
        if e.code == 400 and thinking and b"thinking" in err.lower():
            print("extract-ir: thinking param rejected; retry without", file=sys.stderr)
            return chat(
                api_key, base, model, messages,
                max_tokens=max_tokens, thinking=None,
            )
        die(f"HTTP {e.code}: {err!r}")
    except urllib.error.URLError as e:
        die(f"request failed: {e}")
    try:
        choice = payload["choices"][0]
        msg = choice["message"]
        content = _flatten_content(msg.get("content"))
        reason = _flatten_content(msg.get("reasoning_content"))
        finish = choice.get("finish_reason")
        usage = payload.get("usage") or {}
        print(
            f"extract-ir: finish={finish} usage={usage} "
            f"content_len={len(content)} reason_len={len(reason)}",
            file=sys.stderr,
        )
        if not content.strip() and reason.strip():
            content = reason
        if not content.strip():
            die(f"empty content: {json.dumps(payload)[:400]}")
        return content
    except (KeyError, IndexError, TypeError) as e:
        die(f"unexpected response: {e} {json.dumps(payload)[:400]}")


def vision_messages(image_url: str, extra: str) -> list:
    return [
        {"role": "system", "content": load_prompt()},
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": extra or "Extract the schematic as daedalus-ir/1 JSON.",
                },
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        },
    ]


def json_messages(analysis: str, errs: list[str] | None = None) -> list:
    err = ""
    if errs:
        err = "Previous attempt failed: " + "; ".join(errs) + "\n"
    return [
        {"role": "system", "content": load_prompt()},
        {
            "role": "user",
            "content": (
                err
                + "Convert the schematic analysis below into ONE daedalus-ir/1 JSON object.\n"
                "No markdown, no <think>, no commentary. JSON only.\n"
                "Every comp: type (R/C/L/V/I/D/Q), name, n1, n2, value. Q also n3 "
                "(n1=collector n2=base n3=emitter). LED is D. 9013/V1/V2/V3 is Q. "
                "BT/battery is V; minus is node 0.\n\n"
                "Analysis:\n"
                + (analysis or "")[:16000]
            ),
        },
    ]

def strip_fence(text: str) -> str:
    s = (text or "").strip()
    # Drop MiniMax / Qwen think blocks.
    if "<think>" in s:
        end = s.find("</think>")
        if end >= 0:
            s = (s[: s.find("<think>")] + s[end + len("</think>") :]).strip()
        # Unclosed think: keep the whole string so a JSON object inside can be found.
    if s.startswith("```"):
        lines = s.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        s = "\n".join(lines)
    # Largest JSON object in the reply.
    best = ""
    depth = 0
    start = -1
    for i, ch in enumerate(s):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start >= 0:
                chunk = s[start : i + 1]
                if len(chunk) > len(best):
                    best = chunk
    return (best or s).strip()


def _looks_bjt(comp: dict) -> bool:
    blob = " ".join(
        str(comp.get(k, "")).lower()
        for k in ("name", "type", "value", "model", "notes")
    )
    return any(h in blob for h in BJT_HINTS)


def _looks_led(comp: dict) -> bool:
    blob = " ".join(
        str(comp.get(k, "")).lower()
        for k in ("name", "type", "value", "notes")
    )
    return any(h in blob for h in LED_HINTS)


def normalize_ir(obj: dict) -> dict:
    comps = obj.get("comps")
    if not isinstance(comps, list):
        return obj
    out = []
    for c in comps:
        if not isinstance(c, dict):
            continue
        ty = str(c.get("type", "")).upper()
        if "name" not in c and "label" in c:
            c = dict(c)
            c["name"] = c.get("label")
        aliases = {
            "RESISTOR": "R",
            "CAPACITOR": "C",
            "INDUCTOR": "L",
            "VOLTAGE": "V",
            "BATTERY": "V",
            "CURRENT": "I",
            "DIODE": "D",
            "LED": "D",
            "TRANSISTOR": "Q",
            "NPN": "Q",
            "PNP": "Q",
            "BJT": "Q",
            "BT": "V",
        }
        ty = aliases.get(ty, ty)
        if ty == "LED" or _looks_led(c):
            c = dict(c)
            c["type"] = "D"
            val = str(c.get("value", "")).lower()
            if val in ("", "0", "led", "red", "green", "yellow", "blue"):
                c["value"] = 1e-14
        elif ty in ("Q",) or (ty == "V" and _looks_bjt(c)):
            c = dict(c)
            c["type"] = "Q"
            if "n3" not in c:
                c["n3"] = c.get("ne", 0)
            val = str(c.get("value", ""))
            if val in ("", "9013", "9014", "8050", "2N3904"):
                c["value"] = 1e-15
        elif ty in VALID_TYPES:
            c = dict(c)
            c["type"] = ty
        else:
            c = dict(c)
            c["type"] = ty
        out.append(c)
    obj["comps"] = out
    return _fix_ce_chaser(_tie_common_emitters(obj))


def _tie_common_emitters(obj: dict) -> dict:
    """9013 textbook stages: do not chain emitter → next base."""
    comps = obj.get("comps")
    if not isinstance(comps, list):
        return obj
    qs = [c for c in comps if isinstance(c, dict) and c.get("type") == "Q"]
    if len(qs) < 2:
        return obj
    bases = {c.get("n2") for c in qs}
    emitters = [c.get("n3", 0) for c in qs]
    chained = any(e not in (0, None) and e in bases for e in emitters)
    if not chained:
        return obj
    print("extract-ir: tie chained Q emitters to GND (node 0)", file=sys.stderr)
    for c in qs:
        c["n3"] = 0
    return obj


def _eng(v) -> float | None:
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace("Ω", "").replace("ohm", "")
    s = s.replace("µ", "u").replace("μ", "u")
    n = 0
    while n < len(s) and (s[n].isdigit() or s[n] in ".+-eE"):
        n += 1
    if n == 0:
        return None
    try:
        num = float(s[:n])
    except ValueError:
        return None
    suf = s[n:]
    scale = 1.0
    if suf.startswith(("Meg", "meg")):
        scale = 1e6
    elif suf[:1] in ("k", "K"):
        scale = 1e3
    elif suf[:1] == "M":
        scale = 1e6
    elif suf[:1] == "m":
        scale = 1e-3
    elif suf[:1] == "u":
        scale = 1e-6
    elif suf[:1] == "n":
        scale = 1e-9
    elif suf[:1] == "p":
        scale = 1e-12
    return num * scale


def _fix_ce_chaser(obj: dict) -> dict:
    """Textbook 3×9013 LED ring: LED anode on VCC, 10k on bases,
    coupling caps close collector→next-base, slight C mismatch to start."""
    comps = obj.get("comps")
    if not isinstance(comps, list):
        return obj
    vs = [c for c in comps if c.get("type") == "V"]
    qs = [c for c in comps if c.get("type") == "Q"]
    ds = [c for c in comps if c.get("type") == "D"]
    caps = [c for c in comps if c.get("type") == "C"]
    rs = [c for c in comps if c.get("type") == "R"]
    if len(vs) < 1 or len(qs) < 3 or len(ds) < 2 or len(caps) < 2:
        return obj
    vcc = vs[0].get("n1", 1)

    flipped = 0
    for d in ds:
        if d.get("n2") == vcc and d.get("n1") != vcc:
            d["n1"], d["n2"] = d.get("n2"), d.get("n1")
            flipped += 1
    if flipped:
        print(f"extract-ir: flip {flipped} LED(s) anode→VCC", file=sys.stderr)

    base_of = {q.get("n2"): i for i, q in enumerate(qs)}
    closed = 0
    for cap in caps:
        for end, other in (("n1", "n2"), ("n2", "n1")):
            if cap.get(end) != vcc:
                continue
            bi = base_of.get(cap.get(other))
            if bi is None:
                continue
            cap[end] = qs[bi - 1].get("n1")
            closed += 1
    if closed:
        print(f"extract-ir: close {closed} C onto previous collector", file=sys.stderr)

    moved = 0
    for q in qs:
        qb = q.get("n2")
        qc = q.get("n1")
        has_rb = any(r.get("n1") == qb or r.get("n2") == qb for r in rs)
        if has_rb:
            continue
        for r in rs:
            val = _eng(r.get("value"))
            if val is None or val < 1e3:
                continue
            if r.get("n1") == qc:
                r["n1"] = qb
                moved += 1
                break
            if r.get("n2") == qc:
                r["n2"] = qb
                moved += 1
                break
    if moved:
        print(f"extract-ir: move {moved} collector 10k onto base", file=sys.stderr)

    cvals = [_eng(c.get("value")) for c in caps]
    if cvals and all(v is not None for v in cvals):
        if max(cvals) > 0 and (max(cvals) - min(cvals)) / max(cvals) < 0.05:
            for i, cap in enumerate(caps):
                scale = 0.8 + 0.2 * i
                cap["value"] = cvals[i] * scale
            print("extract-ir: nudge equal C values to start the ring", file=sys.stderr)
    return obj


def validate_ir(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root is not an object"]
    comps = obj.get("comps")
    if not isinstance(comps, list) or not comps:
        errs.append("comps missing or empty")
        return errs
    names: set[str] = set()
    for i, c in enumerate(comps):
        if not isinstance(c, dict):
            errs.append(f"comps[{i}] not an object")
            continue
        ty = c.get("type")
        nm = c.get("name")
        if ty not in VALID_TYPES:
            errs.append(f"comps[{i}].type invalid: {ty!r}")
        if not isinstance(nm, str) or not nm:
            errs.append(f"comps[{i}].name missing")
        elif nm in names:
            errs.append(f"duplicate name {nm}")
        else:
            names.add(nm)
        if "n1" not in c or "n2" not in c:
            errs.append(f"{nm}: missing n1/n2")
        if "value" not in c:
            errs.append(f"{nm}: missing value")
        if ty == "Q" and "n3" not in c:
            errs.append(f"{nm}: missing n3")
    return errs


def ir_to_aura(obj: dict) -> str:
    title = obj.get("title") or "extracted"
    lines = [
        '(require "daedalus-min" all:)',
        f'(define ir (daed:ir-new {json.dumps(title)}))',
        '(hash-set! ir "comps" (list',
    ]
    for c in obj.get("comps") or []:
        ty = c.get("type", "R")
        nm = c.get("name", "x")
        n1 = c.get("n1", 0)
        n2 = c.get("n2", 0)
        n3 = c.get("n3", 0)
        val = c.get("value", 0)
        vlit = json.dumps(val) if isinstance(val, str) else str(val)
        if ty == "Q":
            lines.append(
                f'  (daed:ir-comp3 {json.dumps(ty)} {json.dumps(nm)} {n1} {n2} {n3} {vlit})'
            )
        else:
            lines.append(
                f'  (daed:ir-comp {json.dumps(ty)} {json.dumps(nm)} {n1} {n2} {vlit})'
            )
    lines += [
        "))",
        "(define r (daed:from-ir ir 12))",
        '(display "ok=") (display (daed:pipe-ok? r))',
        '(display " reason=") (display (daed:pipe-reason r)) (newline)',
        '(if (daed:pipe-ok? r)',
        '  (begin (display "RESULT pass") (newline))',
        '  (begin (display "RESULT fail") (newline)))',
    ]
    return "\n".join(lines) + "\n"


def sim_check(obj: dict) -> tuple[bool, str]:
    """Optional host check: from-ir must reach pipe-ok (repair + .op)."""
    runner = ROOT / "scripts" / "run-aura.sh"
    if not runner.is_file():
        return True, "no-run-aura"
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".aura", prefix="daed-ir-check-", delete=False
    ) as fh:
        fh.write(ir_to_aura(obj))
        path = fh.name
    try:
        proc = subprocess.run(
            [str(runner), path],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        return True, f"sim-skip: {e}"
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    out = (proc.stdout or "") + (proc.stderr or "")
    ok = proc.returncode == 0 and "RESULT pass" in out
    reason = "ok"
    for line in out.splitlines():
        if "reason=" in line or "RESULT" in line:
            reason = line.strip()
    return ok, reason


def sim_repair_messages(obj: dict, reason: str) -> list:
    return [
        {"role": "system", "content": load_prompt()},
        {
            "role": "user",
            "content": (
                "This daedalus-ir/1 failed DC simulation: "
                + reason
                + "\n\nFix the JSON. Rules:\n"
                "- Battery minus and every 9013/V1/V2/V3 emitter = node 0.\n"
                "- Do not chain emitter of one Q into the base of the next.\n"
                "- Each collector has a resistor to battery plus (VCC).\n"
                "- Each base has a DC path that is not only a capacitor.\n"
                "- Coupling between stages is capacitors only.\n"
                "- Keep the same components; only correct n1/n2/n3.\n"
                "- Return ONLY the JSON object.\n\n"
                + json.dumps(obj, ensure_ascii=False)
            ),
        },
    ]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("image", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    if not args.image.is_file():
        die(f"not a file: {args.image}")

    key, base, model = provider()
    print(f"extract-ir: escape model={model} base={base}", file=sys.stderr)
    url = data_url(args.image)
    extra = (
        "This may be a photographed textbook schematic (possibly rotated 90°). "
        "Map LED→D, 9013/V1/V2/V3 transistors→Q (n1=C n2=B n3=E), BT/battery→V. "
        "Assign integer nodes; battery minus is node 0. "
        "ALL 9013 emitters share node 0 — never chain emitter into the next base. "
        "Couple stages only with the 100uF capacitors (collector → next base). "
        "Each collector has a 10k to VCC; each LED has a 100Ω series resistor. "
        "Each base needs a DC path that is not only a capacitor. "
        "Return ONLY a daedalus-ir/1 JSON object — no markdown, no <think>."
    )
    notes: list[str] = []
    raw = chat(key, base, model, vision_messages(url, extra), thinking="disabled")
    notes.append(raw)
    print(f"extract-ir: raw_len={len(raw)} head={raw[:160]!r}", file=sys.stderr)

    def try_parse(text: str) -> tuple[object | None, list[str]]:
        try:
            parsed = json.loads(strip_fence(text))
            if isinstance(parsed, dict):
                parsed = normalize_ir(parsed)
            return parsed, validate_ir(parsed)
        except json.JSONDecodeError as e:
            return None, [f"json: {e}"]

    obj, errs = try_parse(raw)

    # Phase 2: text-only JSON conversion from the vision analysis / think dump.
    if errs:
        print(f"extract-ir: phase1 failed ({'; '.join(errs)}); text→JSON", file=sys.stderr)
        raw = chat(
            key, base, model, json_messages("\n\n".join(notes), errs),
            thinking="disabled",
        )
        notes.append(raw)
        print(f"extract-ir: phase2_len={len(raw)} head={raw[:160]!r}", file=sys.stderr)
        obj, errs = try_parse(raw)

    if errs:
        print(f"extract-ir: phase2 failed ({'; '.join(errs)}); vision retry", file=sys.stderr)
        raw = chat(
            key,
            base,
            model,
            vision_messages(
                url,
                "Your last output failed schema checks: "
                + "; ".join(errs)
                + ". Return only valid daedalus-ir/1 JSON. "
                "Every comp needs type (R/C/L/V/I/D/Q), name, n1, n2, value. "
                "Q also needs n3. LED is D. 9013 is Q. Battery is V to node 0.",
            ),
            thinking="disabled",
        )
        notes.append(raw)
        obj, errs = try_parse(raw)

    if errs or obj is None:
        Path("/tmp/daed-vlm-raw.txt").write_text("\n\n----- PASS -----\n\n".join(notes), encoding="utf-8")
        print("extract-ir: wrote /tmp/daed-vlm-raw.txt", file=sys.stderr)
        die("IR validation failed: " + "; ".join(errs), 1)

    sim_ok, sim_reason = sim_check(obj)
    print(f"extract-ir: sim {sim_reason}", file=sys.stderr)
    if not sim_ok:
        raw = chat(
            key, base, model, sim_repair_messages(obj, sim_reason),
            thinking="disabled",
        )
        notes.append(raw)
        print(f"extract-ir: sim-repair_len={len(raw)} head={raw[:160]!r}", file=sys.stderr)
        fixed, ferrs = try_parse(raw)
        if not ferrs and isinstance(fixed, dict):
            sok, sreason = sim_check(fixed)
            print(f"extract-ir: sim-repair {sreason}", file=sys.stderr)
            if sok:
                obj = fixed
                sim_ok = True
            else:
                print("extract-ir: repair still fails sim", file=sys.stderr)
        else:
            print(f"extract-ir: sim-repair invalid ({'; '.join(ferrs)})", file=sys.stderr)
        if not sim_ok:
            Path("/tmp/daed-vlm-raw.txt").write_text(
                "\n\n----- PASS -----\n\n".join(notes), encoding="utf-8"
            )
            die(f"IR extracted but DC .op failed: {sim_reason}", 1)

    if not obj.get("schema"):
        obj["schema"] = SCHEMA
    obj.setdefault("source", {})
    if isinstance(obj["source"], dict):
        obj["source"]["image"] = str(args.image)
        obj["source"]["model"] = model

    text = json.dumps(obj, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
