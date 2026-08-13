# 25-spice-export

**Milestone 4 / issue #26** — export a live FlatAST to a standard SPICE deck.

| Case | What happens |
|------|----------------|
| Divider | title + `V`/`R` + `.options` + `.control`/`op` + `.end` |
| Tuned | agent sets `R2=1k`; deck contains 1000, not 2000 |
| Models | `D(IS,N)`, `NPN(IS,BF,BR)`, `NMOS(LEVEL=1 VTO KP LAMBDA)` |
| Write | `out/divider.cir`, `tuned.cir`, `diode-series.cir`, `bjt-ce.cir` |

`T=Tnom` maps to `tnom=temp=28.555` so ngspice \(kT/q \approx 26\,\mathrm{mV}\) (same as probe 16). MOSFET `Cgs`/`Cgd` are omitted (Daedalus `.tran` only).

Round-trip (optional host oracle): `./scripts/roundtrip-spice.sh`

## Run

```bash
./scripts/run-aura.sh examples/25-spice-export/main.aura
```
