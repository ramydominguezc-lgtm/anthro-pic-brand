# Veredictos

Qué aprobó y qué rechazó Ramses, con las medidas de cada pieza y **el motivo**.
Se anota con `scripts/veredictos.py`; esto se lee antes de componer, y sustituye
al corpus de imágenes que había hasta la v2.11.

Las medidas salen de `scripts/analizar_referencia.py`:

- **`aire_max`** — la franja horizontal completamente vacía más alta, en px.
- **`sangra`** — fracción del borde del lienzo que toca contenido.
- **`densidad`** — cuánta tinta hay.
- **`ejes`** — cuántas alineaciones izquierdas distintas.
- **`bloques`** — bandas horizontales de contenido que lee el ojo.

---

## La regla que salió de esta tabla

> **Ningún hueco vacío de más de 180 px** en una pieza 1080×1350.

Ninguna aprobada pasa de 177. Ninguna rechazada por acomodo baja de 251. Es el
único umbral que separa limpiamente los dos grupos, y **no se vio mirando las
piezas**: apareció comparando la columna. Si sobra sitio, crece la tipografía,
baja el objeto o entra una capa. No se deja el hueco.

Dos cosas que la tabla dice que **no** son el criterio:

- **La densidad no decide.** Las aprobadas van de 0.29 a 0.96. Hay piezas
  vacías buenas y piezas llenas buenas.
- **Los ejes tampoco, por sí solos.** La `post-06` corregida tiene dos ejes y
  está aprobada: la terminal desplazada a la derecha crea un segundo eje a
  propósito. Un eje de más es sospechoso, no un fallo.

### Dónde la métrica está ciega — leer antes de fiarse de un 0

`aire_max` mide filas **sin tinta**. Hay dos montajes donde no queda ni una, y
entonces devuelve 0 sin querer decir «no hay hueco»:

1. **Una trama que cubre el lienzo entero** (grano, semitono, retícula densa).
2. **Una foto a sangre completa**, con o sin velo.

Se coló de verdad: la `06-cita` v1 daba `aire_max = 0` con **420 px muertos** a
la vista, porque la trama de grano ponía tinta en las 1350 filas. Y la `08-tira`
v1 daba 0 con **337 px muertos**, porque la métrica tomaba como fondo el color
de la esquina —que caía dentro de una foto— y así el fondo oscuro entero contaba
como tinta.

Las dos cosas están corregidas en `analizar_referencia.py` desde la v2.14: el
fondo es ahora el color **más frecuente**, no el de la esquina, y una fila
cuenta como contenido si tiene tinta de verdad y no un píxel suelto. Lo que no
se puede arreglar es el caso 1 y 2: ahí el script marca **`aire_fiable = False`**
y hay que medir la pieza renderizada sin la trama, o mirarla.

**Si ves `aire_max = 0`, comprueba `aire_fiable` antes de dar la pieza por buena.**

---

## Tabla

Las medidas son todas de la métrica corregida (v2.14). Las dos piezas
rechazadas marcadas con `†` conservan su número viejo: sus archivos se borraron
al rechazarlas y no se pueden volver a medir.

| Pieza | Fecha | Veredicto | aire_max | sangra | densidad | ejes | bloques | Por qué |
|---|---|---|---|---|---|---|---|---|
| `01-foto-capas` | 2026-09-17 | **aprobada** | 0 | 0.39 | 0.476 | 1 | 1 | foto de contexto atenuada + foto nítida encima, chip a caballo del canto |
| `02-foto-ficha` | 2026-09-17 | **aprobada** | 83 | 0.0 | 0.334 | 1 | 6 | ficha solapando la esquina de la foto: el desajuste crea la profundidad |
| `03-foto-sangre` | 2026-09-17 | **aprobada** | 0 *(no fiable)* | 1.0 | 0.963 | 1 | 1 | foto a sangre completa con velo; titular encima |
| `04-foto-arriba` | 2026-09-17 | **aprobada** | 116 | 0.4 | 0.475 | 4 | 11 | lienzo partido en dos mitades, foto a sangre arriba |
| `05-par-fotos` | 2026-09-17 | **aprobada** | 172 | 0.0 | 0.417 | 2 | 6 | dos fotos distintas en fila, cada una con su ficha |
| `collage-demo` | 2026-09-17 | **aprobada** | 0 | 0.93 | 0.668 | 1 | 1 | collage que se monta solo; tarjeta central fija en pixel, el resto entra por turnos |
| `post-06-terminal-negra (v1)` | 2026-09-17 | **rechazada** † | 251 | 0.0 | 0.398 | 2 | 7 | terminal a todo el ancho y centrada, letra de 29 px, 251 px muertos debajo |
| `post-06-terminal-negra` | 2026-09-17 | **aprobada** | 60 | 0.43 | 0.523 | 2 | 6 | terminal desplazada abajo y a la derecha, sangrando; letra de 44 px; Clawd caminando sobre su canto |
| `post-07-web-chat (v1)` | 2026-09-17 | **rechazada** † | 579 | 0.0 | 0.301 | 2 | 5 | ventana arriba y el 40 % inferior naranja vacío: el peor hueco de la tanda |
| `post-07-web-chat--celeste` | 2026-09-17 | **aprobada** | 92 | 0.35 | 0.489 | 3 | 9 | titular grande arriba, ventana anclada abajo sangrando por derecha y por abajo |
| `post-08-cifra-cintas` | 2026-09-17 | **rechazada** † | 0 | 0.77 | 0.959 | 1 | 1 | una cifra gigante ocupando el lienzo entero; no falla por aire, falla por contenido |
| `post-09-ilustracion` | 2026-09-17 | **rechazada** † | 166 | 0.01 | 0.18 | 3 | 6 | ilustración sola en medio del lienzo, tres ejes distintos |
| `post-10-clawd` | 2026-09-17 | **rechazada** † | 293 | 0.41 | 0.366 | 2 | 8 | mismo esqueleto que las otras cuatro de recursos gráficos; 293 px muertos |

