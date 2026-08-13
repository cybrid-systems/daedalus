# 18-mosfet

**Milestone 2 / issue #19** — Level-1 NMOS (Shichman-Hodges) MNA + NR.

| Case | Circuit | Expect |
|------|---------|--------|
| Cutoff | inverter, `Vin=0` | `vout ≈ Vdd` |
| On | inverter, `Vin=5`, `R=1k` | linear-region `vout ≈ 0.566 V` |
| CS | `R=5k`, `Vin=Vto+√0.5` | sat mid-rail `vout ≈ 2.5 V` |
| Mutate | `Vto 0.8 → 1.2` | `vout` rises; snapshot restores |
| `.tran` | MOSFET + RC load, adaptive BE | off → `Vdd`; on → ~0.57 V |

Defaults: `Kp=2e-4`, `W/L=10`, `Vto=0.8`, `λ=0`. Bulk is tied to source. `Kp`, `W`, `L`, `Vto`, `λ`, `Cgs`, `Cgd` are mutable model fields.

## Run

```bash
./scripts/run-aura.sh examples/18-mosfet/main.aura
```
