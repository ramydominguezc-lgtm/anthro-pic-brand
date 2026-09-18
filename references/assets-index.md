# Catálogo de assets

Todos los archivos están en `assets/`. Para elegir mirando, hay dos vistas:

- **El visor publicado** — https://claude.ai/artifact/TnE6uRwT4KeiBnQsCtEqbr — los recursos y las catorce
  láminas sobre los cuatro fondos, con el veredicto de Ramses, las marcas de
  sobre qué fondo aguanta cada uno y los encargos de mejora pendientes. Es la
  fuente de los veredictos: lo que diga ahí gana a lo que diga esta tabla.
  Se regenera con `python3 scripts/visor.py` y se vuelve a publicar.
- `assets/biblioteca.html` — la hoja de contactos local. La genera
  `scripts/biblioteca.py`; no se versiona.

## Formatos: qué archivo es el bueno

Regla corta: **solo PNG y SVG.** Vector si el dibujo nació vector, raster si
nació raster, un solo master por pieza y el resto derivados que se regeneran.
No quedan WebP en `assets/`: la biblioteca es solo PNG y SVG.

| Familia | Master (el que se edita) | Derivado (se regenera) |
|---|---|---|
| Logos, lockups, ilustraciones | **SVG** | PNG a 3000 px de ancho |
| Iconos, fotos | **PNG** (no hay vector, y es a propósito) | — |
| Clawd | PNG (pixel art) + SVG donde exista | — |

Tres consecuencias que sí cambian decisiones:

- **A Canva sube el SVG, no el PNG.** El SVG entra como elemento vectorial: se
  escala sin pixelar y se le cambia el color desde el panel, que es justo lo que
  hace falta cuando alguien retoca la pieza a mano. El PNG a 3000 px está solo
  para las herramientas que no aceptan SVG.
- **Los iconos no se vectorizan.** Tienen textura y grano: trazarlos los
  convierte en manchas planas. Su master es el PNG a 1080 × 1080, que es
  tamaño 1:1 de un poster — **no los amplíes más allá de eso**.
- **Nada de HTML como formato de asset.** Un HTML que envuelve un SVG no es una
  versión más: es el mismo dibujo con 3.000 tokens de ruido alrededor. Los que
  llegaron así están en `v1/lockups-html/`.

### El peso de los archivos no cuesta tokens

Un SVG de 120 KB cuesta **cero** mientras nadie lo abra: en una pieza se
referencia la ruta, no el contenido. Lo caro es esta documentación. Así que la
biblioteca puede pesar lo que haga falta; lo que se mantiene corto es lo que se
lee para elegir. Abrir un vector solo hace falta al editarlo, y para eso están
`lockup_variantes.py` y `variantes.py`.

## Logos — `assets/logos/`

| Archivo | Medida | Fondo | Cuándo usarlo |
|---|---|---|---|
| `claude-glyph.svg` | Vectorial 1998 × 2000 | Transparente | **Preferido siempre que se pueda.** El asterisco de Claude en `#d97757`, un solo `path`: se recolorea cambiando un `fill`. |
| `claude-glyph.png` | 1998 × 2000 | Transparente | Cuando la herramienta no acepta SVG. |
| `claude-wordmark.svg` | Vectorial 512 × 110 | Transparente | **Preferido siempre que se pueda.** Escala sin pérdida: impresión, web, tamaños grandes. |
| `claude-wordmark.png` | 2000 × 430 | Transparente | Cuando la herramienta no acepta SVG. |

El SVG es la única versión que se puede recolorear limpiamente editando el
atributo `fill`. Los colores permitidos son `#d97757`, `#141413` y `#faf9f5`.

## Clawd — `assets/clawd/`

La mascota, en PNG con transparencia. Registro **informal**: comunidad, stickers,
merch, mensajes de bienvenida, canales internos, piezas divertidas.
No usar en material institucional, ni junto al wordmark, ni como sustituto del logo.

| Archivo | Medida | Escena |
|---|---|---|
| `clawd-base.png` | 640 × 640 | Neutro, sin objeto. El más versátil. |
| `clawd-coffee.png` | 616 × 364 | Con café. Sesiones matutinas, cafecito, coworking. |
| `clawd-headphones.png` | 528 × 473 | Con audífonos azules `#23476e`. Focus, música, sesiones largas. |
| `clawd-search.png` | 526 × 475 | Con lupa. Investigación, búsqueda, exploración. |
| `clawd-skateboard.png` | 498 × 501 | En patineta. Energía, arranque, eventos casuales. |

