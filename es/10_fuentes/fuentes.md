# Fuentes — estado y dato a extraer (regla: solo lo que la cota necesita)

| # | fuente | extraer | estado |
|---|---|---|---|
| 1 | nature.com/articles/s41467-023-38824-8 (riñón rata, nanowarming) | CPA usado, CCR/CWR alcanzadas, tasa de calentamiento, días de almacenamiento, creatinina post-trasplante, n y supervivencia | leído → F1 (vía PMC10256770; nature.com redirige a login) |
| 2 | nature.com/articles/s41467-025-63483-2 | volumen máximo, tasa de calentamiento volumétrica lograda, fracturas sí/no, homogeneidad térmica | leído vía preprint bioRxiv 2024.11.08.622572 → F2. **Tanda 42:** extraído sólo el punto de 1 L (~1 °C/min, LC ~1.4 cm; resumen en PubMed 41006284). F2 no tiene un cuarto volumen: no se sigue leyendo (MATE) |
| 3 | pubmed 41006284 | = #2 (usar solo si #2 no abre) | no necesario (captcha) |
| 4 | PMC10248239 (revisión cuellos de botella) | tabla CCR/CWR por CPA, límites de tamaño, fractura | leído: sin CCR/CWR numéricos; sólo CWR ≈ 10× CCR |
| 5 | PMC10215456 (tecnologías vitrificación) | CCR/CWR de VS55, VM3, M22; Tg | leído: sin tabla; Tg mínima ≈ −140 °C |
| 6 | obgynkey cap. 6 | solo si #4/#5 no dan números | omitido por MATE (F2+F3 dieron los números) |
| 7 | sciencedirect S0011224015001340 | **verificar qué paper es**: el PII parece Cryobiology 2015 — posiblemente McIntyre & Fahy, *Aldehyde-stabilized cryopreservation* (relevante para Q14/15, no para "evitar hielo") | **NO es ASC** (el PII del paper de ASC es S001122401500245X); 403; sin identificar. ASC leído aparte → F7 |
| 8 | thoracickey DHCA | tabla tiempo seguro vs T; Q10 cerebral | leído → F4 |
| 9 | ~~sciencedirect.com/article/abs/pii/S0003497522013200~~ → URL mal formada (falta `/science/`); corregir a sciencedirect.com/science/article/abs/pii/S0003497522013200 | incidencia de daño neurológico vs minutos | omitido por MATE (F4 fija el veredicto) |
| 10 | cardiperf DHCA | redundante con #8; solo contrastar límite 30–40 min | omitido por MATE |
| 11 | clinicalpub | redundante con #8 | omitido por MATE |
| 12 | PMC4733321 (Best, visión pro) | qué afirma como medido | leído → F5 |
| 13 | PMC9219731 | direcciones de investigación | omitido (sin cota que dependa de ella) |
| 14 | cryonicsarchive 2013 update | evidencia estructural cerebral post-M22 (deshidratación, fracturas) | omitido; pendiente sólo si Q15 pasa a experimento |
| 15 | asteriskmag brain-freeze | límites reconocidos por el propio campo | leído → F6 |
| 16 | skeptoid 967 | crítica divulgativa (baja evidencia) | omitido |
| 17–19 | Wikipedia Cryobiology / Cryonics / Suspended animation | mapa de términos. Nota: la frase "levitación no aplica" en #17 es residuo de otro programa; se ignora | referencia |

**Huecos detectados (no están en la lista, candidatos por valor para las cotas):**
- McCullough et al. 1999, *Ann Thorac Surg* — Q10 cerebral y tiempos seguros DHCA (ancla primaria de #8).
- de Vries et al. 2019, *Nat Biotechnol* — superenfriamiento hígado humano ~27 h (vía intermedia sin vidrio).
- Tisherman et al. — EPR (Emergency Preservation and Resuscitation) en trauma: hipotermia profunda ~1 h en humanos.
- Fahy et al. 2009, *Cryobiology* — riñón de conejo vitrificado con M22 (precedente de #1).
- McIntyre & Fahy 2015 — ASC + Brain Preservation Prize (Q14/15).

**Añadidas y leídas:** F3 PMC11611618 (CCR/CWR de VS55 y VMP en tejido renal) · F7 McIntyre & Fahy 2015, Cryobiology 71:448 · F8 de Vries 2019, Nat Biotechnol (resumen) · F9 Tisherman 2022, EPR (resumen) · F10 torpor en ardilla ártica (resúmenes).
**Aún sin leer, candidatas:** Fahy 2009 (riñón de conejo con M22, primaria), McCullough 1999 (primaria), datos de pérdidas de dewar de LN₂ (Q13).

## Tanda 2 (aportada por el usuario el 2026-09-26)
| fuente | estado |
|---|---|
| Wikipedia, Information-theoretic death | omitida por MATE (F15 cubre el concepto con referencias) |
| brainpreservation.github.io/Defining_Death | leída con curl → F15 |
| Merkle, Molecular repair of the brain | omitida por MATE: sólo define el criterio, ya cubierto por F15; texto largo sin números |
| Wowk, Matters-of-Life-and-Death.pdf | leída (extracción de PDF) → F16 |
| McKenzie et al. 2024, Biostasis roadmap | leída en PMC11430499 (MDPI dio 403) → F14 |
| PMC12659898, torpor sintético | leída → F12 |
| Nordeen & Martin 2019, Physiology | sólo el resumen de PubMed (403) → F13 |
| Shemie et al. 2023, guía de Canadá | sólo el resumen de PubMed (Springer pidió login) → F17; el periodo de observación de 5 min queda [P] |
| Añadidas: Larson 2014 (F11), Tessier 2022 (F18), tortuga, lémur y pez pulmonado (F19) | leídas (resúmenes) |

## Tanda 3 (semana 3)
| fuente | estado |
|---|---|
| PDF de la guía canadiense (Springer) | **bloqueado** (redirige a login) desde este entorno. Verificado con F27: el formulario nacional de Saskatchewan reproduce el texto (5 min controlada, 10 min no controlada, ≤ 5 mmHg, reinicio). También lo verificó el usuario en el PDF. |
| Nordeen & Martin, HTML completo | la página devuelve sólo un armazón (5 KB); sigo usando el resumen (F13); **no cambia ningún veredicto** (MATE) |
| F20–F26 | resúmenes de PubMed o PMC; ScienceDirect dio 403 |
