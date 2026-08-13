# 07-diode-op

**Phase 5** denseness probe: Shockley diode + Newton-Raphson `.op`.

```
forward:  vin (5 V) ── R (1 kΩ) ── n2 ── D → GND     vd ≈ 0.7 V
reverse:  vin (5 V) ── R (1 kΩ) ── n2 ── D(cathode)   I ≈ 0, vn2 ≈ 5 V
```

| Item | Value |
|------|--------|
| Axes | Shockley stamp + dense NR + mutate/rollback + metrology |
| Model | `Id = Is (e^{vd/(n Vt)} − 1)`, default `Is=1e-14`, `n=1`, `Vt=26 mV` |
| Forward | `0.55 < vd < 0.85`, `Id ≈ 4.3 mA` |
| Reverse | `vn2 ≈ Vin`, `|I| < 10 nA` |
| Mutate | larger `Is` lowers `vd`; snapshot restores `Is` |
| Core escapes | 0 |

## Run

```bash
./scripts/run-aura.sh examples/07-diode-op/main.aura
```

Expect:

```text
PASS: Shockley diode .op + mutate/rollback (escapes=0)
RESULT pass example=07-diode-op escapes=0
```
