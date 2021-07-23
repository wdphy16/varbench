# Transverse-Field Ising Model


The model is defined on the edges of an arbitray graph and reads
$ H = \Gamma \sum_i \sigma^x_i + V \sum_<i,j> \sigma^z_i \sigma^z_j  $
where we take Pauli matrices $\sigma^{x,y,z}_i$.

## Naming

The name of the data files follows the convention `lattice_N_Gamma_V.md`

---

`lattice` is the name of the lattice, also containing its extent/further information needed to specify the specific lattice, including its periodic boundary conditions. See `lattice.md` in the main repository for further information and examples.

`N` is the total number of spins

`Gamma` is the value of the transverse field Gamma

`V` is the value of the interaction 