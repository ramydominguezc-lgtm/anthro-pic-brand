#!/usr/bin/env python3
"""Trata una foto para que pueda vivir detras de texto de marca.

Cuatro de los doce tratamientos de `assets/templates/fondos.css` no se pueden
hacer con CSS porque piden remapear tonos a tintas: duotono, semitono, riso y
grano de papel. Esos salen de aqui. Los otros ocho son CSS puro.

    python3 tratar_foto.py foto.jpg --recomendar
    python3 tratar_foto.py foto.jpg --modo duotono --sombra "#d97757" -o out.webp
    python3 tratar_foto.py foto.jpg --modo semitono --celda 6 --sombra "#d97757"
    python3 tratar_foto.py foto.jpg --modo riso
    python3 tratar_foto.py --papel papel.webp

--recomendar es el modo que importa. Mide la foto y dice que tratamiento aguanta
y con cuanto velo, en vez de aplicar un valor calibrado sobre OTRAS fotos y
esperar que sirva. Ese "esperar que sirva" fue el error original.

Por que las cuentas son asi
---------------------------
El contraste se mide con luminancia relativa WCAG, no con el promedio de gris.
Un promedio miente: una foto mitad blanca y mitad negra promedia gris medio y
parece segura, y el texto desaparece en la mitad clara.

Por eso se mide el PERCENTIL, no la media. Lo que hunde un texto no es el brillo
tipico del fondo sino su peor zona. Con texto oscuro manda el percentil bajo
(las zonas oscuras de la foto); con texto claro manda el percentil alto.

El semitono es el unico que no necesita medicion previa: su fondo solo puede ser
tinta o papel, nunca un valor intermedio, asi que el peor caso queda acotado por
el color de la tinta y no depende de la imagen.
"""
import argparse
import pathlib

import numpy as np
from PIL import Image

CREMA = (250, 249, 245)
OSCURO = (20, 20, 19)
NARANJA = (217, 119, 87)

OBJETIVO_AA = 4.5


