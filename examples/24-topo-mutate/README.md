# 24-topo-mutate

**Milestone 4 / issue #25** — limited topology mutation surface.

| Case | What happens |
|------|----------------|
| Parallel R | extra `R` across `R2` → `v2=2.5`; restore drops it |
| Series R | insert `Rs` on `R1` → `v2=2.5`; `unseries` reconnects |
| Parallel / miller C | DC voltages unchanged; restore removes `C` |
| Rejects | dup name, `R≤0`, missing remove, F/H losing its `V` |
| Search | `topo-search!` tries a family and keeps `parallel-r` (or `series-r`) |

Invalid topologies roll back via `circuit-snapshot` / `restore-circuit!` (component list included). `topology-ok?` is the Hermes gate.

## Run

```bash
./scripts/run-aura.sh examples/24-topo-mutate/main.aura
```
