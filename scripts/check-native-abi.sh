#!/usr/bin/env bash
# ABI + build conventions (issue #29). No Aura required.
# Builds the kernel (g++; CMake if present), checks unmangled nm symbols,
# and dlopen/dlsym-runs native/example_dense.c.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=== Daedalus native ABI check ==="

fail=0
CXX="${CXX:-g++}"
CC="${CC:-cc}"

if ! ./scripts/build-native.sh; then
  echo "  FAIL  g++ / build-native.sh" >&2
  echo "RESULT fail"
  exit 1
fi

uname_s="$(uname -s)"
if [[ "$uname_s" == Darwin ]]; then
  LIB="$ROOT/native/libdaed_solve.dylib"
else
  LIB="$ROOT/native/libdaed_solve.so"
fi

if [[ ! -f "$LIB" ]]; then
  echo "  MISSING  $LIB" >&2
  echo "RESULT fail"
  exit 1
fi
echo "  OK  lib $LIB"

REQUIRED_SYMS=(
  daed_abi_version
  daed_solve_dense
  daed_solve_dense_ws
  daed_solve_dense_work_n
  daed_set_fail
  daed_dispatch
  daed_copy_f64
)

nm_out="$(nm -D "$LIB" 2>/dev/null || true)"
if [[ -z "$nm_out" ]]; then
  nm_out="$(nm "$LIB" 2>/dev/null || true)"
fi

has_sym() {
  local s="$1"
  printf '%s\n' "$nm_out" | grep -E "[[:space:]]T[[:space:]]+_?${s}$" >/dev/null 2>&1 \
    || printf '%s\n' "$nm_out" | grep -Ew "_?${s}" >/dev/null 2>&1
}

for s in "${REQUIRED_SYMS[@]}"; do
  if has_sym "$s"; then
    echo "  OK  nm $s"
  else
    echo "  MISSING  nm $s" >&2
    fail=1
  fi
  if printf '%s\n' "$nm_out" | grep -E "_Z[0-9]+${s}" >/dev/null 2>&1; then
    echo "  FAIL  mangled $s" >&2
    fail=1
  fi
done

if command -v cmake >/dev/null 2>&1; then
  echo "  -- cmake --"
  cmake -S native -B native/build >/tmp/daedalus-cmake-configure.log
  cmake --build native/build >/tmp/daedalus-cmake-build.log
  if [[ -f "$LIB" ]]; then
    echo "  OK  cmake $LIB"
  else
    echo "  FAIL  cmake did not produce $LIB" >&2
    fail=1
  fi
else
  echo "  skip cmake (not installed; g++ path is enough)"
fi

EX=/tmp/daedalus-example-dense
if [[ "$uname_s" == Darwin ]]; then
  "$CC" -O2 -o "$EX" native/example_dense.c
else
  "$CC" -O2 -o "$EX" native/example_dense.c -ldl
fi
if ! "$EX" "$LIB" | tee /tmp/daedalus-example-dense.log; then
  echo "  FAIL  example_dense" >&2
  fail=1
fi
if ! grep -q "RESULT pass" /tmp/daedalus-example-dense.log; then
  echo "  FAIL  example_dense missing RESULT pass" >&2
  fail=1
fi

if [[ "$fail" -ne 0 ]]; then
  echo "RESULT fail"
  exit 1
fi
echo "RESULT pass"
