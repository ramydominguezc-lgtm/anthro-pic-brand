# Capas, ventanas y acomodo de imágenes

El modo de fallo real de esta skill es la pieza de **una sola capa**: fondo
plano, un gráfico, texto encima. Sale correcta y muerta. Las referencias de
@claudeai y de los Builder Clubs tienen tres o cuatro capas.

Todo lo de aquí vive en `assets/templates/capas.css`, que se importa **después**
de `_base.css`:

```html
<link rel="stylesheet" href="_base.css">
<link rel="stylesheet" href="capas.css">
```

## La excepción de la sombra

**Aprobada por Ramses el 17/09/2026.** No es un pendiente: es regla.

El sistema dice **«nada de sombras suaves»**. Eso se escribió contra el glow y el
drop-shadow decorativo, y sigue valiendo para texto, iconos y botones.

**Una tarjeta o una ventana que flota sí lleva sombra**, porque sin ella no se
lee como capa: es un rectángulo pegado. Está acotada a dos tokens,
`--sombra-baja` y `--sombra-alta`, y solo la llevan `.tarjeta` y las
`.ventana-*`. Evidencia: las piezas oficiales de Anthropic la usan en todos sus
paneles flotantes.

Lo mismo con el redondeo: `--radio-foto` son 14 px. **Discreto no es píldora.**

---

## 1 · Cintas

Una franja de color que cruza el lienzo entero, arriba o abajo. Es la forma más
barata de tener una segunda capa: no añade ningún objeto.

```html
<div class="cinta cinta-abajo cinta--crema"></div>
```

Modificadores: `--crema`, `--oscura`, `--verde`, y `--diagonal` para un corte
inclinado (recto, no degradado).

Va detrás del contenido con `z-index:-1` dentro del `isolation:isolate` de
`.pieza`. **No le pongas `position:relative` a los hijos de `.pieza`** — es la
trampa 11 de `reglas-derivadas.md`.

## 2 · Tarjetas flotantes

```html
<div class="tarjeta tarjeta--alta">…</div>
```

`--crema` la deja sin sombra sobre fondo claro; `--oscura` invierte el texto.

**La ficha que solapa una foto** es el recurso más útil de este grupo: una
tarjeta que sale del borde inferior de la imagen, desplazada hacia fuera y hacia
abajo. Ese desajuste es lo que crea la profundidad — alineada no funciona.

```html
<div class="foto-con-ficha">
  <img src="…">
  <div class="ficha">
    <div class="rotulo">Expedition FEMSA</div>
    <p>Sábado 3 de octubre, de 9:00 a 20:00.</p>
  </div>
</div>
```

Para dos fotos en fila, cada una con su ficha: `.par-fotos`.

## 3 · Ventanas

Las dos comparten la barra de tres puntos. **No es decoración**: es lo que hace
que el bloque se lea como «una pantalla» y no como una caja de texto.

### Terminal

Para datos. Las filas `clave : valor` alinean por los dos puntos y se leen de un
vistazo — mucho mejor que una lista suelta en medio del lienzo.

**Una terminal en un post no es una terminal: es un dibujo de una terminal.**
Leer texto monoespaciado pequeño sobre negro da pereza y nadie lo hace. De ahí
tres condiciones, todas de Ramses tras rechazar la primera versión de la 06:

- **Letra de 40 px o más** en un lienzo de 1080 de ancho, y **cinco o seis
  líneas contadas**. Si el mensaje no cabe así, no va dentro de la terminal:
  va en el titular, y la terminal solo enseña el remate.
- **Una imagen vale igual que el texto.** Una captura tratada, o una
  ilustración en la línea de `proyector-codigo`, dentro del mismo marco de tres
  puntos, cumple la misma función y se lee antes.
- **La terminal nunca va sola ni centrada.** Se desplaza abajo y hacia un lado,
  sangra por el borde, y algo la pisa por arriba: Clawd caminando sobre su
  canto, una ficha, una cinta que la cruza. Una terminal centrada con hueco
  debajo es la pieza de una capa otra vez.

Clawd de paseo (`Clawd - Biblioteca/paseo`) está pensado justo para esto, y la
pieza sale en las dos formas: PNG fijo y **MP4**. La escala no se elige a ojo —
se despeja de tres medidas:

1. el lienzo del paseo mide 1008×544 y Clawd recorre 848 px dentro de él;
2. se escala hasta que **ese recorrido quepa centrado sobre la ventana**, de
   modo que ni empieza ni acaba fuera de ella;
