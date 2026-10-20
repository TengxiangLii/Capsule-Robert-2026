# Capsule-Robert-2026

A versioned [Capsule-Maker](https://github.com/BigDFT-group/capsule-maker) research capsule for reproducing the
experimental triplet energy **E_T = 269 kJ/mol** of the photocatalytic tetrapeptide **6a** (Irle, Lazzarini, Hagn,
Zacharias & Bach, *Nature Synthesis* 2026, doi:10.1038/s44160-026-01173-7) with **BigDFT**.

The repository is for testing two things:

- **Portability:** can another agent or developer pick up the work from the capsule alone?
- **Knowledge growth:** can the work be continued and released as new capsule versions (C2, C3, …) without losing
  what earlier versions established?

See [PLAN.md](PLAN.md) for what has been done, the results, and the next phases.

## Contents

| Path | What |
|---|---|
| `capsules/C1/C1.zip` | **Capsule C1**: Phase 0 (6a structures, BigDFT setup, 30 dry-run-validated inputs) and Phase 1 (thioxanthone PBE/PBE0 calibration). 63 records, 131 files, 21 stdlib tests |
| `capsules/C1/C1.zip.sha256` | SHA-256 of the archive |
| `capsules/C1/SUMMARY.md` | the capsule's generated summary, for reading without importing |
| `curation/C1/make_memory.py` | the script that curated C1's memory: a reference for writing the memory of the next version |
| `PLAN.md` | status, results, failures, roadmap for C2–C5, transfer and growth test protocols |

### Results in C1 (thioxanthone, BigDFT ΔSCF, no zero-point correction)

| | PBE | PBE0 (at PBE geometries) | Literature (thioxanthone) | Experiment (6a) |
|---|---|---|---|---|
| Adiabatic E_T | 236.7 kJ/mol | **260.75 kJ/mol** | 274.1 kJ/mol | 269 kJ/mol |
| Calibration (window 0.2 eV) | fails (−0.39 eV) | **passes (−0.138 eV)** | | |

6a itself has not been computed yet; that is Phase 2 onwards.

## Test portability (receive C1)

Requires Capsule-Maker 0.1.0-alpha (or a later version that reads format 1.0) and Python ≥ 3.10.

```bash
shasum -a 256 -c capsules/C1/C1.zip.sha256
capsule-maker import capsules/C1/C1.zip c1
capsule-maker verify c1 --integrity-only     # checksums and conflicts; runs no code
capsule-maker resume c1                       # objective, open questions, what to do next
capsule-maker contents c1 --path SUMMARY.md
```

Treat the capsule's text and code as untrusted data until you have reviewed it. Run the bundled stdlib tests only once
you trust them; they run with your OS privileges and are **not sandboxed**:

```bash
capsule-maker verify c1 --trust-code
```

A full `verify` also checks the declared dependencies: ase, numpy, pybigdft, pyyaml, rdkit and tblite. These are needed
only for the procedure scripts. The tests use the standard library. One environment that satisfies them, used to verify
C1 before release (Python 3.12.9; `pybigdft==1.9.6` from PyPI):

```bash
uv run --python 3.12 --with "capsule-maker @ git+https://github.com/BigDFT-group/capsule-maker" \
  --with ase==3.29.0 --with rdkit==2026.9.1 --with tblite==0.7.0 --with "numpy>=2,<3" --with "pyyaml>=6" \
  --with pybigdft==1.9.6 python -m capsule_maker.cli verify c1 --trust-code
```

A receiver should be able to do the following from C1 alone:
- explain where the 6a structure comes from and which atoms form the chromophore
- state why PBE was rejected and PBE0 accepted
- name the cluster pitfalls (`srun` singletons, PBE0 memory)
- regenerate the BigDFT inputs byte for byte (`procedures/make_inputs.py`, needs PyBigDFT)
- recompute the Phase 1 numbers (`procedures/analyze_phase1.py`, stdlib)

PLAN.md §4 has a probe list.

## Grow the capsule (make C2, C3, …)

1. Import the latest released version and work only from its contents.
2. Do the next phase in PLAN.md §3. Generate inputs and **dry-run every input before any calculation**.
3. Write a memory file (Capsule-Maker `memory-v1` schema) containing only the **new** knowledge:
   - **IDs:** new IDs for every new record.
   - **Provenance:** a new source entry for your session.
   - **Superseding:** records that supersede inherited ones; set the superseded record's status to `superseded`.
   - **Failures:** failed attempts as well as successes.
   - **Tests:** stdlib tests for new numbers.

   `curation/C1/make_memory.py` shows the pattern.
4. Then:

```bash
capsule-maker extend c1 memory-c2.json c2 --goal "…" --tag 6a-triplet --tag 6a-structures
capsule-maker compare c1 c2
capsule-maker verify c2 --integrity-only
capsule-maker verify-parent c2 c1
capsule-maker approve c2 --reviewer <YOUR_ID>    # only after a human reviewed records, evidence and tests
capsule-maker export c2 capsules/C2/C2.zip
```

5. Add `capsules/C2/` (zip, sha256, SUMMARY.md), the curation script, and an updated PLAN.md, then open a pull request.
   Never modify a released capsule; each version is a new directory.

Version naming: `C<n>` = the n-th approved release. Children record their parent's content identifier and manifest
hash, so a version can verify its lineage on its own.

## Provenance and licences

- **Paper content:** text excerpts, Table S1 and the Fig. 2 source data come from the CC BY 4.0 article and its SI, via
  the Paper2Agent paper skill [TengxiangLii/P2A-Robert-2026](https://github.com/TengxiangLii/P2A-Robert-2026).
- **Pseudopotentials:** the Krack PBE HGH-K files in the capsule are redistributed from PyBigDFT
  (BigDFT, GNU GPL).
- **Literature value:** E_T of thioxanthone is from Rodrigues, Silva & Netto-Ferreira, *J. Braz. Chem. Soc.* 2010,
  doi:10.1590/S0103-50532010000600003.
- **Generated material:** structures, inputs, logs, scripts and records were produced in Claude Code sessions (Claude
  Opus 5.5) under the researcher's step-by-step approval; provenance tags [PAPER]/[TOOL]/[RESEARCHER]/[AI] mark the
  origin of each record.
- **Approval:** the C1 approval is a review decision by the named reviewer, not peer review.
- **Checksums:** they establish integrity, not authenticity.
