# 30-native-hotswap-demo

**Milestone 5 / issue #33** — single end-to-end demo of the native kernel path.

| Step | What happens |
|------|----------------|
| 1 Pure | Divider `v2=10/3`, `escapes=0`, backend `"pure"` |
| 2 Snap | Dual snapshot: circuit + denseness stats + kernel backend |
| 3 Native | `(daed:rebind-safe "solve-mna" "native")`; same `v2`; escape +1; buffers balanced |
| 4 Poison | `daed_set_fail(1)` → fallback to `"pure"`; voltages still match |
| 5 Restore | `restore!` + `kernel-restore!` → circuit, `r2`, and `escapes=0` match pre-swap |
| 6 Replay | Pure `.op` again; no netlist edits |

```bash
./scripts/run-hotswap-demo.sh
# or:
./scripts/build-native.sh
./scripts/run-aura.sh examples/30-native-hotswap-demo/main.aura
```

Default backend stays `"pure"` so probes 00–25 remain E=0.
