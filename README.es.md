# StasisPath

![StasisPath](img/banner.png)

[![Fundamentación verificada](https://img.shields.io/badge/Fundamentaci%C3%B3n-97.3%25-brightgreen.svg)](es/red/motor.py)
[![Frontera decisiva](https://img.shields.io/badge/Frontera%20X2-ABIERTA-critical.svg)](es/ESPACIO.md)
[![Nodos](https://img.shields.io/badge/Nodos-251%20activos-blue.svg)](es/red/stasispath.yaml)
[![Fuentes primarias](https://img.shields.io/badge/Fuentes%20primarias-91-blue.svg)](es/red/stasispath.yaml)
[![Preregistros](https://img.shields.io/badge/Preregistros-5%2F5%20intactos-success.svg)](es/red/prereg.lock)
[![Tests](https://img.shields.io/badge/Tests-79%20pasan-success.svg)](stasispath-tools/)
[![Toolkit](https://img.shields.io/badge/Toolkit-stasispath--tools-orange.svg)](stasispath-tools/)
[![Licencia: CC BY-NC 4.0](https://img.shields.io/badge/Licencia-CC%20BY--NC%204.0-blue.svg)](LICENSE)

**Un marco biofísico cuantitativo de los límites de la preservación reversible.**

*[English version](README.md)*

¿Qué magnitudes, umbrales y ventanas temporales separan un organismo o tejido en una pausa *reversible* de uno que ya no puede recuperarse?

StasisPath responde a esa pregunta como una red computable y auditable, no como una narración. Cada afirmación lleva un estatus y sus dependencias; cada umbral se congeló antes de que existan los datos; y una sola edición de la fuente de verdad se repropaga por todo el marco.

---

## Estado del marco: dos números, separados a propósito

| | valor | qué significa |
|---|---|---|
| **Fundamentación** | **97,3 %** | Fracción de la red de 251 nodos apoyada en fuentes primarias con revisión por pares (91 catalogadas) y en cotas que se mantienen robustas en todas las esquinas de incertidumbre. |
| **Resolución en la frontera decisiva** | **0 %** | La frontera X2 está abierta. **Ningún experimento de este marco se ha ejecutado.** |

Un marco bien fundamentado no es una pregunta contestada. Un juego completo de planos no es un puente que soporte tráfico. Damos los dos números porque un solo porcentaje invita exactamente a esa confusión.

---

## Idiomas

El repositorio es bilingüe y **está dividido por idioma**; cada edición es autocontenida y regenerable:

| | English | Español |
|---|---|---|
| Documentos del marco | [`en/`](en/) | [`es/`](es/) |
| Manuscrito | [`PAPER_STASISPATH_EN.md`](PAPER_STASISPATH_EN.md) · [`.pdf`](PAPER_STASISPATH_EN.pdf) | [`PAPER_STASISPATH_ES.md`](PAPER_STASISPATH_ES.md) · [`.pdf`](PAPER_STASISPATH_ES.pdf) |
| Leer primero | [`en/MARCO.md`](en/MARCO.md) | [`es/MARCO.md`](es/MARCO.md) |

Las dos ediciones son traducciones una de otra y **se mantienen coherentes por máquina**: `python3 tools/check_parity.py` falla si algún número, estatus, dependencia o texto congelado difiere entre los dos grafos, y `python3 tools/check_numbers.py` falla si algún valor calculado difiere entre un documento generado en inglés y su gemelo en español.

**Solo en español, por diseño:** `es/BITACORA.md` (el diario de trabajo, con cada autocorrección), `es/INFORME_SESION_2026-09-27.md` y el registro original de cálculos en `es/20_cotas/`, `es/30_respuestas/` y `es/10_fuentes/`. Son archivo histórico. Los nombres de claves del YAML y los identificadores de Python (`fuentes`, `parametros`, `cotas`, ...) también siguen en español: son nombres, no prosa.

---

## El resultado práctico: invertir la pregunta de cribado

El campo mide los crioprotectores frente a M22 (velocidad crítica de enfriamiento 0,10 °C/min). Eso ancla la búsqueda en una *solución* en lugar de en un *requisito*, y descarta candidatos que bastarían.

StasisPath calcula el requisito directamente:

> **Un cerebro humano de 1400 g exige una velocidad crítica de enfriamiento ≤ 0,425 °C/min: 4,25 veces más permisivo que M22.**

Con eso el cribado de crioprotectores es una sola medida de DSC que cualquier laboratorio puede hacer:

```python
import stasispath as sp

sp.required_ccr(1400.0)                      # 0.425 °C/min — el listón de un cerebro humano
sp.screen_candidate_cpa("M22", 0.10)         # ADMISSIBLE (supera por ×4,25)
sp.screen_candidate_cpa("VS55", 2.5)         # REJECTED  (falla por ×5,9)
sp.screen_candidate_cpa("candidato", None)   # UNMEASURED — nunca aprobado ni suspenso
```

Dos restricciones están impuestas en el código, no en la prosa:

- **Superar el listón de enfriamiento no dice nada sobre la función conservada.** Es condición necesaria solo en el eje del hielo. La frontera X2 es precisamente que ninguna química ha superado aún los dos ejes.
- **Una química sin medir devuelve `UNMEASURED`.** Un valor fijado a mano para una magnitud sin medir es como un marco fabrica avance. Quitamos uno nuestro.

---

## Qué experimento hacer primero

Ordenados por valor esperado de la información por unidad de coste. Una medición merece la pena cuando su rango plausible **cruza un umbral de decisión**.

| Magnitud abierta | EVOI | coste rel. | EVOI/coste | veredicto |
|---|---|---|---|---|
| **Velocidad crítica de un candidato de baja toxicidad (DSC)** | 0,988 | 1,0 | **0,99** | **primero** |
| **Exponente de la ley de enfriamiento (P21)** | 0,241 | 0,5 | **0,48** | **ejecutar** |
| Tasa de nucleación a −6 °C | 0,419 | 12 | 0,03 | aplazar (coste) |
| Isquemia equivalente humana, reperfusión óptima | **1,000** | 30 | 0,03 | aplazar (coste) |
| P19 — LTP tras vitrificación | 0,179 | 20 | 0,01 | aplazar (coste) |

Una **calorimetría diferencial de barrido** es el experimento más valioso del marco. **Ojo:** el candidato que se creía más prometedor, los disolventes eutécticos naturales, ya está medido y **no** sirve: cristalizan en DSC a 30 °C/min (más de 70 veces por encima del listón) y su propio artículo fija el 50 % p/v como techo por toxicidad. Hace falta una química *nueva*.

**P21 es la segunda**: un recipiente de control, tres bolsas pequeñas, tres grandes y un termopar. Cuarenta y ocho veces mejor que P19 por unidad de coste, y sostiene toda la proyección multiórgano.

---

## Cinco preregistros protegidos por hash

Cada umbral se congeló **antes de que existan datos**, con certificados SHA-256 sobre `fecha + texto` en `es/red/prereg.lock`. El motor recalcula cada hash en cada ejecución y se detiene con alarma si un texto congelado cambió.

| ID | Pregunta | SHA-256 (16 primeros) | Estado |
|---|---|---|---|
| P15 | ¿Sobrevive el conectoma a un protocolo criónico real? | `b081e1bef45061f1` | sin datos |
| P18 | Afirmación falsable mínima del marco | `40bf19b0ba442705` | sin datos |
| P19 | ¿Conserva la LTP una química que *escala*? | `5b728de09bf17d1c` | sin datos |
| P20 | Expected run length sin fijación previa | `74ec536bc98a2a7f` | sin datos |
| P21 | ¿El exponente de enfriamiento queda por debajo de 2,34? | `3ed875463de17d30` | sin datos |

**La regla de P19, tal como se congeló:** PASA si el brazo M22 alcanza ≥ 130 % de la LTP basal sin diferir del control positivo V3; FALLA si cae a ≤ 110 % mientras el control funciona; todo lo intermedio es inconcluso y no se reinterpreta. La respiración es una medida secundaria, no un umbral.

**Un umbral no se mueve nunca para salvar una hipótesis.** Añadir un preregistro nuevo es legítimo; editar uno congelado, no. P18 conserva el nombre del prototipo del proyecto dentro de su texto congelado y **no** se ha renombrado a propósito: editar un registro protegido por hash, aunque sea por cosmética, destruiría la prueba de que nunca se alteró.

---

## Lo que encontró la autoauditoría

El marco se auditó contra sus propias premisas. La auditoría se construyó para que los resultados quedaran **peor**.

- **`FAIL_STOP` — una extrapolación no física.** La cota C2 publicaba que diez años de almacenamiento exigen −129 °C. Pero la transición vítrea está en −123 °C: por debajo no hay agua líquida ni metabolismo, así que Q10 está **indefinido**. La cifra se retira como afirmación cuantitativa; el veredicto de C2 (T < 0 °C con *cualquier* Q10 medido) sobrevive intacto.
- **Una premisa geométrica, ahora cuantificada.** La longitud característica se calculaba con fórmula de esfera, incluido el tronco, que es un cilindro. En vez de afirmar que la corrección es inocua, calculamos el **factor de vuelco** de cada órgano. El cerebro se invierte solo a ×1,94 frente a un error geométrico de ×1,5 en el peor caso: **el veredicto sobrevive, con ×1,29 de holgura.**
- **Una densidad asumida en silencio.** Convertir gramos en centímetros exige una densidad. Ahora es un parámetro explícito de la API.
- **Una declaración, no un hallazgo.** El exponente n = 2 de toda la tabla de órganos está prerregistrado (P21) pero **nunca se ha medido**.
- **Un error de este repositorio.** Una versión anterior del toolkit, de los papers y de la plantilla OSF describía para P19 un «doble umbral» (OCR ≥ 85 % y LTP ≥ 120 %) que **no coincidía con el preregistro congelado**. Se ha corregido en todas partes y el toolkit implementa ahora la regla congelada, con tests en cada umbral y cada borde.

---

## Mapa de documentos

Todos los enlaces son de la edición española; el gemelo inglés tiene el mismo nombre bajo [`en/`](en/).

### Manuscritos
| Documento | Qué es |
|---|---|
| **[`PAPER_STASISPATH_ES.md`](PAPER_STASISPATH_ES.md)** | Síntesis en castellano del manuscrito. |
| **[`PAPER_STASISPATH_EN.md`](PAPER_STASISPATH_EN.md)** | **Manuscrito de referencia** (12 secciones, 52 referencias). |
| **PDF** | `python3 build_papers_pdf.py` los reconstruye desde el Markdown. |

### Para laboratorios
| Documento | Qué es |
|---|---|
| **[`es/TABLAS_DE_DISENO_Y_HUECOS_LAB.md`](es/TABLAS_DE_DISENO_Y_HUECOS_LAB.md)** | Tablas operativas de diseño y cinco predicciones falsables (solo la primera, P19, está preregistrada). |
| **[`es/PREREGISTRO_P19_OSF.md`](es/PREREGISTRO_P19_OSF.md)** | Formulario de registro de P19 estilo OSF, **generado desde el texto protegido por hash** con `tools/gen_p19_osf.py`. |
| **[`es/SFSA.md`](es/SFSA.md)** | Informe de autoauditoría. |
| **[`es/00_marco/metodo.md`](es/00_marco/metodo.md)** | El método MATE + TRIADA en una página. |

### Generados por el motor — nunca se editan a mano
[`MARCO`](es/MARCO.md) · [`RUMBO`](es/RUMBO.md) · [`ESPACIO`](es/ESPACIO.md) · [`BARRIDO`](es/BARRIDO.md) · [`TRIANGULACION`](es/TRIANGULACION.md) · [`CONFIANZA`](es/CONFIANZA.md) · [`CASCADA`](es/CASCADA.md) · [`CRUCE`](es/CRUCE.md) · [`ESCALADO`](es/ESCALADO.md) · [`PRECISION`](es/PRECISION.md) · [`MARGENES`](es/MARGENES.md) · [`BRECHAS`](es/BRECHAS.md) · [`DERIVACION`](es/DERIVACION.md) · [`FORMULACION`](es/FORMULACION.md) · [`ENCUENTROS`](es/ENCUENTROS.md) · [`PROYECCION`](es/PROYECCION.md) · [`P21`](es/P21.md)

### Registro de trabajo
[`es/BITACORA.md`](es/BITACORA.md) (diario completo, con cada error encontrado) · [`es/INFORME_SESION_2026-09-27.md`](es/INFORME_SESION_2026-09-27.md)

---

## Estructura del grafo de conocimiento (`es/red/stasispath.yaml`)

Un archivo por edición se edita a mano; todo lo demás se regenera.

| Capa | Contenido |
|---|---|
| `fuentes` | Catálogo de literatura primaria F1–F93 (91 activas), con DOI, método y el valor medido concreto que aporta cada una. |
| `parametros` | Constantes biofísicas con rango de incertidumbre empírica (Q10, Tg, CCR, tensión de fractura, difusividad del CPA). |
| `cotas` | Desigualdades termodinámicas y límites cinéticos C1–C11, cada una evaluada en **todas** las esquinas de incertidumbre. |
| `afirmaciones` | Ontología (O1–O4), magnitudes (G1–G8), fronteras (X1–X2) y leyes (L1–L45), cada una con su cadena de derivación. |
| `vias` | Rutas candidatas V01–V27, con la ventana numérica que tienen o no tienen. |
| `preguntas` | Las preguntas canónicas Q1–Q22 y sus veredictos. |
| `preregistro` | Los cinco diseños experimentales congelados (P15, P18, P19, P20, P21). |
| `derivadas` | Magnitudes **calculadas, nunca escritas a mano**. |

### Etiquetas de estatus

Cada nodo lleva una, y un nodo nunca supera a su dependencia más débil.

| Etiqueta | Significado |
|---|---|
| **M** | *Mate* — robusto en todas las esquinas de incertidumbre. El veredicto no depende de qué extremo de ningún rango se tome. |
| **V** | Verificado frente a una fuente primaria con revisión por pares leída entera. |
| **P** | Prior — apoyado solo en una fuente secundaria, una revisión o un resumen. |
| **A** | Abierto — sin evidencia suficiente en ningún sentido. La frontera X2 vive aquí. |
| **ROTO** | Una afirmación que este marco hizo antes y que ha refutado después. |

---

## Reglas epistémicas

Cinco reglas gobiernan el desarrollo. La segunda es la que carga el peso.

1. **R1 — Mandan las dependencias.** Un nodo derivado nunca tiene más certeza que su premisa más débil. Excepción deliberada: un preregistro no pierde estatus porque lo que prueba esté abierto; ese es su propósito.
2. **R2 — Invarianza de reglas.** Los umbrales de falsación están sellados bajo SHA-256. **Nunca se reformula el tablero ni se mueve un umbral preregistrado para salvar la narrativa.** Editar un umbral congelado dispara una alarma en el motor.
3. **R3 — Conservadurismo en las esquinas.** Toda afirmación física debe cumplirse a la vez en el extremo más optimista y en el más pesimista de cada rango medido.
4. **R4 — Avanzar por las casillas críticas en orden.**
5. **R5 — Parar cuando el veredicto está forzado.** *Si el rival tiene una fuga, no hay mate.*

> [!CAUTION]
> **Tolerancia cero con el autoengaño.**
> * **No** afirmamos que la estasis reversible de cuerpo entero en mamíferos adultos no hibernantes sea viable hoy. Ningún protocolo publicado la logra.
> * La extrapolación de órgano aislado (E3) a cuerpo entero (E0) se trata formalmente como una **conjetura teórica abierta**, no como un resultado.
> * La frontera X2 **sigue abierta `[A]`** y se considerará cerrada solo cuando un laboratorio reporte LTP durable en tejido cerebral vitrificado con un crioprotector de baja velocidad crítica (CCR ≤ 0,43 °C/min).

---

## Cómo ejecutarlo

```bash
(cd es && python3 red/motor.py)                 # recalcula la edición española y regenera sus documentos
(cd en && python3 red/motor.py)                 # recalcula la edición inglesa
python3 tools/check_parity.py                   # los grafos EN y ES coinciden en números, estatus y textos congelados
python3 tools/check_numbers.py                  # cada documento generado EN coincide numéricamente con su gemelo ES
python3 tools/gen_p19_osf.py                    # regenera el formulario de P19 desde el texto congelado
cd stasispath-tools && python3 -m pytest -q     # 79 tests
```

La autoauditoría (`red/sfsa_auditoria.py`) es opcional y necesita el paquete SFSA: instálalo o ejecútala con `SFSA_PATH=/ruta/a/sfsa/python python3 red/sfsa_auditoria.py`. Sin él, el script se detiene con un mensaje claro; nada más depende de él.

---

## Qué aporta, y qué no

**No aporta:** una sola medición, una ley física nueva ni un experimento ejecutado. Todo lo que contiene lo midió otro.

**Sí aporta:**
- una **especificación de diseño** que redirige la búsqueda: el requisito es 0,425 °C/min, no los 0,10 de M22;
- la frontera X2 **cuantificada en dos ejes**, función y escala, con intersección vacía (el gráfico viabilidad–estabilidad es de Fahy, 2004; los ejes de 2026 son nuestros);
- **resultados negativos firmes**: la preservación de cuerpo entero no es viable por conducción, y el tronco no se puede enfriar;
- un **método reutilizable** donde una contradicción se señala en lugar de promediarse.

El valor de este trabajo no lo decide el 97,3 %. Lo decide que alguien meta un disolvente candidato en un calorímetro. **Un marco no puede sustituir al instrumento.**

---

## Licencia

Publicado para investigación académica y científica bajo **CC BY-NC 4.0**. Quedan prohibidos la explotación comercial, la reventa y la relicencia propietaria. Ver `LICENSE`.

## Cita

> Malia, A., con Claude (Anthropic) y Grok (xAI) (2026). *StasisPath: A Quantitative Biophysical Framework for Metabolic Depression, Ice Avoidance, and the Thermodynamic Limits of Reversible Mammalian Preservation.* StasisPath Initiative.
