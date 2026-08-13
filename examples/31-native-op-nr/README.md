# 31-native-op-nr

**Milestone 5 / issue #34** — optional native backend on real `.op` / Newton.

`daed:dense-solve!` is shared by linear `.op` and every Newton step.
`(daed:solve-prefer! "native"|"pure"|"auto")` selects the backend without
changing the circuit.

| Step | What happens |
|------|----------------|
| Pure diode | Shockley `.op`, `vd≈0.7 V`, `escapes=0` |
| Native NR | same netlist; `vd` matches; escape count ≈ NR iters |
| Native lin | divider one-shot; +1 escape |
| Pure again | same `vd`; no new escapes |
| SPICE | `circuit->spice` still emits the diode deck |

```bash
./scripts/build-native.sh
./scripts/run-aura.sh examples/31-native-op-nr/main.aura
```

Default backend is `"pure"` so probes 00–25 stay E=0.
