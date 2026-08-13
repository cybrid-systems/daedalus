# SPICE export (issue #26)

Daedalus explores; ngspice / LTspice signs off. `daed:circuit->spice` emits a
deterministic deck from the live FlatAST. No hand edits for the subset below.

## Supported subset

| Daedalus | SPICE |
|----------|-------|
| `R` `C` `L` | `Rname n1 n2 val` |
| `V` `I` | `Vname n1 n2 DC val` |
| `D` | instance + `.model D(IS N)` |
| `Q` NPN | instance + `.model NPN(IS BF BR)` |
| `M` NMOS L1 | instance `nd ng ns ns` + `.model NMOS(LEVEL=1 VTO KP LAMBDA)` `W` `L` |
| `E` `G` | `n1 n2 nc+ nc- gain` |
| `F` `H` | `n1 n2 Vctrl gain` |

## Temperature

At `T = Tnom = 27 °C` Daedalus freezes `Vt = 26 mV` (Is-scale = 1). The deck
sets `.options tnom=28.555 temp=28.555` so ngspice `kT/q` matches. If
`daed:set-temp!` moves T, `temp` tracks as `28.555 + (T − Tnom)`.

## Limitations

- PNP / PMOS / BSIM are not exported (not in the P0/P1 device set).
- MOSFET `Cgs`/`Cgd` are Daedalus `.tran` parasitics and are omitted.
- Independent sources export as DC; PWL/SIN stimuli are out of scope.
- First line is a title comment (SPICE convention).

## Round-trip

Probe 25 writes `examples/25-spice-export/out/*.cir`.
`scripts/roundtrip-spice.sh` runs `ngspice -b` when installed.
