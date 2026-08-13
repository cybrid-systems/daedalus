#!/usr/bin/env bash
# End-to-end M5 demo (issue #33): build the native GE lib and run
# examples/30-native-hotswap-demo (pure → C++ hot-swap → dual rollback).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
./scripts/build-native.sh
exec ./scripts/run-aura.sh examples/30-native-hotswap-demo/main.aura
