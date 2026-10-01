# -*- coding: utf-8 -*-
"""TANDA 49 - COTAS CON NUMEROS del cluster de campos lejanos (TRIADA, paso 2).

Dos cotas, ambas aritmetica pura sobre datos que YA estan en la red:

 (A) L35 - NADES: el compromiso toxicidad<->vitrificacion queda cerrado por los DOS lados
     con una sola primaria (F80 [V], PDF leido en la tanda 46 y releido en la 49).
 (B) L31 - vitrificacion SIN crioprotector: el dato de F76 se cruza con el que ya estaba
     dentro del PDF de F6 (McKenzie 2024, pag. 8 y 13, citando a Studer et al. 2014) y que
     nadie habia extraido. Corrige por lo alto el techo de espesor que L31 tenia escrito.

Ningun umbral, valor central ni rango se toca (R2). No se inventa ningun dato (R5).
Uso: python3 20_cotas/cota_campos_lejanos.py
"""
import math

print(__doc__)
print("=" * 78)

# ---------------------------------------------------------------- (A) L35 / NADES
print("\n(A) L35 - NADES: distancia a la CCR que exige un cerebro humano\n")

# Dato 1 de F80 (Jesus, Duarte & Paiva 2022, Sci Rep 12:8095; PDF en 10_fuentes/pdf/):
# enfriando en DSC a 30 C/min, las mezclas acuosas de NADES al 50 % p/v CRISTALIZAN
# (Tc onset entre -26.6 y -32.3 C; agua destilada -23.7 C). => su CCR es > 30 C/min.
CCR_NADES_min = 30.0          # C/min, COTA INFERIOR (cristalizan a esa velocidad)

# Dato 2, umbral que ya estaba en la red (C3 -> L44, cota mate): un cerebro humano
# vitrificado por conveccion a LC 4 cm necesita CCR <= 0.426 C/min.
CCR_cerebro = 0.426           # C/min

factor = CCR_NADES_min / CCR_cerebro
decadas = math.log10(factor)
print(f"  CCR de los NADES al 50 % p/v      > {CCR_NADES_min:.1f} C/min   (F80, DSC)")
print(f"  CCR que exige un cerebro humano  <= {CCR_cerebro:.3f} C/min  (C3/L44, mate)")
print(f"  => faltan al menos un factor {factor:.1f}  =  {decadas:.2f} decadas")
assert factor > 70, "la distancia no puede ser menor que x70"

# Dato 3 de F80, NUEVO en la tanda 49 (pag. 6 del PDF, Discussion). Los autores explican
# POR QUE no pasan del 50 % p/v, con sus palabras: "The reason of using 50% (w/v) instead
# of higher percentages of NADES is highly related to their high toxicity at those
# concentrations, as well as, their high viscosity which would difficult the diffusion
# process during freezing."
# => el 50 % p/v NO es una eleccion de conveniencia: es el TECHO DE TOXICIDAD que los
#    propios autores declaran. Y es justo la concentracion a la que la CCR ya falla x70.
print("\n  Los dos lados del compromiso, medidos en el MISMO articulo:")
print("    lado vitrificacion: al 50 % p/v la CCR falla por un factor >= 70")
print("    lado toxicidad    : por encima del 50 % p/v los autores declaran 'high toxicity'")
print("  => para cerrar las 1.85 decadas habria que SUBIR la concentracion por encima")
print("     de un valor que la propia primaria llama toxico. El compromiso esta INTACTO.")
print("  Nota: NO se convierte 50 % p/v a molaridad, porque los NADES son mezclas de")
print("        masa molar variable y hacerlo exigiria suponer una composicion (R5).")

# ---------------------------------------------------------------- (B) L31 / sin CPA
print("\n" + "=" * 78)
print("\n(B) L31 - vitrificar SIN crioprotector: cruce de F76 con el PDF de F6\n")

CCR_agua_pura = 6.4e6         # K/s, medida directa, cero hielo cristalino (F76)
CCR_extrap_1pc = 2.5e5        # K/s, extrapolacion a concentracion 0 para <1 % de hielo (F76)
CCR_studer = 2.0e5            # K/s, "faster than 200,000 K/s" en tejido sin CPA
#                               (F6, pag. 8, citando Studer et al. 2014)

r = CCR_extrap_1pc / CCR_studer
print(f"  F76, medida directa (cero hielo)        : {CCR_agua_pura:.2e} K/s")
print(f"  F76, extrapolacion a <1 % de hielo      : {CCR_extrap_1pc:.2e} K/s")
print(f"  F6/Studer 2014, tejido sin CPA          : {CCR_studer:.2e} K/s")
print(f"  => las dos cifras practicas coinciden dentro de un factor {r:.2f}")
print(f"  => la cifra de cero hielo es {CCR_agua_pura/CCR_extrap_1pc:.0f}x mas exigente que la practica")
assert 1.0 <= r <= 2.0, "las dos estimaciones practicas deberian coincidir en el mismo orden"

# Espesor: lo que L31 tenia escrito era "~3 um" (espesor de muestra de criomicroscopia,
# F76). El PDF de F6 (pag. 8) da los numeros de la CRIOFIJACION de TEJIDO, que son otros:
esp_criomicro_um = 3.0        # um, muestra de cryo-EM (F76)
esp_plunge_um = 20.0          # um, profundidad de vitrificacion por inmersion (F6/Studer)
esp_hpf_um = 200.0            # um, con congelacion a alta presion ~2000 bar (F6/Studer)
factor_presion = 100.0        # la alta presion baja la CCR necesaria x100 (F6/Studer)

LC_cerebro_cm = 4.0
LC_cerebro_um = LC_cerebro_cm * 1e4
print(f"\n  espesor: cryo-EM {esp_criomicro_um:.0f} um · inmersion en tejido {esp_plunge_um:.0f} um"
      f" · alta presion {esp_hpf_um:.0f} um")
print(f"  el techo mas alto sin CPA ({esp_hpf_um:.0f} um) esta a un factor"
      f" {LC_cerebro_um/esp_hpf_um:.0f} de LC = {LC_cerebro_cm:.0f} cm")
print(f"  y en velocidad (tasa ~ 1/LC^2, C3): factor {(LC_cerebro_um/esp_hpf_um)**2:.1e}")
print(f"  la alta presion (2000 bar) compra un factor {factor_presion:.0f} de CCR:")
print(f"    {CCR_studer:.1e} K/s -> {CCR_studer/factor_presion:.1e} K/s, que sigue estando a")
print(f"    {(CCR_studer/factor_presion)*60/CCR_cerebro:.1e} del umbral del cerebro ({CCR_cerebro} C/min)")
assert LC_cerebro_um / esp_hpf_um == 200.0

print("\n  => CONCLUSION de (B): el techo de espesor sin crioprotector no es ~3 um sino")
print("     10-20 um por inmersion y ~200 um con alta presion. La via sigue sin escalar")
print("     (factor 200 en espesor, 4e4 en velocidad), asi que NINGUN veredicto cambia:")
print("     es una correccion de una imprecision propia, al alza, del patron L33.")
print("     Y deja una palanca sin catalogar en el marco: la PRESION como variable que")
print("     baja la CCR x100 (F6/Studer). No se cablea como dependencia de nadie porque")
print("     el dato viene de una revision [P] citando a un tercero.")

print("\n" + "=" * 78)
print("TODAS LAS ASERCIONES PASAN. Ningun umbral movido; ningun dato inventado.")
