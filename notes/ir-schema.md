# Daedalus IR schema — `daedalus-ir/1`

Versioned intermediate representation between a schematic extractor
(VLM or fixture) and `daed:circuit`. Contract for issue #6 / #7.

**Do not treat extractor output as correct.** IR is a high-recall
candidate. Static validation + simulation-feedback repair decide
whether a circuit is runnable.

## Document

| Field | Type | Required | Meaning |
|-------|------|----------|---------|
| `schema` | string | yes | `"daedalus-ir/1"` |
| `title` | string | no | Circuit name |
| `gnd` | int / string | no | Designated ground (default `0` / `"GND"`) |
| `nodes` | list | no | Optional `{id, name}` annotations |
| `comps` | list | yes | Components (see below) |
| `notes` | string | no | Free text from the page |
| `source` | hash | no | `{image, model, conf}` provenance |

## Component

| Field | Type | Required | Meaning |
|-------|------|----------|---------|
| `type` | string | yes | `R` `C` `L` `V` `I` `D` `Q` `E` `G` `F` `H` |
| `name` | string | yes | Unique refdes |
| `n1` `n2` | int | yes | Terminals (Q: C, B) |
| `n3` | int | Q / E / G | Emitter (Q) or control + (E, G) |
| `n4` | int | E / G | Control − |
| `ctrl` | string | F / H | Name of V/E/H whose current is sensed |
| `value` | number / string | yes | What is **printed on the schematic**: `10k`, `100uF`, `3V`, transistor type `9013`, LED color `red`. Not a fake `Is`. |
| `unit` | string | no | Hint: `ohm` `F` `H` `V` `A` |
| `params` | hash | no | Simulator cards: `Is` `n` `vt` `bf` `br` `gmin`. Q/D `Is` lives here (default 1e-15 / 1e-14). |
| `conf` | number | no | Extractor confidence `0..1` |

Node `0` is GND. Extractors may use `"GND"` / `"gnd"`; conversion maps those to `0`.

**Topology.** `n1`/`n2`/`n3` are terminal-to-node pins. The same integer means the same net (wires join). That *is* the netlist:

- R/C/L/V/I/D: `n1`–`n2` (V: plus/minus; D: anode/cathode)
- Q: `n1`=collector, `n2`=base, `n3`=emitter

This circuit is fully described by those pins. Geometry and textbook rotation are not stored.

## Conversion

- `daed:ir->circuit` — deterministic, pure Aura
- `daed:circuit->ir` — simplified round-trip (drops provenance)
- Values: `daed:parse-value` applies SI prefixes after stripping unit suffixes

## Examples

Hand-written instances live in `lib/ir.aura` (`daed:ir-ex-*`) and
`examples/10-vision-pipeline/`.
