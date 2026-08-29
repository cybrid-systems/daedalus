# 32-live-kernel-tran

**Milestone 6 / issue #35** — live kernel hot-swap during `.tran`.

Issue #40 named this PoC `26-live-kernel-tran`. Probes 26–31 already landed
for M5, so the repo path is **32**. The circuit, gates, and contrast are
the ones specified on #35.

| Step | What happens |
|------|----------------|
| Boot | Frozen diode-clamp + PULSE; snapshot `world:tran-cursor` and `kernel:nr-be`; print session pid |
| Illegal | `α=0.1`, `hmax=1ms`, netlist mutate → `mutate-illegal`; K3 stays 0.5 |
| Id stability | 30× K3 rebind/rollback; K1–K4 ids unchanged |
| Split snap | Kernel rollback leaves `t` and `v` byte-identical |
| Agent | Recorded Aether policy: K3 `0.5→1.0` at `t≈0.5ms` → `nr-diverge` → kernel rollback; K2 fixed→LTE; K1 fill-order change; run to 2 ms |
| Audit | `t=1.20ms  k1=…` from the append-only log |

One process for the whole demo. Reloading the netlist or resetting `t` to 0
fails the probe.

## Run

```bash
./scripts/run-aura.sh examples/32-live-kernel-tran/main.aura
```

## Files

| Path | Role |
|------|------|
| `main.aura` | Denseness probe + gates |
| `NOTES.md` | File-agent contrast A/B and what M6 does not claim |
| `spice/clamp.cir` | ngspice deck for the RMSE ruler |
| `ref/ngspice.tsv` | Frozen educational samples |
| `out/audit.tsv` | Step audit written by the probe |

See [notes/roadmap.md](../../notes/roadmap.md) for the M6 section.
