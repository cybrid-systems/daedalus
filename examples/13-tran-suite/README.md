# 13-tran-suite

**Milestone 0 / issue #14** — fixed-step Backward Euler `.tran`.

| Case | Circuit | Check |
|------|---------|--------|
| A | RC low-pass, \(\tau=RC=1\,\mathrm{ms}\) | \(v_2(\tau)\), \(v_2(5\tau)\) vs \(5(1-e^{-t/\tau})\) |
| B | Series RL, \(\tau=L/R=1\,\mathrm{ms}\) | \(v_L=5e^{-t/\tau}\), \(i_L=(5/R)(1-e^{-t/\tau})\) |
| C | Series RLC (overdamped) | completes; \(v_C\to 5\,\mathrm{V}\) |
| D | Mutate \(C:1\mu\mathrm{F}\to 2\mu\mathrm{F}\), re-`.tran` | slower rise vs analytic \(5(1-e^{-1/2})\) |

Inductor current waveforms: `daed:tran-i` / `daed:tran-i-at`.

## Run

```bash
./scripts/run-aura.sh examples/13-tran-suite/main.aura
```

Optional ngspice decks: `spice/rc.cir`, `spice/rl.cir`, `spice/rlc.cir`.
