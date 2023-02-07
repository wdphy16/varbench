| Energy                | Sigma                    | Energy Variance          | DOF | Einf                | Method                                                       | Reference |
|-----------------------|--------------------------|--------------------------|-----|---------------------|--------------------------------------------------------------|-----------|
| -11.980026283471341   |                          |                          | 5   | 0.02666666666666667 | Exact diagonalization                                        | [code](https://github.com/varbench/methods/blob/main/scripts/tV/square_16_P_5_0.01/ed_netket.sh) |
| -11.980033022886133   | 1.0257481572668477e-05   | 4.303658331496602e-05    | 5   | 0.02666666666666667 | VMC Determinant Slater-Jastrow (RBM) Ansatz                  | [paper](https://arxiv.org/abs/2406.09077) [code](https://github.com/varbench/methods/blob/main/scripts/tV/square_16_P_5_0.01/tV_model_no_symm.sh) |
| -11.98002586610116360 | 1.162693337441909767e-06 | 5.502099642279632244e-07 | 5   | 0.02666666666666667 | VMC Determinant Slater-Backflow-Jastrow (RBM) Ansatz with K=0 projections (symmetric wrt translations) | [paper](https://arxiv.org/abs/2406.09077) [code](https://github.com/varbench/methods/blob/main/scripts/tV/square_16_P_5_0.01/tV_model_bf.sh) |