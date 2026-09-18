#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dice qué se puede hacer AQUÍ antes de prometer nada.

    python3 scripts/entorno.py

Es lo primero que hay que correr al abrir la skill en un sitio nuevo.

POR QUE
  Esta skill corre en tres sitios y no son iguales:

    Claude Code en la terminal   todo probado, es donde se desarrolla
    Claude desktop               igual que la terminal si comparte el Python
    claude.ai web                contenedor: puede faltar Chromium y ffmpeg

  La diferencia importa porque casi todo aquí termina en un render. Sin
  Chromium no hay PNG; sin ffmpeg no hay MP4 ni GIF. Prometerlo y fallar a la
  mitad es peor que decirlo al principio, y el modo de fallo por defecto es
  malo: el script revienta con un ImportError a los treinta segundos de trabajo.

  Esto lo pregunta en dos segundos y dice qué hacer con lo que falte.

QUE SE PIERDE SIN CADA COSA
  Chromium (playwright)  no hay PNG ni PDF de ninguna pieza. Queda el HTML, que
                         se abre en un navegador y se captura a mano: todas las
                         piezas de esta skill son HTML autónomo con los assets
                         embebidos, así que el HTML es entregable por sí solo.
  ffmpeg                 no hay MP4 ni GIF. El PNG del último fotograma sí sale.
  Pillow                 no hay nada: es el mínimo.
  numpy + scipy          no se puede medir una pieza (`analizar_referencia`,
                         `veredictos`, `validar`). Se puede componer a ciegas,
                         que es exactamente lo que esta skill intenta evitar.
  cairosvg               no hay `catalogo_pdf.py`. Lo demás no lo usa.
  uharfbuzz + fonttools  no se puede recomponer un lockup desde cero
                         (`lockup.py`). Los lockups ya hechos no lo necesitan.
"""
import importlib.util
import shutil
import subprocess
import sys

# (modulo o binario, para que sirve, que se pierde sin el)
PIEZAS = [
    ('PIL', 'Pillow — abrir y recortar imágenes', 'todo'),
    ('numpy', 'medir piezas', 'analizar_referencia, veredictos, validar'),
    ('scipy', 'medir capas y solapes', 'analizar_referencia, veredictos'),
    ('playwright', 'Chromium — HTML a PNG y a PDF', 'todos los renders'),
    ('cairosvg', 'rasterizar SVG', 'catalogo_pdf'),
    ('reportlab', 'armar PDF', 'catalogo_pdf, manual_pdf'),
    ('uharfbuzz', 'componer texto con la fuente', 'lockup'),
    ('fontTools', 'leer la fuente', 'lockup'),
    ('vtracer', 'vectorizar mapas de bits', 'vectorizar, vectorizar_pixelart'),
]


def hay(modulo):
    try:
        return importlib.util.find_spec(modulo) is not None
    except (ImportError, ValueError):
        return False


def chromium():
    """Tener el paquete `playwright` no es tener el navegador instalado: son dos
    pasos distintos y el segundo se olvida. Se comprueba abriendolo."""
    if not hay('playwright'):
        return False, 'falta el paquete'
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            nav = pw.chromium.launch()
            v = nav.version
            nav.close()
        return True, v
    except Exception as e:                       # noqa: BLE001
        return False, str(e).split('\n')[0][:70]


def main():
    print(f'python {sys.version.split()[0]} · {sys.platform}\n')

    falta = []
    for mod, para, pierde in PIEZAS:
        ok = hay(mod)
        print(f'  {"OK  " if ok else "NO  "}{mod:<12} {para}')
        if not ok:
            falta.append((mod, pierde))

    ok, detalle = chromium()
    print(f'  {"OK  " if ok else "NO  "}{"chromium":<12} navegador de Playwright — {detalle}')
    if not ok:
        falta.append(('chromium', 'todos los renders'))

    ff = shutil.which('ffmpeg')
    if ff:
        v = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        print(f'  OK  {"ffmpeg":<12} {v.stdout.split(chr(10))[0][:58]}')
    else:
        print(f'  NO  {"ffmpeg":<12} vídeo')
        falta.append(('ffmpeg', 'MP4 y GIF de collage_animado y de la pieza de terminal'))

    print()
    if not falta:
        print('Todo disponible: se puede hacer cualquier cosa de la skill.')
        return 0

    print('FALTA:')
    for mod, pierde in falta:
        print(f'  {mod:<12} -> sin esto no hay: {pierde}')
    print('\nQué hacer:')
    if any(m in ('playwright', 'chromium') for m, _ in falta):
        print('  - Sin Chromium: genera el HTML igual y entrégalo. Las piezas de esta')
        print('    skill llevan los assets embebidos, así que el HTML se abre y se')
        print('    captura en cualquier navegador. Prueba `playwright install chromium`.')
    if any(m == 'ffmpeg' for m, _ in falta):
        print('  - Sin ffmpeg: entrega el PNG y di que el MP4 queda pendiente.')
        print('    Prueba `pip install imageio-ffmpeg`.')
    otros = [m for m, _ in falta
             if m not in ('playwright', 'chromium', 'ffmpeg', 'numpy', 'scipy')]
    if otros:
        print(f'  - Lo demás son extras de mantenimiento: pip install {" ".join(otros)}')
    if any(m in ('numpy', 'scipy') for m, _ in falta):
        print('  - Sin numpy/scipy no se puede medir. Avísalo: esta skill decide con')
        print('    números, y sin ellos las decisiones vuelven a ser impresiones.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
