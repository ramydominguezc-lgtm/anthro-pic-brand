# Tanda 02 — diez piezas con fotografía

Generadas el 17/09/2026 con `salida/tanda_fotos.py` y **revisadas por Ramses el
mismo día**. Su veredicto está en `references/veredictos.md`, una fila por
pieza; aquí sólo el resumen.

El encargo era hacer diez de la misma calidad que las cinco de la carpeta de
arriba **sin repetir su acomodo**. Así que ninguna de estas diez usa las
geometrías aprobadas —foto atenuada detrás, ficha solapada, foto a sangre,
mitad y mitad, par de fotos— ni repite la de otra de la tanda.

| # | Geometría | De qué habla | Sirve como | Veredicto |
|---|---|---|---|---|
| 01 | Retícula irregular de tres fotos; el titular ocupa una celda | Convocatoria de nuevos miembros | post | aprobada |
| 02 | Titular sobre color, foto en el corte diagonal inferior | Taller con fecha y sede | post | aprobada |
| 03 | Foto en cuarto de círculo; el texto la rodea en L | Mentorías 1:1 | post | aprobada, bullets agrandados |
| 04 | Foto a sangre en columna de altura completa | Qué es ClaudeTec | portada de carrusel | aprobada |
| 05 | La foto es el contenido de una ventana de navegador | Lanzamiento del sitio | post | aprobada |
| 06 | La cita se parte en dos y una banda de foto pasa por en medio | Testimonio de un miembro | post o lámina | **v2, a revisar** |
| 07 | Cifra en pixel arriba, foto a sangre, franja de datos al pie | Balance del semestre | post | **v2, a revisar** |
| 08 | Cuatro fotos en tira; titular y tabla de cuatro renglones debajo | Recap del semestre | portada de carrusel | corregida, a confirmar |
| 09 | Lista numerada; la foto ancla la esquina | Índice de un carrusel de 5 | portada de carrusel | aprobada |
| 10 | Foto a sangre, tarjeta pixel y Clawd caminando encima | Hackathon | post **+ MP4** | aprobada, tipografía cambiada |

## Lo que cambió tras tu revisión

- **03** — los bullets se leían chicos: 26 → 32 px, y la columna se ensanchó de
  330 a 386 px para que ninguno parta en dos líneas.
- **06** — rehecha entera. La v1 no se entendía: firmaba una cita con la foto de
  un portátil (en el banco no hay una sola persona), la comilla de 170 px caía
  encima del rótulo y dejaba 420 px muertos. Ahora la frase se parte en dos con
  una banda de foto a sangre en medio, que obliga a que las dos mitades estén
  llenas, y la firma es texto.
- **07** — rehecha entera. La v1 ilustraba «312 personas» con la portada de un
  libro que pone **Symbol** en grande: una segunda marca dentro de la pieza.
  Ahora la cifra manda, la foto es un aula vacía y los porcentajes bajan a una
  franja oscura maciza donde no pueden tocar al logo.
- **08** — sobraba hueco, y sobraba de verdad: 337 px. La lista pasó de dos
  columnas apretadas al pie a cuatro renglones en el tercio central, cada uno
  con su dato alineado a la derecha, para que la fila use el ancho entero.
- **10** — la pixel redondeada (Pixelify Sans) no se leía: la `D` se veía `O`.
  Cambiada a **Press Start 2P** en toda la skill. Y, siguiendo tu nota de que
  las ventanas tipo terminal son buen sitio para animar a Clawd, **Clawd camina
  sobre el canto de la tarjeta**: la pieza sale también en `10-pixel.mp4`.

## Lo que se replicó fue el número, no el acomodo

De `references/veredictos.md`: `aire_max ≤ 180 px`. Las diez lo cumplen y el
script lo comprueba en cada corrida.

**Aviso que salió de esta tanda:** la métrica estaba ciega en dos de estas
piezas. La `06` v1 daba 0 con 420 px muertos (la trama de grano tapaba el
lienzo) y la `08` v1 daba 0 con 337 px muertos (el fondo oscuro se contaba
entero como tinta). Corregido en `analizar_referencia.py`; donde sigue sin poder
medirse, el script ahora lo dice con `aire_fiable`.

## Las fotos

Son de archivo, descargadas a `salida/fotos2/` solo para esta prueba. **No son
material de ClaudeTec**: al usar cualquiera de estas diez en serio hay que
cambiar la foto por una real del grupo. La geometría y el texto son lo que se
está enseñando aquí.

Y una regla que costó una pieza: **antes de colocar una foto, leerla.** Qué pone
y de qué habla. Una foto con letras mete una segunda marca en la pieza.
