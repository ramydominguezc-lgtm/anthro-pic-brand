#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera un catalogo PDF con TODOS los assets de la skill, cada uno rotulado.

Sirve para dos cosas: identificar de un vistazo que hay en la biblioteca, y
comprobar visualmente que cada archivo se ve bien. Cada asset se muestra sobre
tres fondos —claro, naranja y oscuro— porque un asset puede verse perfecto sobre
uno y desaparecer sobre otro, y eso es exactamente lo que hay que poder detectar.

Uso:  python3 catalogo_pdf.py [--salida catalogo.pdf]
"""
import argparse, io, pathlib
try:  # dep-guard
    import cairosvg
except ImportError:
    import sys
    sys.exit("Falta el paquete `cairosvg`, que no viene en el contenedor.\n"
             "  pip install cairosvg --break-system-packages\n"
             "Este script es de mantenimiento de la biblioteca, no de\n"
             "produccion: el equipo de comunicacion no lo necesita.")
from PIL import Image
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONDOS = [("claro", (250, 249, 245)), ("naranja", (217, 119, 87)),
          ("oscuro", (20, 20, 19))]
GRUPOS = [
    ("Logos", "logos", "El glifo y el wordmark oficiales. El SVG es la version de trabajo."),
    ("Lockups", "logos-claudetec", "Compuestos con el asterisco oficial. Ver 'Marcas derivadas' antes de usarlos."),
    ("Iconos", "iconos",
     "PNG transparente con textura. Su fondo es el naranja; sobre oscuro se pierden."),
    ("Ilustraciones", "ilustraciones", "Line art a dos tintas. Cada base tiene cinco variantes de color."),
    ("Clawd", "clawd", "La mascota. Registro informal. Solo dos tienen SVG; ver nota."),
]
DARK, LIGHT, MUTED, ORANGE = (.08, .08, .075), (.98, .976, .96), (.49, .48, .45), (.85, .47, .34)


def cargar(ruta, lado=300):
    """Devuelve un PIL RGBA del asset, rasterizando el SVG si hace falta."""
    if ruta.suffix.lower() == ".svg":
        png = cairosvg.svg2png(url=str(ruta), output_width=lado)
        return Image.open(io.BytesIO(png)).convert("RGBA")
    im = Image.open(ruta).convert("RGBA")
    im.thumbnail((lado, lado), Image.LANCZOS)
    return im


def sobre(im, rgb, lado=300):
    fondo = Image.new("RGBA", (lado, lado), rgb + (255,))
    c = im.copy()
    c.thumbnail((lado - 24, lado - 24), Image.LANCZOS)
    fondo.paste(c, ((lado - c.width) // 2, (lado - c.height) // 2), c)
    return fondo.convert("RGB")


def main(salida):
    W, H = landscape(letter)
    c = canvas.Canvas(str(salida), pagesize=(W, H))
    M = 16 * mm

    # --- portada ---
    c.setFillColorRGB(*LIGHT); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColorRGB(*DARK)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(M, H - M - 34, "Biblioteca de marca")
    c.setFont("Helvetica", 15)
    c.setFillColorRGB(*MUTED)
    c.drawString(M, H - M - 58, "anthro-pic-brand \u2014 catalogo de assets")
    c.setFont("Helvetica", 11)
    y = H - M - 100
    total = sum(len(list((RAIZ / "assets" / d).glob("*")))
                for _, d, _ in GRUPOS if (RAIZ / "assets" / d).is_dir())
    for linea in [
        f"{total} archivos. Cada asset aparece sobre los tres fondos del sistema:",
        "claro #faf9f5, naranja #d97757 y oscuro #141413.",
        "",
        "Si un asset desaparece sobre alguno de los tres, esa combinacion no se usa.",
    ]:
        c.setFillColorRGB(*DARK if linea else MUTED)
        c.drawString(M, y, linea); y -= 17
    c.showPage()

    # --- grupos ---
    for titulo, carpeta, nota in GRUPOS:
        d = RAIZ / "assets" / carpeta
        if not d.is_dir():
            continue
        archivos = sorted([f for f in d.iterdir()
                           if f.suffix.lower() in {".svg", ".png", ".webp"}])
        por_pagina = 4
        for i in range(0, len(archivos), por_pagina):
            lote = archivos[i:i + por_pagina]
            c.setFillColorRGB(*LIGHT); c.rect(0, 0, W, H, fill=1, stroke=0)
            c.setFillColorRGB(*DARK); c.setFont("Helvetica-Bold", 19)
            c.drawString(M, H - M - 8, titulo)
            c.setFillColorRGB(*MUTED); c.setFont("Helvetica", 9.5)
            c.drawString(M, H - M - 24, nota)
            c.drawRightString(W - M, H - M - 8,
                              f"{i + 1}\u2013{min(i + por_pagina, len(archivos))} de {len(archivos)}")
            c.setStrokeColorRGB(.91, .90, .86)
            c.line(M, H - M - 32, W - M, H - M - 32)

            fila_h = (H - 2 * M - 46) / por_pagina
            cel = min(fila_h - 12, 46 * mm)
            for j, f in enumerate(lote):
                y0 = H - M - 44 - (j + 1) * fila_h + (fila_h - cel) / 2
                c.setFillColorRGB(*DARK); c.setFont("Helvetica-Bold", 10)
                c.drawString(M, y0 + cel - 9, f.name)
                c.setFillColorRGB(*MUTED); c.setFont("Helvetica", 8)
                kb = f.stat().st_size / 1024
                tipo = "vector" if f.suffix.lower() == ".svg" else "raster"
                c.drawString(M, y0 + cel - 22, f"{tipo} \u00b7 {kb:.1f} KB")
                try:
                    im = cargar(f)
                except Exception as e:
                    c.setFillColorRGB(.8, .2, .2)
                    c.drawString(M, y0 + cel - 36, f"no se pudo abrir: {e}")
                    continue
                x = M + 62 * mm
                for nombre, rgb in FONDOS:
                    c.drawImage(ImageReader(sobre(im, rgb)), x, y0, cel, cel)
                    c.setFillColorRGB(*MUTED); c.setFont("Helvetica", 7)
                    c.drawString(x, y0 - 9, nombre)
                    x += cel + 6 * mm
            c.showPage()

    # --- matriz de compatibilidad ---
    import numpy as np
    filas = []
    for _, carpeta, _ in GRUPOS:
        d = RAIZ / "assets" / carpeta
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            if f.suffix.lower() not in {".svg", ".png", ".webp"}:
                continue
            try:
                a = np.array(cargar(f)).astype(float)
            except Exception:
                continue
            al = a[:, :, 3:4] / 255
            marcas = []
            for nombre, bg in FONDOS:
                comp = a[:, :, :3] * al + np.array(bg) * (1 - al)
                vis = (np.linalg.norm(comp - np.array(bg), axis=2) > 30).mean()
                marcas.append("si" if vis >= 0.03 else "NO")
            if "NO" in marcas:
                filas.append((f"{carpeta}/{f.name}", marcas))

    c.setFillColorRGB(*LIGHT); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColorRGB(*DARK); c.setFont("Helvetica-Bold", 19)
    c.drawString(M, H - M - 8, "Sobre que fondo NO usar cada variante")
    c.setFillColorRGB(*MUTED); c.setFont("Helvetica", 9.5)
    c.drawString(M, H - M - 24,
                 "Es por diseno, no un defecto: una variante --mono desaparece sobre "
                 "oscuro y una --sobre-naranja desaparece sobre claro.")
    c.setStrokeColorRGB(.91, .90, .86); c.line(M, H - M - 32, W - M, H - M - 32)
    y = H - M - 52
    c.setFont("Helvetica-Bold", 8.5); c.setFillColorRGB(*MUTED)
    c.drawString(M, y, "archivo")
    for k, (nombre, _) in enumerate(FONDOS):
        c.drawString(M + 118 * mm + k * 24 * mm, y, nombre)
    y -= 12
    c.setFont("Helvetica", 8.5)
    for nombre, marcas in filas:
        if y < M:
            c.showPage(); y = H - M
        c.setFillColorRGB(*DARK); c.drawString(M, y, nombre)
        for k, mk in enumerate(marcas):
            c.setFillColorRGB(*(ORANGE if mk == "NO" else MUTED))
            c.drawString(M + 118 * mm + k * 24 * mm, y, mk)
        y -= 11.5
    c.showPage()

    c.save()
    return salida


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--salida", default=str(RAIZ / "catalogo.pdf"))
    a = p.parse_args()
    print("->", main(a.salida))
