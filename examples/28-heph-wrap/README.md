# 28-heph-wrap

**Milestone 5 / issue #31** — Hephaestus-pattern wrapper around the native GE kernel.

Composes `heph:rebind-safe` / `heph:with-escape` / `heph:own-check` /
`heph:escape-count` on the circuit solver. Does **not** require the heph
lib (same discipline as agent vs Aether: compose the pattern).

| Step | What happens |
|------|----------------|
| Pure | `solve-mna` backend `"pure"`; divider `v2=10/3`; `escapes=0` |
| Rebind | `(daed:rebind-safe "solve-mna" "native")`; same `v2`; escape +1 via `with-escape` `"daed-solve-dense"` |
| Bad rebind | unknown kernel / kind → `{ok:#f}`; backend unchanged |
| Poison | native rc≠0 → backend back to `"pure"` |
| Restore | `kernel-restore!` of the pre-native snapshot returns `"pure"` |

```bash
./scripts/build-native.sh
./scripts/run-aura.sh examples/28-heph-wrap/main.aura
```

Default backend is `"pure"` so probes 00–25 stay E=0.
