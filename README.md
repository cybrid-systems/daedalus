# Daedalus

**Aura Unify denseness span** — circuit simulation & evolvable netlist space.

> Greek craftsman-inventor who built living automata and labyrinthine mechanisms.
> This span projects **Aether + Hephaestus + Prometheus + Hermes** onto the domain of
> analog circuit simulation (SPICE-class), treating netlists, device models and solvers
> as first-class, mutable, agent-evolvable objects inside Aura’s native semantic space \(V_A\).

## Positioning vs Classic SPICE

Classic SPICE (ngspice, LTspice, HSPICE, …) is a mature **static tool**:
you give it a netlist, it returns waveforms. Decades of work have made its
device models, convergence heuristics and sparse solvers extremely robust.

Daedalus does **not** aim to replace production SPICE on accuracy or model coverage.
Its value lies elsewhere:

| Dimension              | Classic SPICE              | Daedalus                                      |
|------------------------|----------------------------|-----------------------------------------------|
| Accuracy & model library | Industry-grade            | Intentionally limited (P0)                    |
| Numerical robustness   | Battle-hardened            | Will improve over time                        |
| Circuit as data        | Text file                  | Live FlatAST                                  |
| Safe mutation          | External scripts only      | First-class (`mutate:*` + snapshot/rollback)  |
| Agent closed-loop      | Hand-rolled                | Native (Aether-style)                         |
| Kernel hot-swap        | Restart required           | Designed for (Hephaestus-style)               |
| Topology semantics     | Post-hoc parsing           | Explicit (Hermes-style)                       |

**One-sentence difference**:
> SPICE is a calculator you drive from the outside.
> Daedalus is a living laboratory where agents can rewrite the circuit, the models and even the solver strategies, with versioning and rollback built in.

## Span Thesis

\( S_{\text{Daedalus}} \) is the region of practical software consisting of:

- hierarchical, mutable netlists and device models
- numerical kernels (MNA, Newton, transient integration)
- closed-loop agent evolution of circuit topology / parameters / models
- topological correctness and probe insertion

**Claim**: Aura’s \(V_A\) is dense enough on this region that the evolvable core
(description → simulate → observe → decide → safe-mutate → verify → rollback)
remains predominantly pure Aura. Escapes are rare, metered and logged.

## Composition of Existing Spans

| Span | Contribution to Daedalus |
|------|--------------------------|
| **Aether** | Agent closed-loop (observe → decide → mutate → verify → rollback) applied to circuit evolution |
| **Hephaestus** | Numerical / performance kernels (stamp, solve, integrate) with ownership-safe hot-swap |
| **Prometheus** | Large-scale AST mutation surface for complex netlists + continuous LLM-driven model refinement |
| **Hermes** | Explicit topology, node–edge connectivity, interface boundaries and probe insertion |

Daedalus is therefore a **composition span**, not a fifth orthogonal mythic axis.
It reifies the Unify synthesis thesis in a concrete engineering domain.

## Interesting Play Modes

These are the kinds of experiments Daedalus is designed to make natural:

1. **Agent auto-repair**  
   Give a target (e.g. “mid-point voltage = 2.5 V, minimise power”).
   The agent mutates resistors or topology, re-simulates, keeps successful
   changes and rolls back failures.

2. **Living model evolution**  
   Treat simple diode / BJT models themselves as mutable ASTs.
   Agents can change parameters or even the structure of the model and
   immediately see the effect on circuit behaviour.

3. **Topology search with fitness**  
   Use simulation results as fitness. Agents perform genetic-style
   exploration (insert capacitors, move nodes, add buffers) under
   snapshot/rollback discipline.

4. **Live circuit surgery**  
   While a transient is conceptually running, take a snapshot, insert a
   probe or change a parameter, continue, and restore at any moment.

5. **Multi-agent collaboration**  
   One agent proposes topology, another tunes parameters, a third writes
   verification assertions — orchestrated with Aether’s `orch:*` primitives.

6. **Exploration → export**  
   Evolve and explore inside Daedalus, then export a converged netlist to
   a production SPICE engine for final high-accuracy sign-off.

7. **Teaching dual**  
   One system that simultaneously teaches Modified Nodal Analysis and
   safe self-modifying agents.

## Educational Use

Daedalus is particularly well-suited for circuit education because it turns two traditionally separate subjects into a single interactive laboratory.

### What it teaches together

- **Classical circuit theory**: KCL/KVL, nodal analysis, MNA stamping, DC operating point, basic transient response.
- **Modern system thinking**: code-as-data, safe mutation, snapshot/rollback, agent closed-loops.

Students no longer have to learn “circuits first, agents later”. They encounter both in the same runtime.

### From black box to inspectable system

Classic SPICE is largely a black box for learners: write netlist → run → look at waveforms.  
In Daedalus the netlist is a live FlatAST. Students can:

- `query` nodes and connections,
- manually `mutate` a component and re-simulate immediately,
- take snapshots before risky changes and roll back on failure,
- (later) inspect how the matrix is stamped and how the solver behaves.

### From “verify the formula” to “meet a design goal”

Traditional exercises ask students to calculate a known voltage.  
With an agent loop the exercise can become:

> Write a small agent that adjusts resistors so the mid-point voltage approaches 2.5 V while keeping power low.

Students practise both circuit intuition and the discipline of defining goals, trying changes safely, and evaluating results.

### Natural progression of difficulty

1. Manual mutation + simulation (feel the effect of parameters).
2. Simple observe → mutate → re-simulate loops.
3. Multi-agent collaboration (topology, tuning, checking constraints).
4. Advanced: attempt to mutate solver strategies themselves and observe convergence differences.

### Concrete classroom scenarios

