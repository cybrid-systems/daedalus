#!/usr/bin/env bash
# Photo → Grok 4.6 extract → schematic HTML + .tran waveform report.
#
#   ./scripts/vision-report.sh examples/10-vision-pipeline/out/3led.jpeg
#   ./scripts/vision-report.sh photo.jpg --skip-extract
#
# API key: $XAI_API_KEY or ~/code/keys/grok
# Model:   grok-4.6 (override with --model or DAEDALUS_VLM_MODEL)

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [[ -z "${XAI_API_KEY:-}" && -f "${HOME}/code/keys/grok" ]]; then
  XAI_API_KEY="$(tr -d ' \n\r' < "${HOME}/code/keys/grok")"
  export XAI_API_KEY
fi
export DAEDALUS_VLM="${DAEDALUS_VLM:-xai}"
export DAEDALUS_VLM_MODEL="${DAEDALUS_VLM_MODEL:-grok-4.6}"
exec python3 "$ROOT/scripts/vision-report.py" "$@"
