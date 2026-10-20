# Plan and status: reproducing E_T = 269 kJ/mol of catalyst 6a with BigDFT, as a growing research capsule

Status as of 2026-10-20: **capsule C1 released; Phase 0 and Phase 1 are done; Phases 2–5 are open.**

## 1. Goal

Irle et al., *Nature Synthesis* 2026 (doi:10.1038/s44160-026-01173-7) report a triplet energy of
**E_T = 269 kJ/mol (2.788 eV)** for the tetrapeptide photocatalyst **6a**, (R,R,S)-Pga-Pro-Aib-pTxa-OMe. The value is
the inflection point of the 77 K phosphorescence spectrum in an EtOH glass. The paper says the photophysics is "comparable
to parent 9H-thioxanthen-9-one".

The study has two aims:

1. **Science:** reproduce this E_T with BigDFT ΔSCF (S0 closed-shell, T1 as `nspin 2, mpol 2`), as an adiabatic
   energy E[T1 @ T1 geometry] − E[S0 @ S0 geometry].
2. **Method:** show that the knowledge can be **transferred** to other agents and developers as a Capsule-Maker
   research capsule. It should also **grow** checkpoint by checkpoint (C1 → C2 → C3 …) without losing what earlier
   versions established, including corrections, failed attempts and open questions.

Three agent tools make up the pipeline:

| Tool | Role |
|---|---|
| Paper2Agent paper skill for the paper (TengxiangLii/P2A-Robert-2026, commit bc704b2) | target value, conditions, NMR restraints, verbatim excerpts |
| BigDFT agent skills (bigdft-skills 0.12.1: input, pseudopotentials, logfile) + PyBigDFT 1.9.6 | input generation, dry runs, pseudopotentials |
| Capsule-Maker 0.1.0-alpha (BigDFT-group/capsule-maker) | curated memory → capsule → approve/export → import/verify/resume → extend |

The researcher approved each step before it ran. Every calculation used inputs that first passed a BigDFT dry run
(`SystemCalculator(dry_run=True)`). If a dry run gave an error, nothing was calculated.

## 2. What was done

### Phase 0: setup (C1 knowledge, part 1)

| Step | Outcome |
|---|---|
| 0.2 Structure knowledge | Curated from primary sources: the paper skill, the 6a structure files and the transcript of the session that built them. 6a = 77 atoms, C31H34N4O7S, rebuilt from the Chemotion SMILES and fitted to the 33 Table S1 NMR restraints and the type II′ β-turn. **S1** (GFN2-xTB/ALPB(CH2Cl2) with flat-bottom restraints, worst violation 0.07 Å) is the starting geometry, confirmed by the researcher. **S3** (unrestrained) is the sensitivity reference. While re-deriving values from the files, one error was caught: the S1−S3 gap is 0.453 eV, not 0.49 eV. |
| 0.3 BigDFT-ready geometries | S1 and S3 as plain 4-column XYZ (coordinates copied verbatim). Calibration molecule thioxanthone (C13H8OS) built from SMILES and pre-optimised with GFN2-xTB. |
| 0.4 Environment and pseudopotentials | BigDFT 1.9.5 (PSolver 1.10, libxc 4.3.4, OpenMPI 5.0.7) on a CPU Slurm cluster. Krack PBE HGH-K pseudopotentials for C, H, N, O, S (researcher-confirmed): 226 electrons for 6a, 72 for thioxanthone. The HGH-K+NLCC set has no S. PyBigDFT bug: `set_psp_krack/nlcc(elements=[…])` silently loads nothing. |
| 0.5 Inputs and dry run | `make_inputs.py` writes 30 self-contained inputs, deterministically. **Dry run: 30/30 passed.** Environment pitfalls: an absolute `run_dir` is rejected; `bigdft-tool` needs `python` on PATH. The thioxanthone literature E_T was retrieved: 65.5 kcal/mol = **274.1 kJ/mol** (secondary source; ref. 36 and the primary papers were not accessible). |

### Phase 1: calibration on thioxanthone (C1 knowledge, part 2)

| Run | Result |
|---|---|
| PBE S0 and T1 geometry optimisations (hgrid 0.35, rmult 6/9, SQNM) | E_T(PBE, adiabatic) = **236.7 kJ/mol (2.453 eV)**, −0.39 eV from the literature → **fails** the endorsed 0.2 eV window |
| PBE0 single points at the PBE geometries (4 runs) | E_T(PBE0, adiabatic) = **260.75 kJ/mol (2.702 eV)**, −0.138 eV → **passes**. Vertical absorption 273.6 kJ/mol (2.836 eV); vertical emission 238.5 kJ/mol (2.472 eV). |

The functional accounts for most of the PBE deficit: at identical geometries PBE0 adds 24 kJ/mol.

### Failures kept in the capsule

| Failure | Lesson recorded |
|---|---|
| `srun bigdft` started 12 singletons (OpenMPI 5 needs PMIx, Slurm offers only pmi2) and ran out of memory | launch with `mpirun -np $SLURM_NTASKS --map-by slot:PE=$OMP_NUM_THREADS`; check "Number of MPI tasks" at start-up |
| PBE0 jobs killed for running out of memory at 24 GB; BigDFT estimated 501 MB per process | the dry run validates hybrid inputs but **not their memory**. Measured: 30 GB (S0) and about 50 GB (T1) for thioxanthone at 8 MPI × 8 OMP |
| ASE Hookean restraints during the 6a build | cannot enforce lower bounds; replaced by a two-sided flat-bottom restraint |

