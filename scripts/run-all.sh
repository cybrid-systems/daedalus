#!/usr/bin/env bash
# Run full offline denseness suite. Requires Aura binary.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "======== build-native ========"
if ./scripts/build-native.sh; then
  echo "native kernel ready"
else
  echo "warning: native kernel build failed; probe 26 will fail ready?" >&2
fi

PROBES=(
  00-smoke
  01-voltage-divider
  02-rc-lowpass
  03-mutate-resistor
  05-agent-autotune
  06-viz-bidirectional
  07-diode-op
  08-bjt-ce
  09-diode-clamp-tran
  10-vision-pipeline
  11-controlled-sources
  12-linear-op-suite
  13-tran-suite
  14-mutate-rollback
  15-nr-helpers
  16-nl-op-suite
  17-adapt-tran
  18-mosfet
  19-measure
  20-converge-aids
  21-step-temp
  22-monte-carlo
  23-agent-evolve
  24-topo-mutate
  25-spice-export
  26-native-hotswap
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

echo "======== ngspice-compare ========"
if ./scripts/compare-ngspice.sh 2>&1 | tee /tmp/daedalus-ngspice-compare.log | tail -20; then
  if rg -q "RESULT pass|RESULT skip" /tmp/daedalus-ngspice-compare.log 2>/dev/null \
     || grep -Eq "RESULT pass|RESULT skip" /tmp/daedalus-ngspice-compare.log; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    failed_list+=("ngspice-compare")
  fi
else
  fail=$((fail + 1))
  failed_list+=("ngspice-compare")
fi

echo "======== export-roundtrip ========"
if ./scripts/roundtrip-spice.sh 2>&1 | tee /tmp/daedalus-export-roundtrip.log | tail -20; then
  if rg -q "RESULT pass|RESULT skip" /tmp/daedalus-export-roundtrip.log 2>/dev/null \
     || grep -Eq "RESULT pass|RESULT skip" /tmp/daedalus-export-roundtrip.log; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    failed_list+=("export-roundtrip")
  fi
else
  fail=$((fail + 1))
  failed_list+=("export-roundtrip")
fi

echo "======== check-native-abi ========"
if ./scripts/check-native-abi.sh 2>&1 | tee /tmp/daedalus-check-native-abi.log | tail -20; then
  if rg -q "RESULT pass" /tmp/daedalus-check-native-abi.log 2>/dev/null \
     || grep -q "RESULT pass" /tmp/daedalus-check-native-abi.log; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    failed_list+=("check-native-abi")
  fi
else
  fail=$((fail + 1))
  failed_list+=("check-native-abi")
fi

echo "======== summary ========"
echo "pass=$pass fail=$fail total=$(( ${#PROBES[@]} + 3 )) (probes=${#PROBES[@]} + ngspice-compare + export-roundtrip + check-native-abi)"
if [[ "$fail" -ne 0 ]]; then
  echo "failed: ${failed_list[*]}" >&2
  exit 1
fi
echo "ALL PASS"
