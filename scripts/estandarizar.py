#!/usr/bin/env python3
"""Estandariza ilustraciones de line art capturadas de pantalla.

Que hace, en orden:

1. Detecta el color de fondo por las esquinas (son fondos planos).
2. Calcula alfa por distancia al fondo y **desmultiplica** el color: para un pixel
   antialiaseado P = a*F + (1-a)*B, recupera F = (P-(1-a)*B)/a. Sin esto los
   bordes conservan el tinte del fondo viejo y se ve una aureola clara al montar
   la pieza sobre naranja u oscuro.
3. Normaliza la paleta a los valores de marca: los negros a #141413 y los naranjas
   a #d97757, preservando el alfa. Las capturas venian con hasta tres naranjas
   distintos (#d97959, #c15f3c) porque son de fuentes diferentes.
4. Recorta al contenido y lo centra en un lienzo cuadrado con margen constante.

Uso:
    python3 estandarizar.py entrada.png salida.png [--lienzo 1080] [--margen 0.08]
    python3 estandarizar.py --lote "carpeta/*.png" --destino out/
"""
import argparse, glob, pathlib
import numpy as np
from PIL import Image

NEGRO = np.array([20, 20, 19])       # #141413
NARANJA = np.array([217, 119, 87])   # #d97757


def umbrales_auto(a):
    """Deriva los umbrales del ruido real del fondo de la pieza.

    Un umbral fijo sirve para capturas de pantalla con fondo perfectamente plano,
    pero no para arte con textura de papel: ahi el ruido del propio fondo supera
    el umbral y aparecen motas por todas partes. Se mide el percentil 99 del ruido
    en el marco exterior y se ancla el piso por encima.
    """
    h, w, _ = a.shape
    bordes = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3),
                             a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    bg = np.median(bordes, axis=0)
    ruido = np.percentile(np.linalg.norm(bordes - bg, axis=1), 99)
    t0 = max(6.0, ruido * 2.5)
    return t0, t0 + 39.0, ruido


