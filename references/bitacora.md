# Bitácora — veredictos y hallazgos

Historial de por qué el sistema es como es: qué se aprobó, qué se rechazó, qué
hipótesis se cayeron y qué bugs costaron una sesión descubrir.

**Este archivo es para las personas, no para el modelo.** Lo accionable ya está
destilado en `reglas-derivadas.md`, que es el que se lee al trabajar. Aquí se
guarda el razonamiento para poder auditarlo, contradecirlo o retomarlo.

Existe porque el modelo **no aprende entre conversaciones**: sus pesos no cambian
por ver piezas. Lo único que persiste es lo que queda escrito.

---

## 2026-07 · Convocatoria de coordinaciones, 5 variantes

Primer caso con señal real: se produjeron cinco variantes y se aprobaron dos.

| Variante | Veredicto | densidad | bloque macizo | acento |
|---|---|---|---|---|
| 1 · crema, lista numerada 01–05, Clawd audífonos | **aprobada** | 0.077 | 0.00 | 0.015 |
| 3 · naranja, tipográfica, puestos en píldoras | **aprobada** | 0.089 | 0.00 | 0.914 |
| 2 · blanco, Clawd hero, puestos en cajas | rechazada | 0.114 | 0.00 | 0.057 |
| 4 · crema con banda naranja | rechazada | 0.312 | 0.86 | 0.250 |
| 5 · naranja con tarjeta crema | rechazada | 0.379 | 0.90 | 0.622 |

Se probaron ocho variables. Solo una separa limpiamente los dos grupos.

### H1 · "Menos tinta gana" — RETRACTADA

Se derivó de estas 5 piezas propias y se cayó con la primera tanda de referencias
externas: los posts de @claudeai que sí gustan tienen densidad **0.74 a 0.93**.
La hipótesis decía que ≤0.09 era lo bueno.

Qué salió mal: la densidad era un *proxy* de otra cosa. Las dos piezas rechazadas
con densidad alta lo eran por meter un bloque de color plano; las referencias
tienen densidad alta por llevar fotos, capturas y objetos superpuestos. La
métrica no distinguía "bloque macizo aburrido" de "composición cargada de capas".

Se deja escrita en vez de borrarla porque el error es instructivo: **con n=5 y
ocho variables, que una separe los grupos no significa casi nada.**

De ahí salió la regla 3 de `reglas-derivadas.md`, que es la versión específica y
sobreviviente: lo que molesta es el contenedor de color grande, no la tinta.

### H4 · Sangrar del lienzo

| | contenido que toca el borde |
|---|---|
| Posts de @claudeai aprobados | 0.64 – 0.79 |
| Carteles de Builder Club | 0.00 – 0.30 |
| Las 5 variantes propias | 0.00 – 0.09 |

Explica por qué la variante 5 falló y la referencia equivalente funciona: es la
misma idea —fondo naranja con tarjeta clara encima— pero la tarjeta de la
referencia **sangra**, y la propia era un rectángulo redondeado flotando
centrado dentro del margen. Misma receta, resultado opuesto.

**Cuidado con la métrica:** `sangra` cuenta píxeles del borde que difieren del
color de la esquina. En una pieza de fondo naranja completo, el naranja no cuenta
aunque sea el diseño. Sirve para comparar piezas parecidas, no como número
absoluto que perseguir.

### H2 y H3

H2 · El fondo no predice el veredicto: útil por lo que descarta.
H3 · La decoración no puede ser un contenedor: confianza baja a propósito, un
solo par de casos. Es una dirección para probar, no una regla.

---

## 2026-08-15 · Reconstrucción de fondos y láminas

Se rehicieron `fondos.css`, `tratar_foto.py` y las catorce láminas tras perderse
el trabajo de agosto. **No son los archivos originales**: los nombres de clase y
los valores de velo se reconstruyeron desde la hoja de contacto aprobada y desde
las notas, no desde el código. Si aparece el original, gana él.

Al reescribir `fondos.css` se reintrodujo un bug que ya estaba documentado: el
`position:relative` forzado a los hijos de `.pieza` (regla 11 de
`reglas-derivadas.md`). Un bug documentado se reintroduce igual si la
documentación no está donde se escribe el código.

### Dos bugs más, encontrados al montar sobre fotos reales

1. **`url()` en custom property** (regla 12). Es la tercera variante del mismo
   fallo de rutas relativas en este proyecto.

2. **La regla de paleta de `validar.py` no contemplaba contenido fotográfico.**
   Una foto en gris, un duotono o un semitono producen decenas de tonos
   intermedios, y cada uno salía como fallo grave: trece en una sola lámina.
   Corregido excluyendo neutros de chroma menor a 18 que caen entre el oscuro y
   el crema — son valores intermedios de la propia rampa de marca, no colores
   ajenos. Con el ajuste, las dos piezas aprobadas siguen pasando la regresión y
   los dos hallazgos reales que quedaban seguían apareciendo: un `#eab8a3`
   inventado para la lámina 11 y un contraste de 1.8:1 en la 13.

---

## 2026-08-15 · Las catorce láminas, aprobadas

