# Contributors

## Contributors

**Alejo Malia** — StasisPath Initiative. Author and project lead: the research question, the MATE + TRIADA
method, the knowledge-graph architecture, the preregistered experimental designs, and responsibility for
every scientific claim and verdict.

**Claude (Anthropic)** — AI contributor. Literature reading and verification against primary sources, the
verification engine and its self-audit, the toolkit modules, the bilingual documents, and the corrections
recorded in `es/BITACORA.md`.

**Grok (xAI)** — AI contributor. Contributed to the development of the framework and its early drafts.

The AI systems are credited as contributors to the work; responsibility for the claims rests with the human
author, who decided what to keep, correct and publish. Every external source is cited in
`en/red/stasispath.yaml`, and every error found along the way, including those introduced by the AI
contributors, is recorded in `es/BITACORA.md`.

---

## Contributing

StasisPath is a falsifiable framework, so the most valuable contribution is a measurement —
especially one that refutes a preregistered threshold.

**Priority measurements** (ranked by expected value of information per unit cost, see `SFSA.md`):

1. **Differential scanning calorimetry of a low-toxicity cryoprotectant candidate.** If the
   critical cooling rate is ≤ 0.426 °C/min, frontier X2 closes on the scale axis without running
   P19. Days of instrument time. (Natural deep eutectic solvents are already measured and fail: they
   crystallize at 30 °C/min. A new chemistry is needed.)
2. **P21 — the cooling-law exponent.** One control vessel, three small bags, three large bags,
   one thermocouple. It carries the entire multi-organ projection and has never been measured.

**How to submit data.** Open a pull request adding the measurement as a single entry in
`en/red/stasispath.yaml` and mirror it in `es/red/stasispath.yaml`, with its primary source; then run both
engines and `python3 tools/check_parity.py` and `python3 tools/check_numbers.py`. The verdict is
computed, not argued: if the value falls outside the predicted range, the engine reports a
contradiction and names the law that fails.

**Two rules bind every contribution.**

- A preregistered threshold is never moved to accommodate a result (rule R2). Frozen texts are
  hash-protected in `en/red/prereg.lock`; editing one halts the engine with an alarm. Adding a *new*
  preregistration is legitimate.
- A value with no measured source is not a value. Unmeasured quantities stay `UNMEASURED`; they
  never enter as a constant.

Corrections to existing claims are as welcome as new data. Three results in this repository were
revised downward by self-audit, and that record is kept deliberately in `BITACORA.md`.
