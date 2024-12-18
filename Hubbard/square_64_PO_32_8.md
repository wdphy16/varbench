| Energy   | Sigma | Energy Variance | DOF | Einf | Method                                                       | Reference |
|----------|-------|-----------------|-----|------|--------------------------------------------------------------|-----------|
| -31.8998 |       | 1.107           | 64  | 128  | DMRG (MaxLinkDim=10000, MaxTruncErr ~ 3.4E-5, Extrap Energy -32.0027 +/- 0.0206) | [code](https://github.com/varbench/methods/blob/main/programs/dmrg_itensors_hubbard/square_64_PO_32_8.jl) |
| -31.964  | .0023 | 0.03(90)        | 64  | 128  | VAFQMC                                                       | [paper](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.107.115133) |
| -32.029  | 0.015 |                 | 64  | 128  | AFQMC (Metropolis, Trotter error extrapolated), numerically exact | [paper](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.92.033603) [code](https://github.com/varbench/methods/blob/main/scripts/Hubbard/square_64_PO_32_8/AFQMC/)  |
