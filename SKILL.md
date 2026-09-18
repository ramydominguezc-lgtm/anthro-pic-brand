---
name: anthro-pic-brand
description: Sistema de identidad visual de Anthropic y Claude — paleta, tipografía, composición y biblioteca de assets. Úsala al producir o revisar cualquier pieza con marca Claude o Anthropic (post, story, carrusel, cartel, slide, banner, UI) en cualquier herramienta, y cuando pidan "que se vea como Claude".
---

# Anthropic / Claude — sistema de marca

Dos colores base, dos tipografías, mucho aire. Casi todo lo que se siente fuera
de marca viene de meter más cosas. Cuando dudes, quita.

## Fundamentos

```
DARK        #141413   texto principal, fondos oscuros
LIGHT       #faf9f5   fondo por defecto
LIGHT GRAY  #e8e6dc   fondos sutiles, badges
MID GRAY    #b0aea5   líneas y bordes  (NO para texto: da 2:1)
MUTED       #7d7b74   texto secundario accesible

ORANGE      #d97757   acento primario  ← el color de la marca
BLUE        #6a9bcc   acento secundario
GREEN       #788c5d   acento terciario

Titulares:  serif editorial (Newsreader SemiBold) en piezas de comunidad
Pixel:      Press Start 2P (titular, esquina viva) y Departure Mono (terminal)
            solo en piezas de terminal, codigo o producto — no por defecto
Etiquetas, datos, UI:  Poppins (Bold / SemiBold)   fallback Arial
Cuerpo:     Lora (Regular / Italic)                fallback Georgia
```

Las fuentes van por `@font-face` local desde `assets/tokens/tokens.css`, **no por
Google Fonts**: la red está bloqueada y la caída a Arial es silenciosa — la pieza
sale plausible y fuera de marca.

Reglas que no se rompen:

- **El fondo por defecto es claro.** Crema `#faf9f5`. **Fondo oscuro solo si lo
  piden**: es el que menos assets admite y no es el registro de la marca.
- **Un solo acento dominante por pieza.** Naranja es el default; azul y verde
  rotan entre piezas de una serie, no dentro de una.
- **Máximo contraste:** `#141413` sobre `#faf9f5`, o al revés.
- **El naranja no es color de texto largo.** CTA, un dato, un fondo o una forma.
- **Nada de degradados, glow ni esquinas muy redondeadas.** Sombra suave solo
  en tarjetas y ventanas que flotan, con los tokens de `capas.css`; nunca en
  texto, iconos ni botones.
- **Un solo elemento gráfico por pieza.** Nunca dos.
- **Todo alineado a la izquierda**, márgenes iguales de 6–8% del lado corto.
- **Al menos dos recursos** de `references/recursos-compositivos.md`, y **dos o
  tres capas** (`references/capas.md`). Una pieza de fondo plano + gráfico +
  texto sale correcta y muerta: es el modo de fallo real de este sistema.

## Por dónde va a salir la pieza

| Si la pieza… | Ruta | Lee |
|---|---|---|
| la va a seguir editando el equipo | Canva, sobre Brand Template | `references/canva.md` |
| se está explorando, sin dirección aún | Claude Design → Canva | `references/claude-design.md` |
| se necesita ya, exacta, y nadie la retoca | HTML de `assets/templates/` → PNG | sigue aquí |
| es código (web, UI, artifact) | `assets/tokens/tokens.css` | sigue aquí |

**Si va a tener una segunda versión, que nazca en Canva.** Una imagen exportada
es un callejón sin salida: nadie podrá corregirle una fecha sin volver a pedirla.

## Qué abrir según la tarea

No leas todo. Abre solo lo que aplica:

