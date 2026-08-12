# 03-mutate-resistor

**Phase 3** denseness probe: safe parameter mutate + dual snapshot/rollback.

```
vin (5 V) ── R1 (1 kΩ) ── n2 ── R2 (2 kΩ) ── GND
                         │
                    v2 = 5 · R2/(R1+R2)
```

| Item | Value |
|------|--------|
| Axes | safe mutate + dual rollback + `.op` re-sim + metrology |
| Baseline | `R2=2k` → `v2=10/3` |
| Mutate | `R2→1k` → `v2=2.5` |
| Reject | `R2≤0` refused; circuit unchanged |
| Rollback | restore `R2` **and** denseness metrics; then count rollback |
| Core escapes | 0 |

## Run

```bash
./scripts/run-aura.sh examples/03-mutate-resistor/main.aura
```

Expect:

```text
PASS: mutate resistor + dual rollback (escapes=0)
RESULT pass example=03-mutate-resistor escapes=0
```
