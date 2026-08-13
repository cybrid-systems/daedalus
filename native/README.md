# Native kernels (M5 / issues #28, #29)

Thin C ABI so Aura can `c-load` a dense solve and hot-swap it over
`daed:dense-solve-pure!`. The circuit layer stays pure Aura.

## extern "C" export rules

1. Every public symbol is `extern "C"` — no C++ mangling, no overloads.
2. Parameter types are `int64_t`, `double*`, or `void`. No STL, `bool`,
   references, or classes at the boundary.
3. Caller owns every buffer. `A` is **row-major** `n×n` doubles. `b` is
   length `n` and is overwritten with `x` on success.
4. Return `int64_t`: `0` = ok, positive `DAED_ERR_*` on failure.
5. Additive symbols keep `DAED_ABI_VERSION`. Bump the version only when
   an existing signature or meaning changes.
6. Aura binds **one** symbol (`daed_dispatch`) because host `c-func`
   currently treats `cid < n_ffi` as foreign (see `notes/host-residuals.md`).
   Pointers travel as `Int` via `c-opaque->int`. Extra C symbols stay
   `dlsym`-visible for non-Aura callers.

## ABI (`daed_abi.h`)

`DAED_ABI_VERSION` is `1`. `daed_abi_version()` returns that constant.

| Symbol | Signature | Meaning |
|--------|-----------|---------|
| `daed_dispatch` | `int64_t(op,a,b,c)` | **Aura binds this only** (one `c-func`) |
| `daed_abi_version` | `int64_t(void)` | must be `1` (`op=0`) |
| `daed_solve_dense` | `int64_t(double* A, double* b, int64_t n)` | in-place GE; 0 = ok (`op=2`) |
| `daed_solve_dense_work_n` | `int64_t(int64_t n)` | workspace length in doubles (`op=3`) |
| `daed_solve_dense_ws` | `int64_t(A, b, n, work)` | GE on a copy of `A`; `A` preserved |
| `daed_set_fail` | `int64_t(int64_t on)` | poison next solve (`op=1`) |
| `daed_copy_f64` | `int64_t(dst, src, n)` | identity copy (`op=4`) |

| Code | Name | Meaning |
|------|------|---------|
| 0 | `DAED_OK` | success; `b` holds `x` |
| 1 | `DAED_ERR_ARG` | null `A`/`b` or `n <= 0` |
| 2 | `DAED_ERR_POISON` | `daed_set_fail(1)` armed |
| 3 | `DAED_ERR_SINGULAR` | pivot below `DAED_GE_EPS` |
| 4 | `DAED_ERR_OP` | unknown `daed_dispatch` op |
| 5 | `DAED_ERR_WORK` | `work` is null |

Workspace solve is C-only (`work` is a fourth pointer). Dispatch `op=3`
returns `work_n` so Aura can size a buffer later without a new `c-func`.

## Build

Linux `.so` and macOS `.dylib` use the same sources.

**g++ one-liner** (also `./scripts/build-native.sh`):

```bash
# Linux
g++ -O2 -fPIC -std=c++17 -shared -I native -o native/libdaed_solve.so native/daed_solve.cpp

# macOS
g++ -O2 -fPIC -std=c++17 -dynamiclib -I native -o native/libdaed_solve.dylib native/daed_solve.cpp
```

**CMake** (optional; same output path):

```bash
cmake -S native -B native/build
cmake --build native/build
```

Confirm unmangled symbols and a 2×2 solve (no Aura):

```bash
./scripts/check-native-abi.sh
# nm T daed_solve_dense / daed_solve_dense_ws / daed_abi_version …
# dlsym + RESULT pass
```

On Linux, `nm -D native/libdaed_solve.so | grep daed_` shows `T` text
symbols with the C names (no `_Z…` mangling). On macOS, `nm` may prefix
`_`; `dlsym` still uses the unprefixed name.

## Adding a kernel

1. Declare the symbol in `daed_abi.h` inside the `extern "C"` block.
   Use `int64_t` / `double*` / `void` only.
2. Implement it in a `.cpp` under `native/` (or a new `.cpp` listed in
   `CMakeLists.txt` and `scripts/build-native.sh`).
3. Return `DAED_OK` or a documented `DAED_ERR_*`. Do not throw across
   the boundary.
4. Keep `DAED_ABI_VERSION` unless you break an existing signature.
5. If Aura should call it and you can spare a dispatch slot, add an
   `op` in `daed_dispatch`. Do **not** add a second `c-func` until the
   host cid bug is fixed.
6. Add the unmangled name to `REQUIRED_SYMS` in
   `scripts/check-native-abi.sh`.
7. Rebuild (`build-native.sh` or CMake) and run
   `./scripts/check-native-abi.sh` — it must print `RESULT pass`.

## Aura

```scheme
(daed:load-kernels "native/libdaed_solve.so")  ; hash: ok / lib / reason
(daed:bind-solve-dense lib-id)                 ; hash + callable (A b n)
(daed:native-ready?)          ; #t if .so loaded and ABI=1
(daed:solve-prefer! "native") ; or "pure" / "auto" (issue #34)
(daed:simulate-op ckt)        ; linear .op and Newton share dense-solve!
(daed:solve-prefer! "pure")   ; back to V_A
```

Default backend is `"pure"` (existing probes stay E=0).

C example (no Aura): `native/example_dense.c`.

## Buffer lifetime (issue #32)

Aura owns solver vectors. Each call `c-alloc`s scratch, copies in, invokes
C++, copies out on success, and `c-free`s always. C++ must not retain the
pointer. Counters: `daed:buf-live` / `buf-allocs` / `buf-frees`.
Details: [notes/buf-exchange.md](../notes/buf-exchange.md).
