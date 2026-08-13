# 19-measure

**Milestone 2 / issue #20** — `.measure` plus waveform CSV export.

RC step (`Vin=5`, `R=1k`, `C=1µF`, `τ=1ms`, `tstop=5τ`):

| Measure | Analytic | Bound |
|---------|----------|-------|
| FINAL / MAX | \(5(1-e^{-5})\approx 4.966\) | 2 % |
| MIN | 0 | 1 nV |
| AVG | \(5(1-\tau/T(1-e^{-T/τ}))\approx 4.007\) | 5 % |
| WHEN 2.5 V | \(\tau\ln 2\approx 0.693\,\mathrm{ms}\) | 5 % |
| 10–90 % rise | \(\tau\ln 9\approx 2.197\,\mathrm{ms}\) | 8 % |

CSV: `t,v1,v2,…` via `daed:tran->csv` / `daed:write-tran-csv!`. Agent bundle: `daed:measure-summary`.

## Run

```bash
./scripts/run-aura.sh examples/19-measure/main.aura
```
