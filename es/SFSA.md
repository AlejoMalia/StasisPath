<!-- AUTO-GENERADO por red/sfsa_auditoria.py. NO EDITAR A MANO. -->
# StasisPath x SFSA: auditoria de premisas, dimensiones y valor de informacion

> Este modulo **no puede subir el porcentaje**: no escribe en `stasispath.yaml`. Solo audita.
> Lo que encuentre, o baja el numero o lo anota con una salvedad.

## AIE — integridad de supuestos

7 premisas registradas, auditadas contra 12 estados reales del marco.

| estado | premisa | criticidad | diagnostico |
|---|---|---|---|
| `organo:riñón` | Exponente n=2 no verificado experimentalmente | **WARNING** | exp_LC=2.0 se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE |
| `organo:riñón` | Densidad implicita en LC_esfera | **WARNING** | LC_esfera convierte gramos en cm sin declarar densidad: asume rho = 1 g/cm3 en silencio |
| `organo:corazón` | Exponente n=2 no verificado experimentalmente | **WARNING** | exp_LC=2.0 se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE |
| `organo:corazón` | Densidad implicita en LC_esfera | **WARNING** | LC_esfera convierte gramos en cm sin declarar densidad: asume rho = 1 g/cm3 en silencio |
| `organo:hígado` | Exponente n=2 no verificado experimentalmente | **WARNING** | exp_LC=2.0 se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE |
| `organo:hígado` | Densidad implicita en LC_esfera | **WARNING** | LC_esfera convierte gramos en cm sin declarar densidad: asume rho = 1 g/cm3 en silencio |
| `organo:cerebro` | Exponente n=2 no verificado experimentalmente | **WARNING** | exp_LC=2.0 se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE |
| `organo:cerebro` | Densidad implicita en LC_esfera | **WARNING** | LC_esfera convierte gramos en cm sin declarar densidad: asume rho = 1 g/cm3 en silencio |
| `organo:cuerpo_entero` | Geometria esferica de LC | **WARNING** | LC=V/A se calculo con formula de esfera (r/3) sobre una pieza 'cilindro'; un cilindro da r/2, es decir LC 1.5x mayor y tasa 2.25x menor |
| `organo:cuerpo_entero` | Exponente n=2 no verificado experimentalmente | **WARNING** | exp_LC=2.0 se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE |
| `organo:cuerpo_entero` | Densidad implicita en LC_esfera | **WARNING** | LC_esfera convierte gramos en cm sin declarar densidad: asume rho = 1 g/cm3 en silencio |
| `organo:páncreas` | Exponente n=2 no verificado experimentalmente | **WARNING** | exp_LC=2.0 se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE |
| `organo:páncreas` | Densidad implicita en LC_esfera | **WARNING** | LC_esfera convierte gramos en cm sin declarar densidad: asume rho = 1 g/cm3 en silencio |
| `C2:T10y (templado)` | Q10 aplicado por debajo de Tg | **FAIL_STOP** | T=-129.0 C esta por debajo de Tg=-123 C: no hay agua liquida, no hay metabolismo y por tanto Q10 no esta definido ahi |
| `C2:T10y (templado)` | Q10 dentro del rango medido | **WARNING** | T=-129.0 C: ningun Q10 de la red se midio por debajo de -10 C; esto es extrapolacion, no medicion |
| `C2:T10y (templado)` | Exponente n=2 no verificado experimentalmente | **WARNING** | exp_LC=2.0 se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE |
| `C2:T10y (frio)` | Q10 dentro del rango medido | **WARNING** | T=-73.7 C: ningun Q10 de la red se midio por debajo de -10 C; esto es extrapolacion, no medicion |
| `C2:T10y (frio)` | Exponente n=2 no verificado experimentalmente | **WARNING** | exp_LC=2.0 se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE |
| `C2:w0` | Exponente n=2 no verificado experimentalmente | **WARNING** | exp_LC=2.0 se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE |
| `C3:anclaje F2` | Exponente n=2 no verificado experimentalmente | **WARNING** | exp_LC=2.0 se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE |
| `I5:J higado rata` | Regimen de presion en la nucleacion | **SWITCH_MODEL** | J medida en regimen 'isocorico' comparada con una cota isobarica; el isocorico suprime la nucleacion y no son intercambiables |
| `I5:J higado rata` | Exponente n=2 no verificado experimentalmente | **WARNING** | exp_LC=2.0 se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE |
| `escalado global` | Exponente n=2 no verificado experimentalmente | **WARNING** | exp_LC=2.0 se usa en TODO el escalado y P21 (que lo mide) esta PENDIENTE |

**23 violaciones** sobre 12 estados.

## UDE — homogeneidad dimensional

| formula | dimension resultante | coherente |
|---|---|---|
| `C1  r* = sqrt(alpha*dT/CWR)` | cm^2 bajo la raiz -> cm | OK |
| `C3  tasa = anc_rate*(anc_LC/LC)^n` | razon adimensional x C/min -> C/min | OK |
| `C6  t_latente = L_f*m/(P)` | J/(J/s) -> s | OK |
| `sigma_th <= 2*sigma*alpha*(1-nu)/(E*beta*L^2)` | MPa*cm2/min / (MPa*K^-1*cm2) -> K/min | OK |
| `LC_esfera = (3m/4pi)^(1/3)/3` | g^(1/3) DECLARADO cm | **NO** |

Comprobacion de control (g vs cm): Incompatible dimensions: 'g' has DimensionVector(mass=1, length=0, time=0, temp=0, amount=0, current=0, luminous=0) vs 'cm' has DimensionVector(mass=0, length=1, time=0, temp=0, amount=0, current=0, luminous=0)

## VOI — que medir primero

EVOI alto = la medicion tiene probabilidad real de **cambiar el veredicto**. Coste en unidades relativas (P19 = 20).

| candidato | EVOI | coste | EVOI/coste | recomendacion | que es |
|---|---|---|---|---|---|
| I2 · DSC de los NADES | 0.988 | 1.0 | **0.99** | `COMPUTE` | calorimetria, dias, ~1 k |
| P21 · exponente n | 0.241 | 0.5 | **0.48** | `COMPUTE` | 7 bolsas de agua y un termopar |
| I5 · J a -6 C | 0.419 | 12.0 | **0.03** | `USE_CHEAP_SURROGATE` | nucleacion en higado, meses |
| I4 · tau_eq humano | 1.000 | 30.0 | **0.03** | `USE_CHEAP_SURROGATE` | serie clinica, anos |
| P19 · LTP en rodaja | 0.179 | 20.0 | **0.01** | `USE_CHEAP_SURROGATE` | electrofisiologia completa |