**Solo `clawd-base` y `clawd-headphones` tienen `.svg`.** Los otros tres no son
pixel art recuperable: el removebg los reescaló con resampleo y ya no existe una
retícula exacta que reconstruir. Al forzarlos se rompen el sombrero, la lupa y la
patineta. `scripts/vectorizar_pixelart.py` ahora lo detecta solo y se abstiene en
vez de emitir un SVG degradado — mide error de color y además exige que cada tinta
coincida con su región en el original.

Para los tres restantes, **usa el PNG**. Es lo correcto, no una limitación
molesta: son la versión fiel.

Los audífonos son el único punto de la biblioteca donde aparece un azul distinto
al de la paleta; si esa pieza necesita acento, usa `#6a9bcc`, no el navy del PNG.

### Clawd animado

La animación de Clawd vive en dos skills aparte, enlazadas entre sí:
**`clawd-animaciones`** (`Desktop\Animaciones - Clawd`) la genera: poses
canónicas, motor y recetas. **`clawd-biblioteca`** (`Desktop\Clawd - Biblioteca`)
guarda y entrega lo terminado en GIF, WebP, MP4, hoja de sprites, SVG y bloque
HTML: caminando, saltando, confeti, paseo (y su variante mirando arriba), pesas y bandera.
También guarda los **labels de carga** de Claude (la estrella animada con
`Thinking…`, `Researching…`, etc.), en tema claro y oscuro. Se usan con su color
de producto, sin recolorear.

**El criterio para saber dónde vive un Clawd nuevo:** ¿se coloca o se reproduce?
Un dibujo suelto que se pega en una pieza —con café, con lupa, en patineta— es un
asset gráfico y vive aquí, aunque sea pixel art. Una secuencia que solo tiene
sentido en movimiento —un ciclo, una hoja de sprites, un GIF— se genera en
`clawd-animaciones` y se guarda en `clawd-biblioteca`. No se duplica en las dos: una copia en dos sitios se queda
vieja en el primer retoque.

Lo único que hace falta saber desde aquí: **la animación no va en piezas fijas.**
En un post, flyer o PDF se congela y pierde lo único que aportaba. Ahí va un
Clawd quieto de `assets/clawd/`. Y no se mezclan los dibujos: el Clawd animado
tiene un cuerpo de 16 unidades en un lienzo de 28, contra 12 de 16 en
`clawd-base`, y juntos en una pieza se leen como un error.

## Qué fondo aguanta cada familia

Revisión de septiembre de 2026, 65 piezas marcadas una por una en el visor.
**Esta tabla manda sobre cualquier corazonada**: sale de mirar cada archivo sobre
los cuatro fondos, no de deducirlo del color del archivo.

| Familia | Crema | Naranja | Oscuro |
|---|---|---|---|
| Ilustraciones base, `--azul`, `--verde` | **sí** | solo las `--verde` | no |
| Ilustraciones `--claro` | no | no | **sí** — es la única que aguanta oscuro |
| Iconos | según el icono | **sí**, es su fondo | **no, ninguno** |
| Clawd | **sí** | no — es naranja y desaparece | **sí** |
| Lockup `-e-negro`, `-duotono` | **sí** | no | no |
| Lockup `-e-blanco`, `-duotono-claro` | no | no | **sí** |
| Glifo de Claude | **sí** | no | **sí** |
| Wordmark | **sí** | no | recolorea el SVG a `#faf9f5` |

Tres cosas que esta revisión cambió, y que antes la skill decía al revés:

1. **El SVG base NO va sobre naranja.** La idea era que el relleno se fundiera y
   quedaran las líneas; en la práctica el dibujo se pierde. Sobre naranja va la
   variante `--verde`, que es la que separa.
2. **Ningún icono aguanta fondo oscuro.** El catálogo decía "usables sobre
   cualquier fondo". No: la textura se traga el dibujo contra el oscuro.
3. **Clawd sobre naranja ya estaba prohibido y se confirma**, pero además
   `clawd-base` quedó descartado — justo el que estaba descrito como "el más
   versátil". Los que se usan son coffee, headphones, search y skateboard.

Descartes de la revisión, que siguen en la carpeta pero no se usan:
la familia `lampara-escritura` entera (4 archivos), las variantes `--claro` de
ilustración salvo para fondo oscuro, los iconos `columnas-grafica`, `mazo`,
`pendulo-newton`, `rayo-red` y `templo-destello`, la foto `mesa-redonda` y **las
cuatro fotos ya tratadas** de `fotos-demo/` — el duotono y el semitono se
generan por pieza con `tratar_foto.py`, no se toman de ahí.

