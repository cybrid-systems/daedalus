# 26-native-hotswap

**Milestone 5 / issue #28** — pure Aura GE → C++ dense solve → fallback.

| Step | What happens |
|------|----------------|
| Pure | divider `v2=10/3`, `escapes=0` |
| Native | `solve-rebind! "native"`; same `v2`; escape count +1 |
| Poison | `daed_set_fail(1)` → native rc≠0 → backend back to `"pure"`; voltages still match |
| Restore | circuit snapshot after native still rolls back |

Build the `.so` once, then run the probe:

```bash
./scripts/build-native.sh
./scripts/run-aura.sh examples/26-native-hotswap/main.aura
```

Default backend is `"pure"` so probes 00–25 stay E=0.
