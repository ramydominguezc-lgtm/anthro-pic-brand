#!/usr/bin/env python3
"""Vectoriza line art a dos tintas separando cada tinta en su propia capa.

Trazar el PNG a color directamente no funciona: vtracer interpreta cada nivel de
antialiasing como un color propio y devuelve cientos de paths inutiles. La salida
limpia sale de binarizar cada tinta por separado, trazarla en modo binario y
recomponer el SVG apilado — naranja abajo, negro encima, como esta dibujado.

Uso:
    python3 vectorizar.py entrada.png salida.svg
    python3 vectorizar.py --lote "out/*.png" --destino svg/
"""
import argparse, glob, pathlib, re, tempfile
import numpy as np
from PIL import Image
from scipy import ndimage
try:  # dep-guard
    import vtracer
except ImportError:
    import sys
    sys.exit("Falta el paquete `vtracer`, que no viene en el contenedor.\n"
             "  pip install vtracer --break-system-packages\n"
             "Este script es de mantenimiento de la biblioteca, no de\n"
             "produccion: el equipo de comunicacion no lo necesita.")

NEGRO = "#141413"
NARANJA = "#d97757"


def capas(png):
    a = np.array(Image.open(png).convert('RGBA')).astype(int)
    rgb, al = a[:, :, :3], a[:, :, 3]
    tinta = al > 128
    sat = rgb.max(2) - rgb.min(2)
    naranja = tinta & (sat > 40) & (rgb[:, :, 0] > rgb[:, :, 2])
    negro = tinta & ~naranja
    # el naranja va debajo del negro; se dilata para que no quede una costura
    # blanca de un pixel donde las dos capas se tocan
    naranja = ndimage.binary_dilation(naranja, iterations=2) & ~ndimage.binary_erosion(negro, iterations=1)
    return {NARANJA: naranja, NEGRO: negro}


def trazar(mascara, color):
    """Devuelve elementos <path> completos, recoloreados al color de la tinta.

    Dos trampas de vtracer que hay que respetar:
      - cada path trae su propio transform="translate(x,y)"; si se extrae solo el
        atributo d, todas las formas colapsan al origen;
      - segun los parametros puede emitir tambien un path de fondo con relleno
        claro, que taparia la ilustracion entera.
    """
    im = Image.fromarray(np.where(mascara, 0, 255).astype('uint8')).convert('RGB')
    with tempfile.TemporaryDirectory() as d:
        pin, pout = f"{d}/i.png", f"{d}/o.svg"
        im.save(pin)
        vtracer.convert_image_to_svg_py(
            pin, pout, colormode="binary", mode="spline",
            filter_speckle=6, corner_threshold=60,
            length_threshold=4.0, splice_threshold=45)
        s = pathlib.Path(pout).read_text()

    salida = []
    for m in re.finditer(r'<path\b[^>]*/?>', s):
        el = m.group(0)
        fill = re.search(r'fill="(#[0-9a-fA-F]{6})"', el)
        if fill and sum(int(fill.group(1)[i:i + 2], 16) for i in (1, 3, 5)) > 380:
            continue  # relleno claro = fondo, no tinta
        el = re.sub(r'fill="[^"]*"', f'fill="{color}"', el) if fill \
            else el.replace('<path', f'<path fill="{color}"', 1)
        salida.append(el if el.endswith('/>') else el[:-1] + '/>')
    return salida


def redondear(el, dec=1):
    """vtracer emite coordenadas con 15 decimales; a un decimal el archivo baja
    mas de la mitad y la diferencia no es visible ni a 4000 px."""
    return re.sub(r'-?\d+\.\d+',
                  lambda m: f"{float(m.group(0)):.{dec}f}".rstrip('0').rstrip('.') or '0',
                  el)


def vectorizar(entrada, salida, dec=1):
    w, h = Image.open(entrada).size
    piezas = []
    for color, m in capas(entrada).items():
        if not m.any():
            continue
        els = [redondear(e, dec) for e in trazar(m, color)]
        if els:
            piezas.append("<g>" + "".join(els) + "</g>")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}" height="{h}">\n' + "\n".join(piezas) + '\n</svg>\n')
    pathlib.Path(salida).write_text(svg)
    return salida


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("entrada", nargs="?")
    p.add_argument("salida", nargs="?")
    p.add_argument("--lote")
    p.add_argument("--destino", default=".")
    a = p.parse_args()
    if a.lote:
        d = pathlib.Path(a.destino); d.mkdir(parents=True, exist_ok=True)
        for f in sorted(glob.glob(a.lote)):
            o = d / (pathlib.Path(f).stem + ".svg")
            vectorizar(f, o)
            print("->", o, f"{o.stat().st_size/1024:.0f} KB")
    else:
        vectorizar(a.entrada, a.salida)
        print("->", a.salida)
