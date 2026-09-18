#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arma el ZIP que se sube a Claude. Se niega si no cabe o si algo esta roto.

    python3 scripts/empaquetar.py              lo arma en el escritorio
    python3 scripts/empaquetar.py --listar     solo dice que entraria y cuanto pesa
    python3 scripts/empaquetar.py --con-piezas incluye piezas-aprobadas/ (no cabe)

POR QUE HAY UN SCRIPT Y NO UNA LINEA DE `zip`
  Hasta la v2.15 el protocolo de VERSION.md era esto:

      zip -r anthro-pic-brand-vAAAA-MM-DD.zip anthro-pic-brand -x '*/salida/*'

  Tiene tres agujeros y los tres son silenciosos:
    1. No excluye `.git/`. Desde que la skill esta en GitHub son cientos de
       archivos invisibles que revientan el tope de 200 sin que nadie lo vea.
    2. No excluye `__pycache__/` ni `.DS_Store`, que crecen solos.
    3. No cuenta nada. El ZIP sale igual con 240 archivos y el fallo aparece
       al subirlo, cuando ya cerraste la sesion.
  Aqui el limite es una comprobacion, no un recordatorio.

QUE ENTRA Y QUE NO
  Entra lo que el flujo LEE al componer una pieza: SKILL.md y los MD de
  `references/`, los scripts, y `assets/` —que es material que se coloca DENTRO
  de la pieza: logos, ilustraciones, iconos, tipografias, tokens—.

  No entra lo que el flujo solo PRODUJO:

    salida/              trabajo generado; los guiones se quedan en el repo
    piezas-aprobadas/    piezas terminadas. Son tuyas, no herramienta: nada al
                         componer las abre, y mirarlas cuesta ~1,900 tokens por
                         imagen. Lo que la sesion necesita de ellas esta en
                         `references/veredictos.md` en forma de numeros y
                         motivos, que son ~700 tokens para las 23 filas.
    referencias/         inspiracion que cargo Ramses. No la lee ningun script;
                         solo se cita en prosa.
    .git/                el repositorio.

  Lo que sale del ZIP **no se pierde**: vive en el repositorio de GitHub, que es
  el archivo. El ZIP es la herramienta de trabajo. Son dos cosas distintas y
  confundirlas es lo que llenaba el ZIP de material que nadie abria.
"""
import datetime
import pathlib
import subprocess
import sys
import zipfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TOPE = 200                      # archivos que admite una skill

# Carpetas de primer nivel que no viajan. `piezas-aprobadas` sale de aqui si se
# pasa --con-piezas, que es la unica razon por la que la lista es una variable.
FUERA = {'salida', 'piezas-aprobadas', 'referencias', '.git', '.github',
         'assets-canva', 'node_modules'}
# Basura que aparece en cualquier nivel.
BASURA = {'__pycache__', '.DS_Store', 'Thumbs.db', '.pytest_cache'}


def entran(con_piezas=False):
    fuera = FUERA - {'piezas-aprobadas'} if con_piezas else FUERA
    for p in sorted(RAIZ.rglob('*')):
        if not p.is_file():
            continue
        partes = p.relative_to(RAIZ).parts
        if partes[0] in fuera or any(x in BASURA for x in partes):
            continue
        # `.gitignore` y `.gitattributes` son del repositorio, no de la skill.
        if p.name in ('.gitignore', '.gitattributes'):
            continue
        if p.name.startswith('~$') or p.suffix == '.pyc':
            continue
        yield p


def revisar_enlaces():
    """Un ZIP con una ruta rota es peor que no tener ZIP: la pieza sale igual,
    con un hueco donde iba el logo, y nadie se entera hasta publicarla."""
    r = subprocess.run([sys.executable, str(RAIZ / 'scripts' / 'enlaces.py')],
                       capture_output=True, text=True)
    print(r.stdout.strip())
    return r.returncode == 0


def main():
    args = sys.argv[1:]
    if any(a in ('-h', '--help') for a in args):
        print(__doc__)
        return 0

    con_piezas = '--con-piezas' in args
    archivos = list(entran(con_piezas))
    peso = sum(p.stat().st_size for p in archivos) / 1e6

    print(f'\n{len(archivos)} archivos · {peso:.2f} MB sin comprimir')
    porcarpeta = {}
    for p in archivos:
        k = p.relative_to(RAIZ).parts[0] if len(p.relative_to(RAIZ).parts) > 1 else '(raiz)'
        n, m = porcarpeta.get(k, (0, 0))
        porcarpeta[k] = (n + 1, m + p.stat().st_size)
    for k, (n, m) in sorted(porcarpeta.items(), key=lambda x: -x[1][1]):
        print(f'  {k:<22}{n:>5} archivos {m / 1e6:>8.2f} MB')

    if len(archivos) > TOPE:
        print(f'\nNO CABE: {len(archivos)} archivos y el tope son {TOPE}.')
        print('Mira que carpeta de arriba pesa mas y saca lo que no se lea al componer.')
        return 1
    print(f'\nCaben: {TOPE - len(archivos)} archivos de margen.')

    if '--listar' in args:
        return 0

    if not revisar_enlaces():
        print('\nHay rutas rotas. No se empaqueta: la pieza saldria con un hueco.')
        return 1

    hoy = datetime.date.today().isoformat()
    destino = pathlib.Path.home() / 'OneDrive' / 'Desktop' / f'anthro-pic-brand-{hoy}.zip'
    if not destino.parent.is_dir():
        destino = RAIZ.parent / destino.name
    with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in archivos:
            z.write(p, pathlib.Path('anthro-pic-brand') / p.relative_to(RAIZ))
    print(f'\n{destino}\n{destino.stat().st_size / 1e6:.2f} MB comprimido')
    return 0


if __name__ == '__main__':
    sys.exit(main())