### C1 contents

63 records: 15 results, 8 decisions, 3 corrections, 5 failed attempts, 9 open questions, 1 hypothesis, plus
context, evidence and procedures. 131 files (5.7 MB): structures, inputs, dry-run logs, run logs, scripts, and **21 stdlib
tests**. The tests recompute every published number from the packaged files, including 236.70, 260.75, 273.64 and 238.50
kJ/mol. Logs are redacted (install prefix only); the capsule contains no hostnames, usernames or e-mail addresses.

Open items carried in C1 (as `question` records): conformational ensemble, measurement conditions, library versions,
the 6a·ent-5a complex, PBE pseudopotentials with PBE0, the kind of the literature value (0–0 or onset), PBE0 vs PBE
geometries, T1 character (ππ* or nπ*), and zero-point/vibronic corrections. One AI decision is still unconfirmed: the
thioxanthone grid (`dec-tx-grid`).

## 3. What comes next (C2, C3, …)

| Version | Phase | Work | Notes |
|---|---|---|---|
| **C2** | 2 | 6a S1 grid convergence: 24 PBE single points (S0/T1 × hgrid 0.45–0.30 × rmult 5/8–7/10), all already dry-run validated in C1 | pick the setting where ΔE(T1−S0) changes by < 0.01 eV; also checks `dec-tx-grid` |
| C2 | 3a | 6a PBE S0 and T1 geometry optimisations. Freezing is undecided: freezing the backbone keeps the NMR turn (recommended); full relaxation risks leaving the NMR conformation, as S3 did | new inputs → dry run first; check that T1 is localised on the thioxanthone (atoms 28–42) |
| **C3** | 3b | 6a at PBE0 level | memory extrapolated from thioxanthone to roughly 400 GB or more for T1, which is **not measured**. Options: (a) a memory probe on the largest node; (b) PBE E_T(6a) + the thioxanthone PBE0−PBE shift (+24.05 kJ/mol), labelled as an approximation; (c) a larger machine (e.g. TSUBAME) |
| C3 | 3c | compare with 269 kJ/mol using the endorsed criterion (PBE0 adiabatic within ±0.15 eV of 2.79 eV) | report all levels; nothing is tuned toward 269 |
| **C4** | 4 | implicit EtOH (ε = 24.85), S3 and ensemble sensitivity, zero-point estimate, T1 character (spin density) | closes the open questions in C1 |
| C5 | 5 | constrained-DFT charge-transfer states (thioxanthone vs peptide); 6a·ent-5a complex | the original BigDFT cDFT objective |

Each version is made with `capsule-maker extend C<n> memory.json C<n+1>`. Its new records get new IDs and their own
source provenance. Superseding records get the status `superseded`; the parent capsule stays byte-identical. The rules:

1. Start from the imported capsule only.
2. Dry-run every input before any calculation.
3. Record failures, not only successes.
4. A human review precedes `approve`.

## 4. How the transfer and growth will be tested

**Portability (receiver test).** A fresh agent or developer gets only `C1.zip`, with no access to this repository's
history or the creator's sessions, and runs:

```bash
capsule-maker import C1.zip c1 && capsule-maker verify c1 --integrity-only && capsule-maker resume c1
capsule-maker verify c1 --trust-code        # only after deciding to trust the bundled code
```

Then it answers questions whose answers are in C1, including traps that plain document handoff tends to get wrong:

| Probe | Correct answer from C1 |
|---|---|
| S1−S3 GFN2 gap | 0.453 eV (the packaged README still says the superseded 0.49) |
| Thioxanthone atom indices in 6a | 0-based 28–42; S 38, O 35, C 34 |
| Did PBE pass the calibration? | no (−0.39 eV); PBE0 did (−0.138 eV) |
| How to launch BigDFT on that cluster | `mpirun …`, not `srun` (singleton failure) |
| Is the dry-run memory estimate enough for PBE0? | no; measured 30/50 GB for thioxanthone |
| Is the literature E_T of thioxanthone a primary value? | no, a secondary source; kind unknown |
| Which structure, and on whose authority? | S1, confirmed by the researcher |
| What is still open? | the 9 question records and `dec-tx-grid` |

Tasks: regenerate the inputs with `procedures/make_inputs.py` (byte-identical to the packaged ones) and recompute the
Phase 1 numbers with `procedures/analyze_phase1.py`. The control is an agent given only the paper skill.

**Growth (developer test).** Starting from the imported C1, run Phase 2 and record it as C2 with `extend`. Then
`compare C1 C2`, `verify-parent C2 C1`, approve after review, and export. A third agent given only C2 must still
answer the C1 probes and also the new Phase 2 questions.

## 5. Limitations

- The approval records a review decision. It is not peer review or proof of scientific correctness. Checksums establish
  integrity, not authenticity.
- The literature E_T of thioxanthone is from a secondary source; there is no zero-point correction; PBE0 is evaluated
  at PBE geometries; a single conformer of 6a is used.
- The cluster-specific details (module names, launcher) are recorded as observations of one site.
