# Native kernels (M5 / issue #28)

Thin C ABI so Aura can `c-load` a dense solve and hot-swap it over
`daed:dense-solve-pure!`. The circuit layer stays pure Aura.

## ABI (`daed_abi.h`)

| Symbol | Signature | Meaning |
|--------|-----------|---------|
| `daed_dispatch` | `int64_t(op,a,b,c)` | **Aura binds this only** (one `c-func`) |
| `daed_abi_version` | `int64_t(void)` | must be `1` (`op=0`) |
| `daed_solve_dense` | `int64_t(double* A, double* b, int64_t n)` | 0 = ok (`op=2`, `a`/`b` are pointers) |
| `daed_set_fail` | `int64_t(int64_t on)` | poison next solve (`op=1`) |

Aura `c-func` currently treats `cid < n_ffi` as foreign, so we bind **one**
symbol. Pointers travel as `Int` via `c-opaque->int`.

`extern "C"`, no mangling. `A` is row-major `n×n`. `b` is overwritten with `x`.

## Build

```bash
./scripts/build-native.sh
# native/libdaed_solve.so   (Linux)
# native/libdaed_solve.dylib (macOS)
```

Add a kernel: new `extern "C"` symbol in a `.cpp` next to this header, link
into the same `.so` or a second library, bind with `c-func`.

## Aura

```scheme
(daed:native-ready?)          ; #t if .so loaded and ABI=1
(daed:solve-rebind! "native") ; Hephaestus-style snap + switch
(daed:simulate-op ckt)        ; uses native GE
(daed:solve-rebind! "pure")   ; back to V_A
```

Default backend is `"pure"` (existing probes stay E=0).
