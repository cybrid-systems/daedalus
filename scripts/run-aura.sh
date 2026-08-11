#!/usr/bin/env bash
# Run a Daedalus .aura probe against a local Aura host binary.
#
# Usage (from daedalus repo root):
#   ./scripts/run-aura.sh examples/00-smoke/main.aura
#
# Env overrides:
#   AURA_BIN       path to aura binary (default: ../aura-grok/build/aura)
#   AURA_LIB       path to Aura lib/ containing std/ (default: ../aura-grok/lib)
#   DAEDALUS_LIB   path to this repo's lib/ (default: <repo>/lib)

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Prefer explicit AURA_BIN. Else sibling aura-grok, then aura/PATH.
if [[ -z "${AURA_BIN:-}" ]]; then
  if [[ -x "$ROOT/../aura-grok/build/aura" ]]; then
    AURA_BIN="$ROOT/../aura-grok/build/aura"
  elif [[ -x /tmp/aura-denseness-build/build/aura ]]; then
    AURA_BIN=/tmp/aura-denseness-build/build/aura
  elif [[ -x "$ROOT/../aura/build/aura" ]]; then
    AURA_BIN="$ROOT/../aura/build/aura"
  elif command -v aura >/dev/null 2>&1; then
    AURA_BIN="$(command -v aura)"
  else
    echo "error: aura binary not found; set AURA_BIN or build aura-grok" >&2
    exit 1
  fi
fi

if [[ -z "${AURA_LIB:-}" ]]; then
  if [[ "$AURA_BIN" == /tmp/aura-denseness-build/* && -d /tmp/aura-denseness-build/lib/std ]]; then
    AURA_LIB=/tmp/aura-denseness-build/lib
  elif [[ -d "$ROOT/../aura-grok/lib/std" ]]; then
    AURA_LIB="$ROOT/../aura-grok/lib"
  else
    AURA_LIB="$ROOT/../aura/lib"
  fi
fi
DAEDALUS_LIB="${DAEDALUS_LIB:-$ROOT/lib}"

if [[ ! -x "$AURA_BIN" ]]; then
  echo "error: aura binary not executable: $AURA_BIN" >&2
  exit 1
fi

if [[ ! -d "$AURA_LIB/std" ]]; then
  echo "error: Aura stdlib not found under: $AURA_LIB/std" >&2
  echo "  set AURA_LIB to the directory that contains std/" >&2
  exit 1
fi

if [[ ! -d "$DAEDALUS_LIB" ]]; then
  echo "error: Daedalus lib not found: $DAEDALUS_LIB" >&2
  exit 1
fi

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <probe.aura>" >&2
  exit 1
fi

SRC="$1"
if [[ ! -f "$SRC" ]]; then
  echo "error: file not found: $SRC" >&2
  exit 1
fi

# CLI denseness demos: sandbox off; pipeline strict 0 for tree-walker fallback
# (same discipline as Aether / Hephaestus / Hermes).
export AURA_BIN
export AURA_PATH="${AURA_PATH:-$AURA_LIB:$DAEDALUS_LIB}"
export AURA_SANDBOX="${AURA_SANDBOX:-off}"
export AURA_PIPELINE_STRICT="${AURA_PIPELINE_STRICT:-0}"

echo "[daedalus] AURA_BIN=${AURA_BIN}"
echo "[daedalus] AURA_PATH=${AURA_PATH}"
echo "[daedalus] running: ${SRC}"

# Host expects program on stdin (not argv).
exec "$AURA_BIN" < "$SRC"