## Iconos — `assets/iconos/`

Dibujos con textura, sobre transparente: PNG de 1080×1080, mismo lienzo y margen
que las ilustraciones.

**Su fondo es el naranja, no el oscuro.** De los doce revisados en el visor,
**ninguno aguanta fondo oscuro** — la textura se traga el dibujo. Nueve funcionan
sobre naranja; sobre crema solo los que tienen masa oscura propia.

| Archivo | Qué es | Temas |
|---|---|---|
| `manos-alzadas` | Manos levantadas | Participación, voluntariado, convocatorias |
| `columnas-grafica` | Columnas clásicas como gráfica ascendente | Finanzas, crecimiento, resultados |
| `pendulo-newton` | Péndulo de Newton | Causa y efecto, experimentación |
| `cabeza-destello` | Silueta de cabeza con destello | Ideas, aprendizaje |
| `cabeza-red` | Cabeza con red de nodos | Razonamiento, modelos |
| `cabeza-ondas` | Cabeza con ondas y nodos | Percepción, señales |
| `rayo-red` | Rayo con nodos (apaisado) | Velocidad, energía, infraestructura |
| `templo` / `templo-destello` | Frontispicio clásico | Instituciones, gobernanza |
| `mazo` | Mano con mazo | Reglas, decisiones, política |
| `pluma-libro` | Pluma escribiendo en un libro | Escritura, constitución, documentación |
| `faro` | Faro entre olas | Orientación, seguridad |

**No hay SVG y es a propósito.** Estos dibujos tienen entre 69 y 170 tonos
distintos — textura, no line art plano. Al vectorizarlos a dos tintas el error de
color llega al 83%, así que el PNG es la versión fiel.

## Ilustraciones de line art — `assets/ilustraciones/`

Dibujos a dos tintas (`#141413` + `#d97757`), en SVG vectorial y en PNG
transparente de 1080×1080 derivado del SVG. Todos comparten lienzo cuadrado, margen del 8% y arte centrado,
así que se pueden intercambiar en una plantilla sin reajustar nada.

| Archivo | Qué es | Para qué temas |
|---|---|---|
| `globo-red` | Globo terráqueo con retícula y nodos | Redes, alcance, internet, comunidad |
| `globo-llaves` | Globo entre llaves `{ }` | Web + código, APIs, datos abiertos |
| `documento-nodos` | Documento con un grafo de nodos | Contexto, MCP, documentación, RAG |
| `proyector-codigo` | Proyector mostrando `</>` | Talleres, demos, clases de programación |
| `lampara-escritura` | Lámpara iluminando una hoja escrita | Escritura, ideas, estudio, trabajo nocturno |

Cada ilustración viene además en variantes de color, con sufijo `--`:

| Sufijo | Qué cambia | Va sobre |
|---|---|---|
| *(sin sufijo)* | línea negra, relleno naranja | crema, blanco |
| `--verde` | relleno verde | **naranja** — es la que separa |
| `--azul` | relleno azul | crema, blanco; rota el acento en una serie |
| `--claro` | línea clara, relleno naranja | oscuro |
| `--pantalla-clara` | solo `proyector-codigo`: pantalla crema | naranja |

### Los 21 archivos

Cinco dibujos —`documento-nodos`, `globo-llaves`, `globo-red`,
`lampara-escritura`, `proyector-codigo`— cada uno en cuatro variantes, más una
suelta. El sufijo dice el fondo, y la regla no tiene excepciones:

| Sufijo | Fondo |
|---|---|
| *(ninguno)* y `--azul` | crema, blanco |
| `--claro` | oscuro |
| `--verde` | naranja |

La única fuera de patrón es `proyector-codigo--pantalla-clara`, que también va
sobre naranja. Todos existen en `.svg` y `.png`.

**La familia `lampara-escritura` está descartada** en la revisión de septiembre:
sus cuatro archivos siguen en la carpeta pero no se usan.

**Sobre fondo naranja va la variante `--verde`, no el SVG base.** La idea era
que el relleno naranja del base se fundiera con el fondo y quedaran las líneas;
medido pieza por pieza en el visor, el dibujo se pierde. La `--verde` es la que
separa. *Esto invierte lo que decía este catálogo antes de septiembre de 2026.*

Hubo variantes `--mono` y `--sobre-naranja` y **se eliminaron**: funden las dos
tintas en una sola, y como en estas cinco ilustraciones el relleno es entre el 61%
y el 84% de la tinta total, las líneas desaparecen dentro de él y queda una mancha
sólida. `scripts/variantes.py` ahora se niega a generarlas cuando el relleno pasa
del 45% y explica por qué.

