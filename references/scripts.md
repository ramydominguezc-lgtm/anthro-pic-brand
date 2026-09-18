# Scripts

En `scripts/`, todos con `--help`.

En `scripts/`, todos con `--help`. Los que se usan al hacer una pieza:

| Script | Para qué |
|---|---|
| `validar.py` | Revisa una pieza terminada: paleta, acentos, contraste, márgenes, miniatura. Antes de entregar. |
| `tratar_foto.py` | Trata una foto para que aguante texto. `--recomendar` la mide y dice qué tratamiento y cuánto velo. |
| `analizar_referencia.py` | Mide densidad, bandas, ejes, salto tipográfico, aire y acento de una pieza. |
| `collage_animado.py` | Collage progresivo con imagen y vídeo: MP4, GIF y PNG. La receta (caja y turno de cada elemento) la escribe quien pide la pieza. |
| `catalogo_fondos.py` | Saca el catálogo de las 18 tramas de `fondos-color.css` en PNG y PDF. Córrelo tras tocar esa hoja. |
| `biblioteca.py` | Regenera el visor local de assets (`assets/biblioteca.html`). |
| `entorno.py` | Dice qué se puede hacer AQUÍ (Chromium, ffmpeg, numpy…) y qué se pierde sin lo que falte. **Lo primero en un sitio nuevo.** |
| `manual_pdf.py` | Arma el manual de la skill en PDF, con muestras de `piezas-aprobadas/`. |
| `veredictos.py` | Anota el veredicto de una pieza con sus medidas en `references/veredictos.md`. Sustituye al corpus de imágenes. |
| `enlaces.py` | Comprueba que toda ruta citada por los .md, .py, .css y .html existe. Antes de empaquetar. |
| `clawd_biblioteca.py` | Puente con la skill `clawd-biblioteca`: resuelve la ruta de una animación terminada. |
| `visor.py` | Regenera el visor publicado: inventaría los assets y compila el HTML que se publica como Artifact. Córrelo tras añadir o renombrar assets. |
| `lockup_variantes.py` | Reparte el color entre los glifos del lockup de ClaudeTec y saca SVG + PNG de cada variante. |
| `preparar_canva.py` | Arma `assets-canva/` con los archivos a subir, numerados. |
| `inspeccionar.py` | Convierte una imagen en rejilla de texto cuando el visor no funciona. |

Mantenimiento (solo al cambiar la biblioteca; piden paquetes extra):
`derivar_png.py` (saca el PNG de cada SVG nuevo), `auditar.py`,
`catalogo_pdf.py`, `vectorizar.py`,
`vectorizar_pixelart.py`, `variantes.py`, `estandarizar.py`, `lockup.py`.

Requieren: `pip install uharfbuzz fonttools brotli cairosvg vtracer scipy pillow`

Material nuevo que llegue en captura de pantalla pasa por `estandarizar.py` y
`vectorizar.py`, no se recorta a mano. Cada script explica en su encabezado los
enfoques que fallaron — léelos antes de "arreglarlos".

