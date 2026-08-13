# 15-nr-helpers

**Milestone 1 / issue #16** — Newton-Raphson line-search, initial-guess strategies, and failure diagnostics.

| Case | What happens |
|------|----------------|
| Series diode | Cold-start `.op` → \(v_d \approx 0.7\,\mathrm{V}\); residual history length = iters |
| Rectifier | `vin ── D ── n2 ── R → GND` DC `.op` → \(v_\mathrm{load} \approx 4.3\,\mathrm{V}\) |
| Previous guess | `daed:simulate-op-from` restarts from last `x`; fewer iters (≤ 3) |
| Gmin | `daed:simulate-op-gmin` matches the cold-start diode drop |
| Gap circuit | Missing voltage node is singular; `reason` / `hist` / `fail-node` are finite, not NaN |

Line-search tries \(\lambda \in \{1, 1/2, 1/4, 1/8\}\) and keeps the first residual decrease. Gmin ramps \(10^{-6}\to 10^{-12}\) only when the zero start fails.

## Run

```bash
./scripts/run-aura.sh examples/15-nr-helpers/main.aura
```

Expect:

```text
PASS: NR helpers (line-search, guess, diagnostics) (escapes=0)
RESULT pass example=15-nr-helpers escapes=0
```
