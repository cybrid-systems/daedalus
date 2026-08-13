#!/usr/bin/env bash
# Optional host oracle: replay educational .op decks in ngspice and
# compare against frozen refs (same models / T=TNOM=28.555 °C as Daedalus).
# Not on the Aura probe path. Missing ngspice → RESULT skip (exit 0).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

REF="$ROOT/examples/16-nl-op-suite/ref/ngspice.tsv"
SPICE_DIR="$ROOT/examples/16-nl-op-suite/spice"
OUT_DIR="$ROOT/examples/16-nl-op-suite/out"

if ! command -v ngspice >/dev/null 2>&1; then
  echo "ngspice not installed; skip live compare (frozen refs live in probe 16)"
  echo "RESULT skip example=ngspice-compare reason=no-ngspice"
  exit 0
fi

mkdir -p "$OUT_DIR"
report="$OUT_DIR/ngspice-compare.md"
{
  echo "# ngspice live compare"
  echo
  echo "ngspice $(ngspice --version 2>&1 | awk '/ngspice-[0-9]/{print $2; exit}')"
  echo
  echo "| deck | key | got | expected | |Δ| | bound | ok |"
  echo "|------|-----|-----|----------|-----|-------|----|"
} > "$report"

pass=0
fail=0

lc_key() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]'
}

lookup() {
  local deck="$1" key="$2" log="$3"
  local want
  want="$(lc_key "$key")"
  # ngspice prints "v(2) = 6.964593e-01" or "i(vin) = -4.30354e-03"
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
  ' "$log"
}

while read -r deck key expected abs_tol; do
  [[ -z "${deck:-}" || "$deck" == \#* ]] && continue
  cir="$SPICE_DIR/$deck.cir"
  if [[ ! -f "$cir" ]]; then
    echo "MISSING deck $cir" >&2
    fail=$((fail + 1))
    continue
  fi
  log="/tmp/daedalus-ngspice-$deck.log"
  if ! ngspice -b "$cir" >"$log" 2>&1; then
    echo "ngspice failed: $deck" >&2
    fail=$((fail + 1))
    echo "| $deck | $key | FAIL | $expected | — | $abs_tol | FAIL |" >> "$report"
    continue
  fi
  got="$(lookup "$deck" "$key" "$log")"
  if [[ -z "$got" ]]; then
    echo "no $key in $deck output" >&2
    fail=$((fail + 1))
    echo "| $deck | $key | missing | $expected | — | $abs_tol | FAIL |" >> "$report"
    continue
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
  echo "| $deck | $key | $got | $expected | $delta | $abs_tol | $ok |" >> "$report"
  echo "$deck $key got=$got want=$expected |d|=$delta bound=$abs_tol $ok"
  if [[ "$ok" == "PASS" ]]; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
  fi
done < "$REF"

echo
echo "ngspice-compare pass=$pass fail=$fail"
if [[ "$fail" -ne 0 ]]; then
  echo "RESULT fail example=ngspice-compare"
  exit 1
fi
echo "RESULT pass example=ngspice-compare escapes=0"
exit 0
