# 27-ffi-bind

**Milestone 5 / issue #30** — reusable `c-load` / `c-func` binding layer.

| Step | What happens |
|------|----------------|
| Missing lib | `load-kernels` of a bogus path → `{ok:#f, reason:no-lib}` |
| Load | `load-kernels` of `native/libdaed_solve.so` → lib-id ≥ 0 |
| Bind + 2×2 | `bind-solve-dense` returns a callable; `2x+y=5`, `x+2y=4` → `(2,1)` |
| Failures | missing symbol, bad handle, `n=0` stay structured (no evaluator crash) |
| `lib-id=-1` | accepted; after a live bind this **reuses** the already-loaded dispatch (`c-load` is `RTLD_LOCAL`, so bare `RTLD_DEFAULT` cannot see `daed_*`) |
| cid-safe | one `c-func` only (`daed_dispatch`); `daed:V` / `daed:circuit` still work |

```bash
./scripts/build-native.sh
./scripts/run-aura.sh examples/27-ffi-bind/main.aura
```

Default solve backend stays `"pure"`. The 2×2 call is a metered native escape.
