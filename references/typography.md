# Tipografía

## La tipografía del wordmark (caso aparte)

El wordmark "Claude" **no** está en Poppins ni en Lora: está en **Copernicus**, una
reinterpretación del Plantin de Chester Jenkins y Kris Sowersby. Es de licencia
comercial (Labor & Wait) y no viene con esta skill.

La aproximación libre más cercana es **Newsreader SemiBold** — se eligió midiendo
la superposición de píxeles de varias serifs contra el wordmark real, normalizando
por altura de mayúscula: 0.72 de coincidencia y proporción ancho/alto de 4.185
contra 4.245 del original. Las siguientes (Literata 600, Source Serif 600) quedaron
muy por debajo. Está incluida en `assets/fonts/newsreader-semibold.ttf`.

Newsreader es para **lockups y wordmarks**, no para texto corrido. El cuerpo sigue
siendo Lora.

## Las dos familias

| Rol | Fuente | Pesos | Fallback |
|---|---|---|---|
| Títulos (24pt+) | **Poppins** | Bold, SemiBold | Arial, Helvetica, sans-serif |
| Cuerpo | **Lora** | Regular, Italic | Georgia, serif |

El contraste entre una geométrica sin serifa y una serif de lectura es lo que
da el carácter. Si se usa una sola familia para todo, la pieza deja de verse de
marca. Poppins nunca baja de 24pt; por debajo de eso pierde su razón de ser y
compite con Lora.

## Las dos pixel

Salen del vídeo **«The making of Claude Code»** de Anthropic: el titular central
va en una pixel proporcional gruesa y las etiquetas, los pies de foto y el cuerpo
en una pixel monoespaciada fina.

| Rol | Fuente | Token | Cuándo |
|---|---|---|---|
| Titular grande, en caja | **Press Start 2P** | `--font-pixel` | mayúsculas, centrado, dentro de una tarjeta o ventana |
| Terminal, pies de foto, etiquetas | **Departure Mono** | `--font-mono` | texto corto; nunca un párrafo |

Las dos van en `assets/fonts/`, son OFL y viajan dentro de la skill.

### La esquina tiene que estar viva

**Regla, no preferencia: en pixel no entra ninguna fuente que redondee la
esquina del píxel.** Hasta la v2.14 el titular iba en *Pixelify Sans* y Ramses la
descartó por ilegible — redondeada, la `D` se lee `O` y la `B` se lee `8`. Se
cotejaron cuatro al mismo cuerpo, en titular de 62 px y en línea de terminal de
23 px:

| Candidata | Titular | Línea chica | Veredicto |
|---|---|---|---|
| Pixelify Sans | esquina redonda, D≡O | legible pero blanda | **fuera** (v2.14) |
| Silkscreen | esquina viva, pero U≡V | se deshace | fuera |
| Departure Mono | limpia, algo fina para titular | **excelente** | se queda para lo chico |
| **Press Start 2P** | **esquina viva, con cuerpo** | **legible** | **se queda para titular** |

El coste de Press Start 2P es el ancho: ~10 caracteres por línea a 62 px sobre
1080 px. **El titular en pixel se escribe corto o no cabe.** Tiene un solo peso;
está declarada en el rango `400 700` para que el navegador no le sintetice una
negrita y le rompa la rejilla de píxel.

Las dos tienen acentos y signos de apertura, así que aguantan español.

**No son las tipografías por defecto.** El titular de una pieza de comunidad
sigue siendo la serif. La pixel entra cuando la pieza habla de terminal, de
código o del producto, y entonces manda en toda la pieza: mezclar pixel y serif
en el mismo titular no funciona.

Dos detalles de uso:

- **Departure Mono cae en rejilla en múltiplos de 11 px.** A 22, 33 o 44 px los
  píxeles quedan enteros; a 25 px salen bordes sucios.
- **La pixel pide tracking.** `letter-spacing` de `.02em` en el titular y de
  `.25em` a `.30em` en la línea pequeña de debajo, que es lo que le da el aire
  del vídeo. Sin tracking la monoespaciada se apelmaza.

Y la regla que motivó todo esto: **en una terminal, el texto va grande.** Nada
por debajo de 40 px en un lienzo de 1080. Ver `references/capas.md`.

## Imports

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Lora:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
```

```css
--font-heading: 'Poppins', Arial, Helvetica, sans-serif;
--font-body:    'Lora', Georgia, 'Times New Roman', serif;
```

En documentos de Word/PowerPoint sin las fuentes instaladas, usar Arial y Georgia
directamente en vez de dejar que el programa sustituya al azar.

## Escalas por tipo de pieza

**Social 1:1 (1080×1080 px)**

```
Titular        Poppins Bold        88–110 px   line-height 1.05   máx. 3 líneas
Subtítulo      Poppins SemiBold    38–46 px    line-height 1.2
Etiqueta dato  Lora Italic         26 px       ("Cuándo:", "Dónde:")
Dato           Lora Regular        28–32 px
Pie / CTA      Lora Italic         24 px
Lockup esquina Poppins SemiBold    22 px
```

**Presentación (16:9)**

```
Título de portada   Poppins Bold      72–90 pt
Título de slide     Poppins Bold      36–44 pt
Bullet / cuerpo     Lora Regular      20–24 pt
Nota al pie         Lora Italic       14 pt
```

**Web / UI**

```
H1   Poppins Bold      clamp(2.5rem, 5vw, 4rem)   line-height 1.1
H2   Poppins Bold      2rem                        line-height 1.2
H3   Poppins SemiBold  1.375rem
Body Lora Regular      1.0625rem                   line-height 1.65
Small Lora Regular     0.875rem
Botón Poppins SemiBold 1rem                        sin mayúsculas sostenidas
```

**Documento**

```
Título      Poppins Bold      24 pt
Encabezado  Poppins SemiBold  16 pt
Cuerpo      Lora Regular      11 pt   interlineado 1.5
Cita        Lora Italic       11 pt   con sangría
```

## Reglas de composición del texto

- **Sentence case en todo.** Nada de MAYÚSCULAS SOSTENIDAS en titulares. Se
  permiten en etiquetas cortas de una o dos palabras si van con tracking abierto.
- **Alineación izquierda por defecto.** Centrar solo una portada o un cierre, y
  aun así con moderación. Nunca justificar.
- **Interlineado cerrado en titulares** (1.0–1.15) y abierto en cuerpo (1.5–1.65).
  Ese salto de ritmo es parte del look.
- **Medida de línea de 45 a 75 caracteres** en cuerpo. Textos más anchos se
  vuelven ilegibles y delatan una plantilla mal armada.
- **Jerarquía de máximo tres niveles** por pieza. Si necesitas un cuarto, el
  contenido está mal editado, no la tipografía.
- **Itálicas de Lora para matices**: pies de foto, CTAs suaves, etiquetas de dato.
  Nunca para párrafos completos.
- Sin subrayados salvo links, sin tracking negativo, sin escalado horizontal.

## Variante editorial (Builder Club)

Sustituye Poppins por una **serif editorial de alto contraste** (Tiempos
Headline, Copernicus, Playfair Display o EB Garamond como sustituto libre) en
titulares grandes, sentence case, interlineado 1.0–1.1. El cuerpo y los datos
siguen en Lora o en la misma serif a peso regular. Las etiquetas "Cuándo:" y
"Dónde:" van en **negrita itálica**, con el dato en redondas debajo.
