#!/usr/bin/env bash
# Optional host oracle: run ngspice on decks written by probe 25.
# Missing ngspice or missing decks → RESULT skip (exit 0).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
OUT="$ROOT/examples/25-spice-export/out"

if ! command -v ngspice >/dev/null 2>&1; then
  echo "ngspice not installed; skip export round-trip"
  echo "RESULT skip example=export-roundtrip reason=no-ngspice"
  exit 0
fi

if [[ ! -f "$OUT/divider.cir" || ! -f "$OUT/tuned.cir" ]]; then
  echo "export decks missing; run probe 25 first (or skip)"
  echo "RESULT skip example=export-roundtrip reason=no-decks"
  exit 0
fi

lookup() {
  local want
  want="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
  awk -v want="$want" '
    BEGIN { FS="=" }
    {
      k=$1
      gsub(/^[ \t]+|[ \t]+$/, "", k)
      k=tolower(k)
      if (k==want) {
        v=$2
        gsub(/^[ \t]+|[ \t]+$/, "", v)
        print v
        exit
      }
    }
  ' "$2"
}

check() {
  local cir="$1" key="$2" expected="$3" abs_tol="$4"
  local log got ok delta
  log="/tmp/daedalus-export-$(basename "$cir" .cir).log"
  if ! ngspice -b "$cir" >"$log" 2>&1; then
    echo "ngspice failed: $cir" >&2
    return 1
  fi
  got="$(lookup "$key" "$log")"
  if [[ -z "$got" ]]; then
    echo "no $key in $(basename "$cir")" >&2
    return 1
  fi
  ok="$(awk -v g="$got" -v e="$expected" -v t="$abs_tol" 'BEGIN {
    d = g - e
    if (d < 0) d = -d
    if (d < t + 0.0) { print "PASS"; exit 0 }
    print "FAIL"; exit 1
  }')" || true
  delta="$(awk -v g="$got" -v e="$expected" 'BEGIN {
    d = g - e
    if (d < 0) d = -d
    printf "%.6g", d
  }')"
  echo "$(basename "$cir") $key got=$got want=$expected |d|=$delta bound=$abs_tol $ok"
  [[ "$ok" == "PASS" ]]
}

pass=0
fail=0
if check "$OUT/divider.cir" "v(2)" "3.333333" "1e-4"; then pass=$((pass+1)); else fail=$((fail+1)); fi
if check "$OUT/tuned.cir" "v(2)" "2.5" "1e-4"; then pass=$((pass+1)); else fail=$((fail+1)); fi
if [[ -f "$OUT/diode-series.cir" ]]; then
  if check "$OUT/diode-series.cir" "v(2)" "0.696459" "2e-3"; then pass=$((pass+1)); else fail=$((fail+1)); fi
fi
if [[ -f "$OUT/bjt-ce.cir" ]]; then
  if check "$OUT/bjt-ce.cir" "v(2)" "2.700149" "5e-3"; then pass=$((pass+1)); else fail=$((fail+1)); fi
fi

echo
echo "export-roundtrip pass=$pass fail=$fail"
if [[ "$fail" -ne 0 ]]; then
  echo "RESULT fail example=export-roundtrip"
  exit 1
fi
echo "RESULT pass example=export-roundtrip escapes=0"
exit 0
