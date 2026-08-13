# 23-agent-evolve

**Milestone 4 / issue #24** — agent closed-loop parameter tuning.

| Case | What happens |
|------|----------------|
| CE bias | `Rb` starts at 50 kΩ, spec `Vc = 2.5 V ± 2 %`. Hill-climb commits + rollbacks. |
| Good states | `evo-restore-good!` can rewind to any committed snapshot; last still passes. |
| Replay | `evo-replay!` on a fresh netlist reproduces the same `Rb`. |
| RC filter | scale `C` so `.measure WHEN 2.5 V` ≈ `τ ln 2`; `final` stays ≈ 5 V. |
| Skip / refuse | already-in-spec is a skip; `R ≤ 0` is refused. |

`daed:evolve!` is the Aether loop: observe spec → propose → snapshot → mutate → evaluate → commit or rollback. The mutation log plus good-state list make the search inspectable and reproducible.

## Run

```bash
./scripts/run-aura.sh examples/23-agent-evolve/main.aura
```
