# 16-nl-op-suite

**Milestone 1 / issue #17** — nonlinear `.op` denseness vs a trusted reference.

| Case | Circuit | ngspice (matched T) | Bound |
|------|---------|---------------------|-------|
| A | `V=0.7` across D | `Id = 4.93209 mA` | 50 µA |
| B | `5 V ── 1 kΩ ── D → GND` | `vd = 0.696459 V` | 2 mV |
| C | `5 V ── D ── 1 kΩ → GND` | `v_load = 4.303541 V` | 2 mV |
| D | CE: `Vcc=5`, `Rc=1k`, `Vin=1.2`, `Rb=20k` | `vc=2.700 V`, `vb=0.740 V` | 5 mV |

Models match Daedalus educational defaults: Shockley `IS=1e-14 N=1`, Ebers-Moll `IS=1e-15 BF=100 BR=1`. Decks pin `T=TNOM=28.555 °C` so \(V_t \approx 26\,\mathrm{mV}\).

## Accepted error bounds

| Quantity | Bound vs matched-T ngspice | Typical \|Δ\| | Notes |
|----------|----------------------------|---------------|-------|
| Node voltage | 2 mV (CE 5 mV) | tens of µV | NR/GE vs ngspice SPARSE |
| Branch current | 50 µA (Ib 1 µA) | < 6 µA | 0.11 % on `Id(0.7 V)` |
| Default 27 °C ngspice | ~4 mV on \(V_d\), ~20 mV on CE \(V_c\) | **model** | Our \(V_t\) is frozen at 26 mV; \(kT/q(27°C)\approx 25.85\,\mathrm{mV}\) |

Frozen refs: [`ref/ngspice.tsv`](ref/ngspice.tsv). Probe writes [`out/nl-op-report.md`](out/nl-op-report.md).

## Run

```bash
./scripts/run-aura.sh examples/16-nl-op-suite/main.aura
```

Optional live ngspice (not required for denseness; host oracle):

```bash
./scripts/compare-ngspice.sh
```