| Scenario                              | Learning outcome                                      |
|---------------------------------------|-------------------------------------------------------|
| Voltage divider + manual R change     | Voltage division, loading effect                      |
| RC low-pass + change time constant    | Time constants, step response intuition               |
| Agent auto-tune to a target voltage   | Goal-driven design + safe trial-and-error             |
| Deliberately break a connection then fix it | Topology correctness, debugging mindset          |
| Export final netlist to real SPICE    | Understand the boundary between exploration and sign-off tools |

In short: classic SPICE teaches students how to **use a tool to verify known circuits**.  
Daedalus is better at teaching students how to **understand and reshape circuits, and how to let a program help them explore**.

## Phase Targets

**P0 / Phase 1**
- Netlist as FlatAST (R, C, L, V, I + basic controlled sources)
- Linear `.op` (DC operating point)
- Simple fixed-step `.tran`
- Agent can mutate a resistor value (or topology) and obtain consistent results after re-simulation
- Snapshot / rollback preserves both semantic state and denseness metrics
- At least three denseness probes pass

**P1 / Phase 5** ([issue #2](https://github.com/cybrid-systems/daedalus/issues/2))
- Shockley diode and Ebers-Moll NPN (educational-grade, FlatAST-mutable)
- Dense Newton-Raphson `.op` and BE+NR `.tran`
- Linear probes unchanged (one-shot path when no D/Q)

**Non-goals (P0 / P1)**  
Full BSIM, commercial-grade sparse solvers, schematic capture UI, mixed-signal co-simulation.

## Layout

```
daedalus/
├── README.md
├── lib/                      # pure-Aura core (daedalus-min; netlist/stamp/… later)
├── examples/                 # denseness probes 00…
├── projects/
│   └── daedalus-core/        # main evolvable project (SPEC.md + code)
├── scripts/                  # run-aura, run-all, check-structure
├── notes/                    # denseness-report, escape-log, design
└── prompts/
```

## Quick Start

Requires a local Aura binary (default sibling `../aura-grok/build/aura`).

```bash
./scripts/check-structure.sh
./scripts/run-aura.sh examples/00-smoke/main.aura
./scripts/run-all.sh
```

Phase 1 linear `.op` (voltage divider):

```bash
./scripts/run-aura.sh examples/01-voltage-divider/main.aura
```

Phase 2 fixed-step `.tran` (RC low-pass):

```bash
./scripts/run-aura.sh examples/02-rc-lowpass/main.aura
```

Phase 3 safe mutate + dual rollback:

```bash
./scripts/run-aura.sh examples/03-mutate-resistor/main.aura
```

Phase 4 agent auto-tune closed loop:

```bash
./scripts/run-aura.sh examples/05-agent-autotune/main.aura
```

Bidirectional netlist ↔ HTML visualization ([issue #1](https://github.com/cybrid-systems/daedalus/issues/1)):

```bash
./scripts/run-aura.sh examples/06-viz-bidirectional/main.aura
# open examples/06-viz-bidirectional/out/*.html in a browser
```

Phase 5 nonlinear devices + Newton-Raphson ([issue #2](https://github.com/cybrid-systems/daedalus/issues/2)):

```bash
./scripts/run-aura.sh examples/07-diode-op/main.aura
./scripts/run-aura.sh examples/08-bjt-ce/main.aura
./scripts/run-aura.sh examples/09-diode-clamp-tran/main.aura
```

Vision → netlist → repair → simulate ([issue #6](https://github.com/cybrid-systems/daedalus/issues/6)):

```bash
./scripts/run-aura.sh examples/10-vision-pipeline/main.aura
./scripts/from-image.sh examples/10-vision-pipeline/fixtures/divider.svg
```

Controlled sources VCVS/VCCS/CCCS/CCVS ([issue #12](https://github.com/cybrid-systems/daedalus/issues/12)):

```bash
./scripts/run-aura.sh examples/11-controlled-sources/main.aura
```

Linear `.op` denseness suite ([issue #13](https://github.com/cybrid-systems/daedalus/issues/13)):

```bash
./scripts/run-aura.sh examples/12-linear-op-suite/main.aura
```

Fixed-step `.tran` suite ([issue #14](https://github.com/cybrid-systems/daedalus/issues/14)):

```bash
./scripts/run-aura.sh examples/13-tran-suite/main.aura
```

Agent mutate + snapshot/rollback ([issue #15](https://github.com/cybrid-systems/daedalus/issues/15)):

```bash
./scripts/run-aura.sh examples/14-mutate-rollback/main.aura
```

Nonlinear `.op` helpers — damping, previous guess, Gmin, diagnostics ([issue #16](https://github.com/cybrid-systems/daedalus/issues/16)):

```bash
./scripts/run-aura.sh examples/15-nr-helpers/main.aura
```

Nonlinear `.op` vs ngspice ([issue #17](https://github.com/cybrid-systems/daedalus/issues/17)):

```bash
./scripts/run-aura.sh examples/16-nl-op-suite/main.aura
./scripts/compare-ngspice.sh   # optional host oracle
```

Adaptive `.tran` (LTE step control) ([issue #18](https://github.com/cybrid-systems/daedalus/issues/18)):

```bash
./scripts/run-aura.sh examples/17-adapt-tran/main.aura
```

Level-1 NMOS ([issue #19](https://github.com/cybrid-systems/daedalus/issues/19)):

```bash
./scripts/run-aura.sh examples/18-mosfet/main.aura
```

## Relation to Unify

May be consumed as a deep project under `unify/projects/daedalus` or kept as a
first-class sibling span. Failures and denseness gaps are expected to feed back
into Aura via the Unify issue pump.

## License

Apache-2.0
