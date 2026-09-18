#!/usr/bin/env python3
"""Genera variantes de color de un SVG a dos tintas intercambiando los fill.

Existe porque una ilustracion sirve en cuatro contextos distintos —fondo claro,
fondo oscuro, fondo naranja, serie con acento rotado— y redibujarla cuatro veces
es absurdo cuando el vector solo necesita otro par de colores.

Variantes:
    claro     linea en #faf9f5, acento naranja   -> fondo oscuro
    azul      acento #6a9bcc                     -> rotacion de serie
    verde     acento #788c5d                     -> rotacion de serie

Las variantes de una sola tinta (mono, mono-claro, sobre-naranja) solo se emiten
si el relleno de acento es menos del 45% de la tinta. Por encima de eso las lineas
se pierden dentro del relleno y el dibujo queda como una mancha solida.

Para poner una ilustracion sobre fondo naranja **no uses una variante**: usa el
SVG base. Su relleno ya es #d97757, asi que se funde con el fondo y quedan solo
las lineas negras — que es justo el efecto que se busca.

Uso:
    python3 variantes.py entrada.svg --destino assets/ilustraciones/
    python3 variantes.py --lote "assets/ilustraciones/*.svg" --solo claro,azul
"""
import argparse, glob, pathlib, re

LINEA, ACENTO = "#141413", "#d97757"
CLARO = "#faf9f5"

VARIANTES = {
    "claro":         {LINEA: CLARO,  ACENTO: ACENTO},
    "sobre-naranja": {LINEA: CLARO,  ACENTO: CLARO},
    "mono":          {LINEA: LINEA,  ACENTO: LINEA},
    "mono-claro":    {LINEA: CLARO,  ACENTO: CLARO},
    "azul":          {LINEA: LINEA,  ACENTO: "#6a9bcc"},
    "verde":         {LINEA: LINEA,  ACENTO: "#788c5d"},
}

# Variantes que funden las dos tintas en una sola. Solo sirven si el relleno es
# una parte menor del dibujo; si domina, las lineas desaparecen dentro de el y
# queda una mancha.
UNA_TINTA = {"sobre-naranja", "mono", "mono-claro"}
LIMITE_RELLENO = 0.45


def proporcion_relleno(svg_path):
    """Fraccion de la tinta total que es relleno de acento."""
    import io
    import numpy as np
    import cairosvg
    from PIL import Image
    a = np.array(Image.open(io.BytesIO(
        cairosvg.svg2png(url=str(svg_path), output_width=400))).convert("RGBA")).astype(int)
    m = a[:, :, 3] > 128
    rgb = a[:, :, :3]
    linea = m & (np.linalg.norm(rgb - np.array([20, 20, 19]), axis=2) < 60)
    rell = m & (np.linalg.norm(rgb - np.array([217, 119, 87]), axis=2) < 60)
    total = linea.sum() + rell.sum()
    return rell.sum() / total if total else 0.0


def aplicar(svg, mapa):
    def sub(m):
        v = m.group(1).lower()
        return f'fill="{mapa.get(v, m.group(1))}"'
    return re.sub(r'fill="([^"]+)"', sub, svg)


def generar(entrada, destino, cuales):
    src = pathlib.Path(entrada)
    svg = src.read_text()
    tintas = set(c.lower() for c in re.findall(r'fill="(#[0-9a-fA-F]{6})"', svg))
    if not tintas <= {LINEA, ACENTO}:
        print(f"   aviso: {src.name} usa {sorted(tintas)}; solo se remapean "
              f"{LINEA} y {ACENTO}")
    una_tinta = [n for n in cuales if n in UNA_TINTA]
    if una_tinta:
        share = proporcion_relleno(src)
        if share > LIMITE_RELLENO:
            print(f"   {src.name}: el relleno es el {share:.0%} de la tinta; "
                  f"fundir las dos en una lo convierte en mancha. "
                  f"Omitidas: {', '.join(una_tinta)}")
            cuales = [n for n in cuales if n not in UNA_TINTA]
            if not cuales:
                return []

    hechos = []
    for nombre in cuales:
        salida = pathlib.Path(destino) / f"{src.stem}--{nombre}.svg"
        salida.write_text(aplicar(svg, VARIANTES[nombre]))
        hechos.append(salida.name)
    return hechos


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("entrada", nargs="?")
    p.add_argument("--lote")
    p.add_argument("--destino", default=".")
    p.add_argument("--solo", help="lista separada por comas; por defecto todas")
    a = p.parse_args()

    cuales = ([s.strip() for s in a.solo.split(",")] if a.solo
              else list(VARIANTES))
    desconocidas = [c for c in cuales if c not in VARIANTES]
    if desconocidas:
        raise SystemExit(f"variante desconocida: {desconocidas}. "
                         f"Disponibles: {list(VARIANTES)}")

    pathlib.Path(a.destino).mkdir(parents=True, exist_ok=True)
    fuentes = sorted(glob.glob(a.lote)) if a.lote else [a.entrada]
    fuentes = [f for f in fuentes if "--" not in pathlib.Path(f).stem]
    for f in fuentes:
        hechos = generar(f, a.destino, cuales)
        print(f"-> {pathlib.Path(f).stem}: {len(hechos)} variantes")
