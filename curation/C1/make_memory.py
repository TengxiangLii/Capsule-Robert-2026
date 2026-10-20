"""Write source/memory.json (Capsule-Maker memory-v1) for capsule C1, step 1: 6a structures and the E_T target."""
import json
from pathlib import Path

ROOT_INPUTS = sorted(p.name for p in (Path(__file__).parent / "source/bigdft/inputs").iterdir())
ROOT_DRY = sorted(p.name for p in (Path(__file__).parent / "source/bigdft/dryrun").iterdir())
_R = Path(__file__).parent / "source"
DRY0 = sorted(f"bigdft/dryrun_pbe0/{p.name}" for p in (_R / "bigdft/dryrun_pbe0").iterdir())
RUN_FILES = sorted(str(p.relative_to(_R)) for p in (_R / "bigdft/runs").rglob("*") if p.is_file())

SRC = Path(__file__).parent / "source"
T, ET = "6a-structures", "6a-triplet"
SESSION = ["session-structures"]
CUR = ["session-curation"]

sources = [
    dict(id="paper", uri="https://doi.org/10.1038/s44160-026-01173-7",
         description="Irle, Lazzarini, Hagn, Zacharias & Bach, Photocatalytic tetrapeptides for enantioselective visible "
                     "light-induced transformations, Nature Synthesis (2026); CC BY 4.0"),
    dict(id="si", uri="https://doi.org/10.1038/s44160-026-01173-7",
         description="Supplementary Information of the paper (general methods, S4 NMR, Table S1 restraints)"),
    dict(id="chemotion-6a", uri="https://doi.org/10.14272/WQGGCBKETYIIRM-BHIFYINESA-N.2",
         description="Chemotion Repository molecule record of 6a (SMILES/InChI), collection 10.14272/collection/RMI_2026-01-30"),
    dict(id="paper-skill", uri="https://github.com/TengxiangLii/P2A-Robert-2026/tree/bc704b2",
         description="Paper2Agent paper skill irle2026-tetrapeptide-photocatalysis-paper, commit bc704b2 "
                     "(strict verify: reviewed_with_limitations); paper-only, no MCP server"),
    dict(id="session-structures", uri="claude-code-session:b8d95464-d0d1-43eb-b855-93baccca4203",
         description="Claude Code session (Claude Opus 5.5), 2026-10-15 08:46-09:00 UTC, in which the 6a structures were "
                     "built; tool-call IDs in evidence/run_log.md; transcript retained by the researcher, not packaged"),
    dict(id="session-curation", uri="claude-code-session:e3e745d8-25c4-4f71-9ca9-1ce91da60329",
         description="Claude Code session (Claude Opus 5.5), 2026-10-20, that curated this capsule from the primary "
                     "sources and re-derived energies, indices and hashes from the packaged files"),
    dict(id="researcher-request", uri="claude-code-session:e3e745d8-25c4-4f71-9ca9-1ce91da60329#request",
         description="Researcher's objective: build a capsule from the agentified paper, BigDFT skills and Capsule-Maker, "
                     "and reproduce the experimental E_T = 269 kJ/mol of 6a with BigDFT; endorsements and the dry-run "
                     "requirement given in the same session on 2026-10-20"),
    dict(id="jbcs2010", uri="https://doi.org/10.1590/S0103-50532010000600003",
         description="Rodrigues, Silva & Netto-Ferreira, Laser flash photolysis study of the photochemistry of thioxanthone "
                     "in organic solvents, J. Braz. Chem. Soc. 21 (2010); open access; secondary source for E_T(TX)"),
    dict(id="bigdft-skills", uri="https://github.com/BigDFT-group",
         description="Installed BigDFT agent skills (bigdft-skills 0.12.1: input, pseudopotentials, logfile) consulted "
                     "for input keys, pseudopotential families and the dry-run mechanism"),
]

PK = {"pybigdft": "pybigdft>=1.9.6,<1.10", "pyyaml": "pyyaml>=6", "rdkit": "rdkit>=2026.9.1,<2027", "ase": "ase>=3.29,<3.30", "tblite": "tblite>=0.7,<0.8", "numpy": "numpy>=2,<3"}
artifacts = [
    ("structures/build_6a.py", "procedure", ["rdkit"]),
    ("structures/relax_xtb.py", "procedure", ["rdkit", "ase", "tblite", "numpy"]),
    ("structures/6a_nmr_gfn2_ch2cl2_restrained.xyz", "data", []),
    ("structures/6a_nmr_gfn2_ch2cl2_restrained.mol", "data", []),
    ("structures/6a_nmr_restrained_mmff.xyz", "data", []),
    ("structures/6a_nmr_restrained_mmff.mol", "data", []),
    ("structures/6a_nmr_gfn2_ch2cl2.xyz", "data", []),
    ("structures/6a_nmr_gfn2_ch2cl2.mol", "data", []),
    ("structures/6a_nmr_gfn2_ch2cl2_restrained.log", "evidence", []),
    ("structures/6a_nmr_gfn2_ch2cl2.log", "evidence", []),
    ("structures/README.md", "instructions", []),
    ("data/table_s1_noe_restraints.csv", "data", []),
    ("data/6a_chemotion_molecule_record.csv", "data", []),
    ("data/source_data_fig2_6a_photophysics.csv", "data", []),
    ("evidence/paper_excerpts.md", "evidence", []),
    ("evidence/run_log.md", "evidence", []),
    ("procedures/to_plain_xyz.py", "procedure", []),
    ("procedures/build_thioxanthone.py", "procedure", ["rdkit", "ase", "tblite", "numpy"]),
    ("bigdft/6a_S1.xyz", "data", []),
    ("bigdft/6a_S3.xyz", "data", []),
    ("bigdft/thioxanthone_gfn2.xyz", "data", []),
    ("bigdft/thioxanthone_gfn2.log", "evidence", []),
    *[(f"bigdft/psppar/psppar.{e}.yaml", "data", []) for e in "CHNOS"],
    ("procedures/make_inputs.py", "procedure", ["pybigdft", "pyyaml"]),
    ("procedures/dry_run.py", "procedure", ["pybigdft", "pyyaml"]),
    ("procedures/run_bigdft.slurm", "procedure", []),
    *[(f"bigdft/inputs/{n}", "data", []) for n in ROOT_INPUTS],
    *[(f"bigdft/dryrun/{n}", "evidence", []) for n in ROOT_DRY],
    ("evidence/literature_thioxanthone.md", "evidence", []),
    ("procedures/analyze_phase1.py", "procedure", []),
    *[(f, "evidence", []) for f in RUN_FILES],
    *[(f, "evidence", []) for f in DRY0],
    ("tests/test_structures.py", "test", []),
]
INPUTS = [f"bigdft/inputs/{n}" for n in ROOT_INPUTS]
DRY = [f"bigdft/dryrun/{n}" for n in ROOT_DRY]
PSP = [f"bigdft/psppar/psppar.{e}.yaml" for e in "CHNOS"]
BD = ["bigdft/6a_S1.xyz", "bigdft/6a_S3.xyz"]
TX = ["bigdft/thioxanthone_gfn2.xyz", "bigdft/thioxanthone_gfn2.log", "procedures/build_thioxanthone.py"]
S1 = ["structures/6a_nmr_gfn2_ch2cl2_restrained.xyz", "structures/6a_nmr_gfn2_ch2cl2_restrained.mol",
      "structures/6a_nmr_gfn2_ch2cl2_restrained.log"]
