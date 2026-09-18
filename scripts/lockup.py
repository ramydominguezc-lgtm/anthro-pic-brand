#!/usr/bin/env python3
"""Compone un lockup <asterisco de Claude> + <palabra> en SVG vectorial.

El asterisco se toma tal cual del SVG oficial (path sin modificar). La palabra se
compone con HarfBuzz para que respete el kerning real de la fuente, en Newsreader
SemiBold — la aproximacion libre mas cercana a Copernicus, que es la tipografia del
wordmark oficial y es de licencia comercial.

Las constantes salieron de medir el lockup oficial y calibrar hasta reproducirlo:
altura del asterisco = 1.225 x altura de mayuscula, separacion = 0.26 x, ejes
centrados en el bloque de mayuscula. No las muevas sin volver a calibrar.

Requiere:  pip install uharfbuzz fonttools brotli cairosvg

Ejemplos:
    python3 scripts/lockup.py --palabra "ClaudeTec" --salida ct.svg
    python3 scripts/lockup.py --palabra "ClaudeTec" --corte 6 --color-b "#d97757"
    python3 scripts/lockup.py --palabra "ClaudeTec" --color-a "#faf9f5" \
        --color-b "#faf9f5" --salida ct-claro.svg     # para fondo oscuro

Para exportar a PNG transparente:
    python3 -c "import cairosvg; cairosvg.svg2png(url='ct.svg', \
        write_to='ct.png', output_width=3000)"
"""
import pathlib, re, argparse
try:  # dep-guard
    import uharfbuzz as hb
except ImportError:
    import sys
    sys.exit("Falta el paquete `uharfbuzz`, que no viene en el contenedor.\n"
             "  pip install uharfbuzz --break-system-packages\n"
             "Este script es de mantenimiento de la biblioteca, no de\n"
             "produccion: el equipo de comunicacion no lo necesita.")
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

RAIZ = pathlib.Path(__file__).resolve().parent.parent

FONT = str(RAIZ / "assets/fonts/newsreader-semibold.ttf")
OFICIAL = str(RAIZ / "assets/logos/claude-wordmark.svg")

RATIO_ASTERISCO = 1.33349
RATIO_GAP = 0.21073


def glifos(texto, tt, gs, order, font):
    buf = hb.Buffer(); buf.add_str(texto); buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    salida, x = [], 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = SVGPathPen(gs); gs[order[info.codepoint]].draw(pen)
        d = pen.getCommands()
        if d:
            salida.append((d, x + pos.x_offset, pos.y_offset))
        x += pos.x_advance
    return salida, x


def bbox(d):
    nums = [float(v) for v in re.findall(r'-?\d+\.?\d*', d)]
    xs, ys = nums[0::2], nums[1::2]
    return min(xs), min(ys), max(xs), max(ys)


def construir(palabra, corte, color_a, color_b, color_ast, salida):
    tt = TTFont(FONT); gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    upem = tt['head'].unitsPerEm; cap = tt['OS/2'].sCapHeight
    font = hb.Font(hb.Face(pathlib.Path(FONT).read_bytes()))

    gl, avance = glifos(palabra, tt, gs, order, font)

    # asterisco oficial, sin tocar
    ast_d = re.findall(r'<path d="([^"]+)"', pathlib.Path(OFICIAL).read_text())[0]
    ax0, ay0, ax1, ay1 = bbox(ast_d)
    ast_alto = ay1 - ay0

    # todo en unidades de la fuente
    destino = cap * RATIO_ASTERISCO
    k = destino / ast_alto
    gap = cap * RATIO_GAP
    ancho_ast = (ax1 - ax0) * k

    # el SVG de la fuente crece hacia arriba desde la linea base; se voltea
    ty = cap                      # linea base
    ast_y = cap / 2 + destino / 2  # centro optico del bloque de mayuscula

    piezas = [
        f'<g transform="translate({-ax0*k:.2f},{ast_y:.2f}) scale({k:.5f},{-k:.5f})">'
        f'<path d="{ast_d}" fill="{color_ast}"/></g>'
    ]
    dx0 = ancho_ast + gap
    for i, (d, dx, dy) in enumerate(gl):
        color = color_a if i < corte else color_b
        piezas.append(
            f'<g transform="translate({dx0+dx:.2f},{ty+dy:.2f}) scale(1,-1)">'
            f'<path d="{d}" fill="{color}"/></g>')

    ancho = dx0 + avance
    alto = cap * 1.35
    off = (alto - cap) / 2
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho:.0f} {alto:.0f}" '
           f'width="{ancho:.0f}" height="{alto:.0f}">\n'
           f'<g transform="translate(0,{off:.2f})">\n  ' + "\n  ".join(piezas) +
           '\n</g>\n</svg>\n')
    pathlib.Path(salida).write_text(svg)
    print(f"{salida}  ->  {ancho:.0f} x {alto:.0f}  (cap {cap}, upem {upem})")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--palabra", default="ClaudeTec")
    p.add_argument("--corte", type=int, default=6, help="glifos antes del cambio de color")
    p.add_argument("--color-a", default="#141413")
    p.add_argument("--color-b", default="#141413")
    p.add_argument("--color-ast", default="#d97757")
    p.add_argument("--salida", default="lockup.svg")
    a = p.parse_args()
    construir(a.palabra, a.corte, a.color_a, a.color_b, a.color_ast, a.salida)
