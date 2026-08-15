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

OUT_DIR="$ROOT/examples/10-vision-pipeline/out"
mkdir -p "$OUT_DIR"
HTML_REL="examples/10-vision-pipeline/out/${STEM}.html"
PHOTO_NAME="$(basename "$IMG")"
cp -f "$IMG" "$OUT_DIR/$PHOTO_NAME"

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
    (let ((ckt (daed:pipe-circuit r)))
      (hash-set! ckt "source-image" "./${PHOTO_NAME}")
      (let ((n (write-file "$HTML_REL" (daed:circuit->html ckt (daed:pipe-sim r)))))
        (display "html=")
        (display (if (> n 0) "$HTML_REL" "write-fail"))
        (newline)))
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
  cp -f "$JSON" "$OUT_DIR/${STEM}.json"
  if [[ -f "${JSON%.json}.minimax.json" ]]; then
    cp -f "${JSON%.json}.minimax.json" "$OUT_DIR/${STEM}.minimax.json"
    echo "from-image: MiniMax JSON=${OUT_DIR}/${STEM}.minimax.json" >&2
  fi
  echo "from-image: IR json copy=${OUT_DIR}/${STEM}.json" >&2
  cat "$JSON"
  cat > "$DRIVER" <<EOF
(require "daedalus-min" all:)
(define ir (daed:ir-ingest "$JSON"))
(display "=== IR comps ===") (newline)
(let loop ((cs (daed:ir-comps ir)))
  (if (null? cs) 0
    (begin
      (let ((c (car cs)))
        (display "  ") (display (hash-ref c "type" "?"))
        (display " ") (display (hash-ref c "name" "?"))
        (display " n1=") (display (hash-ref c "n1" "?"))
        (display " n2=") (display (hash-ref c "n2" "?"))
        (if (hash-ref c "n3" #f)
          (begin (display " n3=") (display (hash-ref c "n3"))) 0)
        (display " =") (display (hash-ref c "value" "?")) (newline))
      (loop (cdr cs)))))
(define r (daed:from-ir ir 12))
(display "source=json ok=")
(display (daed:pipe-ok? r))
(display " reason=")
(display (daed:pipe-reason r))
(newline)
(define ckt (daed:pipe-circuit r))
(define sim (daed:pipe-sim r))
(display "=== SPICE ===") (newline)
(display (daed:circuit->spice ckt))
(display "=== .op labels ===") (newline)
(let loop ((cs (daed:ir-comps ir)))
  (if (null? cs) 0
    (begin
      (let ((c (car cs)))
        (if (or (equal? (hash-ref c "type" "") "Q")
                (equal? (hash-ref c "type" "") "V"))
          (begin
            (display (hash-ref c "name" "?"))
            (display "=")
            (display (daed:v sim (hash-ref c "n1" 0)))
            (newline))
          0))
      (loop (cdr cs)))))
(hash-set! ckt "source-image" "./${PHOTO_NAME}")
(define nw (write-file "$HTML_REL" (daed:circuit->html ckt sim)))
(display "html=")
(display (if (> nw 0) "$HTML_REL" "write-fail"))
(newline)
(if (daed:pipe-ok? r)
  (begin (display "RESULT pass example=from-image source=json") (newline))
  (begin (display "RESULT fail example=from-image") (newline)))
EOF
  ./scripts/run-aura.sh "$DRIVER"
else
  exit 1
fi
