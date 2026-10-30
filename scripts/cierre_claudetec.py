# Cierre animado del logo ClaudeTec — réplica cuadro a cuadro del cierre del logo de Claude.
#
# La estrella nace como un punto en el centro del logo, crece girando con trazo dibujado a mano
# (43 dibujos extraídos de la referencia, cambian cada 2-3 cuadros), deja una estela al
# desplazarse a la izquierda y la palabra "ClaudeTec" se descubre con una cortinilla.
# Después la estrella sigue "respirando" (cambia de dibujo) mientras el logo queda quieto.
#
# Uso:
#   python scripts/cierre_claudetec.py salida.mp4                       # 1080x1920, fondo durazno de la referencia
#   python scripts/cierre_claudetec.py salida.mp4 --ancho 1080 --alto 1350 --logo 620
#   python scripts/cierre_claudetec.py salida.mov --transparente         # ProRes 4444 con alfa, para montar sobre video
#   python scripts/cierre_claudetec.py salida.mp4 --fondo "#faf9f5" --seg 4
#   python scripts/cierre_claudetec.py carpeta/ --png                    # secuencia PNG con alfa
#
# Datos en assets/animaciones/cierre-claudetec/: estrella-sprites.png, linea.json, palabra-*.png
import argparse, json, os, shutil, subprocess, tempfile
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "..", "assets", "animaciones", "cierre-claudetec")
NARANJA = (217, 119, 87)


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cargar():
    meta = json.load(open(os.path.join(DATOS, "linea.json"), encoding="utf-8"))
    hoja = Image.open(os.path.join(DATOS, "estrella-sprites.png")).getchannel("A")
    rj = meta["rejilla"]
    dibujos = []
    for i in range(rj["n"]):
        x, y = (i % rj["columnas"]) * rj["tam"], (i // rj["columnas"]) * rj["tam"]
        dibujos.append(hoja.crop((x, y, x + rj["tam"], y + rj["tam"])))
    return meta, dibujos


def cuadros(meta, total):
    # los 100 cuadros de la referencia; si se pide más, la estrella sigue respirando
    # repitiendo los dibujos de la parte quieta (desde el cuadro 28)
    L = meta["linea"]
    if total <= len(L):
        return L[:total]
    quietos = L[28:]
    extra = [dict(quietos[i % len(quietos)], f=len(L) + i) for i in range(total - len(L))]
    return L + extra


def componer(meta, dibujos, l, ancho, alto, logo_px, fondo, palabra, color_estrella):
    ref, lg = meta["referencia"], meta["logo"]
    s = logo_px / lg["viewbox"][0]                                  # px por unidad del SVG
    k = lg["estrella_lado"] / ref["px_estrella"]                    # unidades SVG por px de la referencia
    x_izq, x_der = lg["palabra_x"]
    centro_grupo = x_der / 2
    ox = ancho / 2 - centro_grupo * s                               # el logo completo queda centrado
    oy = alto / 2 - lg["estrella_centro"][1] * s
    lienzo = Image.new("RGBA", (ancho, alto), fondo)
    # palabra con cortinilla de izquierda a derecha
    if l["texto"] > 0:
        borde = x_izq + l["texto"] * (x_der - x_izq)
        p = palabra.crop((0, 0, int(round(borde)), palabra.height))
        p = p.resize((max(1, round(p.width * s)), round(palabra.height * s)), Image.LANCZOS)
        lienzo.alpha_composite(p, (round(ox), round(oy)))
    # estrella: posición interpolada entre su lugar final y el centro del grupo
    u = (l["x"] - ref["estrella_final"][0]) / (ref["centro_grupo_x"] - ref["estrella_final"][0])
    sx = lg["estrella_centro"][0] + u * (centro_grupo - lg["estrella_centro"][0])
    sy = lg["estrella_centro"][1] + (l["y"] - ref["estrella_final"][1]) * k
    lado = max(1, round(ref["recorte"] * k * s))
    a = dibujos[l["d"]].resize((lado, lado), Image.LANCZOS)
    est = Image.new("RGBA", (lado, lado), color_estrella + (255,))
    est.putalpha(a)
    lienzo.alpha_composite(est, (round(ox + sx * s - lado / 2), round(oy + sy * s - lado / 2)))
    return lienzo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("salida")
    ap.add_argument("--ancho", type=int, default=1080)
    ap.add_argument("--alto", type=int, default=1920)
    ap.add_argument("--logo", type=int, default=0, help="ancho del logo en px (por defecto 58%% del ancho)")
    ap.add_argument("--fondo", default="#e3c9bb", help="color de fondo; el de la referencia es #e3c9bb")
    ap.add_argument("--clara", action="store_true", help="palabra clara, para fondo oscuro")
    ap.add_argument("--seg", type=float, default=0, help="duración total; por defecto la de la referencia (3.33 s)")
    ap.add_argument("--transparente", action="store_true", help="fondo transparente (MOV ProRes 4444 o PNG)")
    ap.add_argument("--png", action="store_true", help="secuencia PNG en la carpeta de salida")
    a = ap.parse_args()

    meta, dibujos = cargar()
    palabra = Image.open(os.path.join(DATOS, "palabra-clara.png" if a.clara else "palabra-oscura.png")).convert("RGBA")
    logo_px = a.logo or round(a.ancho * 0.58)
    fondo = (0, 0, 0, 0) if (a.transparente or a.png) else hex_rgb(a.fondo) + (255,)
    total = round(a.seg * meta["fps"]) if a.seg else meta["cuadros"]

    carpeta = a.salida if a.png else tempfile.mkdtemp()
    os.makedirs(carpeta, exist_ok=True)
    for l in cuadros(meta, total):
        im = componer(meta, dibujos, l, a.ancho, a.alto, logo_px, fondo, palabra, NARANJA)
        im.save(os.path.join(carpeta, f"{l['f']:04d}.png"))
    if a.png:
        print("ok", carpeta)
        return
    entrada = ["ffmpeg", "-v", "error", "-y", "-framerate", str(meta["fps"]), "-i", os.path.join(carpeta, "%04d.png")]
    if a.transparente:
        cmd = entrada + ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", a.salida]
    else:
        cmd = entrada + ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.salida]
    subprocess.run(cmd, check=True)
    shutil.rmtree(carpeta)
    print("ok", a.salida)


if __name__ == "__main__":
    main()
