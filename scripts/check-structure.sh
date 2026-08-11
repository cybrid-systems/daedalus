#!/usr/bin/env bash
# Structure-only check (no Aura binary required).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=== Daedalus structure check ==="

required=(
  "README.md"
  "LICENSE"
  "notes/span-design.md"
  "notes/denseness-report.md"
  "notes/escape-log.md"
  "notes/host-residuals.md"
  "prompts/GROK.md"
  "lib/README.md"
  "lib/daedalus-min.aura"
  "lib/netlist.aura"
  "lib/stamp.aura"
  "lib/solve.aura"
  "lib/probe.aura"
  "projects/daedalus-core/SPEC.md"
  "examples/README.md"
  "examples/00-smoke/main.aura"
  "examples/00-smoke/README.md"
  "examples/01-voltage-divider/main.aura"
  "examples/01-voltage-divider/README.md"
  "scripts/run-aura.sh"
  "scripts/run-all.sh"
  "scripts/check-structure.sh"
)

missing=0
for f in "${required[@]}"; do
  if [[ -f "$f" ]]; then
    echo "  OK  $f"
  else
    echo "  MISSING  $f"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo "Structure check FAILED" >&2
  exit 1
fi

echo "Structure OK (no Aura binary required)."
