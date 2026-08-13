# 09-diode-clamp-tran

**Phase 5** denseness probe: nonlinear fixed-step `.tran` (Backward Euler + Newton-Raphson).

```
vin (5 V step) ── R (1 kΩ) ── n2 ── C (1 µF) ── GND
                               └── D ────────── GND
```

Zero-state RC would charge toward 5 V (`τ = 1 ms`). The shunt diode clamps `v2` near the Shockley forward drop.

A second circuit (NPN inverter + collector C) starts at zero state and settles with the collector in saturation — clear nonlinear `.tran` startup.

| Item | Value |
|------|--------|
| Axes | BE companions + NR per step + diode/BJT + metrology |
| Diode `.op` | `v2 ≈ Vd` (C open) |
| Diode `.tran` | `v2(0)=0`, `v2(5τ) ∈ (0.5, 0.9)` |
| BJT `.tran` | `vC(end) < 0.5 V` |
| Core escapes | 0 |

## Run

```bash
./scripts/run-aura.sh examples/09-diode-clamp-tran/main.aura
```

Expect:

```text
PASS: diode clamp + BJT switch .tran BE+NR (escapes=0)
RESULT pass example=09-diode-clamp-tran escapes=0
```