3. se comprueba que el punto más alto del salto —`544·escala` menos el `top`
   del cuadro más alto— pase por debajo del titular.

Sobre una terminal de 918 px eso da escala 0.45: recorrido de 382 px, Clawd de
144×122 y el salto a 26 px del titular. El PNG fijo se coloca en la posición que
ocupa su fotograma dentro de ese mismo paseo, así que la imagen es literalmente
un cuadro del vídeo y no un montaje aparte.

El vídeo se compone con ffmpeg, no cuadro a cuadro: el GIF tiene duraciones
variables (de 20 a 1680 ms, 125 cuadros para 11.52 s) y reproducir esos tiempos
a mano es donde se cuela el error. Al escalar, `flags=neighbor` — con el filtro
por defecto el pixel art sale borroso.

### Cualquier ventana sirve de repisa, no solo la terminal

Ramses, 17/09/2026: *«las ventanas tipo terminal son buenas para agregar
animaciones de Clawd, contémplalo»*. Vale para **todo lo que tenga canto recto y
barra de tres puntos**: terminal, ventana de navegador, tarjeta pixel. El canto
superior es una repisa y Clawd camina por ella.

Segundo caso hecho, la `10-pixel` de la tanda 02 — una tarjeta de 912 px sobre
una foto a sangre:

| | Terminal (`post-06`) | Tarjeta sobre foto (`10-pixel`) |
|---|---|---|
| Ancho del objeto | 918 px | 912 px |
| Ancho de la caja del paseo | 454 px (centrada) | 560 px (pegada a la derecha) |
| Clawd resultante | 144×122 | 178×151 |

**Dos cosas que decide el sitio, no el gusto:**

1. **Nunca menos de ~170 px de alto.** A 152 px Clawd se lee como una silueta
   recortada y las patas parecen cortadas por el canto. Hubo que subirlo.
2. **La caja se aparta del texto, no al revés.** En la `10` el párrafo acaba en
   x≈510, así que la caja empieza en 436 y Clawd nunca lo pisa — comprobado
   también con el punto más alto del salto (fotograma 80), que cae en x 667–845,
   lejos del rótulo. Si el texto no deja sitio, el paseo va más corto, no el
   párrafo más pequeño.

Y el PNG **siempre** sale del vídeo: se renderiza la pieza sin Clawd, ffmpeg
superpone el paseo, y la imagen fija se coloca en la posición exacta que tiene
su fotograma dentro de ese mismo paseo. Así no pueden descuadrarse.

```html
<div class="ventana ventana-terminal ventana-terminal--clara">
  <div class="barra"><span class="puntos"><i></i><i></i><i></i></span>
    <span class="titulo">claudetec — hackathon</span></div>
  <div class="contenido">
    <div class="fila"><span class="clave">fecha</span><span>:</span>
      <span class="valor">sábado 3 de octubre</span></div>
    <div class="fila"><span class="clave">sede</span><span>:</span>
      <span class="valor acento">Expedition FEMSA</span></div>
  </div>
</div>
```

Sin `--clara` va en oscuro. La monoespaciada es la del sistema, no hay archivo
de fuente: `ui-monospace, Menlo, Consolas, monospace`.

**Un solo `.valor.acento` por ventana.** Es el único naranja del bloque.

### Navegador

Cuando la pieza habla de algo que vive en una URL. Trae pestaña con favicon y
barra de dirección: `.ventana-navegador` con `.barra`, `.pestana`, `.url` y
`.contenido`.

**Su mejor uso es narrativo:** una conversación de dos turnos dentro de la
ventana explica un concepto mejor que un párrafo suelto. Alguien pregunta,
Claude responde, y el dato que importa va en un destacado dentro de la
respuesta. Es el recurso que Ramses aprobó de la 07.

**Va abajo, no arriba.** Titular grande en la parte superior del lienzo y la
ventana anclada al pie, sangrando por la derecha y por abajo: así es el suelo
de la pieza y se lee como una pantalla que sigue más allá del borde. Arriba y
centrada deja un vacío enorme debajo — 579 px en la primera versión, el peor
número de la tanda.

Dos trampas medidas:

- Si la ventana sangra por la derecha, el `padding-right` del contenido tiene
  que valer **lo que sale del lienzo más su propio margen**. Si no, el sangrado
  se come el final de cada línea.
