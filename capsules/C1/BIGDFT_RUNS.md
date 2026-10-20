# BigDFT calculations in C1

All files listed here are **inside `C1.zip`**: run `capsule-maker import C1.zip c1` and the paths below are relative to `c1/`.
This page is an index only; the numbers come from the packaged logs and are recomputed by `tests/test_structures.py`.

**Common settings:**
- **Code:** BigDFT 1.9.5 (PSolver 1.10, libxc 4.3.4, OpenMPI 5.0.7).
- **Boundary conditions:** free.
- **Pseudopotentials:** Krack PBE HGH-K (`bigdft/psppar/`); 72 valence electrons for thioxanthone, 226 for 6a.
- **Grid:** hgrid 0.35 bohr, rmult (6, 9).
- **SCF:** gnrm_cv 1e-5.
- **Spin:** T1 = `nspin 2, mpol 2`.
- **Launch:** `mpirun -np N --map-by slot:PE=OMP bigdft -n NAME` (`procedures/run_bigdft.slurm`).

## Production runs (Phase 1, thioxanthone C13H8OS)

| Run (`bigdft/runs/<name>/`) | Type | XC | Geometry | MPI×OMP | Wall | Peak RSS | Converged | E (Ha) |
|---|---|---|---|---|---|---|---|---|
| `tx_S0_pbe_geopt` | S0 SQNM geopt | PBE (−101130) | GFN2 start | 12×4 | 8 min 28 s | — | it. 25, Fmax 1.21e-4 | −104.958932176445 |
| `tx_T1_pbe_geopt` | T1 SQNM geopt | PBE | GFN2 start | 12×4 | 37 min 41 s | — | it. 30, Fmax 6.63e-5, M = 2.000 | −104.868778644431 |
| `tx_S0_pbe0_at_S0pbe` | S0 single point | PBE0 (−406) | PBE S0 | 8×8 | 8 min 40 s | 30.1 GB | 46 SCF, gnrm 6.3e-6 | −104.920157843791 |
| `tx_S0_pbe0_at_T1pbe` | S0 single point | PBE0 | PBE T1 | 8×8 | 8 min 34 s | 30.1 GB | 46 SCF, gnrm 7.8e-6 | −104.911685404613 |
| `tx_T1_pbe0_at_S0pbe` | T1 single point | PBE0 | PBE S0 | 8×8 | 36 min 52 s | 48.6 GB | 68 SCF, gnrm 8.8e-6, M = 2.000 | −104.815933904345 |
| `tx_T1_pbe0_at_T1pbe` | T1 single point | PBE0 | PBE T1 | 8×8 | 38 min 10 s | 52.6 GB | 72 SCF, gnrm 8.9e-6, M = 2.000 | −104.820844775510 |

Peak RSS is from Slurm `sacct`. It was not recorded for the PBE geopts.

Each run directory contains:
- the input as run, byte-identical to `bigdft/inputs/<name>.yaml`
- `log-<name>.yaml`, with the install prefix redacted
- `time-<name>.yaml`
- for the geopts: `final_<name>.yaml` (final geometry) and `data-<name>/geopt.mon`
- for the single points: `forces_<name>.yaml`
- the Slurm `.out` file

## Derived energies (`bigdft/runs/phase1_summary.json`, from `procedures/analyze_phase1.py`)

| Quantity | PBE | PBE0 |
|---|---|---|
| Adiabatic E_T = E(T1@T1) − E(S0@S0) | 236.70 kJ/mol (2.453 eV) | **260.75 kJ/mol (2.702 eV)** |
| Vertical absorption E(T1@S0) − E(S0@S0) | — | 273.64 kJ/mol (2.836 eV) |
| Vertical emission E(T1@T1) − E(S0@T1) | — | 238.50 kJ/mol (2.472 eV) |
| vs literature thioxanthone (274.1 kJ/mol) | −0.388 eV, fails the 0.2 eV window | −0.138 eV, passes |

## Inputs and dry runs

| Path | Contents |
|---|---|
| `bigdft/inputs/` | 30 inputs + `index.json`, from `procedures/make_inputs.py`: the 6 above and **24 not yet run**, the 6a S1 S0/T1 PBE grid-convergence set (hgrid 0.45/0.40/0.35/0.30 × rmult 5-8/6-9/7-10) for C2 |
| `bigdft/dryrun/`, `bigdft/dryrun_pbe0/` | `SystemCalculator(dry_run=True)` logs and `dryrun_summary.json` for all 30 inputs: **30/30 passed** |

Dry-run memory estimates for 6a (serial): S0 4.4–24.1 GB, T1 8.8–47.9 GB. These do **not** cover PBE0 exact exchange.

## Failed submissions (recorded in `evidence/run_log.md`, outputs not packaged)

| Jobs | Failure |
|---|---|
| 211183–211184 | `srun` started 12 singletons (no PMIx), which ran out of memory. Fixed by using `mpirun` |
| 211187–211190 | PBE0 at 16×2 with 24 GB per job: OOM in the input guess. Fixed by measuring memory: 30 GB (S0) / 50 GB (T1) at 8×8 |
