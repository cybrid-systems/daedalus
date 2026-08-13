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
import sys
import urllib.error
import urllib.request
from pathlib import Path

SCHEMA = "daedalus-ir/1"
PROMPT = Path(__file__).resolve().parents[1] / "prompts" / "schematic-extract.md"

VALID_TYPES = {"R", "C", "L", "V", "I", "D", "Q"}


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
        base = os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.io/v1")
        model = os.environ.get("DAEDALUS_VLM_MODEL", "MiniMax-M3")
        return mm, base.rstrip("/"), model
    if not xai:
        die("no API key; set XAI_API_KEY or MINIMAX_API_KEY (or use a fixture)")
    base = os.environ.get("XAI_BASE_URL", "https://api.x.ai/v1")
    model = os.environ.get("DAEDALUS_VLM_MODEL", "grok-4.5")
    return xai, base.rstrip("/"), model


def chat(api_key: str, base: str, model: str, image_url: str, extra: str) -> str:
    body = {
        "model": model,
        "temperature": 0,
        "messages": [
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
        ],
    }
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        die(f"HTTP {e.code}: {e.read()[:400]!r}")
    except urllib.error.URLError as e:
        die(f"request failed: {e}")
    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        die(f"unexpected response: {e}")


def strip_fence(text: str) -> str:
    s = text.strip()
    if s.startswith("```"):
        lines = s.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        s = "\n".join(lines)
    return s.strip()


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
    return errs


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
    raw = chat(key, base, model, url, "")
    errs = ["parse"]
    obj = None
    for attempt in range(2):
        try:
            obj = json.loads(strip_fence(raw if attempt == 0 else raw))
            errs = validate_ir(obj)
        except json.JSONDecodeError as e:
            errs = [f"json: {e}"]
            obj = None
        if not errs:
            break
        if attempt == 0:
            raw = chat(
                key,
                base,
                model,
                url,
                "Your last output failed schema checks: "
                + "; ".join(errs)
                + ". Return only valid daedalus-ir/1 JSON.",
            )

    if errs or obj is None:
        die("IR validation failed: " + "; ".join(errs), 1)

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
