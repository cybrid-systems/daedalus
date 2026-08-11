# Daedalus

**Aura Unify denseness span** — circuit simulation & evolvable netlist space.

> Greek craftsman-inventor who built living automata and labyrinthine mechanisms.
> This span projects **Aether + Hephaestus + Prometheus + Hermes** onto the domain of
> analog circuit simulation (SPICE-class), treating netlists, device models and solvers
> as first-class, mutable, agent-evolvable objects inside Aura’s native semantic space \(V_A\).

## Span Thesis

\( S_{\text{Daedalus}} \) is the region of practical software consisting of:

- hierarchical, mutable netlists and device models
- numerical kernels (MNA, Newton, transient integration)
- closed-loop agent evolution of circuit topology / parameters / models
- topological correctness and probe insertion

**Claim**: Aura’s \(V_A\) is dense enough on this region that the evolvable core (description → simulate → observe → decide → safe-mutate → verify → rollback) remains predominantly pure Aura. Escapes are rare, metered and logged.

## Composition of Existing Spans

| Span | Contribution to Daedalus |
|------|--------------------------|
| **Aether** | Agent closed-loop (observe → decide → mutate → verify → rollback) applied to circuit evolution |
| **Hephaestus** | Numerical / performance kernels (stamp, solve, integrate) with ownership-safe hot-swap |
| **Prometheus** | Large-scale AST mutation surface for complex netlists + continuous LLM-driven model refinement |
| **Hermes** | Explicit topology, node–edge connectivity, interface boundaries and probe insertion |

Daedalus is therefore a **composition span**, not a fifth orthogonal mythic axis. It reifies the Unify synthesis thesis in a concrete engineering domain.

## Phase Targets

**P0 / Phase 1**
- Netlist as FlatAST (R, C, L, V, I + basic controlled sources)
- Linear `.op` (DC operating point)
- Simple fixed-step `.tran`
- Agent can mutate a resistor value (or topology) and obtain consistent results after re-simulation
- Snapshot / rollback preserves both semantic state and denseness metrics
- At least three denseness probes pass

**Non-goals (P0)**
Full BSIM, commercial-grade sparse solvers, schematic capture UI, mixed-signal co-simulation.

## Layout

```
daedalus/
├── README.md
├── lib/                      # pure-Aura core (netlist, stamp, solve, probe …)
├── examples/                 # denseness probes 01…
├── projects/
│   └── daedalus-core/        # main evolvable project (SPEC.md + code)
├── tests/
├── scripts/
├── notes/                    # denseness-report, escape-log, design
└── prompts/
```

## Quick Start (once Aura sibling is available)

```bash
source ./scripts/env.sh
./scripts/run-aura.sh examples/01-voltage-divider.aura
./scripts/project-evolve.sh projects/daedalus-core
```

## Relation to Unify

May be consumed as a deep project under `unify/projects/daedalus` or kept as a first-class sibling span. Failures and denseness gaps are expected to feed back into Aura via the Unify issue pump.

## License

Apache-2.0
