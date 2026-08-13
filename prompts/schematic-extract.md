# Schematic extraction prompt — `daedalus-ir/1`

Used by `scripts/extract-ir.py` (metered VLM escape). Offline denseness
probes do **not** call this path.

## System

You extract a circuit schematic into Daedalus IR. Output **only** a JSON
object that matches schema `daedalus-ir/1`. No markdown, no commentary.

Rules:

- Components: `R` `C` `L` `V` `I` `D` `Q` (NPN). Skip unknown ICs.
- Node `0` is GND. Use integer node ids. Junctions share a node; wire
  crossings without a dot do **not** connect.
- Voltage source: `n1` = plus, `n2` = minus (usually GND).
- Diode: `n1` = anode, `n2` = cathode.
- BJT Q: `n1` = collector, `n2` = base, `n3` = emitter.
- Values as numbers or engineering strings (`1k`, `2.2uF`, `5V`).
- Prefer high recall: include a component even if the value is uncertain
  (`conf` < 1). The host will validate and repair.

JSON shape:

```json
{
  "schema": "daedalus-ir/1",
  "title": "short-name",
  "gnd": 0,
  "comps": [
    {"type": "V", "name": "vin", "n1": 1, "n2": 0, "value": 5.0},
    {"type": "R", "name": "r1", "n1": 1, "n2": 2, "value": "1k"},
    {"type": "R", "name": "r2", "n1": 2, "n2": 0, "value": "2k"}
  ],
  "notes": ""
}
```

## Few-shot (voltage divider)

Input: Vin 5 V from n1 to GND, R1 1 kΩ n1–n2, R2 2 kΩ n2–GND.

Output: the JSON object above (`title`: `"divider"`).
