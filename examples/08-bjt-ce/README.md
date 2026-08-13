# 08-bjt-ce

**Phase 5** denseness probe: Ebers-Moll NPN + Newton-Raphson `.op`.

```
Vcc ── Rc ── nC (collector)
Vin ── Rb ── nB (base)
              Q NPN, emitter = GND
```

| Item | Value |
|------|--------|
| Axes | Ebers-Moll Jacobian + dense NR + param mutate + metrology |
| Switch off | `Vin=0` → `vC ≈ Vcc` |
| Switch on | `Vin=5` → `vC < 0.5 V` (saturation) |
| CE bias | `Vin=1.2`, `Rb=20 kΩ`, `Rc=1 kΩ` → mid-rail `vC` |
| Gain polarity | `Vin: 1.20 → 1.22` lowers `vC` (inverting) |
| Mutate | `βF` snapshot / restore |
| Core escapes | 0 |

## Run

```bash
./scripts/run-aura.sh examples/08-bjt-ce/main.aura
```

Expect:

```text
PASS: Ebers-Moll BJT switch + CE .op (escapes=0)
RESULT pass example=08-bjt-ce escapes=0
```
