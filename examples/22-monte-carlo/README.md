# 22-monte-carlo

**Milestone 3 / issue #23** — Monte Carlo under parameter distributions.

| Case | What happens |
|------|----------------|
| PRNG | Park-Miller `u01` after seed 1 is `16807/m`; gauss(0,1) moments ~N(0,1) |
| Divider | `R1,R2 ±5 %` uniform, N=80 → mean ≈ 10/3, std in (0.015, 0.09) |
| Replay | same seed reproduces trial 0; circuit restored |
| Agent | yield `[3.15, 3.52]` ≥ 0.85 (robust); `[3.32, 3.34]` at 90 % is not |
| `.tran` | `C ±20 %`, `measure-final` at `τ` spreads |

`daed:mc-op` / `daed:mc-tran` snap+restore. `daed:mc-yield` / `daed:mc-robust?` are the agent query.

## Run

```bash
./scripts/run-aura.sh examples/22-monte-carlo/main.aura
```