**Usa el SVG siempre que puedas.** El PNG es para herramientas que no aceptan
vectores. Para generar variantes nuevas: `python3 scripts/variantes.py`.

Vinieron de capturas de pantalla y se procesaron con los scripts de la skill:
fondo eliminado con desmultiplicado de color en los bordes, paleta normalizada
(las capturas traían tres naranjas distintos, incluido `#c15f3c`), y vectorizado
por capas de tinta con 0.95 de fidelidad medida contra el original.

## Lockups de ClaudeTec — `assets/logos-claudetec/`

Lockups de organización compuestos con el asterisco oficial (path sin modificar)
más una palabra en Newsreader SemiBold, calibrados a las proporciones del wordmark
real: asterisco a 1.225× la altura de mayúscula, separación de 0.26×, ejes
centrados en el bloque de mayúscula.

| Archivo | Cuándo usarlo |
|---|---|
| `claudetec.svg` / `.png` | **La variante por defecto sobre fondo claro.** Texto completo en `#141413`, asterisco en `#d97757`. Lleva la **"e" corregida** (agosto 2026): es la versión buena del dibujo. |
| `claudetec--claro.svg` / `.png` | La misma, con el texto en `#faf9f5`, para fondo oscuro o naranja. |
| `claudetec--duotono.svg` / `.png` | "Claude" en `#141413` y "Tec" en `#d97757`. El corte de color deja leer dos palabras en vez de una que imita el logotipo, así que es la más defendible ante la regla de marcas derivadas — pero **arrastra la "e" vieja**. Si se va a usar, hay que regenerarla con la letra corregida. |

Los SVG son la versión de trabajo — escalan y se recolorean editando `fill`. Los
PNG salen a 3000 px con fondo transparente. Los `.html` de los que se extrajeron
están en `v1/lockups-html/`: no son un formato de asset, son el mismo vector
envuelto en una página para verlo.

**Para generar otros:** `scripts/lockup.py` compone cualquier palabra con el mismo
sistema. `--corte N` marca cuántos glifos van en el primer color, `--color-a` y
`--color-b` los dos colores, `--color-ast` el asterisco. Las constantes de
proporción están calibradas contra el lockup oficial; no las muevas sin recalibrar.

**Antes de usar cualquiera de estos, lee la advertencia de marcas derivadas en
`layout.md`.** Un lockup que fusiona "Claude" con otro nombre es una marca
derivada, no una aplicación de la marca, y eso tiene implicaciones de permiso.

## Hojas de estilo — `assets/templates/`

No hay plantillas HTML: se retiraron en la v2.12 porque escribían «ClaudeTec»
como texto plano. Cada pieza escribe su propio marco sobre estas cuatro hojas,
que son el sistema. Se importan en este orden:

| Archivo | Qué trae |
|---|---|
| `_base.css` | Base de `.pieza`, tipografía y sus clases `acento` y `oscuro`. Importa los tokens |
| `capas.css` | Cintas, tarjetas flotantes, ventanas de terminal y navegador, acomodo de fotos. Ver `references/capas.md` |
| `fondos-color.css` | Las once tramas de fondo y los dos huecos de imagen |
| `fondos.css` | Los doce tratamientos de fotografía |

El marco canónico está en `SKILL.md`; `salida/ventanas_67.py` es el ejemplo
completo, con medición del alto y verificación de contenido.

## Tokens — `assets/tokens/`

| Archivo | Para qué |
|---|---|
| `tokens.css` | Variables CSS de color, tipografía y ritmo. Es lo que se le da a Claude Design en el onboarding y lo que importan las plantillas. Impórtalo en vez de escribir hex sueltos. |
| `brand-kit.json` | Los mismos valores como datos, más las reglas. Sirve para cargar el Brand Kit de Canva y para cualquier herramienta que consuma JSON. |

## Visor — `assets/biblioteca.html`

Página autónoma con los assets de `assets/`. Filtra por carpeta, busca por texto, alterna
el fondo entre claro, naranja y oscuro para ver cómo se comporta cada pieza, y
copia la ruta al hacer clic. Regenerar tras añadir assets:
`python3 scripts/biblioteca.py`.

## Compatibilidad con el fondo — el otro método

`scripts/auditar.py` mide **contraste**, no si el dibujo se lee. Donde discrepe
con la tabla de arriba, **gana la tabla de arriba**: esa sale de mirar cada
archivo sobre los cuatro fondos. Corre el script cuando añadas assets nuevos;
no hace falta guardar su salida aquí.