### Tanda 02 — diez piezas con foto, una geometría cada una

Veredicto de Ramses del 17/09, **cerrado**: las diez aprobadas. Sobre las tres
rehechas dijo *«no son las mejores pero pasan»*, así que entran con esa nota —
se pueden usar, y si aparece una geometría mejor para esos tres encargos,
sustituirlas no rompe nada.

| Pieza | Veredicto | aire_max | sangra | densidad | ejes | bloques | Por qué |
|---|---|---|---|---|---|---|---|
| `01-rejilla` | **aprobada** | 167 | 0.35 | 0.509 | 3 | 5 | retícula irregular; el titular ocupa una celda, no flota sobre una foto |
| `02-corte` | **aprobada** | 114 | 0.52 | 0.607 | 2 | 6 | corte diagonal con la foto incrustada; ficha de datos a caballo del corte |
| `03-circulo` | **aprobada, corregida** | 56 | 0.31 | 0.344 | 4 | 8 | cuarto de círculo con el texto en L. Corrección: los bullets pasaron de 26 a 32 px |
| `04-columna` | **aprobada** | 0 | 0.4 | 0.404 | 1 | 1 | columna de foto a sangre de altura completa contra fondo oscuro |
| `05-ventana` | **aprobada** | 46 | 0.38 | 0.598 | 2 | 12 | la foto es el contenido de una ventana de navegador |
| `06-cita` (v1) | **rechazada** | 0 *(no fiable)* | 0.0 | — | — | — | «no le entiendo»: la cita la firmaba un portátil porque no hay personas en el banco de fotos; la comilla pisaba el rótulo; 420 px muertos que la trama de grano escondió |
| `06-cita` (v2) | **aprobada, «pasa»** | 153 | 0.14 | 0.292 | 4 | 11 | la frase se parte en dos y una banda de foto a sangre pasa por en medio; la firma es texto, sin retrato falso |
| `07-cinta` (v1) | **rechazada** | 78 | 0.6 | — | — | — | la foto era la portada de un libro que pone «Symbol» en grande —una segunda marca dentro de la pieza— y no hablaba de las 312 personas; los porcentajes acababan pegados al logo |
| `07-cifra` (v2) | **aprobada, «pasa»** | 95 | 0.56 | 0.646 | 2 | 5 | la cifra manda, en pixel; foto de aula vacía (que sí habla de aforo); franja oscura maciza con los datos al pie |
| `08-tira` | **aprobada, «pasa»** | 177 | 0.36 | 0.295 | 2 | 13 | la idea sí, el acomodo no: 337 px muertos. La lista pasa de dos columnas apretadas al pie a cuatro renglones que ocupan el tercio central, cada uno con su dato a la derecha |
| `09-indice` | **aprobada** | 0 | 0.71 | 0.32 | 1 | 1 | lista numerada de carrusel con la foto anclando la esquina inferior |
| `10-pixel` | **aprobada, corregida** | 34 | 0.12 | 0.478 | 2 | 4 | foto a sangre + tarjeta pixel. Corrección: la pixel redondeada no se leía → Press Start 2P, y Clawd camina sobre el canto de la tarjeta (sale también en MP4) |

---

## Lo que ninguna medida ve

Gracia, ritmo, si el chiste visual funciona, si el tono le habla a la audiencia.
Para eso está la columna **Por qué**, y para eso están las imágenes de
`referencias/inspiracion/`, que se miran pero no se miden.

Cinco motivos recurrentes de rechazo que no tienen número y conviene releer:

1. **Todas las piezas de la tanda comparten esqueleto.** Rótulo, titular, un
   objeto centrado, nota, pie, repetido cinco veces. Hundió las cinco piezas de
   recursos gráficos del 17/09. De una referencia se copia el número, no el
   acomodo.
2. **El texto de terminal, pequeño.** Leer monoespaciada de 29 px sobre negro da
   pereza y nadie lo hace. Mínimo 40 px y cinco líneas contadas.
3. **Una ventana centrada con hueco debajo.** El objeto flota en medio del
   lienzo y el resto es color. Va desplazado y sangrando por un borde.
4. **La foto no habla de lo que dice el texto.** Hundió la `07-cinta`: un dato
   sobre 312 personas ilustrado con la portada de un libro. Peor todavía si la
   foto trae letras: esa portada metía la palabra «Symbol» a 200 px dentro de
   una pieza de marca. **Antes de colocar una foto, leerla: qué pone y de qué
   habla.**
5. **Firmar una voz con algo que no es una voz.** Hundió la `06-cita`: un
   testimonio con un retrato que era un portátil. Si el material no da caras, la
   cita se firma con texto. No se disimula con una ficha.

---

## Cómo anotar una pieza

```bash
python3 scripts/veredictos.py salida/post-06-terminal-negra.png \
        --veredicto aprobada --porque "terminal desplazada, Clawd encima"
```

Una pieza, una fila: si ya estaba, se sustituye. **Una pieza rechazada no se
guarda como archivo**, solo su fila — el archivo pesa y la fila es lo que
enseña. Las aprobadas que además sirven como material publicable se copian a
`piezas-aprobadas/`.
