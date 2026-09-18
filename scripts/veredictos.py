#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anota el veredicto de una pieza con sus medidas, en texto.

    python3 scripts/veredictos.py salida/post-06-terminal-negra.png \\
            --veredicto aprobada --porque "terminal desplazada, Clawd encima"

    python3 scripts/veredictos.py --tabla        solo imprime lo anotado

Escribe en `references/veredictos.md`, que es lo que se lee al trabajar.

POR QUE ESTO Y NO UN CORPUS DE IMAGENES
  Hasta la v2.11 esto era `referencias/aprobadas/` y `referencias/rechazadas/`:
  dos carpetas de WebP y un test que corria el validador contra ellas. Se retiro
  por tres motivos medidos, no por gusto:

  1. ABRIR UNA IMAGEN CUESTA. Una pieza de 1080x1350 son ~1,900 tokens solo por
     mirarla. Veinte piezas de corpus son 38,000 tokens por sesion que quiera
     saber que funciono. La tabla entera de aqui cuesta unos 700.

  2. EL VEREDICTO NO ESTA EN LOS PIXELES. Ninguna medida distingue "esta bien"
     de "esta mal" por si sola: lo que distingue es la RAZON, y la razon la dice
     una persona con palabras. Un corpus de imagenes guarda el resultado y tira
     el motivo. Aqui el motivo es la columna que importa.

  3. LA REGLA QUE FUNCIONO SALIO DE LOS NUMEROS, NO DE MIRAR. `aire_max <= 180`
     —el unico umbral que separa limpiamente lo aprobado de lo rechazado— se
     encontro comparando la tabla, no las imagenes. Nadie lo vio mirando.

  Las imagenes siguen existiendo donde sirven: `referencias/inspiracion/` para
  que las mire una persona, y `piezas-aprobadas/` como archivo entregable. Lo
  que desaparece es la carpeta que se media.

  Corolario: una pieza rechazada NO se guarda como archivo. Se guarda su fila.
"""
import argparse
import datetime
import glob
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TABLA = RAIZ / 'references' / 'veredictos.md'

COLUMNAS = ('aire_max', 'sangra', 'densidad', 'ejes', 'bloques')
CABECERA = ('| Pieza | Fecha | Veredicto | aire_max | sangra | densidad | ejes | '
            'bloques | Por qué |\n|---|---|---|---|---|---|---|---|---|\n')


def medir(ruta):
    """Usa el mismo medidor que `analizar_referencia.py`, sin duplicarlo."""
    sys.path.insert(0, str(RAIZ / 'scripts'))
    from analizar_referencia import props
    return props(ruta)


def anotar(ruta, veredicto, porque, fecha=None):
    p = pathlib.Path(ruta)
    m = medir(p)
    fecha = fecha or datetime.date.today().isoformat()
    valores = ' | '.join(str(m[c]) for c in COLUMNAS)
    fila = f'| `{p.stem}` | {fecha} | **{veredicto}** | {valores} | {porque} |'

    txt = TABLA.read_text(encoding='utf-8') if TABLA.exists() else ''
    if CABECERA not in txt:
        txt = (txt.rstrip() + '\n\n' if txt else '') + CABECERA + '\n'

    # Las filas son las lineas que empiezan por "| `" justo debajo de la
    # cabecera: se leen enteras, se quita la de esta pieza si ya estaba, se anade
    # la nueva y se reescribe el bloque ordenado. Insertar "por posicion" metia
    # las filas detras del separador de la seccion siguiente.
    i = txt.index(CABECERA) + len(CABECERA)
    resto = txt[i:].lstrip('\n')
    lineas = []
    while resto.startswith('| `'):
        corte = resto.index('\n') + 1
        lineas.append(resto[:corte].strip())
        resto = resto[corte:]
    lineas = [l for l in lineas if not l.startswith(f'| `{p.stem}` |')] + [fila]
    lineas.sort()
    TABLA.write_text(txt[:i] + '\n'.join(lineas) + '\n\n' + resto.lstrip('\n'),
                     encoding='utf-8')
    print(fila)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('piezas', nargs='*', help='PNG a medir (admite comodines)')
    ap.add_argument('--veredicto', choices=('aprobada', 'rechazada'))
    ap.add_argument('--porque', default='—', help='la razon, en una frase')
    ap.add_argument('--fecha', help='AAAA-MM-DD; por defecto hoy')
    ap.add_argument('--tabla', action='store_true', help='solo imprimir lo anotado')
    a = ap.parse_args()

    if a.tabla or not a.piezas:
        print(TABLA.read_text(encoding='utf-8') if TABLA.exists() else 'sin veredictos')
        return
    if not a.veredicto:
        ap.error('hace falta --veredicto')
    for patron in a.piezas:
        for f in sorted(glob.glob(patron)) or [patron]:
            anotar(f, a.veredicto, a.porque, a.fecha)


if __name__ == '__main__':
    main()
