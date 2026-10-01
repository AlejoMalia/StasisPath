# Respuestas — semana 1 (prioridad: 1, 4, 5, 8, 10, 14, 17, 18 + las que cayeron por cota)

Estatus: [V] verificado con fuente · [M] cerrado por cota forzada + dato · [A] abierto · [P] prior.
Fuentes: F1 = Han et al. 2023 *Nat Commun* 14:3407 (PMC10256770) · F2 = Etheridge/Bischof et al., preprint bioRxiv 2024.11.08.622572 (versión publicada = #2, *Nat Commun* 2025) · F3 = PMC11611618 (CCR/CWR en tejido renal) · F4 = McCullough et al. 1999 *Ann Thorac Surg* 67:1895 vía thoracickey (#8) · F5 = Best 2008 (#12, PMC4733321) · F6 = asteriskmag "Brain freeze" (#15) · F7 = McIntyre & Fahy 2015 *Cryobiology* 71:448 (ASC) · F8 = de Vries et al. 2019 *Nat Biotechnol* · F9 = Tisherman 2022 *Ann NY Acad Sci* (EPR) · F10 = datos de torpor en ardilla ártica (Buck & Barnes; ADFG).

---

## Q1 — Magnitudes que separan estasis reversible de daño irreversible · [M] marco / [A] umbrales finos
StasisPath propone **cinco magnitudes**; reversible ⇔ las cinco por debajo de su umbral.

| magnitud | definición operativa | umbral actual (cerebro/órgano) | estatus |
|---|---|---|---|
| **τ_eq — dosis isquémica equivalente** | τ_eq = ∫ Q10^((T−37)/10) dt, con Q10 ≈ 2.3 | ≈ 5 min a 37 °C para recuperación sin déficit (clínico); 10–12 min en animales con flush frío (EPR: 2 h a 10 °C) | [V] F4, F9 |
| **f_hielo** | fracción de volumen cristalizada | 0 detectable (µCT/visual) | [V] F2 |
| **σ_térmica** | ΔT máx. centro–borde en fase vítrea | < 20 °C para evitar grietas | [V] F2 |
| **D_CPA — dosis tóxica de crioprotector** | concentración × tiempo × temperatura de exposición | no hay cifra única; VS55 tóxico en riñón rata, VMP no | [A] Q6 |
| **I_estructura** | trazabilidad del conectoma/ultraestructura por EM | ASC la conserva; criónica convencional no demostrado en casos reales | [V] F7 / [A] |

**Clave:** τ_eq unifica la hipotermia. La tabla de McCullough es exactamente τ_eq ≈ 5 min constante (ver Q8). Por encima de ~−130 °C la química no es nula; bajo Tg, τ_eq por año es despreciable (F5: ~34 000 años de cambio químico a −120 °C, prior de un autor pro-criónica, a verificar).

## Q2 — ¿Muerte legal = pérdida irreversible de información? · [M] No
Muerte legal = cese irreversible de función circulatoria/respiratoria o encefálica **con la medicina disponible** (criterio dependiente de tecnología). La pérdida de información es un umbral **físico** (I_estructura). Prueba de que difieren: DHCA de 30–45 min cumple criterios clínicos de parada y es reversible (F4); ASC destruye la viabilidad biológica pero conserva la estructura (F7). Son ejes ortogonales → StasisPath debe reportarlos por separado.

## Q3 — ¿Qué cuenta como éxito? · [M] escala E0–E5
E0 estructura conservada (EM) · E1 células viables · E2 tejido/lonchas funcionales · E3 órgano funcional trasplantado · E4 animal completo reanimado · E5 humano con memoria/identidad.
Máximo demostrado por vía: vitrificación órgano **E3** (riñón rata, F1; riñón conejo M22, F5) · lonchas hipocampo vitrificadas **E2** (>90 % viabilidad, F5) · ASC **E0** · criónica **E0 parcial** · DHCA/EPR **E5** pero sólo minutos–horas.

## Q4 — ¿A qué velocidades se forma hielo dañino? · [V]
Se forma hielo si enfriamiento < CCR o calentamiento < CWR (desvitrificación). CWR ≈ 10× CCR (#4).

| CPA | CCR solución | CWR solución | CCR tejido renal | CWR tejido renal |
|---|---|---|---|---|
| VS55 | 2.5 °C/min | 50 °C/min | < 1 | 18 |
| VMP | 5.4 | 190 | 5.3–5.6 | 55–70 |
| M22 | ~0.1 | ~0.4 | — | — |
Fuentes: F3, F2. Almacenar VS55 6 meses justo bajo Tg subió su CWR de 50 a ~100 °C/min (F2): **el almacenamiento largo empeora el recalentamiento** → almacenar muy por debajo de Tg.

## Q5 — Vitrificación y por qué falla al escalar · [M]
Tres líneas forzadas, cada una verificada:
1. **Recalentamiento (C1):** por conducción desde superficie, la tasa en el centro cae como 1/r². A ~5 cm < 0.3 °C/min: por debajo de la CWR de cualquier CPA usado en órganos. ⇒ calentamiento volumétrico obligatorio. Nanowarming lo resuelve porque **su tasa no depende del volumen** (F2): 88 °C/min en 2 L con bobina RF de 120 kW; ~1 500 °C/min en volumen pequeño.
2. **Enfriamiento (C3):** no existe enfriamiento volumétrico ⇒ el enfriamiento es ahora el paso limitante (lo dice F2). Medido: 3 L → ~0.45 °C/min. Escalado 1/LC² ⇒ VMP (CCR 5.4) **no vitrifica ni un riñón humano**; M22 (CCR 0.1) sí hasta escala cabeza/cuerpo promedio, **no el centro del tronco** (~0.04 °C/min).
3. **Toxicidad:** los CPA con CCR bajo (M22, VS83) son los más tóxicos (F2). ⇒ tensión CCR-bajo ↔ toxicidad es la restricción que queda (Q6, [A]).

## Q7 — ¿Rajado térmico = límite duro? · [V] no es duro, es un límite de protocolo
Con recocido (annealing) cerca de Tg y enfriamiento lento (< 1 °C/min) a −150 °C, ΔT < 20 °C y **sin grietas hasta 3 L** (F2). Deja de ser límite duro a escala de órgano; a escala de tronco no hay dato ([A]).

## Q8 — DHCA segura · [V] (C2 confirmada)
McCullough 1999 (CMRO₂ medido en 37 pacientes):

| T (°C) | CMRO₂ % | seguro (min) medido | cota C2 (Q10 = 2.3) |
|---|---|---|---|
| 37 | 100 | 5 | 5.0 |
| 30 | 56 | 9 | 9.0 |
| 25 | 37 | 14 | 13.6 |
| 20 | 24 | 21 | 20.6 |
| 15 | 16 | 31 | 31.2 |
| 10 | 11 | 45 | 47.4 |
Umbrales clínicos: > 25 min → déficits cognitivos sutiles; > 40 min sin perfusión cerebral → aumento de necrosis (F4).

## Q9 — De minutos a 37 °C a horas/días · [V]
Reversible (E5): 5 min a 37 °C → ~45 min a 10 °C (clínico) → 2 h a 10 °C (EPR animal, F9). Órganos aislados: ~27 h con superenfriamiento a −4 °C (hígado humano, F8, n = 5 descartados). Estructural sin función: necrosis del 15 % de neuronas a 6 h y del 65 % a 12 h de isquemia en corteza de rata (F5). **Días reversibles sin vidrio: no hay dato.**

## Q10 — ¿Recuperación funcional tras vitrificar un órgano completo? · [V] sí, sólo en rata y conejo
Riñón de rata, VMP 8.4 M, enfriamiento 20.5 °C/min, nanowarming 72 °C/min (CWR ~50), hasta 100 días a −150 °C; 5/5 receptores nefrectomizados vivos a 30 días; creatinina normal el día 23 (F1). Precedente: riñón de conejo con M22, función como único riñón (F5, Fahy 2009). Nada a escala humana con función.

## Q11 — Brecha riñón de rata → humano años · [M] cuatro saltos
1. Enfriamiento (C3): el CPA que funcionó (VMP) no vitrifica a escala humana ⇒ hace falta un CPA de CCR bajo **y** poco tóxico, que hoy no existe.
2. Perfusión: cargar CPA y nanopartículas en todos los lechos vasculares, incluido el cerebro (barrera hematoencefálica, deshidratación, [A]).
3. Recalentamiento: nanowarming escala en tasa, pero no hay bobina de tamaño cuerpo; a 88 °C/min la eficiencia medida es ~7 % (≈ 2 kg × 3 kJ/kg·K × 88 K/min ≈ 9 kW absorbidos de 120 kW) ⇒ cuerpo de 70 kg ≈ 300 kW absorbidos, ~4 MW de bobina a la misma eficiencia [P].
4. Tronco: grietas y CCR sin datos a LC ~ 7 cm.

## Q12 — ¿Estasis espacial exige vitrificación? · [M]
> **Corregido en semana 2 (H3):** la frase "ningún sistema biológico..." es falsa tal como está escrita (el pez pulmonado estiva 3–4 años). La versión forzada se limita a mamíferos. Ver `respuestas_semana2.md`.
Para años, sí. C2 verificada: 10 años exige supresión equivalente a ~−129 °C (< Tg). **Fuga comprobada:** torpor activo — la ardilla ártica baja al 2–4 % del metabolismo a ~−3 °C, pero sus episodios continuos duran ≤ ~3 semanas y los interrumpen despertares obligatorios (F10). Equivale a supresión pasiva Q10 a ~−5 / −10 °C. **Ningún sistema biológico conocido pasa años en pausa continua sin vidrio** (salvo anhidrobiosis, que no aplica a mamíferos). ⇒ Misión: torpor/hipotermia = semanas con ciclos; años = vitrificación, que no está demostrada a escala de cuerpo.

## Q13 — Energía, monitorización, fallo único · [P] cotas
- Almacenaje bajo Tg: energía ≈ sólo mantener frío (pérdidas de dewar); sin fallo agudo si el aislamiento es pasivo.
- **Punto único de fallo = recalentamiento:** evento de minutos, ~MW, con uniformidad < 20 °C y sin reintento posible. Energía mínima del recalentamiento ≈ 70 kg × ~3 kJ/kg·K × 130 K ≈ 27 MJ.
- Deriva de almacenamiento: mantener lejos de Tg (Q4: la CWR se duplica si se almacena justo bajo Tg).

## Q14 — Criónica: qué está medido y qué es esperanza · [V]
**Medido:** vitrificación funcional en lonchas y órganos pequeños (F5); ASC conserva el conectoma trazable en cerebro entero de cerdo (F7, premio de la Brain Preservation Foundation), pero es fijación química, irreversible biológicamente.
**No medido / esperanza:** reparación molecular, reanimación, reversión del daño isquémico. Los casos reales sufren retrasos de horas a días, mientras que la ventana práctica de perfusión ronda los 12 min (F6); τ_eq real ≫ umbral. **Ningún organismo ha sido reanimado** (lo admite el propio campo, F6).
Métrica que usa la criónica: muerte "teórico-informacional" (F5) = I_estructura de Q1, no reversibilidad.

## Q15 — Experimentos que falsarían "el conectoma sobrevive al protocolo actual" · [M] diseño
1. Cerebro animal sometido al **protocolo criónico real** (retraso típico de horas + perfusión de CPA + −196 °C), comparado con ASC y con control fijado inmediatamente: segmentación EM ciega de volumen y fracción de sinapsis trazables. Falsa si la trazabilidad cae bajo un umbral preregistrado (p.ej. < 90 % de las del control).
2. Mismo ensayo con retrasos de 0, 1, 6 y 24 h ⇒ curva de I_estructura frente a τ_eq.
3. Detectar grietas y deshidratación por µCT en cabezas completas (F2 da el método).
4. Engrama funcional: memoria condicionada en *C. elegans* o en lonchas → vitrificar → recalentar → comprobar si se conserva (E2 con información).

## Q16 — Fuera de StasisPath · [M]
Alma; subida mental o copia digital sin sustrato medido; nanorreparación sin datos; toda afirmación sin magnitud medible en Q1.

## Q17 — Mejor residual clínico hoy · [V]
Clínico: gametos, embriones, ovario (nacimientos vivos, F5) · órganos en frío estático (horas) · DHCA/EPR (minutos–2 h, E5) · superenfriamiento hepático 27 h (preclínico humano).
Frontera experimental: riñón de rata vitrificado 100 días → E3 (F1); vidrio físico de 3 L + nanowarming de 2 L sin tejido funcional (F2).

## Q18 — Afirmación falsable mínima StasisPath 2026 · [M] borrador
> **Para cualquier tejido ≥ 1 L, la pausa reversible de más de 1 día exige, a la vez: (a) T < Tg sin hielo detectable; (b) enfriamiento ≥ CCR del CPA en tejido, lo que por convección limita el volumen a LC ≲ 4 cm incluso con CCR = 0.1 °C/min; (c) recalentamiento volumétrico ≥ CWR con ΔT < 20 °C; (d) τ_eq acumulado ≲ 5–12 min.**
> Predicción: el primer órgano humano vitrificado que funcione tras trasplante usará un CPA de la clase CCR ≤ 1 °C/min (tipo M22, no VMP) o un CPA nuevo de toxicidad menor; ningún cuerpo completo de mamífero grande se reanimará tras > 1 día sin cumplir (a)–(d).
> **Se falsa si** un órgano ≥ 1 L o un mamífero recupera función tras > 1 día incumpliendo alguna de (a)–(d).

## Quedan abiertas (R1 — tensión conservada)
Q6 (función de toxicidad D_CPA), Q7 a escala de tronco, Q11.2 (perfusión cerebral de CPA), Q13 (datos de dewar/bobina), y el umbral de τ_eq en humanos con flush frío.
