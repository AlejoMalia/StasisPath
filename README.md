# StasisPath

![StasisPath](img/banner.png)

[![Verified Grounding](https://img.shields.io/badge/Grounding-97.3%25-brightgreen.svg)](en/red/motor.py)
[![Decisive Frontier](https://img.shields.io/badge/Frontier%20X2-OPEN-critical.svg)](en/ESPACIO.md)
[![Nodes](https://img.shields.io/badge/Nodes-251%20active-blue.svg)](en/red/stasispath.yaml)
[![Primary Sources](https://img.shields.io/badge/Primary%20sources-91-blue.svg)](en/red/stasispath.yaml)
[![Preregistrations](https://img.shields.io/badge/Preregistrations-5%2F5%20intact-success.svg)](en/red/prereg.lock)
[![Tests](https://img.shields.io/badge/Tests-79%20passing-success.svg)](stasispath-tools/)
[![Toolkit](https://img.shields.io/badge/Toolkit-stasispath--tools-orange.svg)](stasispath-tools/)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-blue.svg)](LICENSE)

**A quantitative biophysical framework for the limits of reversible preservation.**

What magnitudes, thresholds and time windows separate an organism or tissue in a *reversible*
pause from one that can no longer recover?

StasisPath answers that question as a computable, auditable network rather than a narrative. Every
claim carries a status and its dependencies; every threshold was frozen before the data exist; and
a single edit to the source of truth repropagates through the whole framework.

---

## State of the framework — two numbers, deliberately separate

| | value | what it means |
|---|---|---|
| **Grounding** | **97.3 %** | Fraction of the 251-node network resting on primary peer-reviewed sources (91 catalogued) and on bounds that stay robust at every uncertainty corner. |
| **Resolution at the decisive frontier** | **0 %** | Frontier $X_2$ is open. **No experiment in this framework has been executed.** |

A well-grounded framework is not an answered question. A complete set of blueprints is not a
bridge that carries traffic. We report both numbers because one headline percentage invites
exactly that confusion.

## Languages

The repository is bilingual and **split by language**, each edition self-contained and regenerable:

| | English | Español |
|---|---|---|
| Framework documents | [`en/`](en/) | [`es/`](es/) |
| Manuscript | [`PAPER_STASISPATH_EN.md`](PAPER_STASISPATH_EN.md) · [`.pdf`](PAPER_STASISPATH_EN.pdf) | [`PAPER_STASISPATH_ES.md`](PAPER_STASISPATH_ES.md) · [`.pdf`](PAPER_STASISPATH_ES.pdf) |
| Read first | [`en/MARCO.md`](en/MARCO.md) | [`es/MARCO.md`](es/MARCO.md) |
| README | this file | [`README.es.md`](README.es.md) |

The two editions are translations of each other and are **kept consistent by machine**:
`python3 tools/check_parity.py` fails if any number, status, dependency or frozen text differs between the two knowledge graphs,
and `python3 tools/check_numbers.py` fails if any computed value differs between a generated English document and its Spanish twin.

**Spanish only, by design:** `es/BITACORA.md` (the working log, including every self-correction), `es/INFORME_SESION_2026-09-27.md`,
and the original calculation record in `es/20_cotas/` (scripts and outputs), `es/30_respuestas/` and `es/10_fuentes/`.
They are archival and are referenced from the English documents by path. The YAML schema keys and the Python identifiers
(`fuentes`, `parametros`, `cotas`, ...) are also still Spanish; they are names, not prose.

---

## The practical result: invert the screening question

The field benchmarks cryoprotectants against M22 (critical cooling rate 0.10 °C/min). That anchors
the search on a *solution* instead of a *requirement*, and discards candidates that would suffice.

StasisPath computes the requirement directly:

> **A 1400 g human brain requires a critical cooling rate of ≤ 0.425 °C/min — 4.25× more
> permissive than M22.**

This turns CPA screening into a single DSC measurement any laboratory can run:

```python
import stasispath as sp

sp.required_ccr(1400.0)                      # 0.425 °C/min — the bar for a human brain
sp.screen_candidate_cpa("M22", 0.10)         # ADMISSIBLE (clears by ×4.25)
sp.screen_candidate_cpa("VS55", 2.5)         # REJECTED  (misses by ×5.9)
sp.screen_candidate_cpa("candidate", None)   # UNMEASURED — never a pass or a fail
```

Two constraints are enforced in code, not in prose:

- **Clearing the cooling-rate bar says nothing about preserved function.** It is a necessary
  condition on the ice-avoidance axis only. Frontier $X_2$ is precisely the fact that no chemistry
  has yet cleared both axes.
- **An unmeasured chemistry returns `UNMEASURED`.** A hardcoded value for an unmeasured quantity
  is how a framework fabricates progress. We removed one of our own.

---

## Which experiment to run first

Ranked by expected value of information per unit cost. A measurement is worth doing when its
plausible range **straddles a decision threshold**.

| Open quantity | EVOI | rel. cost | EVOI/cost | verdict |
|---|---|---|---|---|
| **Critical cooling rate of a low-toxicity candidate (DSC)** | 0.988 | 1.0 | **0.99** | **run first** |
| **Cooling-law exponent (P21)** | 0.241 | 0.5 | **0.48** | **run** |
| Nucleation rate at −6 °C | 0.419 | 12 | 0.03 | defer on cost |
| Human equivalent ischemia, optimal reperfusion | **1.000** | 30 | 0.03 | defer on cost |
| P19 — LTP after vitrification | 0.179 | 20 | 0.01 | defer on cost |

A **differential scanning calorimetry run** is the single most valuable experiment in the
framework. If a low-toxicity candidate clears 0.426 °C/min, frontier $X_2$ closes on the scale axis
**without running P19** — days of instrument time instead of a full electrophysiology campaign.

**Caution:** the candidate that looked most promising, natural deep eutectic solvents, is already measured
and does **not** qualify: it crystallizes in DSC at 30 °C/min (more than 70× above the bar), and its own paper sets
50 % w/v as a toxicity ceiling. A *new* chemistry is needed.

**P21 ranks second**: one control vessel, three small bags, three large bags, one thermocouple.
Forty-eight times better than P19 per unit cost, and it carries the entire multi-organ projection.
It had been deprioritized for looking trivial.

---

## Five hash-locked preregistrations

Every threshold was frozen **before any data exist**, with SHA-256 certificates over
`date + protocol text` in `en/red/prereg.lock`. The engine recomputes each hash on every run and halts
with an alarm if a frozen text changed.

| ID | Question | SHA-256 (first 16) | Status |
|---|---|---|---|
| P15 | Does the connectome survive a realistic cryonics protocol? | `b081e1bef45061f1` | no data |
| P18 | Minimum falsifiable claim of the framework | `40bf19b0ba442705` | no data |
| P19 | Does a chemistry that *scales* preserve LTP? | `5b728de09bf17d1c` | no data |
| P20 | Expected run length without prior fixation | `74ec536bc98a2a7f` | no data |
| P21 | Is the cooling-law exponent below 2.34? | `3ed875463de17d30` | no data |

**The P19 rule, exactly as frozen:** PASS if the M22 arm reaches ≥ 130 % of baseline LTP without differing from the V3 positive control; FAIL if it falls to ≤ 110 % while the control works; everything between is inconclusive and never reinterpreted. Respiration is a secondary measure, not a threshold.

**A threshold is never moved to rescue a hypothesis.** Adding a new preregistration is legitimate;
editing a frozen one is not. P18 still contains the project's prototype name inside its frozen
text, and has deliberately *not* been renamed — editing a hash-locked record, even cosmetically,
would destroy the evidence that it was never altered.

---

## What the self-audit found

The framework was audited against its own premises. The audit was built to make results *worse*.

- **`FAIL_STOP` — an unphysical extrapolation.** Bound C2 reported that ten-year storage requires
  −129 °C. But the glass transition is −123 °C: below it there is no liquid water and no
  metabolism, so Q10 is **undefined**, not merely extrapolated. The figure is withdrawn as a
  quantitative claim; C2's actual verdict (storage requires T < 0 °C under *any* measured Q10)
  survives untouched.
- **A geometry premise, now quantified.** Characteristic length was computed with a sphere formula
  throughout, including for the torso, which is a cylinder. Rather than assert the correction is
  harmless, we computed the **flip factor** for every organ — the multiplicative error at which a
  verdict reverses. The brain flips only at ×1.94 against a worst-case geometric error of ×1.5:
  **the verdict survives, with ×1.29 to spare.** That margin was not visible before the audit.
- **A density assumed in silence.** Converting grams to centimetres needs a density. 1.0 g/cm³ was
  assumed without declaring it. Now an explicit API parameter.
- **A disclosure, not a finding.** The exponent n = 2 behind the whole organ table is
  preregistered (P21) but has **never been measured**. Flagged on every computation.
- **A mistake of this repository.** An earlier version of the toolkit, the manuscripts and the OSF template described, for P19, a "double threshold" (OCR ≥ 85 % and LTP ≥ 120 %) that **did not match the frozen preregistration**. It has been corrected everywhere, and the toolkit now implements the frozen rule with a test at every threshold and boundary.

---

## Document map

Every link below is the English edition; the Spanish twin has the same name under [`es/`](es/).

### Manuscripts
| Document | What it is |
|---|---|
| **[`PAPER_STASISPATH_EN.md`](PAPER_STASISPATH_EN.md)** | **Reference manuscript** (12 sections, 52 references). Full analytical development, comparative biology, the design specification, the five hash-locked preregistrations and the self-audit. |
| **[`PAPER_STASISPATH_ES.md`](PAPER_STASISPATH_ES.md)** | Spanish synthesis of the same manuscript. |
| **[`PAPER_STASISPATH_EN.pdf`](PAPER_STASISPATH_EN.pdf)** · **[`ES.pdf`](PAPER_STASISPATH_ES.pdf)** | Typeset PDFs, rebuilt from the Markdown with `python3 build_papers_pdf.py`. |

### For laboratories
| Document | What it is |
|---|---|
| **[`en/LAB_DESIGN_TABLES_AND_GAPS.md`](en/LAB_DESIGN_TABLES_AND_GAPS.md)** | Operational design tables: biological scales (E5 → E0), comparative CPA toxicity, phase-by-phase reperfusion matrix, non-Q10 domains, regulatory framing (TRL 1–7), and five falsifiable predictions (only the first, P19, is preregistered). |
| **[`en/PREREGISTRATION_P19_OSF.md`](en/PREREGISTRATION_P19_OSF.md)** | OSF / AsPredicted-style registration form for P19, **generated from the hash-locked text** by `tools/gen_p19_osf.py` so it cannot drift from the preregistration. |
| **[`en/SFSA.md`](en/SFSA.md)** | Self-audit report: regime guards, dimensional homogeneity, value-of-information ranking. |
| **[`en/00_marco/method.md`](en/00_marco/method.md)** | The MATE + TRIADA method in one page. |

### Generated by the engine — never hand-edited
| Document | What it answers |
|---|---|
| **[`en/MARCO.md`](en/MARCO.md)** | The complete framework: every node, its status, its derivation chain. |
| **[`en/RUMBO.md`](en/RUMBO.md)** | Greedy minimum path of experimental closures, and what each one is worth. |
| **[`en/ESPACIO.md`](en/ESPACIO.md)** | The two-dimensional chemical space of frontier X2: required cooling rate vs demonstrated synaptic viability. |
| **[`en/BARRIDO.md`](en/BARRIDO.md)** | Value-by-value sweeps of every margin against the framework. |
| **[`en/TRIANGULACION.md`](en/TRIANGULACION.md)** | Unknowns projected by independent paths; empty intersections reported as contradictions. |
| **[`en/CONFIANZA.md`](en/CONFIANZA.md)** | Monte Carlo robustness of each verdict, and which parameters to measure first. |
| **[`en/CASCADA.md`](en/CASCADA.md)** | Uncertainty propagation along the P19 inference chain. |
| **[`en/CRUCE.md`](en/CRUCE.md)** | Physiological data crossed against the Arrhenius thermal law, isolating active mechanisms. |
| **[`en/ESCALADO.md`](en/ESCALADO.md)** | Cross-species scaling laws with leave-one-out validation. |
| **[`en/PRECISION.md`](en/PRECISION.md)** | Biot regime check, Monte Carlo viable mass, Poisson nucleation. |
| **[`en/MARGENES.md`](en/MARGENES.md)** · **[`BRECHAS`](en/BRECHAS.md)** · **[`DERIVACION`](en/DERIVACION.md)** · **[`FORMULACION`](en/FORMULACION.md)** · **[`ENCUENTROS`](en/ENCUENTROS.md)** · **[`PROYECCION`](en/PROYECCION.md)** · **[`P21`](en/P21.md)** | Margins, gaps to human, Arrhenius derivation, internal formulation, layer collisions, conditional projection, P21 status. |
| **[`en/red/grafo.md`](en/red/grafo.md)** · **[`en/red/informe.md`](en/red/informe.md)** | Dependency graph and engine report. |

### Working record (Spanish)
| Document | What it is |
|---|---|
| **[`es/BITACORA.md`](es/BITACORA.md)** | Full working log, including every self-correction and every error found. |
| **[`es/INFORME_SESION_2026-09-27.md`](es/INFORME_SESION_2026-09-27.md)** | Technical memo on the 94.7 % → 97.3 % verification pass and the source audit. |

---

## Knowledge graph structure (`en/red/stasispath.yaml`)

One file per edition is edited by hand; everything else regenerates. It holds the framework in interconnected layers:

| Layer | Contents |
|---|---|
| `fuentes` | Primary literature catalogue, F1–F93 (91 active), each with DOI, method and the specific measured value it supplies. |
| `parametros` | Biophysical constants with empirical uncertainty ranges (Q10, Tg, CCR, fracture stress, CPA diffusivity). |
| `cotas` | Thermodynamic inequalities and kinetic limits, C1–C11, each evaluated at **every** uncertainty corner. |
| `afirmaciones` | Ontology (O1–O4), magnitudes (G1–G8), frontiers (X1–X2) and laws (L1–L45), each with its derivation chain. |
| `vias` | Candidate pathways V01–V27, with the numerical window each one does or does not have. |
| `preguntas` | The canonical questions Q1–Q22 and their verdicts. |
| `preregistro` | The five frozen experimental designs (P15, P18, P19, P20, P21) with explicit stopping criteria. |
| `derivadas` | Quantities **computed, never written by hand** — characteristic lengths, cooling rates, the CCR–molarity line. |

### Status tags

Every node carries one, and a node can never outrank its weakest dependency.

| Tag | Meaning |
|---|---|
| **M** | *Mate* — robust at every uncertainty corner. The verdict does not depend on which end of any range you take. |
| **V** | Verified against a primary peer-reviewed source read in full. |
| **P** | Prior — supported only by a secondary source, a review or an abstract. |
| **A** | Open — no sufficient evidence either way. Frontier X2 lives here. |
| **ROTO** | Broken — a claim this framework previously made and has since refuted. |

---

## Epistemic rules

Five rules govern development. The second is the load-bearing one.

1. **R1 — Dependencies rule.** A derived node can never hold a higher certainty than its weakest premise: `status(A) ≤ min(status(deps))`. The one deliberate exception is a preregistration, which does not lose status because the thing it tests is open — that is its purpose.
2. **R2 — Invariance of rules.** Falsification thresholds are sealed under SHA-256 in [`red/prereg.lock`](en/red/prereg.lock). **Never reformulate the board, and never move a preregistered threshold to save the narrative.** Editing a frozen threshold triggers an alarm in the engine.
3. **R3 — Corner conservatism.** Every physical claim must hold simultaneously at the most optimistic and the most pessimistic end of every measured range.
4. **R4 — Advance through critical squares in order.**
5. **R5 — Stop when the verdict is forced.** *If the opponent has one escape, there is no mate.*

> [!CAUTION]
> **Zero tolerance for self-deception.**
> * We do **not** claim that reversible whole-body stasis in adult non-hibernating mammals is viable today. No published protocol achieves it.
> * Extrapolation from isolated organ (E3) to whole body (E0) is treated formally as an **open theoretical conjecture**, not a result.
> * Frontier X2 **remains open `[A]`** and will be considered closed only when a laboratory reports durable LTP in brain tissue vitrified with a low-critical-rate cryoprotectant (CCR ≤ 0.43 °C/min).

---

## Repository layout

```
en/                         English edition                     es/   Spanish edition (same shape)
├── red/                    The framework itself
│   ├── stasispath.yaml     SINGLE SOURCE OF TRUTH of this edition — the only file edited by hand
│   ├── motor.py            Verification engine: statuses, bounds, corner evaluation, scoring
│   ├── prereg.lock         SHA-256 certificates for the frozen preregistrations
│   ├── sfsa_auditoria.py   Self-audit (optional: needs the SFSA package, see below)
│   └── *.py                Scaling, margins, triangulation, sweeps, precision, projection
├── MARCO.md ... RUMBO.md   Generated documents
└── LAB_DESIGN_TABLES_AND_GAPS.md · PREREGISTRATION_P19_OSF.md

stasispath-tools/           Installable toolkit — 79 unit tests, zero dependencies
└── stasispath/
    ├── design_spec.py      What a given organ REQUIRES; CPA screening; flip factors
    ├── assumptions.py      Executable regime guards (Biot, Q10 below Tg, isochoric, geometry)
    ├── experiment_value.py EVOI-per-cost ranking of the open set
    ├── predictions.py      The FROZEN P19 decision rule, and four exploratory hypotheses (H2–H5)
    ├── f3_ischemia.py      Piecewise Q10 kinetics and equivalent ischemic dose
    ├── f4_nucleation.py    Stochastic ice nucleation (Poisson)
    ├── f5_cooling.py       Cooling phases and rate constraints
    ├── thermal_stress.py   Thermomechanical stress and fracture near Tg
    ├── cpa_toxicity.py     Arrhenius toxicity rescue at subzero temperatures
    ├── cpa_washout.py      Kedem–Katchalsky stepwise washout
    ├── organ_projector.py  Anthropometric multi-organ constraint projection
    └── boa_connector.py    Ingests TotalSegmentator / BOA radiologic volume masks

tools/                      check_parity.py · check_numbers.py · gen_p19_osf.py
PAPER_STASISPATH_{EN,ES}.md/.pdf · build_papers_pdf.py · README.es.md · CONTRIBUTORS.md · LICENSE · img/
```

Every `.md` under `en/red`, `en/` and `es/` that is not named above as hand-written is **generated by the engine**. None is hand-edited.

---

## Running it

```bash
(cd en && python3 red/motor.py)                 # recompute the English edition and regenerate its documents
(cd es && python3 red/motor.py)                 # recompute the Spanish edition
python3 tools/check_parity.py                   # EN and ES graphs agree on every number, status and frozen text
python3 tools/check_numbers.py                  # every generated EN document agrees numerically with its ES twin
python3 tools/gen_p19_osf.py                    # regenerate the P19 registration form from the frozen text
cd stasispath-tools && python3 -m pytest -q     # 79 tests
```

The self-audit (`red/sfsa_auditoria.py`) is optional and needs the SFSA package: install it, or run with
`SFSA_PATH=/path/to/sfsa/python python3 red/sfsa_auditoria.py`. Without it the script stops with a clear message; nothing else depends on it.

Edit `en/red/stasispath.yaml`, rerun the engine, and bounds, derived quantities, margins, triangulation and sweeps all repropagate.
**If a new value falls outside a predicted range, the framework reports a contradiction and names the law that fails — it does not absorb the data.**
That has happened twice without being sought. Edit one edition and mirror the change in the other, then run the two checks above.

---

## Method

Development follows a fixed protocol, applied before any compute is spent:

1. **Inventory** — is it already measured, or already on disk?
2. **Mathematics** — write the numeric bound *before* running or reading anything.
3. **Reuse** — what existing computation applies?

Five governing rules, of which the second is the load-bearing one:

- **R1** — preserve tension; do not force a hypothesis closed.
- **R2** — **invariance of rules: never reformulate the board, never move a preregistered threshold
  to save the narrative.**
- **R3** — project the last three forced moves and stop.
- **R4** — advance through critical squares in order.
- **R5** — stop when the verdict is forced. *If the opponent has one escape, there is no mate.*

---

## What this contributes, and what it does not

**Does not:** a single measurement, a new physical law, or an executed experiment. Everything
inside was measured by someone else.

**Does:**
- a **design specification** that redirects the search — the requirement is 0.425 °C/min, not
  M22's 0.10, which admits a class of chemistries that M22-anchored screening excludes a priori;
- frontier $X_2$ **quantified on two axes**, function and scale, with an empty intersection
  (the viability–stability plot is Fahy's, 2004; the 2026 axes are ours);
- firm **negative results** — whole-body preservation is not viable by conduction, and the trunk
  cannot be cooled;
- a **reusable method** where contradictions are reported rather than averaged away.

The value of this work is not decided by 97.3 %. It is decided by whether someone puts a candidate
solvent in a calorimeter. **A framework cannot substitute for the instrument.**

---

## License

Released for academic and scientific research under **CC BY-NC 4.0**. Commercial exploitation,
resale and proprietary relicensing are prohibited. See `LICENSE`.

## Citation

> Malia, A., with Claude (Anthropic) and Grok (xAI) (2026). *StasisPath: A Quantitative Biophysical Framework for Metabolic
> Depression, Ice Avoidance, and the Thermodynamic Limits of Reversible Mammalian Preservation.*
> StasisPath Initiative.
