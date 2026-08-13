# 10-vision-pipeline

**Issue #6** denseness probe: Vision → Netlist → Repair → Simulate (offline fixture path).

The VLM is **not trusted**. IR is a candidate. Static validation + simulation-feedback
repair (snapshot / mutate / rollback) decide whether the circuit is runnable.

| Layer | What it proves |
|-------|----------------|
| IR | `daedalus-ir/1` → `daed:circuit`; unit parse; round-trip |
| Validate | ≥10 broken IRs diagnosed; good divider is clean |
| Repair | ≥70% of 10 seeded failures recover within budget |
| from-image | basename fixture lookup; missing image fails explicitly |
| Escapes | 0 on the core path (no live VLM in this probe) |

## Run

```bash
./scripts/run-aura.sh examples/10-vision-pipeline/main.aura
```

One-command image path (fixture if no API key):

```bash
./scripts/from-image.sh examples/10-vision-pipeline/fixtures/divider.png
```

Live extraction (optional escape):

```bash
export XAI_API_KEY=...          # or MINIMAX_API_KEY
./scripts/extract-ir.py photo.jpg
```

## Adding a fixture

1. Drop a schematic image in `fixtures/` (any `stem.png` / `.svg`).
2. Register the IR with `daed:fixture-register!` or add a `daed:ir-ex-*` and map the stem in `daed:install-builtin-fixtures!`.
3. Re-run this probe / `from-image.sh`.