def quitar_fondo(a, t0=6.0, t1=45.0):
    """a: HxWx3 float. Devuelve (rgb, alfa) con el color desmultiplicado.

    El umbral es fijo y estrecho a proposito. Escalarlo al contraste de la pieza
    parece mas listo pero rompe el arte a dos tintas: el naranja plano queda mucho
    mas cerca del fondo que el negro (d~155 contra d~330), asi que un umbral
    proporcional lo convierte en semitransparente. Solo la banda de antialiasing
    —los primeros ~45 de distancia— debe llevar alfa parcial; cualquier tinta
    plena queda opaca.
    """
    h, w, _ = a.shape
    bordes = np.concatenate([a[:3].reshape(-1, 3), a[-3:].reshape(-1, 3),
                             a[:, :3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
    bg = np.median(bordes, axis=0)

    dist = np.linalg.norm(a - bg, axis=2)
    alfa = np.clip((dist - t0) / (t1 - t0), 0, 1)

    seguro = np.maximum(alfa, 1e-3)[..., None]
    rgb = np.clip((a - (1 - seguro) * bg) / seguro, 0, 255)
    return rgb, alfa


def normalizar_paleta(rgb, alfa):
    """Lleva cada pixel opaco al negro o al naranja de marca, segun a cual se parece."""
    lum = rgb.mean(2)
    sat = rgb.max(2) - rgb.min(2)
    es_naranja = (sat > 40) & (rgb[:, :, 0] > rgb[:, :, 2])
    es_negro = (lum < 120) & ~es_naranja

    salida = rgb.copy()
    salida[es_naranja] = NARANJA
    salida[es_negro] = NEGRO
    # el resto (bordes intermedios) se acerca al destino mas cercano sin saltar
    resto = ~(es_naranja | es_negro) & (alfa > 0.02)
    if resto.any():
        d_n = np.linalg.norm(rgb[resto] - NEGRO, axis=1)
        d_o = np.linalg.norm(rgb[resto] - NARANJA, axis=1)
        destino = np.where((d_n < d_o)[:, None], NEGRO, NARANJA)
        salida[resto] = rgb[resto] * 0.35 + destino * 0.65
    return salida


def centrar(rgb, alfa, lienzo, margen):
    """Recorta al contenido y centra en lienzo cuadrado.

    El reescalado se hace con alfa PREMULTIPLICADO. PIL interpola los canales de
    color ignorando el alfa, asi que el color que quedo guardado en los pixeles
    transparentes —basura, despues de desmultiplicar— se sangra hacia el borde y
    aparece un anillo claro que solo se ve al montar la pieza sobre fondo oscuro.
    Premultiplicar, escalar y volver a dividir elimina el efecto por completo.
    """
    ys, xs = np.where(alfa > 0.06)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    c_rgb = rgb[y0:y1, x0:x1]
    c_al = alfa[y0:y1, x0:x1]

    util = int(lienzo * (1 - 2 * margen))
    h, w = c_al.shape
    k = util / max(h, w)
    nw, nh = max(1, round(w * k)), max(1, round(h * k))

    pre = np.dstack([c_rgb * c_al[..., None], c_al * 255]).astype('uint8')
    pre = np.array(Image.fromarray(pre, 'RGBA').resize((nw, nh), Image.LANCZOS)).astype(float)

    a2 = pre[:, :, 3:4] / 255
    seguro = np.maximum(a2, 1e-3)
    out = np.dstack([np.clip(pre[:, :, :3] / seguro, 0, 255), pre[:, :, 3]])
    im = Image.fromarray(out.astype('uint8'), 'RGBA')

    fondo = Image.new('RGBA', (lienzo, lienzo), (0, 0, 0, 0))
    fondo.paste(im, ((lienzo - im.width) // 2, (lienzo - im.height) // 2))
    return fondo


def procesar(entrada, salida, lienzo, margen, normalizar, auto=False):
    a = np.array(Image.open(entrada).convert('RGB')).astype(float)
    if auto:
        t0, t1, ruido = umbrales_auto(a)
        if ruido > 40:
            raise ValueError(
                f"{pathlib.Path(entrada).name}: el fondo tiene ruido {ruido:.0f} "
                f"(textura fuerte). No se puede separar por color sin comerse el "
                f"arte; deja esta pieza como fondo completo.")
        rgb, alfa = quitar_fondo(a, t0, t1)
    else:
        rgb, alfa = quitar_fondo(a)
    if normalizar:
        rgb = normalizar_paleta(rgb, alfa)
    centrar(rgb, alfa, lienzo, margen).save(salida)
    return salida


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("entrada", nargs="?")
    p.add_argument("salida", nargs="?")
    p.add_argument("--lote")
    p.add_argument("--destino", default=".")
    p.add_argument("--lienzo", type=int, default=1080)
    p.add_argument("--margen", type=float, default=0.08)
    p.add_argument("--sin-normalizar", action="store_true",
                   help="conserva los colores originales de la captura")
    p.add_argument("--auto-umbral", action="store_true",
                   help="deriva el umbral del ruido del fondo; usalo con arte "
                        "que tenga textura en vez de fondo plano perfecto")
    a = p.parse_args()

    if a.lote:
        d = pathlib.Path(a.destino); d.mkdir(parents=True, exist_ok=True)
        for f in sorted(glob.glob(a.lote)):
            out = d / (pathlib.Path(f).stem + ".png")
            try:
                procesar(f, out, a.lienzo, a.margen, not a.sin_normalizar,
                         a.auto_umbral)
                print("->", out)
            except ValueError as e:
                print("   OMITIDO ", e)
    else:
        procesar(a.entrada, a.salida, a.lienzo, a.margen, not a.sin_normalizar,
                 a.auto_umbral)
        print("->", a.salida)
