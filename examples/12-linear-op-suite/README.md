# 12-linear-op-suite

**Milestone 0 / issue #13** — linear `.op` denseness suite.

Three circuits vs **hand calculation** (same numbers ngspice `.op` should match).
Branch currents come from the MNA extra unknowns (`daed:i`).

| Case | Circuit | Hand calc |
|------|---------|-----------|
| A | Divider `V=5`, `R1=1k`, `R2=2k` | \(v_2=10/3\), \(i(V)=-(5-10/3)/1\mathrm{k}=-1/600\) |
| B | `I=1mA` into series `1k+1k` | \(v_1=2\), \(v_2=1\) |
| C | VCVS \(\mu=2\), `Rl=1k` | \(v_2=10\), \(i(E)=-10\,\mathrm{mA}\) |
| D | Snapshot → mutate `R2` → restore | voltages / `i(vin)` match A |

Relative error < `1e-6` on voltages. Core escapes = 0.

## Run

```bash
./scripts/run-aura.sh examples/12-linear-op-suite/main.aura
```

Optional ngspice cross-check (not required for denseness):

```bash
ngspice -b examples/12-linear-op-suite/spice/divider.cir
ngspice -b examples/12-linear-op-suite/spice/i-net.cir
ngspice -b examples/12-linear-op-suite/spice/vcvs.cir
```
