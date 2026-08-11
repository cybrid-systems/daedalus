# 01-voltage-divider

**Phase 1** denseness probe: linear MNA DC operating point (`.op`).

```
vin (5 V) ── R1 (1 kΩ) ── n2 ── R2 (2 kΩ) ── GND
                n1              │
                               v2 ≈ 3.333 V
```

| Item | Value |
|------|--------|
| Axes | circuit kernel (netlist, stamp, solve) + metrology |
| Analysis | `.op` (linear) |
| Components | `V`, `R` |
| Expected | `v1 = 5`, `v2 = 10/3 ≈ 3.333` |
| Core escapes | 0 |

## Run

```bash
./scripts/run-aura.sh examples/01-voltage-divider/main.aura
```

Expect:

```text
PASS: linear .op voltage divider (escapes=0)
RESULT pass example=01-voltage-divider escapes=0
```