Replicadas del plano original y aprobadas por Ramses tras cuatro correcciones
suyas: bajar la saturación del duotono en 05, 11 y 13; oscurecer las
descripciones grises de la 02; y en la 06 centrar el texto en la zona limpia y
agrandarlo hasta llenarla. Son las reglas 6, 8, 9 y 10 de `reglas-derivadas.md`.

Guardadas como `referencias/aprobadas/lamina-*.webp`. El corpus pasa de 2 a 16
piezas, que es lo que hace que `regresion.py` signifique algo: con dos ejemplos
cualquier umbral se ajusta a un par de casos.

**Lo que dice el corpus nuevo sobre el sistema:**

- El sangrado dejó de ser un hallazgo general. De 16 piezas aprobadas, solo 5 no
  cruzan ningún elemento el borde; las otras 11 sangran, casi siempre por la
  foto. La distancia contra @claudeai que señalaba el validador en julio está en
  buena parte cerrada.
- Aparece un hallazgo de severidad media en 2 piezas: margen mínimo de 0 px. Son
  las de foto a sangre, donde el margen cero es la decisión, no el descuido. El
  validador no distingue sangrado deliberado de contenido pegado al canto, y por
  eso la regla es media y no alta. **No subirla sin resolver esa distinción.**

---

## 2026-08-15 · Compresión del corpus

Al adelgazar la skill de 57 a 17 MB se convirtió el corpus a WebP con pérdida, y
`regresion.py` marcó al instante un hallazgo grave en `lamina-11` que como PNG no
existía: contraste 3.0:1. De ahí la regla 13 de `reglas-derivadas.md`.

---

## Qué pedir en la siguiente ronda

Para que la muestra deje de ser anecdótica hacen falta referencias **externas**,
no solo variantes propias: piezas de otras cuentas que gusten, con una línea de
por qué. Y sirve igual —o más— cargar piezas que **no** gusten: sin
contraejemplos cualquier variable parece explicarlo todo.

Con unas 10 aprobadas y 10 rechazadas *externas*, las hipótesis de confianza
media pasan de plausibles a utilizables.

---

## 2026-09-15 · Reorganización v2

- `SKILL.md` pasó de ~3,900 a ~1,500 tokens. El `description:` del frontmatter
  bajó de ~250 palabras a 2 líneas: se carga en todas las sesiones, se use la
  skill o no.
- `gustos.md` se partió en `reglas-derivadas.md` (lo accionable, se lee al
  trabajar) y este archivo (el razonamiento, para personas).
- Todo lo de animación pixel art salió a una skill aparte, `clawd-animaciones`:
  `references/animacion-pixel.md`, `animar_pixel.py`, `clawd_caminando.py`,
  `assets/clawd/caminando/` y `assets/clawd/bandera/`.
  `vectorizar_pixelart.py` quedó copiado en las dos.
- Se resolvió la contradicción de titulares: `SKILL.md` mandaba Poppins mientras
  la evidencia del corpus (regla 5) decía serif. Ahora manda la serif.
- Copia de los archivos v1 en `v1/` para comparar antes de borrar.

### Los lockups corregidos estaban, pero invisibles

`claudetec` y `claudetec--claro` —la versión con la "e" corregida—
llevaban en `assets/logos-claudetec/` desde el 29 de agosto sin aparecer en ningún lado:
`assets-index.md` documentaba tres archivos (`duotono`, `oscuro`, `claro`) de los
que solo existía el primero, y `preparar_canva.py` pedía los dos inexistentes sin
quejarse porque el bucle saltaba en silencio lo que no encontraba.

Corregido: catálogo al día, SVG extraído del HTML que ya traía el vector completo,
script apuntando a los archivos buenos y avisando cuando un archivo declarado no
existe. **El duotono sigue con la "e" vieja** — hay que regenerarlo antes de
usarlo, y esa es la variante que la regla de marcas derivadas prefiere.

### Renombrado de los lockups — 16 de septiembre de 2026

Los cuatro lockups se llamaban `claudetec-e-negro`, `claudetec-e-blanco`,
`claudetec-duotono` y `claudetec-duotono-claro`. Mezclaban dos criterios en el
mismo sufijo: `-negro`/`-blanco` decían de qué color era el texto, `-claro` decía
sobre qué fondo iba. Y en las ilustraciones `--claro` ya significaba "para fondo
oscuro", asi que la misma palabra queria decir dos cosas.

Ahora hay un solo criterio, el fondo de destino:

| Antes | Ahora |
|---|---|
| `claudetec-e-negro` | `claudetec` |
| `claudetec-e-blanco` | `claudetec--claro` |
| `claudetec-duotono` | `claudetec--duotono` |
| `claudetec-duotono-claro` | `claudetec--duotono-claro` |

Se migraron tambien los cuatro veredictos del visor, que estaban guardados con
el nombre viejo. `lockup_variantes.py` regenera los cuatro SVG identicos byte a
byte tras el cambio, asi que el renombrado no tocó ningún dibujo.

**Si encuentras el nombre viejo en algún sitio, es de antes de esta fecha.**