| Tarea | Abre |
|---|---|
| Componer un post, cartel o serie | `references/recursos-compositivos.md` + `references/layout.md` |
| **Dar profundidad: cintas, ventanas, fotos con ficha** | `references/capas.md` |
| **Escribir el texto de una pieza** | `references/claudetec.md` — qué es el grupo, a quién le habla, sus datos |
| Elegir un gráfico o saber sobre qué fondo funciona | `references/assets-index.md` |
| Ver la biblioteca entera y qué opina Ramses de cada pieza | el visor: https://claude.ai/artifact/TnE6uRwT4KeiBnQsCtEqbr |
| Antes de rehacer algo que ya se intentó | `references/reglas-derivadas.md` |
| Detalle de color o tipografía | `references/color.md`, `references/typography.md` |
| Meter una foto | `assets/templates/fondos.css` |
| **Elegir el fondo de una pieza sin foto** | `assets/templates/fondos-color.css` — 11 tramas, los dos huecos de imagen y el juego de colores |
| **Una pieza que se monta sola (imagen + vídeo)** | `scripts/collage_animado.py` + el apartado de collage en `references/capas.md` |
| Montar el Brand Kit en Canva | `references/guia-canva.md` |
| Animar a Clawd, o un label de carga (`✻ Thinking…`) | skills aparte: `clawd-biblioteca` entrega lo que ya existe; `clawd-animaciones` genera lo nuevo |
| Saber qué hace cada script | `references/scripts.md` |
| Diseñar láminas de carrusel | `references/laminas-carrusel.md` |

## Biblioteca

`logos`, `ilustraciones` (line art a dos tintas), `clawd`, `iconos`, `logos-claudetec` y
`templates`, todo en `assets/`. Catálogo con medidas y compatibilidad
de fondo en `references/assets-index.md`; para elegir visualmente, abre
`assets/biblioteca.html` en el navegador.

Cuatro cosas que cambian decisiones y conviene saber sin abrir el catálogo:

- **Sobre fondo naranja va la variante `--verde`**, no el SVG base: el base se
  pierde contra el naranja. Sobre fondo oscuro, la variante `--claro`. Tabla
  completa en `references/assets-index.md`.
- **Ningún icono aguanta fondo oscuro.** Su fondo es el naranja.
- **Usa siempre el SVG cuando exista** (logos, lockups, ilustraciones); el PNG
  es el derivado para herramientas que no aceptan vector. Iconos y fotos son
  PNG y no se amplían más allá de 1080 px. Detalle en `references/assets-index.md`.
- **Clawd es registro informal** — comunidad, merch, bienvenidas. No va en
  material institucional ni junto al wordmark, y no sustituye al logo.
- **Antes de usar un lockup de organización, lee "Marcas derivadas" en
  `references/layout.md`**: fusionar "Claude" con otro nombre crea una marca
  derivada, y eso pide permiso, no criterio de diseño.
- **Los stickers quietos de Clawd se quedan aquí**, en `assets/clawd/`. Los
  animados son de `clawd-biblioteca` — ver abajo.

## Formato: Instagram manda

Salvo que se pida otra cosa, una pieza sale en medida de Instagram:

| Pieza | Medida |
|---|---|
| **Post y carrusel** | **1080 × 1350** (4:5) — el default |
| **Story y reel** | **1080 × 1920** (9:16) |
| Post cuadrado, si se pide | 1080 × 1080 (1:1) |
| Presentación | 1920 × 1080 (16:9) |
| Lona, cartel, web | a medida |

Dos cosas que cambian la composición:

- **En un carrusel, todas las láminas van a la misma proporción**, o Instagram
  recorta desigual. Hasta 20 láminas.
- **La cuadrícula del perfil recorta a 3:4**, más estrecha que el 4:5: lo que
  tenga que verse en la miniatura no puede tocar los cantos laterales.

**La pieza se escribe, no se rellena una plantilla.** Las cinco plantillas HTML
se retiraron en la v2.12: escribían «ClaudeTec» como texto plano. El marco
canónico son cuatro líneas, y el resto lo pone el script de la pieza:

```html
<link rel="stylesheet" href="../assets/templates/_base.css">
<link rel="stylesheet" href="../assets/templates/capas.css">
<link rel="stylesheet" href="../assets/templates/fondos-color.css">
<style>.pieza{width:1080px;height:1350px;position:relative;padding:74px}</style>
```

`salida/ventanas_67.py` es el ejemplo completo: mide el alto, comprueba que no
falte nada y saca PNG y MP4.

## Dónde corre

Tres sitios, y no son iguales. **Lo primero al abrir la skill en uno nuevo:**

```bash
python3 scripts/entorno.py
```

Dice qué hay y qué se pierde sin lo que falte, en dos segundos.

| | Claude Code / desktop | claude.ai web |
|---|---|---|
| Comando | `python` en Windows, `python3` en el resto | `python3` |
| HTML de la pieza | Sí | Sí — siempre, no depende de nada |
| PNG y PDF | Sí | Solo con Chromium. `playwright install chromium` |
| MP4 y GIF | Sí | Solo con ffmpeg. Probar `pip install imageio-ffmpeg` |
| Medir la pieza | Sí | Necesita numpy y scipy |
| La biblioteca de Clawd | En `Desktop\Clawd - Biblioteca` | Solo si esa skill está instalada |
| Escribir en la skill | Sí | **No**: `/mnt/skills/user/` es efímero. Ver el protocolo de `VERSION.md` |

