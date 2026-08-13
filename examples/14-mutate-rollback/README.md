# 14-mutate-rollback

**Milestone 0 / issue #15** — safe mutation + snapshot/rollback of circuit, solver state, and denseness metrics.

| Step | What happens |
|------|----------------|
| Snapshot | `daed:snapshot-sim` stores netlist, stats, last `.op` volts / branch currents |
| Agent | `daed:agent-step!` sets `R2=1k` → `v2=2.5` (commit) |
| Rollback | `daed:restore!` → `R2=2k`, re-`.op` matches pre-mutation `v` and `i` |
| Topology | `daed:mutate-nodes!` reconnects `R2` as `2–2` → `v2=Vin`; restore undoes it |
| Log | `daed:mutlog` lists value / nodes / restore events |

Cached snap voltages remain readable after later mutations (`daed:snap-v`).

## Run

```bash
./scripts/run-aura.sh examples/14-mutate-rollback/main.aura
```
