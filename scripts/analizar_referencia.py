#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrae propiedades MEDIBLES de una pieza de diseño.

Para que se entienda el alcance: esto no "aprende gusto". Convierte una imagen en
un vector de numeros comparables, de modo que al ver varias piezas aprobadas y
varias rechazadas se pueda buscar que variable las separa. La conclusion la saca
una persona leyendo la tabla, o el modelo comparando; el script solo evita que
esa conclusion se base en impresiones.

Lo que mide y por que importa:
  densidad        cuanta tinta hay. Separa piezas aireadas de piezas cargadas.
  bloques         cuantas bandas horizontales de contenido. Proxy de cuantos
                  "trozos" independientes lee el ojo.
  ejes            cuantas alineaciones izquierdas distintas. Una retícula limpia
                  tiene pocos; una pieza desordenada tiene muchos.
  salto_tipo      alto de la banda mas grande dividido entre la mediana. Mide el
                  contraste de escala tipografica.
  aire_max        la franja vacia mas alta. Es el UNICO numero que separo las
                  piezas aprobadas de las rechazadas: umbral <= 180 px en
                  1080x1350. Ojo con `aire_fiable`.
  aire_fiable     False cuando la pieza lleva una trama que cubre el lienzo
                  entero: entonces no hay filas vacias y aire_max sale 0 sin
                  querer decir nada. Para medirla, renderizarla sin trama.
  grafico         que fraccion de la tinta es imagen y no texto (aproximado por
                  bloques anchos y macizos).
  colores         cuantos tonos ocupan mas del 1% del lienzo.
  acento          fraccion del lienzo con el naranja de marca.

Uso:
    python3 analizar_referencia.py pieza.png
    python3 analizar_referencia.py "carpeta/*.png" --tabla
"""
import argparse, glob, json, pathlib
import numpy as np
from PIL import Image
from scipy import ndimage


def props(ruta):
    im = Image.open(ruta).convert("RGB")
    a = np.array(im).astype(int)
    h, w, _ = a.shape
    # El fondo es el color MAS FRECUENTE, no la esquina. La esquina falla en dos
    # casos reales y los dos se colaron: una pieza de fondo oscuro (la esquina
    # cae dentro de la foto y entonces el fondo entero cuenta como tinta) y una
    # pieza con trama de grano (la esquina cae en una mota). En ambos aire_max
    # daba 0 con 300-400 px de banda muerta a la vista.
    plano = (a[..., 0].astype(np.int32) << 16 | a[..., 1].astype(np.int32) << 8
             | a[..., 2].astype(np.int32)).ravel()
    conteo = np.bincount(plano, minlength=1 << 24)
    clave = int(conteo.argmax())
    bg = np.array([clave >> 16 & 255, clave >> 8 & 255, clave & 255])
    tinta = np.linalg.norm(a - bg, axis=2) > 24

    # bandas horizontales de contenido. Una fila cuenta como contenido si tiene
    # tinta de verdad, no un pixel suelto: con `any` una trama de fondo o el
    # ruido del JPEG llenan las 1350 filas y no queda ningun hueco que medir.
    frac = tinta.mean(1)
    filas = frac > 0.004

    # aire_max no siempre SIGNIFICA algo. Sobre una trama que cubre el lienzo
    # entero (grano, semitono, retícula densa) no queda ninguna fila vacia, asi
    # que sale 0 y 0 se lee como "sin hueco" cuando en realidad es "no medible".
    # Paso: si hasta la fila mas limpia esta medio cubierta, se avisa. Para medir
    # el aire de una pieza asi hay que renderizarla sin la trama.
    fiable = bool(np.percentile(frac, 5) < 0.5)
    bandas, dentro = [], False
    for y in range(h):
        if filas[y] and not dentro:
            ini, dentro = y, True
        elif not filas[y] and dentro:
            bandas.append((ini, y)); dentro = False
    if dentro:
        bandas.append((ini, h))
    altos = [b - a_ for a_, b in bandas] or [0]

    # huecos verticales
    huecos = [bandas[i + 1][0] - bandas[i][1] for i in range(len(bandas) - 1)] or [0]

    # ejes de alineacion izquierda (redondeados a 8px)
    ejes = set()
    for a_, b in bandas:
        xs = np.where(tinta[a_:b].any(0))[0]
        if len(xs):
            ejes.add(int(xs.min()) // 8)

    dominantes = int((conteo / (h * w) > 0.01).sum())
    acento = float((np.linalg.norm(a - np.array([217, 119, 87]), axis=2) < 45).mean())

    # bloques macizos = probable imagen o forma de color
    macizo = 0
    for a_, b in bandas:
        franja = tinta[a_:b]
        if franja.mean() > 0.55 and (b - a_) > h * 0.08:
            macizo += franja.sum()

    # --- capas y solape ---
    # Lo que separa una pieza "plana" de una con personalidad no es cuanta tinta
    # hay, sino cuantos objetos independientes flotan y si se encabalgan. Se
    # etiquetan componentes conexos y se mide: cuantas islas pequenas hay (chips,
    # etiquetas, marcas sueltas), y cuantos pares de objetos tienen bounding boxes
    # que se solapan (elementos montados unos sobre otros en vez de en carriles).
    lab, n = ndimage.label(ndimage.binary_closing(tinta, np.ones((5, 5))))
    cajas = ndimage.find_objects(lab)
    area = h * w
    islas, grandes = 0, []
    for i, sl in enumerate(cajas, 1):
        tam = (lab[sl] == i).sum()
        if 0.0006 * area < tam < 0.03 * area:
            islas += 1
        if tam > 0.02 * area:
            grandes.append(sl)
    solapes = 0
    for i in range(len(grandes)):
        for j in range(i + 1, len(grandes)):
            a1, b1 = grandes[i]; a2, b2 = grandes[j]
            if a1.start < a2.stop and a2.start < a1.stop and \
               b1.start < b2.stop and b2.start < b1.stop:
                solapes += 1

    # --- sangrado: fraccion del borde del lienzo tocada por contenido ---
    borde = np.concatenate([tinta[0], tinta[-1], tinta[:, 0], tinta[:, -1]])
    sangra = float(borde.mean())

    return dict(
        densidad=round(float(tinta.mean()), 3),
        islas=islas,
        solapes=solapes,
        sangra=round(sangra, 2),
        bloques=len(bandas),
        ejes=len(ejes),
        salto_tipo=round(max(altos) / max(1, float(np.median(altos))), 2),
        aire_max=int(max(huecos)),
        aire_fiable=fiable,
        grafico=round(macizo / max(1, tinta.sum()), 2),
        colores=dominantes,
        acento=round(acento, 3),
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("rutas", nargs="+")
    p.add_argument("--tabla", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    archivos = [f for r in a.rutas for f in sorted(glob.glob(r))] or a.rutas

    datos = {pathlib.Path(f).stem: props(f) for f in archivos}
    if a.json:
        print(json.dumps(datos, indent=1, ensure_ascii=False)); return

    claves = list(next(iter(datos.values())))
    print(f"{'pieza':30} " + " ".join(f"{k:>11}" for k in claves))
    for n, d in datos.items():
        print(f"{n:30} " + " ".join(f"{d[k]:>11}" for k in claves))


if __name__ == "__main__":
    main()
