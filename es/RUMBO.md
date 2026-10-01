<!-- AUTO-GENERADO por red/rumbo.py. NO EDITAR A MANO. -->
# StasisPath: rumbo — qué cerrar, en qué orden y cuánto vale

**Progreso actual: 97.3 %. Meta fijada en el YAML (`rumbo.meta`): 98.0 %.**

El marco simula en memoria el cierre de cada nodo abierto y repropaga los estatus con la regla del motor. **No cierra nada**: un nodo sólo sube cuando entra su dato o su fuente en `red/stasispath.yaml`.

- **Techo si se cerrara TODO lo abierto:** 100.0 %. Lo que queda por encima no depende de nodos abiertos, sino de preguntas o ramas que nadie ha medido.
- **Camino mínimo hacia la meta:** 1 cierres llevan de 97.3 % a 98.7 % (meta alcanzada).
- 9 nodos abiertos **no suben el total por sí solos** (otro nodo más débil los sujeta). Por eso el orden importa.

## Camino voraz (cada paso, el cierre que más sube con lo anterior ya hecho)

| # | nodo | tipo | estatus | gana | acumulado | qué lo cierra |
|---|---|---|---|---|---|---|
| 1 | X2 | afirmacion | A | +1.35 | 98.7 % | [laboratorio] calorimetría (DSC) de la CCR de los NADES; si ≤ 0.426 cierra sin P19. Alternativa: ejecutar P19 |

## Ranking individual (cada nodo cerrado solo)

| nodo | tipo | estatus | gana solo | qué lo cierra |
|---|---|---|---|---|
| X2 | afirmacion | A | +1.35 | [laboratorio] calorimetría (DSC) de la CCR de los NADES; si ≤ 0.426 cierra sin P19. Alternativa: ejecutar P19 |
