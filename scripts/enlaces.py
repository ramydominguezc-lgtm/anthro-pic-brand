#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprueba que todo lo que la skill menciona existe de verdad.

    python3 scripts/enlaces.py

Recorre los .md, .py, .css y .html de la skill, saca cada ruta que citan y dice
cuales no existen. Sale con codigo 1 si encuentra alguna, para poder encadenarlo
antes de empaquetar.

POR QUE EXISTE
  El 17/09/2026 la carpeta `assets/logos-claudetec/` se renombro a mano a
  "Logos ClaudeTec". Diez archivos la seguian citando —cuatro .md, tres scripts,
  dos visores y una hoja— y **ninguno dio error**: los scripts escribian su HTML
  igual, Chromium no encontraba el SVG, no avisaba, y las piezas salian con un
  hueco donde va el logo. Es el mismo modo de fallo que la trampa 12 de
  reglas-derivadas.md (rutas relativas en `url()`): plausible y silencioso.

  Lo que se rompe renombrando una carpeta no lo detecta ningun test de imagen,
  porque la imagen sale. Se detecta leyendo el texto, que es lo que hace esto.

DOS CLASES DE CITA
  1. Rutas escritas enteras: `assets/logos-claudetec/claudetec.svg`.
  2. NOMBRES SUELTOS de carpeta dentro de una lista de scripts:
         CARPETAS = ["logos", "logos-claudetec", "iconos", ...]
     Estos no parecen rutas y la primera version de este script no los miraba.
     Al renombrar la carpeta, cinco scripts se quedaron apuntando al nombre
     viejo: `biblioteca.py` empezo a inventariar 65 assets en vez de 75 —sin
     fallar— y `visor.py` reventaba. Un catalogo con diez piezas menos es
     exactamente el fallo plausible y silencioso de siempre.

QUE MIRA Y QUE NO
  Mira rutas relativas a la raiz de la skill y rutas relativas al archivo que las
  cita, que son las dos formas que se usan aqui. Ignora a proposito:

    - `salida/` y `piezas-aprobadas/`  no son la skill, son trabajo producido
    - URLs http(s) y data:                  no son archivos
    - rutas dentro de bloques de ejemplo con `…`, `<`, `{` o `$`
    - lo que cita un script de mantenimiento como ruta de ENTRADA del usuario
      (`foto.jpg`, `pieza.png`): son argumentos, no archivos de la skill
"""
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent

MIRA = ('.md', '.py', '.css', '.html')
FUERA_DE_LA_SKILL = {'salida', 'piezas-aprobadas', 'v1', 'node_modules', '.git'}

# Rutas que aparecen como ejemplo o como argumento del usuario, no como archivo.
EJEMPLOS = {
    'foto.jpg', 'pieza.png', 'mi.json', 'contexto.png', 'momento.png',
    'equipo.png', 'claude-glyph.svg', 'imagen.png', 'archivo.svg',
    'referencias/*.webp', 'carpeta/*.png', 'assets-canva/',
}

PATRON = re.compile(r"""['"(\s]((?:\.\./|\./)?(?:assets|references|referencias|scripts)/[^'"()\s,;:*?<>|]+)""")


def candidatas(f):
    """Rutas citadas por un archivo, ya resueltas contra la raiz."""
    try:
        txt = f.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return
    # En un .md, lo que va dentro de un bloque ``` es un EJEMPLO de codigo: sus
    # rutas son relativas al script que se muestra, no a este archivo. Dejarlas
    # dentro daba tres falsos positivos por cada fragmento pegado.
    if f.suffix == '.md':
        trozos, dentro = [], False
        for linea in txt.split('\n'):
            if linea.lstrip().startswith('```'):
                dentro = not dentro
            elif not dentro:
                trozos.append(linea)
        txt = '\n'.join(trozos)

    for m in PATRON.finditer(txt):
        cruda = m.group(1)
        if any(c in cruda for c in '…{}$<>') or cruda in EJEMPLOS:
            continue
        cruda = cruda.rstrip('.,;:)`')
        # Relativa al archivo si empieza por ../ o ./; si no, relativa a la raiz.
        destino = (f.parent / cruda).resolve() if cruda.startswith(('../', './')) \
            else (RAIZ / cruda).resolve()
        yield cruda, destino


def carpetas_sueltas(f):
    """Nombres de carpeta citados como texto suelto en una lista de scripts."""
    txt = f.read_text(encoding='utf-8', errors='ignore')
    for m in re.finditer(r'CARPETAS\s*=\s*[\[(](.*?)[\])]', txt, re.S):
        for nombre in re.findall(r'["\']([a-z][a-z0-9-]+)["\']', m.group(1)):
            yield nombre, (RAIZ / 'assets' / nombre)


def main():
    rotas, vistas = [], 0
    for f in sorted(RAIZ.rglob('*')):
        if f.suffix not in MIRA or not f.is_file():
            continue
        if set(f.relative_to(RAIZ).parts) & FUERA_DE_LA_SKILL:
            continue
        for cruda, destino in candidatas(f):
            vistas += 1
            if not destino.exists():
                rotas.append((f.relative_to(RAIZ).as_posix(), cruda))
        if f.suffix == '.py':
            for nombre, destino in carpetas_sueltas(f):
                vistas += 1
                if not destino.is_dir():
                    rotas.append((f.relative_to(RAIZ).as_posix(),
                                  f'assets/{nombre}  (nombre suelto en CARPETAS)'))

    print(f'{vistas} rutas citadas en la skill')
    if not rotas:
        print('todas existen')
        return 0
    print(f'\n{len(rotas)} ROTAS:\n')
    ancho = max(len(a) for a, _ in rotas)
    for archivo, ruta in rotas:
        print(f'  {archivo:<{ancho}}  ->  {ruta}')
    return 1


if __name__ == '__main__':
    sys.exit(main())
