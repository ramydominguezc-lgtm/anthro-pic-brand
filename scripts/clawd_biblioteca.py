#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Puente con la skill `clawd-biblioteca`: encuentra una animación terminada.

    python3 scripts/clawd_biblioteca.py              lista lo que hay
    python3 scripts/clawd_biblioteca.py paseo mp4    imprime la ruta

Y desde otro script:

    from clawd_biblioteca import pieza
    gif = pieza('paseo', 'transparente')      # ruta al GIF con alfa
    f62 = pieza('paseo', 'fotograma', 62)     # ruta a un cuadro suelto

POR QUE ESTO EXISTE
  La skill de marca **no genera animaciones**. Las consume. Hasta ahora esa
  dependencia estaba escrita como una ruta absoluta dentro de un script:

      PASEO = pathlib.Path(r'C:\\Users\\alfav\\OneDrive\\Desktop\\Clawd - Biblioteca\\paseo')

  Eso funciona en una maquina y en ninguna otra, y cuando falla lo hace al abrir
  el archivo, no al empezar. Aqui la busqueda esta en un sitio, prueba varias
  ubicaciones y, si no encuentra la biblioteca, lo dice con el nombre de la skill
  que hay que instalar en vez de soltar un FileNotFoundError.

EL REPARTO ENTRE LAS TRES SKILLS
  `clawd-animaciones`  genera. Metodo, motor y recetas.
  `clawd-biblioteca`   almacena y entrega lo terminado. Su `CATALOGO.md` manda.
  `anthro-pic-brand`   (esta) compone piezas. Consume de la biblioteca.

  Los **stickers quietos** de Clawd —`clawd-base`, `coffee`, `search`,
  `skateboard`, `headphones`— se quedan aqui, en `assets/clawd/`. No es una
  preferencia: la biblioteca guarda animaciones, su tabla de entrega son formatos
  animados (gif, webp, mp4, hoja de sprites), y su regla 3 dice que `clawd-base`
  de la skill de marca **es otro dibujo** —brazos de distinto ancho— que no se
  mezcla con los animados. Moverlos alli juntaria dos dibujos en una biblioteca
  que existe para no mezclarlos.

QUE CONSUME HOY LA SKILL DE MARCA
  `paseo` — en `salida/ventanas_67.py` (la pieza de terminal). El fotograma 62
  para el PNG fijo y `clawd-paseo-transparente.gif` para el MP4. Si alguien
  regenera `paseo` en `clawd-animaciones`, esa pieza cambia.
"""
import pathlib
import sys

CANDIDATAS = [
    pathlib.Path.home() / 'OneDrive' / 'Desktop' / 'Clawd - Biblioteca',
    pathlib.Path.home() / 'Desktop' / 'Clawd - Biblioteca',
    pathlib.Path('/mnt/skills/user/clawd-biblioteca'),
    pathlib.Path(__file__).resolve().parent.parent.parent / 'Clawd - Biblioteca',
]


def raiz():
    for c in CANDIDATAS:
        if (c / 'CATALOGO.md').exists():
            return c
    raise FileNotFoundError(
        'No encuentro la skill `clawd-biblioteca`. Se busco en:\n  '
        + '\n  '.join(str(c) for c in CANDIDATAS)
        + '\nInstalala o pasa la ruta a mano. Esta skill no genera animaciones: '
          'las toma de ahi.')


def pieza(animacion, formato='mp4', n=None):
    """Ruta a un archivo de una animacion. `formato`: mp4, gif, transparente,
    webp, bloque, hoja, css, fotograma (con n) o svg (con n)."""
    d = raiz() / animacion
    if not d.is_dir():
        disponibles = ', '.join(sorted(x.name for x in raiz().iterdir() if x.is_dir()
                                       and not x.name.startswith('_')))
        raise FileNotFoundError(f'`{animacion}` no esta en la biblioteca. Hay: {disponibles}')
    mapa = {
        'mp4': f'clawd-{animacion}.mp4',
        'gif': f'clawd-{animacion}.gif',
        'transparente': f'clawd-{animacion}-transparente.gif',
        'webp': f'clawd-{animacion}.webp',
        'bloque': f'clawd-{animacion}-bloque.html',
        'hoja': f'clawd-{animacion}-hoja.png',
        'css': f'clawd-{animacion}.css',
    }
    n = int(n) if n is not None else None   # llega como texto desde la linea de ordenes
    if formato == 'fotograma':
        f = d / 'fotogramas' / f'clawd-{animacion}-f{n:03d}.png'
    elif formato == 'svg':
        f = d / 'svg' / f'clawd-{animacion}-f{n:03d}.svg'
    else:
        if formato not in mapa:
            raise ValueError(f'formato desconocido: {formato}. Hay: '
                             + ', '.join(list(mapa) + ['fotograma', 'svg']))
        f = d / mapa[formato]
    if not f.exists():
        raise FileNotFoundError(
            f'{f} no existe. Mira el CATALOGO.md de la biblioteca; si la '
            f'animacion hace falta en otro formato, la regenera `clawd-animaciones`.')
    return f


def main():
    if any(a in ('-h', '--help') for a in sys.argv[1:]):
        print(__doc__)
        return
    if len(sys.argv) == 1:
        r = raiz()
        print(f'clawd-biblioteca en {r}\n')
        for d in sorted(x for x in r.iterdir() if x.is_dir() and not x.name.startswith('_')):
            n = len(list((d / 'fotogramas').glob('*.png'))) if (d / 'fotogramas').is_dir() else 0
            print(f'  {d.name:<16} {n:>4} fotogramas')
        print('\nEl CATALOGO.md de la biblioteca tiene el estado de cada una.')
        return
    print(pieza(sys.argv[1], *(sys.argv[2:])))


if __name__ == '__main__':
    main()
