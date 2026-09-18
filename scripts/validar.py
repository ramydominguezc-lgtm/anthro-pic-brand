#!/usr/bin/env python3
"""Revisa una pieza terminada contra el sistema de marca y reporta que se salio.

Pensado para revisar lo que mandan otros antes de que llegue a publicarse. No
sustituye mirar la pieza: detecta lo medible —color, contraste, margenes,
legibilidad en miniatura— y no ve si el mensaje esta bien escrito o si la
composicion tiene gracia.

Uso:
    python3 validar.py pieza.png
    python3 validar.py "carpeta/*.png" --estricto
"""
import argparse, glob, sys
import numpy as np
from PIL import Image

PALETA = {
    "#141413": (20, 20, 19),   "#faf9f5": (250, 249, 245),
    "#b0aea5": (176, 174, 165), "#e8e6dc": (232, 230, 220),
    "#d97757": (217, 119, 87), "#6a9bcc": (106, 155, 204),
    "#788c5d": (120, 140, 93), "#cc785c": (204, 120, 92),
    "#f0eee6": (240, 238, 230), "#7d7b74": (125, 123, 116),
}


def lum(c):
    c = [v / 255 for v in c]
    c = [(v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4) for v in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def contraste(a, b):
    l1, l2 = sorted([lum(a), lum(b)], reverse=True)
    return (l1 + .05) / (l2 + .05)


def revisar(ruta, estricto=False):
    im = Image.open(ruta).convert('RGB')
    a = np.array(im).astype(int)
    h, w, _ = a.shape
    hallazgos = []

    def falla(sev, msg, arreglo):
        hallazgos.append((sev, msg, arreglo))

    # --- 1. colores fuera de paleta -------------------------------------
    cols, cuenta = np.unique(a.reshape(-1, 3), axis=0, return_counts=True)
    dominantes = cols[cuenta.argsort()[::-1][:12]]
    peso = cuenta[cuenta.argsort()[::-1][:12]] / (h * w)
    ref = np.array(list(PALETA.values()))
    for c, p in zip(dominantes, peso):
        if p < 0.015:
            continue
        d = np.linalg.norm(ref - c, axis=1).min()
        # Un tono NEUTRO que cae entre el oscuro y el crema es un valor
        # intermedio de la propia rampa de marca: lo produce cualquier foto en
        # escala de grises, un duotono o un semitono, y no es un color ajeno.
        # Sin esta excepcion, toda pieza con fotografia sale con diez fallos
        # graves y el equipo deja de correr el validador. La chroma se mide como
        # el recorrido entre el canal mas alto y el mas bajo: por debajo de 18 el
        # color no tiene tinte propio.
        chroma = int(c.max()) - int(c.min())
        neutro_de_marca = chroma < 18 and 20 <= c.mean() <= 250
        if neutro_de_marca and p < 0.55:
            continue
        if d > 26:
            falla("alta", f"color #{c[0]:02x}{c[1]:02x}{c[2]:02x} ocupa "
                          f"{p*100:.0f}% y no esta en la paleta",
                  "sustituyelo por el token de marca mas cercano")

    # --- 2. numero de acentos -------------------------------------------
    acentos = {"#d97757": 0, "#6a9bcc": 0, "#788c5d": 0}
    for k in acentos:
        v = np.array(PALETA[k])
        acentos[k] = (np.linalg.norm(a - v, axis=2) < 30).mean()
    usados = [k for k, v in acentos.items() if v > 0.01]
    if len(usados) > 1:
        falla("alta", f"hay {len(usados)} acentos en la misma pieza ({', '.join(usados)})",
              "deja uno dominante; los otros se rotan entre piezas, no dentro de una")

    # --- 3. contraste fondo/texto ---------------------------------------
    # La "tinta principal" no es simplemente el segundo color mas dominante: en una
    # pieza con ilustracion o acentos, ese segundo lugar suele ser el naranja del
    # grafico, y medirle el contraste dispara una alerta que no corresponde — el
    # naranja ahi es forma, no texto. Se busca el color dominante que mas se parece
    # a una tinta de texto de la marca (#141413 o #faf9f5).
    fondo = tuple(cols[cuenta.argmax()])
    tintas_texto = [np.array(PALETA["#141413"]), np.array(PALETA["#faf9f5"]),
                    np.array(PALETA["#7d7b74"])]
    tinta, mejor = None, 1e9
    for c, p in zip(dominantes, peso):
        if np.linalg.norm(np.array(c) - fondo) < 60 or p < 0.002:
            continue
        d = min(np.linalg.norm(np.array(c) - t) for t in tintas_texto)
        if d < mejor:
            tinta, mejor = tuple(c), d
    if tinta:
        cr = contraste(fondo, tinta)
        if cr < 4.5:
            falla("alta" if cr < 3 else "media",
                  f"contraste fondo/tinta principal = {cr:.1f}:1",
                  "por debajo de 4.5 solo aguanta texto de 24pt o mas; "
                  "oscurece la tinta o aclara el fondo")

    # --- 4. margenes -----------------------------------------------------
    d = np.linalg.norm(a - np.array(fondo), axis=2) > 24
    if d.any():
        ys, xs = np.where(d)
        m = [xs.min(), w - 1 - xs.max(), ys.min(), h - 1 - ys.max()]
        lado = min(h, w)
        borde = np.concatenate([d[0], d[-1], d[:, 0], d[:, -1]])
        sangra_a_proposito = borde.mean() > 0.12
        if min(m) < lado * 0.04 and not sangra_a_proposito:
            falla("media", f"margen minimo de {min(m)}px ({100*min(m)/lado:.1f}% del lado corto)",
                  "el sistema pide 6-8%; si no cabe, sobra texto")
        if max(m) - min(m) > lado * 0.06:
            falla("baja", f"margenes desiguales: izq {m[0]} der {m[1]} arr {m[2]} abj {m[3]}",
                  "iguala los cuatro lados salvo que sea una decision deliberada")
    else:
        falla("alta", "la pieza parece estar vacia o ser de un solo color", "revisa el archivo")

    # --- 5. legibilidad en miniatura -------------------------------------
    mini = np.array(im.resize((200, int(200 * h / w)), Image.LANCZOS)).astype(int)
    dm = np.linalg.norm(mini - np.array(fondo), axis=2) > 24
    if dm.mean() < 0.02:
        falla("media", "a 200px de ancho casi no queda nada visible",
              "el titular necesita mas peso o mas tamano")

    # --- 6. planitud ------------------------------------------------------
    # Solo se mide el sangrado, y a proposito. Se intento tambien detectar
    # "elementos sueltos" y "jerarquia por bandas", y ambos salieron invertidos:
    # en una pieza rica el contenido se fusiona en un solo componente, asi que
    # esas submedidas unicamente saben ver composiciones planas — justo lo que se
    # queria detectar. El sangrado si discrimina: 0.00 en las piezas planas, 0.37
    # en una con capas, 0.79 en las referencias.
    #
    # El resto de recursos de references/recursos-compositivos.md NO se puede
    # verificar automaticamente todavia. Se revisan a ojo con inspeccionar.py.
    tinta_b = np.linalg.norm(a - np.array(fondo), axis=2) > 24
    marco = np.concatenate([tinta_b[0], tinta_b[-1], tinta_b[:, 0], tinta_b[:, -1]])
    if marco.mean() < 0.10:
        falla("baja",
              f"ningun elemento cruza el borde (sangrado {marco.mean():.2f})",
              "las referencias van de 0.64 a 0.79; saca al menos un elemento del "
              "lienzo — ver recurso 1 en references/recursos-compositivos.md")

    # --- 7. formato -------------------------------------------------------
    r = w / h
    conocidos = {1.0: "post 1:1", 0.5625: "story 9:16", 0.8: "carrusel 4:5",
                 1.7778: "slide 16:9"}
    if not any(abs(r - k) < 0.02 for k in conocidos):
        falla("baja", f"proporcion {w}x{h} ({r:.2f}) no es un formato del sistema",
              "los formatos previstos estan en references/layout.md")

    return hallazgos


def main():
    p = argparse.ArgumentParser()
    p.add_argument("rutas", nargs="+")
    p.add_argument("--estricto", action="store_true",
                   help="devuelve codigo 1 si hay algun hallazgo de severidad alta")
    a = p.parse_args()

    archivos = [f for r in a.rutas for f in sorted(glob.glob(r))] or a.rutas
    graves = 0
    for f in archivos:
        hs = revisar(f, a.estricto)
        print(f"\n{f}")
        if not hs:
            print("   sin hallazgos")
            continue
        for sev, msg, arreglo in sorted(hs, key=lambda x: "abm".index(x[0][0])):
            marca = {"alta": "!!", "media": " !", "baja": "  "}[sev]
            print(f"  {marca} {msg}\n       -> {arreglo}")
            graves += sev == "alta"
    print()
    if a.estricto and graves:
        sys.exit(1)


if __name__ == "__main__":
    main()
