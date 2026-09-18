#!/usr/bin/env python3
"""Genera el PNG derivado de cada SVG de la biblioteca.

    python3 scripts/derivar_png.py              # solo los que faltan
    python3 scripts/derivar_png.py --todos      # rehace todos

POR QUE EXISTE
La regla de la skill es que nada derivado se guarda sin un script que lo
produzca. Los 21 PNG de ilustracion se anadieron en v2.4 para cumplir el
estandar de "solo PNG y SVG", asi que hacia falta este script: sin el, esos
archivos serian 1.5 MB que nadie sabe regenerar.

POR QUE PLAYWRIGHT Y NO CAIROSVG
cairosvg ignora `image-rendering`, asi que suaviza el pixel art de Clawd y lo
arruina. Chromium lo respeta. Ademas es el mismo motor con el que se
rasterizan las piezas, asi que no hay dos renderizadores que discrepen.

El lienzo es cuadrado de 1080 px — tamano 1:1 de un poster — con el arte
centrado y fondo transparente, igual que los iconos.
"""
import argparse
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CARPETAS = ('ilustraciones', 'clawd', 'logos', 'logos-claudetec')
LADO = 1080


def pendientes(todos):
    for carpeta in CARPETAS:
        for svg in sorted((RAIZ / 'assets' / carpeta).glob('*.svg')):
            if todos or not svg.with_suffix('.png').exists():
                yield svg


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--todos', action='store_true',
                    help='rehace tambien los PNG que ya existen')
    ap.add_argument('--lado', type=int, default=LADO, help='lado del lienzo')
    a = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit('Falta Playwright:  pip install playwright && playwright install chromium')

    lista = list(pendientes(a.todos))
    if not lista:
        print('Nada que generar: todos los SVG ya tienen su PNG.')
        return

    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for svg in lista:
            pg = nav.new_page(viewport={'width': a.lado, 'height': a.lado})
            marca = svg.read_text(encoding='utf-8').replace(
                '<svg', "<svg style='width:100%;height:100%;image-rendering:pixelated'", 1)
            pg.set_content(
                f'<body style="margin:0">'
                f'<div style="width:{a.lado}px;height:{a.lado}px;display:grid;place-items:center">'
                f'{marca}</div></body>')
            pg.screenshot(path=str(svg.with_suffix('.png')), omit_background=True)
            pg.close()
            print(f'  {svg.stem}.png')
        nav.close()
    print(f'\n{len(lista)} PNG derivados en assets/')


if __name__ == '__main__':
    main()