**Sin Chromium la pieza igual se entrega.** Todas las piezas de esta skill son
HTML autónomo con los assets embebidos en `data:` URI: el archivo se abre en
cualquier navegador y se captura. Lo que no se puede es medirla, y sin medida
las decisiones vuelven a ser impresiones — dilo en vez de disimularlo.

## Las tres skills de Claude

| Skill | Hace | Carpeta |
|---|---|---|
| **`anthro-pic-brand`** (esta) | Compone piezas. Paleta, tipografía, capas, fondos | `Desktop\anthro-pic-brand` |
| `clawd-animaciones` | **Genera** animaciones de Clawd y labels de carga | `Desktop\Animaciones - Clawd` |
| `clawd-biblioteca` | **Almacena y entrega** lo terminado. Su `CATALOGO.md` manda | `Desktop\Clawd - Biblioteca` |

**Esta skill no anima: consume.** Para meter una animación en una pieza:

```python
from clawd_biblioteca import pieza          # scripts/clawd_biblioteca.py
gif = pieza('paseo', 'transparente')
f62 = pieza('paseo', 'fotograma', 62)
```

El puente busca la biblioteca en varias rutas y, si no está, dice qué skill
falta en vez de soltar un error de archivo. `python3 scripts/clawd_biblioteca.py`
lista lo que hay.

**Si la animación no existe o hay que cambiarla**, no se edita a mano: se pasa a
`clawd-animaciones`, que la regenera en la biblioteca. Y al revés: si alguien
regenera `paseo`, la pieza de terminal de esta skill cambia con ella.

**No mezclar dibujos de Clawd en una pieza.** `clawd-base` y los stickers de
aquí, `caminando`/`saltando`/`confeti`/`pesas` de la biblioteca y
`paseo`/`paseo-arriba` son tres dibujos distintos —los brazos miden distinto—.
Juntos se leen como error.

## Scripts

`validar.py` revisa una pieza terminada antes de entregarla; `tratar_foto.py`
prepara una foto para que aguante texto. El resto —biblioteca, visor, variantes,
Canva, vectorizado— y lo que necesita cada uno, en `references/scripts.md`.

## Piezas de grupos estudiantiles del Tec

Esta skill define el lenguaje visual, **no la reglamentación**. El logo LiFE, la
posición del logo del grupo y los elementos obligatorios los manda la skill
`publicaciones-grupos-estudiantiles`. Ante conflicto, gana la regla del Tec.

## Checklist antes de entregar

O corre `python3 scripts/validar.py pieza.png`.

- ¿Fondo y texto son un par de máximo contraste?
- ¿Un solo acento dominante y **al menos dos recursos compositivos**?
- ¿Titular en serif, y Poppins solo en etiquetas y datos?
- ¿Márgenes amplios e iguales, todo sobre un solo eje a la izquierda?
- ¿Cero glow y esquinas muy redondeadas? (velo, duotono, semitono, grano y la
  sombra de tarjetas y ventanas **sí** entran)
- ¿Ninguna zona muerta grande? Si sobra hueco, el texto crece o la composición
  se recorta.
- ¿El asset elegido se ve sobre ESE fondo?
- ¿Si es serie, comparten lockup y alternan fondo?
- ¿Queda editable por el equipo, o es un callejón sin salida?
- Si es de un grupo estudiantil, ¿lleva el bloque LiFE?

---

Para las personas del equipo, no para el modelo: `README.md` (qué hace la skill
y cómo se mantiene), `MANUAL-COMUNICACION.md` (cómo escribir un encargo y
revisar antes de publicar), `PENDIENTES.md` (decisiones abiertas y qué falta),
`VERSION.md` (qué entró en cada versión), `references/bitacora.md` (historial).

Dos PDF se arman solos y son los que se mandan fuera del equipo:
`scripts/guia_pdf.py` (cómo se usan las tres skills y por dónde se hablan — el
que acompaña al ZIP) y `scripts/manual_pdf.py` (cómo se compone una pieza, con
muestras). El manual necesita las imágenes de la rama `piezas`; la guía no.
