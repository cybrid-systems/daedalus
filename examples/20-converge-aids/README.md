# 20-converge-aids

**Milestone 3 / issue #21** — Gmin stepping, source stepping, pseudo-transient.

| Case | What happens |
|------|----------------|
| Diode | `simulate-op-aid` uses `aid=none` (already converges) |
| Floating C | DC row empty → cold fail; Gmin-to-ground succeeds, `v=0` |
| Floating MOSFET gate | cold fail; aid chain picks `gmin-step`, `vout≈Vdd` |
| Source-step | ramps V/I 0.2→1; same diode drop as cold start |
| Ptran | grounded-C pseudo-tran then DC NR; diode still ~0.7 V |

Order: `none → gmin-step → source-step → gmin-dev → ptran`. Query `daed:op-aid`, `daed:op-aid-steps`, `daed:op-aid-tried`. Cold `simulate-op` is unchanged.

## Run

```bash
./scripts/run-aura.sh examples/20-converge-aids/main.aura
```
