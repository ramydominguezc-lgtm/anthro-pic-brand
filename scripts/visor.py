#!/usr/bin/env python3
"""Compila el visor de la biblioteca: inventario de assets + plantilla -> HTML.

    python3 scripts/visor.py                 # escribe visor-veredictos.html
    python3 scripts/visor.py --solo-lista    # imprime el inventario y sale

El HTML que sale se publica como Artifact para revisar la biblioteca desde el
navegador: cada recurso sobre los cuatro fondos, con veredicto, marcas por fondo
y encargos de mejora. Los veredictos NO viven aqui: los guarda el Artifact.

CORRE ESTO tras anadir, quitar o renombrar un asset — el inventario se lee del
disco, asi que la unica forma de que el visor mienta es no regenerarlo.

DE DONDE SALE CADA COSA
- Medidas: de la imagen (PIL) o del viewBox del SVG. No se escriben a mano.
"""
import argparse
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'visor-veredictos.html'
PLANTILLA = RAIZ / 'scripts/visor.plantilla.html'

# carpeta, titulo, nota que explica para que sirve el grupo
CARPETAS = [
    ('logos',         'Logos',          'El asterisco y el wordmark oficiales.'),
    ('logos-claudetec',       'Lockups',        'ClaudeTec compuesto. Marca derivada: ver la advertencia del catalogo.'),
    ('ilustraciones', 'Ilustraciones',  'Line art a dos tintas, con sus variantes de color.'),
    ('clawd',         'Clawd',          'La mascota, registro informal. No va en material institucional.'),
    ('iconos',        'Iconos',         'Dibujos con textura sobre transparente. Van sobre naranja, no sobre oscuro.'),
    ('fotos',         'Fotos',          'Fototeca base. El tratamiento se aplica por pieza con tratar_foto.py.'),
]
EXT = {'.png', '.svg', '.webp'}


def medida(p):
    if p.suffix == '.svg':
        t = p.read_text(encoding='utf-8', errors='ignore')[:4000]
        m = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', t)
        return f'{round(float(m.group(1)))} x {round(float(m.group(2)))} vect.' if m else 'vectorial'
    try:
        from PIL import Image
        w, h = Image.open(p).size
        return f'{w} x {h}'
    except ImportError:
        sys.exit('Falta Pillow:  pip install pillow')
    except Exception:
        return '—'


def inventario():
    grupos = []
    for carpeta, titulo, nota in CARPETAS:
        d = RAIZ / 'assets' / carpeta
        # Una ficha por DIBUJO, no por archivo: el SVG y su PNG derivado son la
        # misma pieza y comparten veredicto. Se muestra el vector si lo hay.
        por_dibujo = {}
        for p in sorted(d.iterdir()):
            if p.suffix.lower() not in EXT:
                continue
            por_dibujo.setdefault(p.stem, []).append(p)
        items = []
        for nombre, rutas in por_dibujo.items():
            rutas.sort(key=lambda r: r.suffix != '.svg')   # el vector primero
            principal = rutas[0]
            items.append({
                'id': f'{carpeta}--{nombre}',
                'ruta': f'assets/{carpeta}/{principal.name}',
                'nombre': nombre,
                'formato': ' + '.join(r.suffix[1:].upper() for r in rutas),
                'medida': medida(principal),
                'kb': round(sum(r.stat().st_size for r in rutas) / 1024),
            })
        grupos.append({'carpeta': carpeta, 'tipo': 'asset', 'titulo': titulo,
                       'nota': nota, 'items': items})

    return grupos


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--solo-lista', action='store_true',
                    help='imprime las rutas, una por linea, y no escribe el HTML')
    a = ap.parse_args()

    grupos = inventario()
    if a.solo_lista:
        for g in grupos:
            for i in g['items']:
                print(i['ruta'])
        return

    html = PLANTILLA.read_text(encoding='utf-8')
    if '__DATOS__' not in html:
        sys.exit('La plantilla perdio el marcador __DATOS__.')
    SALIDA.write_text(
        html.replace('__DATOS__', json.dumps(grupos, ensure_ascii=False)),
        encoding='utf-8')

    for g in grupos:
        print(f'  {g["titulo"]:22} {len(g["items"]):>3}')
    total = sum(len(g['items']) for g in grupos)
    print(f'\n{SALIDA.name}: {total} piezas · {round(SALIDA.stat().st_size / 1024)} KB')


if __name__ == '__main__':
    main()
