| Energy             | Sigma   | Energy Variance | DOF | Einf | Method                                                  | Reference |
|--------------------|---------|-----------------|-----|------|---------------------------------------------------------|-----------|
| -33.83169340557936 |         |                 | 16  | 0    | Exact diagonalization                                   | [code](https://github.com/varbench/methods/blob/main/scripts/J1J2/square_16_P_0.5/ed_netket.sh) |
| -33.8315064        |         | 7e-3            | 16  | 0    | VQE + symm. circuit (64 pars., exact grad, statevector) | [code](https://github.com/varbench/methods/blob/main/scripts/J1J2/square_16_P_0.5/vqe.sh) |
| -33.83169340557946 |         | 1e-15           | 16  | 0    | DMRG (bond dimension = 256)                             | [code](https://github.com/varbench/methods/blob/main/scripts/J1J2/square_16_P_0.5/dmrg.sh) |
| -33.0219           | 0.0036  | 12.9877         | 16  | 0    | RBM (alpha = 1)                                         | [code](https://github.com/varbench/methods/blob/main/scripts/J1J2/square_16_P_0.5/vmc_rbm.sh) |
| -32.5106           | 0.0015  | 2.20818         | 16  | 0    | Jastrow baseline                                        | [code](https://github.com/varbench/methods/blob/main/scripts/J1J2/square_16_P_0.5/vmc_jastrow.sh) |
| -33.831039193      | 0.00031 | 0.01741932679   | 16  | 0    | ClebschTree                                             | [paper](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.104.045123) |
