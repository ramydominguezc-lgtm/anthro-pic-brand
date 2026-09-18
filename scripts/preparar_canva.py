#!/usr/bin/env python3
"""Arma la carpeta de assets lista para subir a Canva a mano.

    python3 scripts/preparar_canva.py            # -> ./assets-canva/
    python3 scripts/preparar_canva.py /ruta/dest

POR QUE ES UN SCRIPT Y NO UNA CARPETA
Antes esto vivia como `assets-canva/` dentro de la skill, y era una copia literal
de archivos que ya estaban en `assets/`: 9 MB duplicados que ademas se quedaban
viejos en cuanto se tocaba un asset. La carpeta se genera en tres segundos, asi
que no hay razon para guardarla.

Los pasos de montaje —colores en orden, fuentes, campos de autofill— estan en
`references/guia-canva.md`. Este script solo prepara los archivos.
"""
import argparse
import pathlib
import shutil
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent

# Que se sube y en que orden. Los numeros son para que Canva los liste asi.
GRUPOS = {
    '1-logos': [
        'assets/logos/claude-wordmark.svg',
        'assets/logos-claudetec/claudetec.svg',
        'assets/logos-claudetec/claudetec--claro.svg',
        'assets/logos-claudetec/claudetec--duotono.svg',
        'assets/logos/claude-glyph.svg',
    ],
    '2-ilustraciones': ['assets/ilustraciones/*.svg'],
    '3-clawd': [
        'assets/clawd/clawd-base.svg',
        'assets/clawd/clawd-headphones.svg',
    ],
    '4-fotos': ['assets/fotos/*.png'],
}

# Variantes que no se suben: multiplican la biblioteca sin aportar en Canva,
# donde el color se cambia desde el propio editor.
EXCLUIR = ('--azul.svg', '--verde.svg')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('destino', nargs='?', default='assets-canva')
    a = ap.parse_args()
    destino = pathlib.Path(a.destino)

    if destino.exists():
        shutil.rmtree(destino)

    n = 0
    for grupo, patrones in GRUPOS.items():
        (destino / grupo).mkdir(parents=True)
        for patron in patrones:
            rutas = sorted(RAIZ.glob(patron)) if '*' in patron else [RAIZ / patron]
            for r in rutas:
                if not r.exists():
                    # Avisa en vez de saltar en silencio: dos lockups declarados
                    # aqui llevaban meses sin existir y nadie se entero.
                    print(f'  AVISO: declarado pero no existe: {patron}')
                    continue
                if r.name.endswith(EXCLUIR):
                    continue
                shutil.copy2(r, destino / grupo / r.name)
                n += 1

    mb = sum(f.stat().st_size for f in destino.rglob('*') if f.is_file()) / 1048576
    print(f'{n} archivos en {destino}/ · {mb:.1f} MB')
    print('Siguiente paso: references/guia-canva.md')


if __name__ == '__main__':
    main()
