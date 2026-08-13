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
| `type` | string | yes | `R` `C` `L` `V` `I` `D` `Q` |
| `name` | string | yes | Unique refdes |
| `n1` `n2` | int | yes | Terminals (Q: C, B) |
| `n3` | int | Q only | Emitter |
| `value` | number / string | yes | SI value or engineering string (`1k`, `2.2uF`) |
| `unit` | string | no | Hint: `ohm` `F` `H` `V` `A` |
| `params` | hash | no | `n` `vt` `bf` `br` `gmin` `Is` |
| `conf` | number | no | Extractor confidence `0..1` |

Node `0` is GND. Extractors may use `"GND"` / `"gnd"`; conversion maps those to `0`.

## Conversion

- `daed:ir->circuit` — deterministic, pure Aura
- `daed:circuit->ir` — simplified round-trip (drops provenance)
- Values: `daed:parse-value` applies SI prefixes after stripping unit suffixes

## Examples

Hand-written instances live in `lib/ir.aura` (`daed:ir-ex-*`) and
`examples/10-vision-pipeline/`.
