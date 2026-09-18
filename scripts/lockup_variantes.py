#!/usr/bin/env python3
"""Genera las variantes de color del lockup de ClaudeTec a partir del vector bueno.

    python3 scripts/lockup_variantes.py            # escribe en assets/logos-claudetec/
    python3 scripts/lockup_variantes.py salida/

POR QUE ESTE SCRIPT Y NO `lockup.py`
`lockup.py` compone una palabra desde la fuente Newsreader. Este lockup NO sale
de ahi: las dos "e" son glifos redibujados a mano (la correccion de agosto de
2026) e insertados como paths propios con su transform. Recomponerlo desde la
fuente devuelve la "e" vieja. Por eso la fuente de verdad es el SVG corregido y
lo unico que hace este script es repartir el color entre sus glifos.

ESTRUCTURA DEL SVG FUENTE
    <g fill=NARANJA>   el asterisco, un solo path
    <g fill=TEXTO>     nueve paths, uno por glifo, en orden C l a u d e T e c
                       (los paths 6 y 8 son las dos "e" corregidas, con su
                       propio transform y escala)

"Claude" son los primeros seis paths y "Tec" los tres ultimos. El duotono se
consigue sacando esos tres a un grupo con otro fill; no se toca ninguna
coordenada.
"""
import argparse
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FUENTE = RAIZ / 'assets/logos-claudetec/claudetec.svg'
GLIFOS_CLAUDE = 6          # C l a u d e  — el resto es "Tec"

DARK, LIGHT, ORANGE = '#141413', '#faf9f5', '#d97757'

# nombre: (color del asterisco, color de "Claude", color de "Tec")
VARIANTES = {
    'claudetec':                 (ORANGE, DARK,   DARK),    # fondo claro, una tinta
    'claudetec--claro':          (ORANGE, LIGHT,  LIGHT),   # fondo oscuro o naranja
    'claudetec--duotono':        (ORANGE, DARK,   ORANGE),  # fondo claro
    'claudetec--duotono-claro':  (ORANGE, LIGHT,  ORANGE),  # fondo oscuro
    # Sobre naranja el asterisco naranja desaparece: esta es la unica
    # variante que aguanta ese fondo, con las tres tintas en claro.
    'claudetec--monocromo-claro': (LIGHT, LIGHT,  LIGHT),   # fondo naranja
}


def componer(svg, ast, claude, tec):
    """Devuelve el SVG con los tres colores aplicados."""
    # 1. asterisco: el primer grupo con fill
    ast_m = re.search(r'(<g[^>]*?)fill="#d97757"', svg)
    if not ast_m:
        sys.exit('No encontre el grupo del asterisco en el SVG fuente.')
    nuevo_ast = ast_m.group(1) + f'fill="{ast}"'
    svg = svg[:ast_m.start()] + nuevo_ast + svg[ast_m.end():]
    tras_ast = ast_m.start() + len(nuevo_ast)

    # 2. el grupo del texto: se le pone el color de "Claude"...
    #    Se busca DESPUES del asterisco a proposito. Buscando desde el
    #    principio, si el asterisco acaba de pintarse claro la expresion
    #    vuelve a encontrarlo A EL, lo repinta, y el texto se queda con su
    #    color original. Asi salio mal `--monocromo-claro` la primera vez:
    #    asterisco claro y "ClaudeTec" negro sobre fondo naranja.
    m = re.search(r'<g[^>]*fill="(#141413|#faf9f5)"[^>]*>', svg[tras_ast:])
    if not m:
        sys.exit('No encontre el grupo de texto en el SVG fuente.')
    ini_m, fin_m = tras_ast + m.start(), tras_ast + m.end()
    svg = svg[:ini_m] + m.group(0).replace(m.group(1), claude) + svg[fin_m:]

    if tec == claude:
        return svg

    # 3. ...y los tres ultimos glifos se sacan a un grupo propio.
    ini = ini_m + len(m.group(0).replace(m.group(1), claude))
    fin = svg.index('</g>', ini)
    paths = re.findall(r'<path[^>]*/>', svg[ini:fin])
    if len(paths) <= GLIFOS_CLAUDE:
        sys.exit(f'Esperaba mas de {GLIFOS_CLAUDE} glifos, encontre {len(paths)}.')

    cuerpo = ''.join(paths[:GLIFOS_CLAUDE])
    # El grupo anidado hereda el transform del padre: los glifos de "Tec"
    # conservan su posicion sin recalcular nada.
    cuerpo += f'<g fill="{tec}">' + ''.join(paths[GLIFOS_CLAUDE:]) + '</g>'
    return svg[:ini] + cuerpo + svg[fin:]


def rasterizar(svgs, destino, ancho=3000):
    """SVG -> PNG transparente. Sin playwright avisa y no revienta."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('\nPNG no generados: falta playwright.')
        print('  pip install playwright && python -m playwright install chromium')
        return
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for ruta in svgs:
            svg = ruta.read_text(encoding='utf-8')
            vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
            w, h = float(vb.group(1)), float(vb.group(2))
            alto = round(ancho * h / w)
            pg = nav.new_page(viewport={'width': ancho, 'height': alto},
                              device_scale_factor=1)
            pg.set_content(
                f'<style>html,body{{margin:0;background:transparent}}'
                f'svg{{width:{ancho}px;height:{alto}px;display:block}}</style>{svg}')
            pg.screenshot(path=str(destino / (ruta.stem + '.png')),
                          omit_background=True)
            pg.close()
            print(f'  {ruta.stem}.png  {ancho}x{alto}')
        nav.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('destino', nargs='?', default='assets/logos-claudetec')
    ap.add_argument('--ancho', type=int, default=3000, help='ancho del PNG')
    ap.add_argument('--solo-svg', action='store_true')
    a = ap.parse_args()

    destino = pathlib.Path(a.destino)
    if not destino.is_absolute():
        destino = RAIZ / destino
    destino.mkdir(parents=True, exist_ok=True)

    base = FUENTE.read_text(encoding='utf-8')
    escritos = []
    for nombre, (ast, claude, tec) in VARIANTES.items():
        ruta = destino / (nombre + '.svg')
        ruta.write_text(componer(base, ast, claude, tec), encoding='utf-8')
        escritos.append(ruta)
        print(f'  {nombre}.svg')

    if not a.solo_svg:
        rasterizar(escritos, destino, a.ancho)


if __name__ == '__main__':
    main()
