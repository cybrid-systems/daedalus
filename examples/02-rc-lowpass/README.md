# 02-rc-lowpass

**Phase 2** denseness probe: fixed-step Backward-Euler `.tran` plus DC `.op`.

```
vin (5 V step) ── R (1 kΩ) ── n2 ── C (1 µF) ── GND
                              │
                         v2(t) ≈ 5(1−e^{−t/τ}),  τ = RC = 1 ms
```

| Item | Value |
|------|--------|
| Axes | circuit `.op` + `.tran` companions + metrology |
| Components | `V`, `R`, `C` |
| `.op` expected | `v2 = 5` (C open) |
| `.tran` checks | IC `v2(0)=0`; `v2(τ)` and `v2(5τ)` vs analytic (rel tol) |
| Core escapes | 0 |

## Run

```bash
./scripts/run-aura.sh examples/02-rc-lowpass/main.aura
```

Expect:

```text
PASS: RC low-pass .op + .tran (escapes=0)
RESULT pass example=02-rc-lowpass escapes=0
```
