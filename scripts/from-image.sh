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
  echo "from-image: IR json=${JSON}" >&2
  cat "$JSON"
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
lines.append('(display "=== IR comps ===") (newline)')
for c in comps:
    extra = f" n3={c.get('n3')}" if c.get("type") == "Q" else ""
    row = (
        f"  {c.get('type')} {c.get('name')} "
        f"n1={c.get('n1')} n2={c.get('n2')}{extra} ={c.get('value')}"
    )
    lines.append(f"(display {json.dumps(row)}) (newline)")
lines += [
    "(define r (daed:from-ir ir 12))",
    '(display "source=vlm ok=")',
    "(display (daed:pipe-ok? r))",
    '(display " reason=")',
    "(display (daed:pipe-reason r))",
    "(newline)",
    "(define ckt (daed:pipe-circuit r))",
    "(define sim (daed:pipe-sim r))",
    '(display "=== SPICE ===") (newline)',
    "(display (daed:circuit->spice ckt))",
    '(display "=== .op nodes ===") (newline)',
    "(let ((nmax (daed:max-node (daed:ckt-comps ckt))))",
    "  (let loop ((i 0))",
    "    (if (> i nmax) 0",
    "      (begin",
    '        (display "v(") (display i) (display ")=")',
    "        (display (daed:v sim i)) (newline)",
    "        (loop (+ i 1))))))",
]

has_dyn = any(c.get("type") in ("C", "L") for c in comps)
qcols = [c.get("n1") for c in comps if c.get("type") == "Q"]
watch = qcols or [2, 3]
if has_dyn:
    csv_path = str(Path(sys.argv[1]).with_suffix(".tran.csv"))
    lines += [
        '(display "note: .op treats C as open; oscillation is .tran") (newline)',
        "(define tr (daed:simulate-tran ckt 0.1 40))",
        '(display "=== .tran tstop=")',
        "(display (daed:tran-tstop tr))",
        '(display " ok=")',
        "(display (daed:tran-ok? tr))",
        "(newline)",
        "(let ((ts (list 0.0 0.4 0.8 1.2 1.6 2.0 2.4 2.8 3.2 4.0)))",
        "  (let loop ((xs ts))",
        "    (if (null? xs) 0",
        "      (begin",
        '        (display "  t=") (display (car xs))',
    ]
    for n in watch:
        lines += [
            f'        (display " v({n})=")',
            f"        (display (daed:tran-v-at-t tr {n} (car xs)))",
        ]
    lines += [
        "        (newline)",
        "        (loop (cdr xs))))))",
    ]
    for n in watch:
        lines += [
            f"(let ((mx (daed:measure-max tr {n})) (mn (daed:measure-min tr {n})))",
            f'  (display "  pp v({n})=")',
            "  (display (- (daed:meas-value mx) (daed:meas-value mn)))",
            "  (newline))",
        ]
    lines += [
        f"(daed:write-tran-csv! tr {json.dumps(csv_path)})",
        f'(display "tran csv={csv_path}") (newline)',
    ]

lines += [
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
