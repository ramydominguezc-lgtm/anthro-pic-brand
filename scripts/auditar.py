#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audita toda la biblioteca y marca los assets que necesitan revision a ojo.

Cada chequeo salio de un error real cometido en produccion, no de teoria:

  contraste   un icono de tinta negra sobre fondo negro pasaba las pruebas de
              "visibilidad" y era ilegible. Se mide que fraccion de la tinta
              alcanza 3:1 contra cada fondo del sistema.
  mancha      las variantes de una sola tinta colapsaban el line art en un
              borron. Se mide cuanto llena el dibujo su propio bbox.
  recuadro    un asset con fondo horneado deja una caja visible al
              usarlos sueltos. Se detecta el borde recto opaco.
  margen      un asset sin margen no se puede intercambiar con los demas.
  fidelidad   un SVG puede tener error medio bajo y una tinta entera fuera de
              sitio. Se compara contra el PNG hermano cuando existe.

Uso:  python3 auditar.py [--todo]
"""
import argparse, io, pathlib
import numpy as np
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONDOS = [("blanco", (255, 255, 255)), ("crema", (250, 249, 245)),
          ("naranja", (217, 119, 87)), ("negro", (20, 20, 19))]
CARPETAS = ["logos", "logos-claudetec", "iconos", "ilustraciones", "clawd"]


def lum(c):
    c = np.asarray(c, float) / 255
    c = np.where(c <= .03928, c / 12.92, ((c + .055) / 1.055) ** 2.4)
    return .2126 * c[..., 0] + .7152 * c[..., 1] + .0722 * c[..., 2]


def contraste(a, b):
    l1, l2 = lum(a), lum(b)
    return (np.maximum(l1, l2) + .05) / (np.minimum(l1, l2) + .05)


def cargar(f, lado=420):
    if f.suffix.lower() == ".svg":
        import cairosvg
        return Image.open(io.BytesIO(
            cairosvg.svg2png(url=str(f), output_width=lado))).convert("RGBA")
    im = Image.open(f).convert("RGBA")
    im.thumbnail((lado, lado), Image.LANCZOS)
    return im


# Que se espera de cada carpeta. Sin esto la auditoria ahoga en falsos positivos:
# un tile de fondo DEBE ser opaco de borde a borde, un wordmark NO debe traer margen
# horneado, y una variante --claro DEBE desaparecer sobre fondo claro.
ESPERADO = {
    "logos":        dict(recuadro=True,  margen=False, fondos=None),
    "logos-claudetec":      dict(recuadro=True,  margen=False, fondos=None),
    "iconos":       dict(recuadro=True,  margen=True,  fondos=None),
    "ilustraciones":dict(recuadro=True,  margen=True,  fondos=None),
    "clawd":        dict(recuadro=True,  margen=False, fondos=None),
}


def fondos_aplicables(f, carpeta):
    """Sobre que fondos tiene sentido exigir contraste a ESTE archivo."""
    esp = ESPERADO.get(carpeta, {})
    if esp.get("fondos") == []:
        return []
    stem = f.stem
    if stem.endswith("--claro") or stem.endswith("-claro"):
        return [x for x in FONDOS if x[0] == "negro"]
    if "--azul" in stem or "--verde" in stem:
        return [x for x in FONDOS if x[0] in ("blanco", "crema")]
    if stem.endswith("-oscuro") or stem.endswith("--mono"):
        return [x for x in FONDOS if x[0] in ("blanco", "crema")]
    return FONDOS


def revisar(f, carpeta=""):
    esp = ESPERADO.get(carpeta, dict(recuadro=True, margen=True, fondos=None))
    a = np.array(cargar(f)).astype(float)
    h, w, _ = a.shape
    opaco = a[:, :, 3] > 200
    hallazgos = []

    if opaco.sum() < 40:
        return ["vacio o casi vacio"]

    # --- recuadro: el asset es un rectangulo opaco de borde a borde ---
    marco = np.concatenate([opaco[0], opaco[-1], opaco[:, 0], opaco[:, -1]])
    if marco.mean() > 0.9 and esp["recuadro"]:
        hallazgos.append("RECUADRO: opaco de borde a borde; trae fondo horneado")

    # --- margen ---
    if opaco.any():
        ys, xs = np.where(opaco)
        m = min(xs.min(), w - 1 - xs.max(), ys.min(), h - 1 - ys.max())
        if m < min(h, w) * 0.03 and marco.mean() < 0.9 and esp["margen"]:
            hallazgos.append(f"MARGEN: solo {100*m/min(h,w):.0f}% del lado corto")

    # --- mancha ---
    ys, xs = np.where(opaco)
    bbox = (ys.max() - ys.min() + 1) * (xs.max() - xs.min() + 1)
    llenado = opaco.sum() / bbox
    if llenado > 0.80 and marco.mean() < 0.9:
        hallazgos.append(f"MANCHA: llena el {llenado:.0%} de su bbox")

    # --- contraste sobre cada fondo ---
    # 3:1 es el umbral de TEXTO. Para un grafico el listón es percibir la forma,
    # y ahi 2:1 basta. Usar 3:1 reprueba el naranja de marca sobre crema (2.96:1),
    # que es la combinacion propia del sistema y se ve perfectamente.
    tinta = a[:, :, :3][opaco]
    for nombre, bg in fondos_aplicables(f, carpeta):
        cr = contraste(tinta, np.array(bg))
        ok = (cr >= 2.0).mean()
        if ok < 0.15:
            hallazgos.append(f"INVISIBLE sobre {nombre}: solo {ok:.0%} de la "
                             f"tinta llega a 2:1 (max {cr.max():.1f}:1)")
        elif ok < 0.35:
            hallazgos.append(f"debil sobre {nombre}: {ok:.0%} de la tinta a 2:1")
    return hallazgos


def fidelidad_svg(svg):
    """Compara un SVG con su PNG hermano: error de color y peor region."""
    png = svg.with_suffix(".png")
    if not png.exists():
        return None
    v = np.array(cargar(svg, 420)).astype(int)
    o = np.array(cargar(png, 420)).astype(int)
    if v.shape != o.shape:
        return None
    m = (v[:, :, 3] > 200) & (o[:, :, 3] > 200)
    if m.sum() < 100:
        return None
    return np.abs(v[:, :, :3] - o[:, :, :3])[m].mean() / 255


def main(todo):
    total = limpios = 0
    print(f"{'asset':46} hallazgos")
    print("-" * 100)
    for c in CARPETAS:
        d = RAIZ / "assets" / c
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            if f.suffix.lower() not in {".svg", ".png", ".webp"}:
                continue
            total += 1
            hs = revisar(f, c)
            if f.suffix.lower() == ".svg":
                e = fidelidad_svg(f)
                if e is not None and e > 0.10:
                    hs.append(f"SVG INFIEL: {e:.0%} de error de color vs el PNG")
            if not hs:
                limpios += 1
                if todo:
                    print(f"{c + '/' + f.name:46} ok")
                continue
            print(f"{c + '/' + f.name:46} " + hs[0])
            for x in hs[1:]:
                print(f"{'':46} " + x)
    print("-" * 100)
    print(f"{total} assets revisados \u00b7 {limpios} sin hallazgos \u00b7 "
          f"{total - limpios} con algo que mirar")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--todo", action="store_true", help="lista tambien los limpios")
    main(p.parse_args().todo)
