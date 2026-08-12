# 06-viz-bidirectional

**Issue #1** denseness probe: bidirectional netlist ↔ HTML visualization.

| Layer | What it proves |
|-------|----------------|
| **P0** | `daed:circuit->html` self-contained SVG schematic + node voltages |
| **P1** | After `mutate!`, re-sim + re-emit reflects new R and v |
| **P2** | `daed:apply-viz-edits!` applies parameter edits with snapshot rollback |

## Run

```bash
./scripts/run-aura.sh examples/06-viz-bidirectional/main.aura
```

HTML artifacts (written by the probe):

```text
examples/06-viz-bidirectional/out/divider-before.html
examples/06-viz-bidirectional/out/divider-after-mutate.html
examples/06-viz-bidirectional/out/divider-after-edits.html
examples/06-viz-bidirectional/out/rc-lowpass.html
```

Open any file in a browser. Edit values → **Export edits JSON** / **Copy Aura apply form**, then apply with `daed:apply-viz-edits!` in a denseness session.

## Closed loop

```text
load → simulate → emit-html → mutate → simulate → emit-html
                 ↘ edit in browser → JSON edits → apply-viz-edits! → simulate → emit-html
```