S2 = ["structures/6a_nmr_restrained_mmff.xyz", "structures/6a_nmr_restrained_mmff.mol"]
S3 = ["structures/6a_nmr_gfn2_ch2cl2.xyz", "structures/6a_nmr_gfn2_ch2cl2.mol", "structures/6a_nmr_gfn2_ch2cl2.log"]


def rec(id, kind, status, content, tags=(T,), references=(), evidence=(), arts=(), prov=SESSION,
        supersedes=(), contradicts=(), claim_key=None):
    r = dict(id=id, kind=kind, status=status, content=content, tags=list(tags), references=list(references),
             evidence=list(evidence), artifacts=list(arts), provenance=list(prov), supersedes=list(supersedes),
             contradicts=list(contradicts), sensitive=False)
    if claim_key:
        r["claim_key"] = claim_key
    return r


records = [
    # ---- evidence ----
    rec("ev-paper", "evidence", "verified",
        "[PAPER] Verbatim excerpts E1-E13 of the paper and SI from the paper skill (with line numbers): E_T 269 kJ/mol "
        "from the 77 K EtOH phosphorescence inflection point, 383 nm absorption, comparison with parent thioxanthone "
        "(ref. 36), luminescence method, NMR conditions, restraint bounds, Xplor-NIH bundle, type II' turn, substrate "
        "complex, data availability. Table S1, the Chemotion 6a record and the Fig. 2 source data are packaged as CSV.",
        tags=(T, ET), arts=["evidence/paper_excerpts.md", "data/table_s1_noe_restraints.csv",
                            "data/6a_chemotion_molecule_record.csv", "data/source_data_fig2_6a_photophysics.csv"],
        prov=["paper", "si", "chemotion-6a", "paper-skill"]),
    rec("ev-runlog", "evidence", "verified",
        "[TOOL] Chronological run log (42 steps) of the structure construction with tool-call IDs, commands, printed "
        "metrics and outcomes, plus the two BFGS logs of the GFN2-xTB relaxations; steps 19-42 re-derived or run at curation.",
        arts=["evidence/run_log.md", "structures/6a_nmr_gfn2_ch2cl2_restrained.log", "structures/6a_nmr_gfn2_ch2cl2.log"],
        prov=SESSION + CUR),
    rec("ev-structures", "evidence", "verified",
        "[TOOL] The three 6a geometries (S1, S2, S3) as XYZ and MOL with their generating scripts; SHA-256, composition "
        "C31H34N4O7S, thioxanthone indices and the S1-S3 energy difference are checked by tests/test_structures.py "
        "plus the BigDFT-ready plain XYZ copies and the thioxanthone geometry (stdlib, 21 tests, passing at curation).",
        tags=(T, ET), arts=S1 + S2 + S3 + BD + TX[:2] + ["structures/build_6a.py", "structures/relax_xtb.py",
                                                          "tests/test_structures.py"],
        prov=SESSION + CUR),

    # ---- context ----
    rec("ctx-request", "context", "verified",
        "[RESEARCHER] Objective of this capsule: reproduce the experimental triplet energy E_T = 269 kJ/mol of catalyst 6a "
        "with BigDFT, starting from the agentified paper (Paper2Agent skill), the BigDFT agent skills and Capsule-Maker. "
        "Earlier questions that produced the structures: whether the authors give optical excitation energies, and "
        "obtaining 6a 'in a position good for the simulation of excitation'.",
        tags=(T, ET), evidence=["ev-runlog"], prov=["researcher-request"] + SESSION),
    rec("ctx-paper", "context", "verified",
        "[PAPER] 6a = (R,R,S)-Pga-Pro-Aib-pTxa-OMe, C31H34N4O7S, <750 Da. N-terminal pyroglutamic acid binds lactam "
        "substrates by two H-bonds; the C-terminal pTxa thioxanthone absorbs visible light and sensitises by triplet "
        "energy transfer. NMR (33 ROE restraints, 233 K, CD2Cl2, Xplor-NIH; 10-structure bundle, heavy-atom r.m.s.d. "
        "0.22 A) gives a type II' beta-turn with a pTxa NH...O=C Pga H-bond and the thioxanthone above the turn.",
        evidence=["ev-paper"], prov=["paper", "si", "paper-skill"]),
    rec("ctx-target", "context", "verified",
        "[PAPER] Experimental target: E_T(6a) = 269 kJ/mol, from the inflection point of the 77 K phosphorescence spectrum "
        "in EtOH (Fig. 2, main text; FluoroMax-4P, 0.1 ms delay). Longest-wavelength absorption 383 nm, epsilon 5,700 "
        "M-1 cm-1 (EtOH). The paper attributes both to the thioxanthone in pTxa and calls them comparable to parent "
        "9H-thioxanthen-9-one (ref. 36, Nikitas et al., Org. Biomol. Chem. 19, 5237 (2021)). The paper gives no "
        "photophysical data for other catalysts or substrates. [AI conversion] 269 kJ/mol = 2.788 eV; 383 nm = 3.24 eV.",
        tags=(T, ET), evidence=["ev-paper"], prov=["paper", "si", "paper-skill"], claim_key="et-exp"),
    rec("ctx-phos-data", "context", "verified",
        "[PAPER] Fig. 2 source data are packaged: UV/Vis (700-200 nm) and 77 K phosphorescence (400-650 nm), both "
        "normalized. The 'Steady state rt' emission column is a source defect (it normalizes the wavelength column) and "
        "carries no emission data. The phosphorescence curve permits an independent re-derivation of the onset energy.",
        tags=(T, ET), evidence=["ev-paper"], arts=["data/source_data_fig2_6a_photophysics.csv"],
        prov=["paper", "paper-skill"]),
    rec("ctx-p2a", "context", "verified",
        "[TOOL] The paper has no code repository, so Paper2Agent produced a paper-only skill (no MCP server); it was "
        "used for reading and searching the paper and SI. Structures were computed with RDKit, ASE and tblite via uv.",
        tags=(T, ET), evidence=["ev-paper", "ev-runlog"], prov=["paper-skill"] + SESSION),

    # ---- decisions ----
    rec("dec-rebuild", "decision", "verified",
        "[TOOL+AI] The authors deposited no coordinates (no PDB/BMRB; Chemotion has SMILES/spectra only), so 6a was "
        "rebuilt from the Chemotion SMILES and fitted to Table S1 restraints 1-33 plus the reported type II' turn.",
        evidence=["ev-paper", "ev-runlog"], prov=SESSION + ["chemotion-6a", "si"]),
    rec("dec-bounds", "decision", "verified",
        "[PAPER-supported AI interpretation] Table S1 'Lower/Upper bound' columns are deviations from the calculated "
        "distance: bounds = d_calc - lower and d_calc + upper (SI: 'lower and upper error bounds of 0.2 and 0.5 A').",
        evidence=["ev-paper"], prov=["si"] + SESSION),
    rec("hyp-group-min", "hypothesis", "hypothesis",
        "[AI] Methyl and CH2 groups are treated by the minimum distance over group members (r^-6 dominated); the "
        "unreported pro-S/pro-R methyl and Pro H-beta assignments are resolved by taking the best of 4 assignment sets "
        "(set 1 chosen). The authors' Xplor-NIH averaging may differ.",
        references=["dec-bounds"], evidence=["ev-runlog"], arts=["structures/build_6a.py"]),
    rec("dec-state", "decision", "verified",
        "[AI] 6a is treated as an isolated neutral closed-shell singlet (charge 0, 77 atoms, all 34 H explicit); "
        "coordinates in Angstrom.",
        tags=(T, ET), evidence=["ev-structures"]),

    # ---- procedure ----
    rec("proc-generation", "procedure", "verified",
        "[TOOL] build_6a.py: RDKit ETKDGv3 (seed 20261015, 600 attempts, prune 0.3 A) -> MMFF94 -> score vs Table S1 + "
        "turn H-bond -> best conformer refined with flat-bottom MMFF distance restraints (k 50), H-bond 1.8-2.5 A and "
        "II' torsion windows -> S2. relax_xtb.py: GFN2-xTB/ALPB(CH2Cl2), ASE BFGS fmax 0.02 eV/A; default mode applies "
        "FlatBottom restraints (k 2.5 eV/A^2) -> S1; '--free' -> unrestrained (S3 was made by an earlier version "
        "without restraint code that ran the same calculation). Versions: rdkit 2026.9.1, tblite 0.7.0, ase 3.29.0.",
        references=["dec-rebuild", "dec-bounds", "hyp-group-min"], evidence=["ev-runlog", "ev-structures"],
        arts=["structures/build_6a.py", "structures/relax_xtb.py", "structures/README.md"]),

    # ---- results and history ----
    rec("res-mmff-v1", "result", "superseded",
        "[TOOL] First MMFF refinement (cid 82 of 569): max violation 0.22 A, H...O 2.38 A, but Aib phi/psi -162/29, "
        "not a type II' turn.", evidence=["ev-runlog"]),
    rec("cor-turn", "correction", "verified",
        "[AI decision] Because the paper reports a type II' turn and Aib phi = -162 deg is far from ideal (-80), ideal II' "
        "torsion windows (Pro 60/-120, Aib -80/0, +/-30 deg) were added to the MMFF refinement.",
        references=["ctx-paper"], evidence=["ev-runlog"], supersedes=["res-mmff-v1"]),
    rec("res-s2", "result", "verified",
        "[TOOL] S2 (6a_nmr_restrained_mmff): MMFF94 with NOE and II' torsion restraints; max violation 0.24 A, none "
        "> 0.3 A; Pro 71/-126, Aib -89/15; H...O 2.41 A; E_MMFF 122.09 kcal/mol (+1.57 vs v1). Start for xTB runs. "
        "Plain 4-column XYZ.", references=["cor-turn", "proc-generation"], evidence=["ev-runlog", "ev-structures"], arts=S2),
    rec("res-s3", "result", "verified",
        "[TOOL] S3 (6a_nmr_gfn2_ch2cl2): unrestrained GFN2-xTB/ALPB(CH2Cl2) from S2, 237 BFGS steps, E = -3465.1108 eV. "
        "Turn kept (53/-141, -84/21) but the pTxa side chain rotates (chi1 -41 -> -61 deg); 8 restraints violated by "
        "> 0.3 A (max 1.40 A; ids 5, 6, 10, 13, 16, 19, 22, 27). Nearest local minimum; reference only, not an NMR model.",
        tags=(T, ET), references=["res-s2"], evidence=["ev-runlog", "ev-structures"], arts=S3),
    rec("fail-hookean", "failed_attempt", "verified",
        "[TOOL] Restraining xTB with ASE Hookean springs at the Table S1 upper bounds (k 5) failed: max violation 1.49 A, "
        "6 > 0.3 A, all too SHORT (ids 5, 6, 11, 13, 15, 22), because Hookean acts only above rt and cannot enforce lower "
        "bounds. Replaced by a two-sided FlatBottom constraint. Do not reuse Hookean for this.",
        evidence=["ev-runlog"]),
    rec("res-s1", "result", "verified",
        "[TOOL] S1 (6a_nmr_gfn2_ch2cl2_restrained): GFN2-xTB/ALPB(CH2Cl2) with two-sided flat-bottom Table S1 restraints "
        "(k 2.5 eV/A^2), 176 BFGS steps. Max violation 0.07 A, none > 0.3 A; type II' turn Pro 56/-126, Aib -81/1; "
        "NH...O 2.02 A; thioxanthone plane r.m.s. 0.155 A, C9=O 1.230 A. Electronic energy -3464.6577 eV (sum of the "
        "per-atom column); the BFGS log value -3464.6176 eV includes +0.040 eV restraint penalty.",
        tags=(T, ET), references=["res-s2", "fail-hookean", "proc-generation"], evidence=["ev-runlog", "ev-structures"],
        arts=S1),
    rec("res-strain-old", "result", "superseded",
        "[TOOL] S1 lies 0.49 eV (11.4 kcal/mol) above S3 (session value, also stated in structures/README.md).",
        references=["res-s1", "res-s3"], evidence=["ev-runlog"], claim_key="gap-s1-s3"),
    rec("cor-strain", "correction", "verified",
        "[TOOL, curation] The 0.49 eV figure used the penalty-inclusive energy. The GFN2 electronic difference S1 - S3 "
        "is 0.453 eV (10.4 kcal/mol): -3464.6577 vs -3465.1108 eV from the per-atom energy columns. structures/README.md "
        "is packaged unchanged and still says 0.49 eV.",
        references=["res-s1", "res-s3"], evidence=["ev-structures", "ev-runlog"], arts=["structures/README.md"],
        prov=CUR, supersedes=["res-strain-old"], claim_key="gap-s1-s3"),
    rec("res-index-old", "result", "superseded",
        "[TOOL] First README draft: thioxanthone = C28-C45, S43.", evidence=["ev-runlog"], claim_key="tx-indices"),
    rec("cor-index", "correction", "verified",
        "[TOOL] Thioxanthone atoms are 0-based indices 28-42 (1-based 29-43): S 38, O 35, carbonyl C 34; pTxa C-beta 27 "
        "bonded to ring C2 (28); ring C1 is 33. Identical in S1, S2 and S3 (43 heavy atoms first, then 34 H).",
        tags=(T, ET), evidence=["ev-structures", "ev-runlog"], arts=["structures/README.md"],
        prov=SESSION + CUR, supersedes=["res-index-old"], claim_key="tx-indices"),
    rec("res-format", "result", "verified",
        "[TOOL] S1 and S3 .xyz are 9-column extended XYZ (element, x, y, z, per-atom energy, 3 forces, charge); S2 .xyz "
        "is plain 4-column. Strict readers (e.g. BigDFT) need the extra columns stripped; the .mol files carry the "
        "same coordinates with bonds.",
        tags=(T, ET), evidence=["ev-structures"], arts=S1[:1] + S3[:1] + S2[:1], prov=CUR),
    rec("dec-select", "decision", "unverified",
        "[AI recommendation, not yet confirmed by the researcher] Use S1 as the starting geometry for excitation and "
        "triplet calculations: the only structure satisfying all Table S1 restraints and the II' turn at an "
        "electronic-structure level. Use S3 as a sensitivity check for chromophore placement; S2 is a force-field "
        "intermediate. A free DFT re-optimisation would drift out of the NMR conformation as S3 did, so freeze or "
        "restrain the backbone.",
        tags=(T, ET), references=["res-s1", "res-s3", "res-s2"], evidence=["ev-structures"]),

    # ---- BigDFT preparation (step 0.3) ----
    rec("res-plain-xyz", "result", "verified",
        "[TOOL] BigDFT-ready plain 4-column XYZ (Angstrom) of S1 and S3: bigdft/6a_S1.xyz and bigdft/6a_S3.xyz, made by "
        "procedures/to_plain_xyz.py (stdlib), which copies the coordinate tokens verbatim (identity checked by test). "
        "Same atom order as structures/, so the thioxanthone is atoms 28-42.",
        tags=(T, ET), references=["res-format", "cor-index", "res-s1", "res-s3"], evidence=["ev-structures"],
        arts=BD + ["procedures/to_plain_xyz.py"], prov=CUR),
    rec("dec-calibration", "decision", "unverified",
        "[AI proposal] Use parent 9H-thioxanthen-9-one as a calibration system for the BigDFT triplet protocol, because "
        "the paper calls the photophysics of 6a comparable to it (ref. 36). Its experimental E_T must be retrieved "
        "from the literature (ref. 36 or primary data), not recalled. Awaits the researcher's endorsement.",
        tags=(ET,), references=["ctx-target"], evidence=["ev-paper"], prov=CUR),
    rec("res-thioxanthone", "result", "verified",
        "[TOOL] Thioxanthone C13H8OS (23 atoms) built from SMILES O=C1c2ccccc2Sc2ccccc21 by procedures/"
        "build_thioxanthone.py: RDKit ETKDGv3 (seed 20261020) -> MMFF94 -> gas-phase GFN2-xTB BFGS (fmax 0.01 eV/A, 23 "
        "steps), E = -1067.0693 eV; planar (heavy-atom plane r.m.s. 0.0000 A), C9=O 1.222 A. Pre-optimisation only. "
        "Environment: Python 3.12.9, numpy 2.5.0, rdkit 2026.09.1, ase 3.29.0, tblite 0.7.0.",
        tags=(ET,), references=["dec-calibration"], evidence=["ev-structures", "ev-runlog"], arts=TX, prov=CUR),
    rec("q-tx-lit", "question", "unresolved",
        "Partly answered by res-tx-lit (secondary source, 274.1 kJ/mol). Still open: the primary measurement (Dalton & "
        "Turro 1971; Dalton & Montgomery 1974) and paper ref. 36 were not accessed, so the method, temperature and "
        "whether the value is a 0-0 or an onset energy are unconfirmed.",
        tags=(ET,), references=["dec-calibration"], evidence=["ev-paper"], prov=CUR),

    # ---- BigDFT environment and pseudopotentials (step 0.4) ----
    rec("ctx-env", "context", "verified",
        "[TOOL] Compute environment for the BigDFT runs: BigDFT module build with libbigdft 1.9.5, PSolver 1.10, futile "
        "1.9, libxc 4.3.4 (hybrids such as PBE0 available), CHESS 0.2.4, OpenMPI 5.0.7; Slurm CPU cluster, AMD EPYC 7713 "
        "(Zen3), 64-128 cores per node, no GPUs. The BigDFT module does not provide PyBigDFT; PyBigDFT 1.9.6 is available "
        "on the cluster in a user conda environment and locally. bigdft-tool needs a 'python' on PATH and BIGDFT_ROOT "
        "pointing at the BigDFT bin directory.",
        tags=(ET,), evidence=["ev-runlog"], prov=CUR),
    rec("dec-psp", "decision", "unverified",
        "[AI proposal, awaiting the researcher's endorsement] Use the Goedecker-Krack PBE HGH-K pseudopotentials (PyBigDFT "
        "Database/psppar/Krack/PBE, XC 11) for all elements: C 4, H 1, N 5, O 6, S 6 valence electrons, giving 226 "
        "electrons (113 doubly occupied orbitals) for 6a and 72 (36) for thioxanthone. Reason: one consistent family; the "
        "HGH-K+NLCC 'SS' set lacks S. The same PBE pseudopotentials would be used for PBE0, a standard approximation.",
        tags=(ET,), references=["ctx-env", "dec-state"], evidence=["ev-runlog", "ev-structures"], arts=PSP, prov=CUR),
    rec("fail-psp-api", "failed_attempt", "verified",
        "[TOOL] PyBigDFT 1.9.6 Inputfile.set_psp_krack('PBE', elements=[...]) and set_psp_nlcc(elements=[...]) silently "
        "load nothing: set_psp_directory matches psp.endswith(element), but the files are named psppar.X.yaml. "
        "Workaround: set_psp_file(filename='.../psppar.X.yaml', element='X') per element, then check that every "
        "psppar.X key is present and the electron count is 226 (6a) or 72 (thioxanthone).",
        tags=(ET,), references=["dec-psp"], evidence=["ev-runlog"], prov=CUR),
    # ---- researcher endorsements, inputs and dry run (step 0.5) ----
    rec("dec-select-ok", "decision", "verified",
        "[RESEARCHER, 2026-10-20] Confirmed: S1 is the starting geometry for the triplet calculations; S3 serves as the "
        "sensitivity check for chromophore placement.",
        tags=(T, ET), references=["res-s1", "res-s3"], evidence=["ev-structures"], prov=["researcher-request"],
        supersedes=["dec-select"]),
    rec("dec-calibration-ok", "decision", "verified",
        "[RESEARCHER, 2026-10-20] Confirmed: calibrate the Delta-SCF triplet protocol on parent thioxanthone before 6a.",
        tags=(ET,), references=["res-thioxanthone"], evidence=["ev-paper"], prov=["researcher-request"],
        supersedes=["dec-calibration"]),
    rec("dec-psp-ok", "decision", "verified",
        "[RESEARCHER, 2026-10-20] Confirmed: Goedecker-Krack PBE HGH-K pseudopotentials for C, H, N, O and S "
        "(226 electrons for 6a, 72 for thioxanthone).",
        tags=(ET,), references=["ctx-env"], evidence=["ev-structures"], arts=PSP, prov=["researcher-request"],
        supersedes=["dec-psp"]),
    rec("dec-dryrun-first", "decision", "verified",
        "[RESEARCHER, 2026-10-20] Every BigDFT input must first pass a dry run (PyBigDFT SystemCalculator(dry_run=True), "
        "i.e. bigdft-tool memory estimation without SCF). If any input gives an error, no calculation is performed.",
        tags=(ET,), evidence=["ev-runlog"], prov=["researcher-request"]),
    rec("proc-inputs", "procedure", "verified",
        "[TOOL] procedures/make_inputs.py (PyBigDFT 1.9.6) writes 26 self-contained YAML inputs (dft + geopt + embedded "
        "Angstrom posinp + psppar from bigdft/psppar via set_psp_file) and index.json. Common: ixc PBE, free boundary "
        "conditions, gnrm_cv 1e-5. T1 = spin_polarize(mpol=2) -> nspin 2, mpol 2. Phase 1: tx_S0/T1_pbe_geopt, hgrid "
        "0.35 bohr, rmult (6, 9), SQNM, 300 steps, betax 1.0, forcemax 2e-4 Ha/bohr. Phase 2: 6a S1 S0/T1 single points "
        "at hgrid 0.45/0.40/0.35/0.30 x rmult (5,8)/(6,9)/(7,10). Phase 1b: thioxanthone PBE0 single points "
        "tx_{S0,T1}_pbe0_at_{S0,T1}pbe at the converged PBE geometries (hgrid 0.35, rmult (6, 9)). Output is "
        "deterministic (regenerated byte-identical). "
        "procedures/dry_run.py runs SystemCalculator(dry_run=True) on a directory of inputs and writes a summary; "
        "procedures/run_bigdft.slurm runs one input (mpirun -np $SLURM_NTASKS --map-by slot:PE=$OMP_NUM_THREADS bigdft -n NAME).",
        tags=(ET,), references=["dec-psp-ok", "fail-psp-api", "res-plain-xyz", "res-thioxanthone"],
        evidence=["ev-runlog"], arts=["procedures/make_inputs.py", "procedures/dry_run.py", "procedures/run_bigdft.slurm"] + INPUTS, prov=CUR),
    rec("dec-tx-grid", "decision", "unverified",
        "[AI choice] Thioxanthone geometry optimisations use hgrid 0.35 bohr and rmult (6, 9), chosen as a "
        "conservative grid before the 6a convergence study; it is to be checked against that study.",
        tags=(ET,), references=["proc-inputs"], prov=CUR),
    rec("fail-dryrun-env", "failed_attempt", "verified",
        "[TOOL] The first dry-run attempts failed for environment reasons, not input errors: PyBigDFT rejects an "
        "absolute run_dir ('must be a sub-directory'), and bigdft-tool (#!/usr/bin/env python) found no python on the "
        "cluster PATH. Fixed by a relative run_dir in dry_run.py and by putting the conda env with PyBigDFT first on "
        "PATH; BIGDFT_ROOT must be the BigDFT bin directory.",
        tags=(ET,), references=["ctx-env"], evidence=["ev-runlog"], arts=["procedures/dry_run.py"], prov=CUR),
    rec("fail-srun", "failed_attempt", "verified",
        "[TOOL] Launching BigDFT with srun on this cluster fails: OpenMPI 5 needs PMIx, Slurm offers only pmi2, so srun "
        "starts N independent single-process copies ('12 singletons'), which overwrite each other's logs and run out of "
        "memory (first Phase 1 submission, cancelled after 42 s, no results). Use mpirun -np $SLURM_NTASKS --map-by "
        "slot:PE=$OMP_NUM_THREADS inside the Slurm allocation, and check 'Number of MPI tasks' in the log at start-up.",
        tags=(ET,), references=["ctx-env", "proc-inputs"], evidence=["ev-runlog"], arts=["procedures/run_bigdft.slurm"],
        prov=CUR),
    rec("res-dryrun", "result", "verified",
        "[TOOL] Dry run of all 26 inputs on the cluster (bigdft-tool memory estimation, no SCF): 26/26 passed, no "
        "errors. Electrons 226 (6a) / 72 (thioxanthone). T1 inputs are read as collinear nspin 2, mpol 2, all orbitals "
        "singly occupied. Pseudopotentials come from the given files. Serial memory-peak estimates: 6a S0 4.4 "
        "(h0.45 r5-8) to 24.1 GB (h0.30 r7-10), T1 8.8-47.9 GB; thioxanthone S0 2.0 GB, T1 4.0 GB. Grids from "
        "84x72x79 to 146x128x139 points. The up/down orbital split is not printed in a dry run and must be checked in "
        "the first real log.",
        tags=(ET,), references=["proc-inputs", "dec-dryrun-first"], evidence=["ev-runlog"], arts=DRY, prov=CUR),
    rec("res-tx-lit", "result", "verified",
        "[LITERATURE, secondary] E_T(thioxanthone) = 65.5 kcal/mol (274.1 kJ/mol, 2.840 eV) in hydroxylic solvents, as "
        "stated by Rodrigues et al., J. Braz. Chem. Soc. 2010, citing Dalton & Turro 1971 and Dalton & Montgomery 1974. "
        "That is 5 kJ/mol (0.05 eV) above E_T(6a) = 269 kJ/mol, consistent with the paper's 'comparable'.",
        tags=(ET,), references=["dec-calibration-ok", "ctx-target"], evidence=["ev-lit-tx"], prov=["jbcs2010"] + CUR),
    rec("ev-lit-tx", "evidence", "verified",
        "[LITERATURE] Quoted excerpts and references for the thioxanthone triplet energy, with what could not be "
        "retrieved (paper ref. 36, primary 1971/1974 measurements).",
        tags=(ET,), arts=["evidence/literature_thioxanthone.md"], prov=["jbcs2010"] + CUR),

    # ---- Phase 1: thioxanthone PBE (step 1) ----
    rec("dec-criteria", "decision", "unverified",
        "[AI, from the study plan; not explicitly endorsed] Pre-registered criteria: the calibration on thioxanthone passes "
        "if the protocol is within 0.2 eV of the literature E_T; 6a counts as reproduced if the PBE0 adiabatic Delta-SCF "
        "E_T is within +/-0.15 eV (+/-15 kJ/mol) of 2.79 eV. All levels are reported; nothing is tuned toward 269 kJ/mol.",
        tags=(ET,), references=["ctx-target", "res-tx-lit"], prov=CUR),
    rec("dec-criteria-ok", "decision", "verified",
        "[RESEARCHER, 2026-10-20] Endorsed: calibration passes within 0.2 eV of the literature E_T of thioxanthone; 6a "
        "is reproduced if the PBE0 adiabatic Delta-SCF E_T is within +/-0.15 eV of 2.79 eV.",
        tags=(ET,), references=["ctx-target", "res-tx-lit"], evidence=["ev-runlog"], prov=["researcher-request"],
        supersedes=["dec-criteria"]),
    rec("res-dryrun-pbe0", "result", "verified",
        "[TOOL] Dry run of the 4 thioxanthone PBE0 inputs: 4/4 passed, 72 electrons; read as ixc -406 'PBEH (PBE0)', exact "
        "exchange parallelised with OP2P; serial memory estimates 2.0 GB (S0) and 4.0 GB (T1). The only warning is "
        "'PSP generated with a different XC' (PBE pseudopotentials with PBE0). No errors.",
        tags=(ET,), references=["proc-inputs", "dec-dryrun-first", "q-hybrid-psp"], evidence=["ev-runlog"], arts=DRY0,
        prov=CUR),
    rec("fail-pbe0-oom", "failed_attempt", "verified",
        "[TOOL] First PBE0 submission (4 thioxanthone single points, 16 MPI x 2 OMP, 24 GB per job) was OOM-killed after "
        "about 8 min, in the input guess and before the first SCF iteration; MaxRSS 23-25 GB per job, no results. BigDFT's "
        "own estimate was 501 MB per process (about 8 GB per job): the dry-run memory estimate does not include "
        "exact-exchange memory, so a dry run validates hybrid inputs but not their memory. PBE0 memory must be measured "
        "before sizing jobs.",
        tags=(ET,), references=["res-dryrun-pbe0", "dec-dryrun-first"], evidence=["ev-runlog"], prov=CUR),
    rec("res-tx-pbe", "result", "verified",
        "[TOOL] Thioxanthone, BigDFT 1.9.5 PBE, Krack PBE pseudopotentials, free BC, hgrid 0.35 bohr, rmult (6, 9), "
        "gnrm 1e-5, SQNM geopt from the GFN2 geometry: S0 E = -104.958932176445 Ha (converged at iteration 25, Fmax "
        "1.21e-4 Ha/bohr); T1 (nspin 2, mpol 2, magnetization 2.000) E = -104.868778644431 Ha (iteration 30, Fmax 6.63e-5). "
        "Adiabatic Delta-SCF E_T = 0.09015353 Ha = 2.4532 eV = 236.70 kJ/mol. T1 vs S0: C9=O 1.2355 -> 1.2867 A, C9-C(ring) "
        "1.483 -> 1.453 A, C-S 1.742 -> 1.731 A; both planar. No zero-point correction. Jobs 211185/211186, 12 MPI x 4 "
        "OMP; inputs byte-identical to the dry-run-validated files.",
        tags=(ET,), references=["proc-inputs", "res-dryrun", "dec-calibration-ok", "dec-psp-ok", "fail-srun"],
        evidence=["ev-runlog", "ev-phase1"], arts=["procedures/analyze_phase1.py", "bigdft/runs/phase1_summary.json"],
        prov=CUR, claim_key="tx-et-pbe"),
    rec("ev-phase1", "evidence", "verified",
        "[TOOL] Packaged Phase 1 runs: inputs as run, BigDFT logs (install prefix redacted), geopt.mon, final geometries, "
        "timing files, Slurm outputs, and phase1_summary.json from procedures/analyze_phase1.py (stdlib).",
        tags=(ET,), arts=RUN_FILES, prov=CUR),
    rec("res-tx-calib-pbe", "result", "verified",
        "[TOOL] Calibration check, PBE: 236.70 kJ/mol (2.453 eV) vs literature 274.1 kJ/mol (2.840 eV) for thioxanthone: "
        "-37.4 kJ/mol (-0.39 eV), outside the 0.2 eV calibration window. PBE alone does not pass the calibration.",
        tags=(ET,), references=["res-tx-pbe", "res-tx-lit", "dec-criteria"], evidence=["ev-phase1", "ev-lit-tx"], prov=CUR),
    rec("hyp-pbe-underestimate", "hypothesis", "hypothesis",
        "[AI interpretation, untested] The PBE deficit is attributed to the semilocal functional (self-interaction error "
        "lowers the open-shell triplet); the planned PBE0 single points at the PBE S0/T1 geometries should raise E_T. "
        "Other contributions (grid, zero-point energy, solvent, the literature value being an onset or 0-0 energy) are "
        "not yet separated.",
        tags=(ET,), references=["res-tx-calib-pbe", "q-tx-lit", "q-hybrid-psp"], prov=CUR),
    rec("res-pbe0-memory", "result", "verified",
        "[TOOL] Measured PBE0 memory (BigDFT 1.9.5, thioxanthone, hgrid 0.35, rmult (6, 9), 8 MPI x 8 OMP, OP2P): peak "
        "RSS 30.1 GB for S0 and 48.6-52.6 GB for T1, reached during the input guess; wall time about 8.6 min (S0, 46 SCF "
        "iterations) and 37-38 min (T1, 68-72 iterations). BigDFT's own estimate (501 MB per process) is far too low for "
        "hybrids. Use these measurements to size PBE0 jobs for 6a, which has 3x the electrons and a larger grid.",
        tags=(ET,), references=["fail-pbe0-oom"], evidence=["ev-runlog"], prov=CUR),
    rec("res-tx-pbe0", "result", "verified",
        "[TOOL] Thioxanthone PBE0 single points (ixc -406, Krack PBE pseudopotentials, hgrid 0.35, rmult (6, 9), gnrm < 1e-5) "
        "at the converged PBE S0 and T1 geometries: E(S0@S0) = -104.920157843791, E(S0@T1) = -104.911685404613, "
        "E(T1@S0) = -104.815933904345, E(T1@T1) = -104.820844775510 Ha (T1 magnetization 2.000). PBE0 adiabatic E_T = "
        "0.09931307 Ha = 2.7024 eV = 260.75 kJ/mol. Vertical absorption to T1 (at S0) 2.836 eV = 273.64 kJ/mol; vertical "
        "emission (at T1) 2.472 eV = 238.50 kJ/mol; relaxation energies T1 0.134 eV, S0 0.231 eV. No zero-point correction.",
        tags=(ET,), references=["res-tx-pbe", "res-dryrun-pbe0", "dec-calibration-ok", "dec-psp-ok"],
        evidence=["ev-runlog", "ev-phase1"], arts=["procedures/analyze_phase1.py", "bigdft/runs/phase1_summary.json"],
        prov=CUR, claim_key="tx-et-pbe0"),
    rec("res-tx-calib-pbe0", "result", "verified",
        "[TOOL] Calibration check, PBE0: adiabatic 260.75 kJ/mol (2.702 eV) vs literature 274.1 kJ/mol (2.840 eV): -13.35 "
        "kJ/mol (-0.138 eV), inside the endorsed 0.2 eV window. The PBE0 Delta-SCF protocol passes the calibration; PBE "
        "(-0.388 eV) does not. Caveat: the literature value is from a secondary source of uncertain kind (0-0 vs onset).",
        tags=(ET,), references=["res-tx-pbe0", "res-tx-lit", "dec-criteria-ok", "res-tx-calib-pbe"],
        evidence=["ev-phase1", "ev-lit-tx"], prov=CUR),
    rec("res-functional-effect", "result", "verified",
        "[TOOL] At identical PBE geometries, PBE0 raises the adiabatic E_T of thioxanthone by 24.05 kJ/mol (0.249 eV) "
        "relative to PBE (236.70 -> 260.75 kJ/mol), supporting the hypothesis that the PBE deficit is mainly due to the "
        "functional. Grid, zero-point, solvent and PBE0-geometry effects remain unseparated.",
        tags=(ET,), references=["res-tx-pbe", "res-tx-pbe0", "q-zpe"], evidence=["ev-phase1"], prov=CUR,
        supersedes=["hyp-pbe-underestimate"]),
    rec("q-pbe0-geometry", "question", "unresolved",
        "PBE0 energies were evaluated at PBE geometries, not PBE0-optimised ones; the effect on the adiabatic E_T is not "
        "quantified.", tags=(ET,), references=["res-tx-pbe0"], prov=CUR),
    rec("q-t1-character", "question", "unresolved",
        "The character of the computed thioxanthone T1 (pi-pi* vs n-pi*) is not determined: no spin density or orbital "
        "analysis yet. The 0.051 A C9=O elongation shows carbonyl involvement but does not decide it.",
        tags=(ET,), references=["res-tx-pbe"], prov=CUR),
    rec("q-zpe", "question", "unresolved",
        "Zero-point and vibronic corrections are not computed; the Delta-SCF values are electronic adiabatic energies, "
        "while experiment reports the phosphorescence onset / inflection point.",
        tags=(ET,), references=["ctx-target", "res-tx-pbe"], prov=CUR),

    rec("q-hybrid-psp", "question", "unresolved",
        "Effect of using PBE-generated pseudopotentials with PBE0 on the triplet energy is not quantified.",
        tags=(ET,), references=["dec-psp"], prov=CUR),

    # ---- open questions ----
    rec("q-ensemble", "question", "unresolved",
        "A single conformer stands in for the NMR ensemble (authors' bundle r.m.s.d. 0.22 A, 10 of 90 structures). "
        "Sensitivity of excitation energies to conformation is unknown; other seeds of build_6a.py can supply more "
        "restraint-compatible conformers.", tags=(T, ET), references=["res-s1"], evidence=["ev-paper"]),
    rec("q-conditions", "question", "unresolved",
        "Conditions differ: NMR in CD2Cl2 at 233 K, E_T and absorption in EtOH (E_T in a 77 K glass), reactions in "
        "CH2Cl2 at -70 C. The authors' restraint averaging and stereo-assignments are not reported.",
        tags=(T, ET), references=["ctx-target", "hyp-group-min"], evidence=["ev-paper"]),
    rec("q-versions", "question", "unresolved",
        "Library versions were not pinned at run time; rdkit/tblite/ase versions were recovered from the uv cache, "
        "numpy and Python versions are unknown. Exact ETKDG reproduction is version- and platform-dependent.",
        references=["proc-generation"], evidence=["ev-runlog"], prov=CUR),
    rec("q-complex", "question", "unresolved",
        "The catalyst-substrate complex 6a.ent-5a (Table S1 intermolecular ids 34-35; allene ~4 A from the "
        "thioxanthone) has not been built.", references=["ctx-paper"], evidence=["ev-paper"], prov=SESSION + ["si"]),
]

