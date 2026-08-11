# 00-smoke

**Phase 0** scaffolding probe: host binary + `daedalus-min` load.

| Item | Value |
|------|--------|
| Axes | scaffolding / metrology helpers |
| Circuit | none |
| Mutation | none |
| Expected escapes | 0 |

## Run

```bash
./scripts/run-aura.sh examples/00-smoke/main.aura
```

Expect:

```text
PASS: host + daedalus-min load (escapes=0)
RESULT pass example=00-smoke escapes=0
```
