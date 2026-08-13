# ngspice live compare

ngspice ngspice-45.2

| deck | key | got | expected | |Δ| | bound | ok |
|------|-----|-----|----------|-----|-------|----|
| diode-bias | v(1) | 7.000000e-01 | 7.000000e-01 | 0 | 1e-9 | PASS |
| diode-bias | i(vin) | -4.93209e-03 | -4.93209e-03 | 0 | 5e-5 | PASS |
| diode-series | v(1) | 5.000000e+00 | 5.000000e+00 | 0 | 1e-9 | PASS |
| diode-series | v(2) | 6.964593e-01 | 6.964593e-01 | 0 | 2e-3 | PASS |
| diode-series | i(vin) | -4.30354e-03 | -4.30354e-03 | 0 | 5e-5 | PASS |
| rectifier | v(1) | 5.000000e+00 | 5.000000e+00 | 0 | 1e-9 | PASS |
| rectifier | v(2) | 4.303541e+00 | 4.303541e+00 | 0 | 2e-3 | PASS |
| rectifier | i(vin) | -4.30354e-03 | -4.30354e-03 | 0 | 5e-5 | PASS |
| bjt-ce | v(1) | 5.000000e+00 | 5.000000e+00 | 0 | 1e-9 | PASS |
| bjt-ce | v(2) | 2.700149e+00 | 2.700149e+00 | 0 | 5e-3 | PASS |
| bjt-ce | v(3) | 7.400299e-01 | 7.400299e-01 | 0 | 5e-3 | PASS |
| bjt-ce | v(4) | 1.200000e+00 | 1.200000e+00 | 0 | 1e-9 | PASS |
| bjt-ce | i(vcc) | -2.29985e-03 | -2.29985e-03 | 0 | 5e-5 | PASS |
| bjt-ce | i(vin) | -2.29985e-05 | -2.29985e-05 | 0 | 1e-6 | PASS |
