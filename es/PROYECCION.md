<!-- AUTO-GENERADO por red/proyeccion.py. NO EDITAR A MANO. -->
# StasisPath: proyección condicional al cierre

> **Esto NO es progreso.** El marco está en **97.3 %** y sigue ahí hasta que alguien mida. Lo que hay debajo es un **escenario condicional**: cómo quedaría *si* cada predicción se confirma. Un escenario no es un logro. Dejar que el código se redondee solo al 100 % sería fabricar avance, y por eso no se hace.

Lo que sí aporta: **hace el marco enteramente falsable**. Cada predicción lleva valor, dispersión y **qué resultado la refutaría**.

## Las dos campanas

| campana | n | dispersión mediana | rango |
|---|---|---|---|
| **lo que tenemos** | 22 parámetros verificados | ±14.7 % | del ±2.78 % al ±50 % |
| **lo que necesitamos** | 4 predicciones abiertas | ±55 % | del ±45 % al ±120 % |

**Lo que dice la comparación:** lo que ya tenemos está medido con una dispersión mediana del **±14.7 %**; lo que falta lo predecimos con **±55 %**, es decir **3.74 veces más ancho**. ⇒ **No hace falta medir mejor de lo que ya medimos**: basta con medir lo que falta **con la misma calidad** que lo que ya está, y el marco se cierra.

## Lo que el marco predice, y qué lo refuta

| id | magnitud | predicción | ±1σ | de dónde sale | qué la REFUTA |
|---|---|---|---|---|---|
| I1 | daño del brazo frío de P19 | 0.142  | ±55 % | Arrhenius × punto de German (DERIVACION) | un daño > 0.25 refuta la derivación; > 0.22 además haría fallar a P19 |
| I2 | CCR de los NADES | 0.3 °C/min | ±120 % | cota superior por inmersión + orden de los CPA conocidos | una CCR > 0.426 deja el cerebro humano fuera y obliga a ejecutar P19 |
| I4 | τ_eq humano con reperfusión óptima | 17 min | ±45 % | invariancia entre especies (T1 del escalado) | un valor < 12.5 min refutaría la invariancia; > 60 min contradiría a la gata de Hossmann |
| I5 | J de nucleación a −6 °C | 0.57 /L·h | ±50 % | ajuste con los dos puntos del hígado de rata | una J > 0.85 impide llegar a 4 h con 95 % en hígado humano |
| X2 | ¿resuelve la química el cuello? | 1 veredicto | ±0 % | B1: ambos caminos predicen PASA | que P19 dé LTP ≤ 110 % con el control positivo válido |

## Escenario de cierre (condicional, no logrado)

| concepto | valor | naturaleza |
|---|---|---|
| Estado real hoy | 97.3 % | medido |
| Si se confirma la CCR de los NADES (cierra X2, V26, F80) | +1.3 | **escenario simulado** |
| Si además se confirma I5 (L41, V27, F85, F22) | +0.0 | **escenario simulado** |
| **Techo del escenario de predicciones** | **98.7 %** | **escenario simulado** |
| No cubierto por ninguna predicción | 1.3 % | fuentes secundarias y vías sin dato (ver RUMBO.md) |
| Techo si se cerrara TODO lo abierto | 100.0 % | RUMBO.md |

> **Las predicciones solas no cierran el marco.** Confirmarlas todas da 98.7 %; los **1.3 puntos** restantes no dependen de ninguna predicción sino de **leer fuentes primarias y conseguir datos de vías** que nadie ha publicado todavía. RUMBO.md los ordena por puntos. **Los puntos se simulan con la regla del motor; ya no se escriben a mano.**

## La autocorrección, que sí es real

Cuando llegue un dato para cualquiera de estas predicciones, el procedimiento es automático:

1. Se añade como parámetro o fuente en `red/stasispath.yaml` (una línea).
2. El motor recalcula cotas, derivadas, márgenes, triangulación y barrido.
3. **Si el valor cae fuera del rango predicho, la triangulación lo marca como contradicción** y señala qué ley del marco falla — que es exactamente lo que pasó con I1 y con el régimen isocórico de I5.

Eso es autocorrección: **el marco no se ajusta para encajar el dato, señala qué tendría que cambiar.**
