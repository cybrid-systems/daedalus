#!/usr/bin/env bash
# Run full offline denseness suite. Requires Aura binary.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PROBES=(
  00-smoke
  01-voltage-divider
  02-rc-lowpass
  03-mutate-resistor
  05-agent-autotune
)

pass=0
fail=0
failed_list=()

for p in "${PROBES[@]}"; do
  echo "======== $p ========"
  if ./scripts/run-aura.sh "examples/$p/main.aura" 2>&1 | tee "/tmp/daedalus-$p.log" | tail -12; then
    if rg -q "RESULT pass" "/tmp/daedalus-$p.log" 2>/dev/null || grep -q "RESULT pass" "/tmp/daedalus-$p.log"; then
      pass=$((pass + 1))
    else
      fail=$((fail + 1))
      failed_list+=("$p")
      echo "FAIL: no RESULT pass line for $p" >&2
    fi
  else
    fail=$((fail + 1))
    failed_list+=("$p")
  fi
done

echo "======== summary ========"
echo "pass=$pass fail=$fail total=${#PROBES[@]}"
if [[ "$fail" -ne 0 ]]; then
  echo "failed: ${failed_list[*]}" >&2
  exit 1
fi
echo "ALL PASS"
