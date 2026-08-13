# Nonlinear .op vs ngspice

**Issue #17.** Educational Shockley / Ebers-Moll in Daedalus compared with ngspice 45.2
on the same netlists and the same model cards. Live ngspice is a **host oracle**
(`scripts/compare-ngspice.sh`); the Aura probe uses frozen numbers and stays in \(V_A\).

## Models

| Device | Daedalus | ngspice card |
|--------|----------|--------------|
| Diode | `Id = Is (e^{vd/(n Vt)} − 1) + gmin vd`, `Is=1e-14`, `n=1`, `Vt=0.026`, `gmin=1e-12` | `.model Dedu D(IS=1e-14 N=1)` + `.options tnom=28.555 temp=28.555 gmin=1e-12` |
| NPN | Transport Ebers-Moll, `Is=1e-15`, `BF=100`, `BR=1`, `Vt=0.026` | `.model Qedu NPN(IS=1e-15 BF=100 BR=1)` at the same T |

`T=28.555 °C` makes \(kT/q \approx 26\,\mathrm{mV}\), matching the frozen Daedalus `Vt`.

## Numbers (matched T)

| Case | Quantity | Daedalus | ngspice | \|Δ\| | Bound |
|------|----------|----------|---------|-------|-------|
| A diode bias | `Id` at 0.7 V | 4.92656 mA | 4.93209 mA | 5.5 µA | 50 µA |
| B series D+R | `vd` | 0.696485 V | 0.696459 V | 26 µV | 2 mV |
| B series D+R | `Id` | 4.30352 mA | 4.30354 mA | 20 nA | 50 µA |
| C rectifier DC | `v_load` | 4.30352 V | 4.303541 V | 21 µV | 2 mV |
| D CE bias | `vc` | 2.70029 V | 2.700149 V | 0.14 mV | 5 mV |
| D CE bias | `vb` | 0.740059 V | 0.740030 V | 0.03 mV | 5 mV |
| D CE bias | `Ic` | 2.2997 mA | 2.29985 mA | 0.15 µA | 50 µA |

## What is numerical vs model

- **Numerical** (matched T): tens of µV / sub-µA. Dense NR+GE vs ngspice SPARSE, plus
  `pnjlim` / line-search vs ngspice's own limiting. Well inside the bounds above.
- **Model / temperature**: at default `T=27 °C` ngspice, series `vd` drops to 0.692891 V
  (Δ ≈ 3.6 mV) and CE `vc` to 2.682 V (Δ ≈ 18 mV). Cause: \(V_t = kT/q\) and SPICE
  temperature scaling of `IS`. Daedalus freezes `Vt=26 mV` for educational stability.
  This is **not** a solver failure.

No high-performance kernel is used on the Daedalus path (core \(E=0\)).
