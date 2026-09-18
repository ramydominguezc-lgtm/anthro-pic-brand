#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convierte una imagen en una representacion de TEXTO legible por el modelo.

Por que existe: en algunos entornos la herramienta de ver imagenes devuelve un
marcador vacio y el contenido nunca llega al modelo. Sin esto, la unica forma de
"revisar" una pieza son metricas agregadas — y las metricas agregadas dejan pasar
errores obvios a simple vista: un recuadro de fondo, un dibujo colapsado en
mancha, unos audifonos rotos. Esta herramienta cierra ese hueco: rasteriza a una
rejilla gruesa y la imprime como caracteres, de modo que la forma se puede leer.

No sustituye a un ojo humano. Sirve para detectar problemas de forma y de tono:
manchas solidas, recuadros de fondo, elementos ausentes, contraste invertido.

Uso:
    python3 inspeccionar.py pieza.png                 # rejilla de tonos
    python3 inspeccionar.py icono.svg --ancho 80
    python3 inspeccionar.py pieza.png --color         # mapa de colores de marca
    python3 inspeccionar.py a.png b.png --comparar    # dos imagenes lado a lado
"""
import argparse, io, pathlib
import numpy as np
from PIL import Image

# de mas claro a mas oscuro
RAMPA = " .:-=+*#%@"

MARCA = {
    ".": ("fondo/transparente", None),
    "K": ("oscuro #141413", (20, 20, 19)),
    "L": ("claro #faf9f5", (250, 249, 245)),
    "O": ("naranja #d97757", (217, 119, 87)),
    "B": ("azul #6a9bcc", (106, 155, 204)),
    "V": ("verde #788c5d", (120, 140, 93)),
    "g": ("gris medio", (176, 174, 165)),
    "?": ("fuera de paleta", None),
}


def cargar(ruta, ancho, fondo):
    ruta = pathlib.Path(ruta)
    if ruta.suffix.lower() == ".svg":
        import cairosvg
        png = cairosvg.svg2png(url=str(ruta), output_width=ancho * 8)
        im = Image.open(io.BytesIO(png)).convert("RGBA")
    else:
        im = Image.open(ruta).convert("RGBA")
    base = Image.new("RGBA", im.size, fondo + (255,))
    im = Image.alpha_composite(base, im).convert("RGB")
    # las celdas de texto son ~2x mas altas que anchas
    alto = max(1, round(ancho * im.height / im.width / 2.1))
    return np.array(im.resize((ancho, alto), Image.BOX)).astype(int)


def rejilla_tono(a):
    lum = a.mean(2)
    lo, hi = lum.min(), lum.max()
    if hi - lo < 1:
        return ["(imagen de un solo tono)"]
    norm = (lum - lo) / (hi - lo)
    idx = ((1 - norm) * (len(RAMPA) - 1)).round().astype(int)
    return ["".join(RAMPA[i] for i in fila) for fila in idx]


def rejilla_color(a, fondo):
    filas = []
    ref = [(k, np.array(v)) for k, v in
           [(k, v[1]) for k, v in MARCA.items() if v[1] is not None]]
    for fila in a:
        s = ""
        for px in fila:
            if np.linalg.norm(px - np.array(fondo)) < 18:
                s += "."
                continue
            k, d = min(((k, np.linalg.norm(px - v)) for k, v in ref),
                       key=lambda x: x[1])
            s += k if d < 60 else "?"
        filas.append(s)
    return filas


def informe(a, fondo):
    lum = a.mean(2)
    dif = np.linalg.norm(a - np.array(fondo), axis=2)
    tinta = dif > 24
    out = []
    if tinta.any():
        ys, xs = np.where(tinta)
        bbox = (ys.max() - ys.min() + 1) * (xs.max() - xs.min() + 1)
        cobertura = tinta.mean()
        out.append(f"cobertura de tinta: {cobertura:.0%} del lienzo, "
                   f"{tinta.sum()/bbox:.0%} de su propio bbox")
        # el aviso solo aplica a assets sueltos: en una pieza terminada con fondo
        # a sangre todo difiere del color muestreado y el 100% es lo normal
        if tinta.sum() / bbox > 0.75 and cobertura < 0.75:
            out.append("  AVISO: llena casi todo su bbox — puede ser una mancha "
                       "solida y no un dibujo")
    out.append(f"rango de luminancia: {lum.min():.0f}-{lum.max():.0f}")
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("rutas", nargs="+")
    p.add_argument("--ancho", type=int, default=64)
    p.add_argument("--color", action="store_true",
                   help="mapa de colores de marca en vez de rampa de tonos")
    p.add_argument("--fondo", default="250,249,245",
                   help="fondo sobre el que componer (r,g,b)")
    p.add_argument("--comparar", action="store_true",
                   help="imprime las imagenes lado a lado")
    a = p.parse_args()
    fondo = tuple(int(v) for v in a.fondo.split(","))

    bloques = []
    for r in a.rutas:
        m = cargar(r, a.ancho, fondo)
        filas = rejilla_color(m, fondo) if a.color else rejilla_tono(m)
        bloques.append((pathlib.Path(r).name, filas, informe(m, fondo)))

    if a.comparar and len(bloques) > 1:
        alto = max(len(b[1]) for b in bloques)
        print("  ".join(f"{n[:a.ancho]:<{a.ancho}}" for n, _, _ in bloques))
        for i in range(alto):
            print("  ".join(f"{(f[i] if i < len(f) else ''):<{a.ancho}}"
                            for _, f, _ in bloques))
    else:
        for nombre, filas, inf in bloques:
            print(f"\n=== {nombre} ===")
            for f in filas:
                print(f)
            for l in inf:
                print(l)
    if a.color:
        print("\nleyenda: " + " | ".join(
            f"{k}={v[0]}" for k, v in MARCA.items()))


if __name__ == "__main__":
    main()
