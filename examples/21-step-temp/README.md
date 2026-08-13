# 21-step-temp

**Milestone 3 / issue #22** — `.step` parameter sweeps and temperature.

| Case | What happens |
|------|----------------|
| Linear | `R2 = 1k,2k,3k` → `v2 = 2.5, 10/3, 3.75` |
| Agent | `daed:sweep-best` picks `R2=1k` for target 2.5 V |
| Nested | `R1×R2 ∈ {1k,2k}²` four DC points |
| Temp | diode `T=27→100 °C`: `Is` scales ≫1, `Vd` drops |
| `.tran` | `C = 0.5u,1u,2u` → `v(τ)` decreases |

`daed:set-temp!` scales Shockley/Ebers-Moll `Is` and `Vt`, and MOSFET `Vto` (`−2 mV/°C`). At `T=Tnom` scaling is exactly 1 (probes 07/16 unchanged).

## Run

```bash
./scripts/run-aura.sh examples/21-step-temp/main.aura
```