- El color de texto de la ventana va **fijo en `capas.css`**, no heredado. Sobre
  una `.pieza` naranja u oscura heredaba texto claro y el nombre de la pestaña
  salía blanco sobre blanco.
- **Sobre fondo crema la ventana desaparece.** Su cuerpo es `--light` y su barra
  `--crema-capa`: los dos tonos del propio fondo. Ahí lleva filete de
  `--mid-gray` y la barra baja a `--light-gray`. Sobre azul, lila u oscuro no
  hace falta.

Fondos probados para esta pieza: **azul** `#6a9bcc`, **lila** `#cbcada` y
**crema** `#f0eee6`, los tres con texto oscuro y lockup oscuro. El naranja se
retiró: a 2.96:1 obliga a texto claro, y con la ventana blanca abajo la pieza
queda partida en dos temperaturas.

## 4 · Acomodo de imágenes

Tres patrones, en orden de cuánto cambian una pieza:

**Foto atenuada al fondo + foto nítida encima.** La de atrás va a sangre y
tratada (`filter:grayscale(1) sepia(.35) brightness(.62)` da el duotono cálido
de las referencias); la de delante flota, más pequeña, redondeada y con sombra.

```html
<div class="foto-capas">
  <div class="fondo"><img src="contexto.png"></div>
  <div class="encima"><img src="momento.png"></div>
</div>
```

**Tienen que ser fotos distintas.** La misma dos veces se lee como un error de
render, no como una capa.

**Chip de estado montando el canto.** Píldora blanca con el asterisco y una
palabra: en las referencias dice *Learning*, *Analyzing…*, *Researching…* —
comentario sobre lo que pasa, no información. Se coloca a caballo del borde de
la foto, nunca dentro ni fuera del todo.

```html
<div class="chip-foto"><img src="claude-glyph.svg">Expedition FEMSA</div>
```

**Foto con ficha solapada** — arriba, en tarjetas.

---

## El hueco máximo

`scripts/analizar_referencia.py` da `aire_max`: la franja horizontal
completamente vacía más alta. En las cinco piezas aprobadas de `piezas-aprobadas/`
vale 0, 0, 0, 82 y 171 px; en las rechazadas por acomodo, 251, 293 y 579.

> **Ningún hueco vacío de más de 180 px** en 1080×1350. Si sobra sitio, crece la
> tipografía, baja el objeto o entra una capa. No se deja el hueco.

Es la única métrica que separa limpiamente aprobadas de rechazadas, y se
comprueba en una línea antes de entregar.

## Cuántas capas

Dos o tres. Fondo + una cinta + una ventana ya es una pieza rica. Cuatro empieza
a ser ruido, y la regla de **un solo elemento gráfico** sigue en pie: la ventana
y la ficha son estructura, no gráficos, pero una ilustración y un icono en la
misma pieza siguen siendo dos.

---

## Collage que se monta solo

El recurso del vídeo «The making of Claude Code»: una tarjeta central fija y,
alrededor, fotos, capturas y clips que entran **uno a uno** hasta llenar el
lienzo. Lo que cuenta la historia no es el collage final, es el orden de llegada.

Lo produce `scripts/collage_animado.py` a partir de una receta en JSON. **La
receta la escribe la persona que pide la pieza, no el script**: cada elemento
trae su caja en píxeles y su turno.

```json
{"src": "fotos/junta.jpg", "caja": [-40, 64, 430, 300], "turno": 1,
 "pie": "Primera junta"}
```

- `caja` — `[x, y, ancho, alto]` sobre el lienzo de 1080×1350. Los valores
  negativos sangran por el borde, a propósito.
- `turno` — 1, 2, 3… Dos elementos con el mismo turno entran a la vez.
- `desde` — solo para vídeo: por qué segundo del clip empieza.

Admite imagen y vídeo en la misma pieza. Los clips avanzan al ritmo del collage,
no al de la máquina que renderiza, porque el tiempo es un argumento de la
función que pinta y no el reloj del navegador — por eso dos corridas dan el
mismo MP4.

**Si la pieza lleva animación, el entregable es MP4.** Salen los tres: `.mp4`
para Instagram, `.gif` para chat y el `.png` del último fotograma para cuando
haga falta una imagen fija. El PNG es literalmente un cuadro del vídeo, no un
montaje aparte — la misma regla que ya seguía la pieza de terminal con Clawd.
