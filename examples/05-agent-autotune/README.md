# 05-agent-autotune

**Phase 4** denseness probe: agent closed loop on a live netlist.

```
observe (.op) → decide → snapshot → mutate R → re-sim → verify → rollback-if-worse
```

| Item | Value |
|------|--------|
| Circuit | Divider Vin=5, R1=1k, R2 starts 2k |
| Goal | `v2 → 2.5 V` (tune `R2`) |
| Strategies | iterative `scale` + `analytic-divider` one-shot |
| Negative paths | refuse `R2≤0`; rollback if mutation worsens error |
| Core escapes | 0 |

## Run

```bash
./scripts/run-aura.sh examples/05-agent-autotune/main.aura
```

Expect:

```text
PASS: agent auto-tune closed loop (escapes=0)
RESULT pass example=05-agent-autotune escapes=0
```
