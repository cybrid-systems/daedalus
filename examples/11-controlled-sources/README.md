# 11-controlled-sources

**Milestone 0 / issue #12** — complete FlatAST netlist + MNA stamp for
P0 linear devices including controlled sources.

| Type | SPICE | Relation |
|------|-------|----------|
| `daed:E` | VCVS | \(v_{n1n2} = \mu\, v_{c+c-}\) |
| `daed:G` | VCCS | \(i_{n1\to n2} = g_m\, v_{c+c-}\) |
| `daed:F` | CCCS | \(i_{n1\to n2} = \beta\, i_{\mathrm{ctrl}}\) |
| `daed:H` | CCVS | \(v_{n1n2} = r_m\, i_{\mathrm{ctrl}}\) |

`F` / `H` sense the branch current of a named `V`, `E`, or `H`.

| Item | Value |
|------|--------|
| Axes | netlist ADT + stamp + query + topology |
| VCVS | \(\mu=2\) → \(v=10\) |
| VCCS | \(g_m=2\,\mathrm{mS},\,R=1\,\mathrm{k}\Omega\) → \(v=-10\) |
| CCCS / CCVS | vs \(i_V=-5\,\mathrm{mA}\) |
| Query | `daed:query-comp` / `query-by-type` / `query-nodes` |
| Core escapes | 0 |

## Run

```bash
./scripts/run-aura.sh examples/11-controlled-sources/main.aura
```
