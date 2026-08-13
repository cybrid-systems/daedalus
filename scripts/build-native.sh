#!/usr/bin/env bash
# Build the Daedalus dense-solve shared library (issue #28 / #29).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
CXX="${CXX:-g++}"
SRC="$ROOT/native/daed_solve.cpp"
INC="$ROOT/native"
OUTDIR="$ROOT/native"
uname_s="$(uname -s)"
if [[ "$uname_s" == Darwin ]]; then
  OUT="$OUTDIR/libdaed_solve.dylib"
  EXTRA=(-dynamiclib)
else
  OUT="$OUTDIR/libdaed_solve.so"
  EXTRA=(-shared)
fi

if ! command -v "$CXX" >/dev/null 2>&1; then
  echo "error: $CXX not found; set CXX or install a C++ compiler" >&2
  exit 1
fi

"$CXX" -O2 -fPIC -std=c++17 "${EXTRA[@]}" -I"$INC" -o "$OUT" "$SRC"
echo "[daedalus] native kernel: $OUT"
nm -D "$OUT" 2>/dev/null | grep -E 'daed_(abi_version|solve_dense|set_fail|dispatch)' || \
  nm "$OUT" 2>/dev/null | grep -E 'daed_(abi_version|solve_dense|set_fail|dispatch)' || true
