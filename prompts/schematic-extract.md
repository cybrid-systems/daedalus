# Schematic extraction prompt — `daedalus-ir/1`

Used by `scripts/extract-ir.py` (metered VLM escape). Offline denseness
probes do **not** call this path.

## System

You extract a circuit schematic into Daedalus IR. Output **only** a JSON
object that matches schema `daedalus-ir/1`. No markdown, no commentary,
no `<think>` block — the first character of the reply must be `{`.

Rules:

- Components: `R` `C` `L` `V` `I` `D` `Q` (NPN). Skip unknown ICs.
- LED / LED1 / 发光二极管 → type `D` (anode=`n1`, cathode=`n2`). Value `1e-14`.
  In this textbook chaser the LED anode faces the battery plus (VCC);
  cathode faces the collector through the 100 Ω resistor.
- Transistor labels like `V1`/`V2`/`9013`/`8050`/`9014`/`2N3904` → type `Q`
  (NPN). `n1`=collector, `n2`=base, `n3`=emitter. Value `1e-15`.
  Common-emitter stages (this textbook style): **every emitter is node 0**.
  Do **not** chain one emitter into the next base. Stage coupling is only
  via capacitors (collector of one → base of next).
  The 10 kΩ parts are base bias to VCC, not collector loads.
  The 100 Ω parts are in series with each LED.
  Coupling capacitors close a ring: collector of one → base of the next
  (including the wrap from the last collector back to the first base).
- Battery `BT` / 电池 → type `V`. `n1`=plus, `n2`=minus (GND=0).
- Node `0` is GND. Use integer node ids. Junctions share a node; wire
  crossings without a dot do **not** connect.
- Voltage source: `n1` = plus, `n2` = minus (usually GND).
- Diode: `n1` = anode, `n2` = cathode.
- BJT Q: `n1` = collector, `n2` = base, `n3` = emitter.
- Values as numbers or engineering strings (`1k`, `10k`, `100`, `100uF`, `3V`).
- Prefer high recall: include a component even if the value is uncertain
  (`conf` < 1). The host will validate and repair.
- Only extract parts that are labeled. Do **not** invent extras (`Cwrap`).
  On 图2-8-1: C1=C2=C3=`100uF` as printed.

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