def hexa(s):
    s = s.lstrip('#')
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def _lin(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def luminancia(rgb):
    """Luminancia relativa WCAG. Acepta un color o un array (h,w,3)."""
    a = np.asarray(rgb, dtype=float)
    r, g, b = _lin(a[..., 0]), _lin(a[..., 1]), _lin(a[..., 2])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(l1, l2):
    hi, lo = np.maximum(l1, l2), np.minimum(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def velo_necesario(lum_fondo, lum_texto, color_velo, objetivo=OBJETIVO_AA):
    """Opacidad minima de velo para que `lum_texto` llegue al objetivo.

    Se resuelve numericamente y no por formula porque la luminancia no es lineal
    en el canal: mezclar en sRGB y luego linealizar no es lo mismo que al reves,
    y la diferencia se nota justo en el rango que importa.
    """
    lv = np.asarray(color_velo, dtype=float)
    for alfa in np.arange(0, 1.001, 0.01):
        mezcla = lum_fondo * 0 + luminancia(
            (1 - alfa) * np.asarray(_desde_lum(lum_fondo)) + alfa * lv)
        if contraste(mezcla, lum_texto) >= objetivo:
            return round(float(alfa), 2)
    return None


def _desde_lum(l):
    """Color gris equivalente a una luminancia dada. Solo para el calculo."""
    l = float(np.clip(l, 0, 1))
    c = 12.92 * l if l <= 0.0031308 else 1.055 * (l ** (1 / 2.4)) - 0.055
    v = c * 255
    return np.array([v, v, v])


def cargar(ruta, ancho=None):
    im = Image.open(ruta).convert('RGB')
    if ancho and im.width != ancho:
        im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
    return im


# ------------------------------------------------------------------ medir ---

def recomendar(ruta):
    im = cargar(ruta, 600)
    a = np.asarray(im, dtype=float)
    lum = luminancia(a)

    p05, p50, p95 = (float(np.percentile(lum, p)) for p in (5, 50, 95))
    l_osc, l_cre = float(luminancia(OSCURO)), float(luminancia(CREMA))

    print(f"\n{ruta}")
    print(f"  luminancia  p05 {p05:.3f}  ·  mediana {p50:.3f}  ·  p95 {p95:.3f}")
    sat = np.asarray(im.convert('HSV'))[..., 1].mean() / 255
    print(f"  saturacion media {sat:.2f}"
          f"{'   (muy saturada: el duotono la mejora)' if sat > 0.35 else ''}")

    print("\n  Texto OSCURO #141413 sobre la foto")
    c = contraste(np.array(p05), l_osc)
    if c >= OBJETIVO_AA:
        print(f"    sin velo ya da {float(c):.1f}:1 — no necesita nada")
    else:
        v = velo_necesario(np.array(p05), l_osc, CREMA)
        print(f"    peor zona da {float(c):.1f}:1 — velo crema al "
              f"{int(v * 100)}%" if v else "    no llega ni con velo opaco")

    print("\n  Texto CREMA #faf9f5 sobre la foto")
    c = contraste(np.array(p95), l_cre)
    if c >= OBJETIVO_AA:
        print(f"    sin velo ya da {float(c):.1f}:1 — no necesita nada")
    else:
        v = velo_necesario(np.array(p95), l_cre, OSCURO)
        print(f"    peor zona da {float(c):.1f}:1 — velo oscuro al "
              f"{int(v * 100)}%" if v else "    no llega ni con velo opaco")

    print("\n  Tratamientos")
    rango = p95 - p05
    if rango > 0.45:
        print("    fondo-banda / fondo-corte / fondo-tarjeta — RECOMENDADOS.")
        print("      la foto tiene mucho rango: cualquier velo parejo mata el")
        print("      detalle. Separa las zonas y no pagas contraste por foto.")
    if p50 < 0.25:
        print("    fondo-scrim (oscuro) — encaja, la foto ya es oscura")
    elif p50 > 0.6:
        print("    fondo-scrim--claro — encaja, la foto ya es clara")
    print("    fondo-semitono — SIEMPRE seguro, no depende de esta foto")
    if sat > 0.3:
        print("    fondo-duotono — unifica el color, util si choca con el naranja")
    print()


# ------------------------------------------------------------- tratamientos --

def duotono(im, sombra, luz, claridad=1.0):
    """claridad > 1 empuja la imagen hacia la tinta clara.

    Sin esto, una foto con sombras profundas sale como un bloque de tinta llena y
    el resultado compite con el texto en vez de sostenerlo. El duotono util de
    esta marca es PALIDO: la foto se reconoce, no se impone.
    """
    lum = luminancia(np.asarray(im, dtype=float))
    lum = (lum - lum.min()) / max(np.ptp(lum), 1e-6)
    lum = lum ** (1.0 / claridad)
    s, l = np.array(sombra, float), np.array(luz, float)
    out = s + (l - s) * lum[..., None]
    return Image.fromarray(out.astype(np.uint8))


def semitono(im, celda, sombra, papel, claridad=1.0):
    """Puntos de tamano variable segun el tono. Ni un pixel intermedio.

    `claridad` adelgaza el punto. Un semitono al 100% de cobertura es una mancha
    plana: pierde la textura que justifica el tratamiento y tapa la escena.
    """
    a = np.asarray(im.convert('L'), dtype=float) / 255
    a = a ** (1.0 / claridad)
    h, w = a.shape
    out = Image.new('RGB', (w, h), papel)
    px = out.load()
    r_max = celda / 2 * 1.42
    for cy in range(0, h, celda):
        for cx in range(0, w, celda):
            blq = a[cy:cy + celda, cx:cx + celda]
            if blq.size == 0:
                continue
            r = (1 - blq.mean()) ** 0.85 * r_max
            ccy, ccx = cy + celda / 2, cx + celda / 2
            for y in range(max(0, int(ccy - r)), min(h, int(ccy + r) + 1)):
                for x in range(max(0, int(ccx - r)), min(w, int(ccx + r) + 1)):
                    if (x - ccx) ** 2 + (y - ccy) ** 2 <= r * r:
                        px[x, y] = sombra
    return out


def riso(im, tinta, papel, grano=14):
    lum = luminancia(np.asarray(im, dtype=float))
    lum = (lum - lum.min()) / max(np.ptp(lum), 1e-6)
    rng = np.random.default_rng(7)          # semilla fija: mismo grano siempre
    ruido = rng.normal(0, grano / 255, lum.shape)
    lum = np.clip(lum + ruido, 0, 1)
    t, p = np.array(tinta, float), np.array(papel, float)
    return Image.fromarray((t + (p - t) * lum[..., None]).astype(np.uint8))


def papel(destino, medida=(1080, 1350), tinta=OSCURO, fuerza=0.07):
    rng = np.random.default_rng(11)
    w, h = medida
    base = np.array(CREMA, float)[None, None, :] * np.ones((h, w, 1))
    ruido = rng.normal(0, fuerza, (h, w, 1))
    out = np.clip(base + (np.array(tinta, float) - base) * np.abs(ruido) * 6, 0, 255)
    Image.fromarray(out.astype(np.uint8)).save(destino)
    print(f"  grano de papel -> {destino}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('foto', nargs='?')
    ap.add_argument('--recomendar', action='store_true',
                    help='mide la foto y dice que tratamiento y cuanto velo')
    ap.add_argument('--modo', choices=['duotono', 'semitono', 'riso'])
    ap.add_argument('--sombra', default='#141413')
    ap.add_argument('--luz', default='#faf9f5')
    ap.add_argument('--celda', type=int, default=6)
    ap.add_argument('--claridad', type=float, default=1.0,
                    help='>1 aclara: empuja la imagen hacia la tinta clara')
    ap.add_argument('--ancho', type=int, default=1080)
    ap.add_argument('--papel', metavar='SALIDA', help='genera textura de grano')
    ap.add_argument('-o', '--salida')
    a = ap.parse_args()

    if a.papel:
        papel(a.papel)
        return
    if not a.foto:
        ap.error('falta la foto (o usa --papel)')
    if a.recomendar:
        recomendar(a.foto)
        return
    if not a.modo:
        ap.error('elige --modo o --recomendar')

    im = cargar(a.foto, a.ancho)
    s, l = hexa(a.sombra), hexa(a.luz)
    if a.modo == 'duotono':
        out = duotono(im, s, l, a.claridad)
    elif a.modo == 'semitono':
        out = semitono(im, a.celda, s, l, a.claridad)
    else:
        out = riso(im, s, l)

    destino = a.salida or str(pathlib.Path(a.foto).with_suffix('')) + f'-{a.modo}.webp'
    out.save(destino, quality=92)
    print(f"  {a.modo} -> {destino}")


if __name__ == '__main__':
    main()
