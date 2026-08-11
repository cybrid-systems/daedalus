# Daedalus Span Design

## Why a new composition span?

Aether, Hephaestus, Prometheus and Hermes each stress one axis of Aura’s density:

- Aether – long-running agent loops + safe mutation
- Hephaestus – numerical kernels under load + ownership
- Prometheus – large mutable ASTs + continuous LLM mutation + incremental cost
- Hermes – topology, boundaries, wiring

Circuit simulation simultaneously demands all four. Therefore it is not an extension of any single existing span; it is their **composition** projected onto the analog-circuit domain.

## Mapping

```
                  Aether (agent loop)
                        │
        ┌───────────────┼───────────────┐
        │               │               │
     Hermes          Daedalus        Prometheus
   (topology)     (netlist +        (large AST
    nets/probes)   models +          mutation)
        │          results)             │
        └───────────────┼───────────────┘
                        │
                  Hephaestus
               (MNA / Newton /
                integration kernels)
```

## Naming

**Daedalus** (Δαίδαλος) — the archetypal craftsman-inventor of Greek myth.  
He built living automata, self-moving tripods and the labyrinth: the perfect mythic counterpart to an evolvable, self-modifying circuit-simulation space.

Alternative considered: **Talos** (the bronze automaton forged by Hephaestus).  
Daedalus was preferred because it denotes the *space of craft and invention* rather than a single artifact.

## Denseness claim

On \(S_{\text{Daedalus}}\) the evolvable core can stay inside \(V_A\).  
Only carefully metered escapes (high-performance linear algebra, etc.) are permitted; every escape is recorded in `notes/escape-log.md`.
