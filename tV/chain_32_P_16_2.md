| Energy             | Sigma | Energy Variance | DOF | Einf              | Method                          | Reference |
|--------------------|-------|-----------------|-----|-------------------|---------------------------------|-----------|
| -12.32869972364372 |       |                 | 16  | 15.48387096774194 | Exact diagonalization           | [code](https://github.com/varbench/methods/blob/main/scripts/tV/chain_32_P_16_2/ed_lattice_symmetries.sh) |
| -12.32869928774351 |       |                 | 16  | 15.48387096774194 | DMRG (maxbonddim = 200)         | [code](https://github.com/varbench/methods/blob/main/scripts/tV/chain_32_P_16_2/dmrg.sh) |
| -12.32494350621494 |       | 5.05e-3         | 16  | 15.48387096774194 | QMC (continuous-time expansion) | [paper](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.93.155117) [code](https://github.com/wangleiphy/SpinlesstV-LCT-INT) |
| -12.20726          | 6.3e-4 | 0.4109529      | 16  | 15.48387096774194 | Jastrow baseline                |           |
| -10.5012           | 1.5e-3 | 2.220112       | 16  | 15.48387096774194 | RBM (alpha = 1)                 |           |
