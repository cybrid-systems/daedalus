#!/usr/bin/env bash
# One-command image → simulate (issue #6 / #11).
#
# Offline: basename matches a registered fixture → pure-Aura from-image.
# Live: if no fixture and an API key is set, extract-ir.py (metered escape)
# then convert JSON to a tiny Aura driver.
#
# Usage:
#   ./scripts/from-image.sh examples/10-vision-pipeline/fixtures/divider.svg

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <image-or-fixture>" >&2
  exit 2
fi

IMG="$1"
if [[ ! -f "$IMG" ]]; then
  echo "error: not a file: $IMG" >&2
  exit 2
fi

STEM="$(basename "$IMG")"
STEM="${STEM%.*}"
DRIVER="$(mktemp /tmp/daed-from-image.XXXXXX.aura)"
cleanup() { rm -f "$DRIVER"; }
trap cleanup EXIT

# Always try the fixture path first (no escape).
cat > "$DRIVER" <<EOF
(require "daedalus-min" all:)
(define r (daed:from-image "$IMG"))
(display "source=")
(display (hash-ref r "source" ""))
(display " ok=")
(display (daed:pipe-ok? r))
(display " reason=")
(display (daed:pipe-reason r))
(newline)
(if (daed:pipe-ok? r)
  (begin
    (display "v1=")
    (display (daed:v (daed:pipe-sim r) 1))
    (display " v2=")
    (display (daed:v (daed:pipe-sim r) 2))
    (newline)
    (display "RESULT pass example=from-image fixture=${STEM}")
    (newline))
  (begin
    (display "RESULT fail example=from-image reason=")
    (display (daed:pipe-reason r))
    (newline)))
EOF

if ./scripts/run-aura.sh "$DRIVER" 2>&1 | tee "/tmp/daed-from-image.log" | tail -20; then
  if grep -q "RESULT pass" /tmp/daed-from-image.log; then
    exit 0
  fi
fi

if grep -q "no-fixture" /tmp/daed-from-image.log 2>/dev/null; then
  if [[ -z "${MINIMAX_API_KEY:-}" && -f "${HOME}/code/keys/minimax" ]]; then
    MINIMAX_API_KEY="$(tr -d ' \n\r' < "${HOME}/code/keys/minimax")"
    export MINIMAX_API_KEY
    export DAEDALUS_VLM="${DAEDALUS_VLM:-minimax}"
    export DAEDALUS_VLM_MODEL="${DAEDALUS_VLM_MODEL:-MiniMax-M3}"
  fi
  if [[ -z "${XAI_API_KEY:-}" && -z "${MINIMAX_API_KEY:-}" ]]; then
    echo "no fixture for ${STEM}; set XAI_API_KEY or MINIMAX_API_KEY to extract" >&2
    exit 1
  fi
  echo "from-image: fixture miss → extract-ir.py (escape)" >&2
  JSON="$(mktemp /tmp/daed-ir.XXXXXX.json)"
  python3 "$ROOT/scripts/extract-ir.py" "$IMG" -o "$JSON"
  python3 - "$JSON" "$DRIVER" <<'PY'
import json, sys
from pathlib import Path
obj = json.loads(Path(sys.argv[1]).read_text())
title = obj.get("title") or "extracted"
comps = obj.get("comps") or []
lines = [
    '(require "daedalus-min" all:)',
    f'(define ir (daed:ir-new {json.dumps(title)}))',
    "(hash-set! ir \"comps\" (list",
]
for c in comps:
    ty = c.get("type", "R")
    nm = c.get("name", "x")
    n1 = c.get("n1", 0)
    n2 = c.get("n2", 0)
    n3 = c.get("n3", 0)
    val = c.get("value", 0)
    if isinstance(val, str):
        vlit = json.dumps(val)
    else:
        vlit = str(val)
    if ty == "Q":
        lines.append(
            f'  (daed:ir-comp3 {json.dumps(ty)} {json.dumps(nm)} {n1} {n2} {n3} {vlit})'
        )
    else:
        lines.append(
            f'  (daed:ir-comp {json.dumps(ty)} {json.dumps(nm)} {n1} {n2} {vlit})'
        )
lines.append("))")
lines += [
    "(define r (daed:from-ir ir 12))",
    '(display "source=vlm ok=")',
    "(display (daed:pipe-ok? r))",
    '(display " reason=")',
    "(display (daed:pipe-reason r))",
    "(newline)",
    "(let ((sim (daed:pipe-sim r)))",
    '  (display "v1=")',
    "  (display (daed:v sim 1))",
    '  (display " v2=")',
    "  (display (daed:v sim 2))",
    '  (display " v3=")',
    "  (display (daed:v sim 3))",
    "  (newline))",
    '(if (daed:pipe-ok? r)',
    '  (begin (display "RESULT pass example=from-image source=vlm") (newline))',
    '  (begin (display "RESULT fail example=from-image") (newline)))',
]
Path(sys.argv[2]).write_text("\n".join(lines) + "\n")
PY
  ./scripts/run-aura.sh "$DRIVER"
else
  exit 1
fi
