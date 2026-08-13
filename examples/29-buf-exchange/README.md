# 29-buf-exchange

**Milestone 5 / issue #32** — Opaque buffer exchange between Aura vectors and C++.

| Step | What happens |
|------|----------------|
| Identity | `c-alloc` → copy-in → `daed_copy_f64` → copy-out → `(1.5, -2.25, 3.125, 0)` |
| Soak | 32 cycles; `buf-live=0` and `allocs=frees` |
| Own | `daed:own-check` still ok; solve backend stays `"pure"` |
| Solve | tracked 2×2 GE also pairs every alloc with a free |

Aura owns FlatAST / solver vectors. Native scratch lives only for the call.
C++ must not retain the pointer. See [notes/buf-exchange.md](../../notes/buf-exchange.md).

```bash
./scripts/build-native.sh
./scripts/run-aura.sh examples/29-buf-exchange/main.aura
```
