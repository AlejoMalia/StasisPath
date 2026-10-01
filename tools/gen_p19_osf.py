#!/usr/bin/env python3
"""Generate the OSF / AsPredicted-style registration form for P19 from the knowledge graph.

The form is GENERATED from the frozen text, never written by hand, so it cannot drift from the
hash-locked preregistration (an earlier hand-written template did, and registered a different experiment).

    python3 tools/gen_p19_osf.py
"""
import pathlib, hashlib, yaml
ROOT = pathlib.Path(__file__).resolve().parent.parent

def build(lang):
    d = yaml.safe_load(open(ROOT / f"{lang}/red/stasispath.yaml", encoding="utf-8"))
    pr = d["preregistro"]; p = pr["P19"]
    frozen = p["t"]; amend = p.get("enmiendas") or ""
    h = hashlib.sha256((pr["fecha"] + frozen).encode()).hexdigest()
    shown = p.get("t_en") or frozen
    L = {
     "en": dict(title="PREREGISTRATION FORM: EXPERIMENT P19 (FRONTIER X2)",
        sub="Does a chemistry that scales preserve LTP in a vitrified hippocampus?",
        std="OSF / AsPredicted-compatible · generated from `red/stasispath.yaml` · DO NOT EDIT BY HAND",
        lock="> **Frozen text.** The text below is registered under SHA-256 `%s` (preregistration date %s, stored in `red/prereg.lock`). "
             "Any deviation must be reported as a post-hoc exploratory analysis. The English text is a non-binding translation; **the Spanish original governs**.",
        s1="1. Study", s2="2. The frozen protocol", s3="3. Decision rule", s4="4. Amendments registered before any data",
        s5="5. Secondary measures", s6="6. What the frozen text does not specify",
        rule=["**PASS** if arm C reaches ≥ 130 % of baseline fEPSP at 60 min after HFS and does not differ from arm B (95 % CI of the difference within ±25 percentage points).",
              "**FAIL** if arm C ≤ 110 % (no useful potentiation) while arm B ≥ 130 %.",
              "Between 110 and 130 %, or with arm B failed: **inconclusive**, and it is not reinterpreted.",
              "**Quality control:** arm B must replicate the published result (138.1 %) within ±20 percentage points; otherwise the experiment is not interpretable and is repeated before arm C is read."],
        sec=["Basal respiration and reserve capacity (Seahorse OCR), recorded to compare with the published values (control 173.3 ± 6.7; 65 % at 10 °C, 80.4 ± 5.6).",
             "The framework's Arrhenius derivation predicts damage 0.142 in arm C (OCR retention ≈ 86 %). Damage above 0.25 refutes that **derivation**; at or below 0.10 confirms it. This tests the derivation (I1), **not P19**, which is decided by LTP alone."],
        gap=["The frozen text fixes the arms, the primary variable, the thresholds, n and blinding. It is **silent** on randomization procedure, exact washout step schedule, sample-exclusion rules beyond the quality control above, and the statistical test used to compute the 95 % CI.",
             "Whoever executes P19 must register those choices **before any data are collected**. They may not change the thresholds, the arms or the primary variable (rule R2).",
             "An earlier hand-written template specified a different experiment (different arms, an OCR ≥ 85 % threshold, an invented washout schedule). It did not match this preregistration and was withdrawn."],
        auth="Principal investigator: ________   Institution: ________   Ethics approval (IACUC): ________"),
     "es": dict(title="FORMULARIO DE PRERREGISTRO: EXPERIMENTO P19 (FRONTERA X2)",
        sub="¿Conserva la LTP una química que escala en un hipocampo vitrificado?",
        std="Compatible con OSF / AsPredicted · generado desde `red/stasispath.yaml` · NO EDITAR A MANO",
        lock="> **Texto congelado.** El texto siguiente está registrado bajo SHA-256 `%s` (fecha de prerregistro %s, guardado en `red/prereg.lock`). "
             "Cualquier desviación debe reportarse como análisis exploratorio post-hoc.",
        s1="1. Estudio", s2="2. El protocolo congelado", s3="3. Regla de decisión", s4="4. Enmiendas registradas antes de cualquier dato",
        s5="5. Medidas secundarias", s6="6. Lo que el texto congelado no especifica",
        rule=["**PASA** si el brazo C alcanza ≥ 130 % del fEPSP basal a los 60 min tras HFS y no difiere del brazo B (IC 95 % de la diferencia dentro de ±25 puntos porcentuales).",
              "**FALLA** si el brazo C ≤ 110 % (sin potenciación útil) mientras el brazo B ≥ 130 %.",
              "Entre 110 y 130 %, o con el brazo B fallido: **inconcluso**, y no se reinterpreta.",
              "**Control de calidad:** el brazo B debe replicar el resultado publicado (138.1 %) dentro de ±20 puntos porcentuales; si no, el experimento no es interpretable y se repite antes de leer el brazo C."],
        sec=["Respiración basal y capacidad de reserva (OCR Seahorse), registradas para comparar con los valores publicados (control 173.3 ± 6.7; 65 % a 10 °C, 80.4 ± 5.6).",
             "La derivación de Arrhenius del marco predice daño 0.142 en el brazo C (retención de OCR ≈ 86 %). Un daño > 0.25 refuta esa **derivación**; ≤ 0.10 la confirma. Esto prueba la derivación (I1), **no P19**, que se decide solo por la LTP."],
        gap=["El texto congelado fija los brazos, la variable primaria, los umbrales, n y el cegamiento. **No dice nada** sobre el procedimiento de aleatorización, el calendario exacto de lavado, reglas de exclusión de muestras más allá del control de calidad anterior, ni la prueba estadística con la que se calcula el IC 95 %.",
             "Quien ejecute P19 debe registrar esas decisiones **antes de recoger ningún dato**. No pueden cambiar los umbrales, los brazos ni la variable primaria (regla R2).",
             "Una plantilla anterior escrita a mano especificaba otro experimento (otros brazos, un umbral de OCR ≥ 85 %, un calendario de lavado inventado). No coincidía con este prerregistro y se retiró."],
        auth="Investigador principal: ________   Institución: ________   Aprobación ética (CEEA): ________"),
    }[lang]
    out = [f"<!-- AUTO-GENERATED by tools/gen_p19_osf.py from red/stasispath.yaml. DO NOT EDIT BY HAND. -->",
           f"# {L['title']}", f"## {L['sub']}", f"*{L['std']}*", "", L["lock"] % (h, pr["fecha"]), "",
           f"## {L['s1']}", f"- **P19** · hash `{h[:16]}…` · {pr['fecha']}", f"- {L['auth']}", "",
           f"## {L['s2']}", "", shown.strip(), "", f"## {L['s3']}", ""] + [f"- {r}" for r in L["rule"]] + ["", f"## {L['s4']}", ""]
    out += [amend.strip() if amend else "—", "", f"## {L['s5']}", ""] + [f"- {x}" for x in L["sec"]]
    out += ["", f"## {L['s6']}", ""] + [f"- {x}" for x in L["gap"]] + [""]
    return "\n".join(out)

for lang, path in (("en", ROOT / "en/PREREGISTRATION_P19_OSF.md"), ("es", ROOT / "es/PREREGISTRO_P19_OSF.md")):
    path.write_text(build(lang), encoding="utf-8"); print("written", path.relative_to(ROOT))
