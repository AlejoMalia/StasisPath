# Cotas escritas antes de leer (TRIADA · MATEMÁTICA)

## C1 — Conducción limita el recalentamiento convectivo (Q5, Q7, Q11) · [M] condicionado a priors de CWR
Script: `20_cotas/cota_difusion.py`. t_dif ~ r²/α, α ≈ 1.3e-7 m²/s; recorrer 100 K (Tg → −20 °C).

| escala | tasa máx. en el centro | ¿supera CWR? (VS55 50 / VM3 3 / M22 0.4 °C/min [P]) |
|---|---|---|
| embrión 0.1 mm | ~8e4 °C/min | sí / sí / sí |
| tejido 1 mm | ~780 | sí / sí / sí |
| riñón rata ~1 cm | ~8 | no / sí / sí |
| órgano humano ~5 cm | ~0.3 | no / no / no |
| cabeza/torso ~12 cm | ~0.05 | no / no / no |

**Línea forzada:** a ≥ 5 cm, ningún CPA conocido se recalienta por superficie por encima de su CWR → el calentamiento **volumétrico** (nanowarming, RF, etc.) es obligatorio, y además la tasa debe ser **uniforme** o aparece gradiente → estrés térmico → fractura (Q7).
**Fugas a comprobar:** (a) CPA con CWR < 0.05 °C/min (implicaría toxicidad muy alta → Q6); (b) α distinto en un orden de magnitud (improbable). Si #4/#5 confirman CWR de M22 ≈ 0.4 °C/min, C1 pasa a [M] firme.

## C2 — Hipotermia sin cambio de fase no llega a días (Q8, Q9, Q12) · [M] con una fuga abierta
Script: `20_cotas/cota_q10.py`. Ventana ≈ 5 min × Q10^((37−T)/10), Q10 = 2.3 [P].
- 18 °C → ~24 min; 15 °C → ~31 min (coincide con el rango DHCA clínico 30–40 min [P], a verificar con #8).
- 0 °C → ~2 h; −10 °C (superenfriado) → ~4 h.
- 1 día exige ~−31 °C; 1 año ~−102 °C; 10 años ~−129 °C ≈ **por debajo de Tg (~−123 °C)**.

**Línea forzada:** para años, la supresión metabólica pasiva exige temperaturas bajo Tg → estado vítreo. Hipotermia profunda = vía de **minutos–horas**; vitrificación = única vía física para **años**.
**Fuga abierta (R1, no se cierra):** supresión metabólica **activa** (torpor/hibernación, Q10 aparente ≫ 2.3). Los hibernadores pasan semanas a ~2–5 °C pero con despertares periódicos; no hay dato de años. Queda como [A] hasta tener cifra.

## C3 — Muerte legal ≠ pérdida irreversible de información (Q2) · [P]
Muerte legal = cese irreversible de funciones circulatorio-respiratorias o encefálicas (criterio clínico, definido por *irreversibilidad con la medicina disponible*). La pérdida de información cerebral es un criterio **estructural** distinto (criterio "teórico-informacional"). Son magnitudes diferentes: la primera depende de la tecnología del momento; la segunda es la frontera física que StasisPath busca. Pendiente: fijar una magnitud medible para la segunda (p.ej. trazabilidad del conectoma por EM, Q15).

---
## Estado tras la lectura (2026-09-26)
- **C1 → [V]:** M22 CCR ~0.1 y CWR ~0.4 °C/min (F2), iguales al prior. VMP en riñón: CWR 55–70, nanowarming 72 °C/min (F1, F3). En rata, la convección (~8 °C/min a 1 cm) ya no bastaba, y por eso se usó nanowarming.
- **C2 → [V]:** la tabla de McCullough reproduce la cota con un error ≤ 1–2 min a todas las temperaturas. Fuga de torpor comprobada y cerrada para años (F10).
- **C3 (nueva) → [M]:** enfriamiento convectivo anclado en el dato medido de 3 L (script `cota_enfriamiento_cuerpo.py`). La predicción para hígado (0.70 °C/min) coincide con la de F2 (~0.6). VMP falla ya en riñón humano; M22 falla en el centro del tronco.