# a record superseded by a later one (correction, researcher confirmation, measured result) is marked superseded
_sup = {i for r in records for i in r["supersedes"]}
for r in records:
    if r["id"] in _sup:
        r["status"] = "superseded"

memory = dict(
    format_version="1.0",
    origin=dict(backend="local-json",
                description="Curated by the agent from primary sources: the Paper2Agent paper skill, the project's 6a "
                            "structure files and the session b8d95464 transcript; records tagged by provenance class "
                            "[PAPER]/[TOOL]/[RESEARCHER]/[AI]"),
    records=records,
    sources=sources,
    python=">=3.10",
    artifacts=[dict(path=p, role=r, packages=[PK[k] for k in pk]) for p, r, pk in artifacts],
)

if __name__ == "__main__":
    for a in memory["artifacts"]:
        assert (SRC / a["path"]).is_file(), a["path"]
    ids = {r["id"] for r in records}
    for r in records:
        for k in ("references", "evidence", "supersedes"):
            assert set(r[k]) <= ids, (r["id"], k)
        assert set(r["provenance"]) <= {s["id"] for s in sources}, r["id"]
    (SRC / "memory.json").write_text(json.dumps(memory, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {SRC / 'memory.json'}: {len(records)} records, {len(memory['artifacts'])} artifacts")
