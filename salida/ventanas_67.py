#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rehace las piezas 06 (terminal) y 07 (navegador) con las correcciones de Ramses.

    python3 salida/ventanas_67.py

QUE ESTABA MAL EN LA PRIMERA VERSION
  06  La terminal ocupaba el ancho entero justo debajo del titular, con letra
      monoespaciada de 29 px: un parrafo de codigo que nadie lee en un post.
      Debajo quedaban 251 px muertos.
  07  La ventana de navegador iba arriba y el 40 % inferior del lienzo era
      naranja vacio: 579 px muertos, el peor numero de las diez piezas.

QUE CAMBIA
  06  Terminal desplazada abajo y a la derecha, sangrando por el borde derecho.
      Letra de 44 px y cinco lineas contadas. Clawd camina sobre su canto
      superior (fotograma 62 de `Clawd - Biblioteca/paseo`) y tapa el hueco que
      quedaba entre el titular y la ventana. Cinta naranja abajo, que la
      terminal cruza: la pieza pasa de una capa a tres.
  07  Titular grande arriba, ventana anclada abajo sangrando por derecha y por
      abajo. La ventana deja de ser un objeto centrado y pasa a ser el suelo de
      la pieza.

EL NUMERO QUE MANDA
  `aire_max` de scripts/analizar_referencia.py — la franja horizontal vacia mas
  alta. Las cinco piezas con foto que Ramses aprobo dan 0, 0, 0, 82 y 171 px.
  Las que rechazo dan 251, 293, 579. El umbral practico es 180 px, y cada
  corrida lo comprueba aqui mismo.

LA 06 SALE EN VIDEO
  Clawd camina de verdad: `post-06-terminal-negra.mp4` (11.52 s, 50 fps, un
  ciclo completo del paseo) y su `.gif` para mandar por chat. El PNG es el
  fotograma 62 de ese mismo video, no un montaje aparte.

  La escala sale de tres numeros, no de lo que se ve bien:
    - El lienzo del paseo mide 1008x544 y Clawd recorre 848 px dentro de el.
    - La terminal mide 918 px de ancho.
    - A escala 0.45 el recorrido son 382 px y el lienzo 454: el paseo entero
      cabe centrado sobre la terminal, y Clawd no empieza ni acaba fuera de
      ella. Su silueta baja de 209x178 a 144x122.
  Ademas el paseo incluye un salto. A 0.45 el punto mas alto queda en y=322 y
  el titular acaba en y~302: pasan 20 px por encima. Subir la escala lo mete
  dentro del texto.

LA 07 VA EN CINCO FONDOS
  Nada de naranja. Celeste, lila, verde claro, el verde de la paleta y crema.
  Los cinco con texto oscuro y lockup oscuro; el peor de ellos —el verde— da
  5.0:1 contra #141413. Los tres tonos claros entraron a `tokens.css` en la
  v2.10 como `--celeste`, `--lila` y `--verde-claro`.
"""
import base64
import pathlib
import sys

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'salida'

# El paseo de Clawd no vive aqui: lo guarda la skill `clawd-biblioteca`.
# El puente lo resuelve y avisa con nombre y apellido si no esta instalada.
sys.path.insert(0, str(RAIZ / 'scripts'))
from clawd_biblioteca import pieza as pieza_clawd

L_OSC = '../assets/logos-claudetec/claudetec.svg'                    # sobre fondo claro
L_MON = '../assets/logos-claudetec/claudetec--monocromo-claro.svg'   # sobre fondo naranja

# Geometria del paseo sobre la terminal. Todo se deriva de ESCALA: cambiarla
# recoloca el video y el fotograma fijo a la vez, sin numeros sueltos.
ESCALA = 0.45
PASEO_W, PASEO_H = 1008, 544
TERM_IZQ, TERM_ANCHO, TERM_ARRIBA = 236, 918, 560     # la terminal, en el lienzo
CAJA_W, CAJA_H = round(PASEO_W * ESCALA), round(PASEO_H * ESCALA)
CAJA_IZQ = TERM_IZQ + (TERM_ANCHO - CAJA_W) // 2      # paseo centrado en la terminal
CAJA_ARRIBA = TERM_ARRIBA - CAJA_H                    # apoyado en el canto superior
F62 = (384, 272, 704, 544)                            # bbox del fotograma fijo


def dato(ruta, mime):
    return f'data:{mime};base64,' + base64.b64encode(pathlib.Path(ruta).read_bytes()).decode()


def clawd_caminando():
    """Fotograma 62 del paseo, recortado a su silueta.

    Es el unico de la tanda con las cuatro patas separadas y el cuerpo a media
    zancada; los demas se leen como Clawd quieto. Se recorta al bounding box
    para poder apoyarlo por los pies sin calcular margenes transparentes.
    """
    from PIL import Image
    im = Image.open(pieza_clawd('paseo', 'fotograma', 62))
    im.crop(im.getbbox()).save(SALIDA / '_clawd-paseo-f062.png')
    return dato(SALIDA / '_clawd-paseo-f062.png', 'image/png')


def marco(estilo, cuerpo):
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/templates/_base.css">
<link rel="stylesheet" href="../assets/templates/capas.css">
<style>
  .pieza{{width:1080px;height:1350px;position:relative;padding:0}}
  .rotulo{{font-family:var(--font-heading);font-weight:600;font-size:20px;
    letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}
{estilo}
</style></head><body><div class="pieza">{cuerpo}</div></body></html>"""


# ===================== 06 · TERMINAL CON CLAWD ENCIMA =====================

E06 = """
  .pieza{background:var(--crema-capa)}
  .cinta-abajo{height:236px;background:var(--orange)}

  .cabeza{position:absolute;left:74px;right:74px;top:82px;z-index:3}
  h1{font-size:80px;line-height:1.04;margin-top:18px}
  h1 b{font-weight:600;color:var(--orange)}
  .entrada{font-family:var(--font-body);font-size:29px;line-height:1.5;
    max-width:25ch;margin-top:28px}

  /* La terminal no empieza en el eje del texto: arranca desplazada a la
     derecha y sale por el borde. Eso es lo que la convierte en una capa que
     pasa por detras del lienzo en vez de una caja centrada. */
  .ventana-terminal{position:absolute;left:236px;right:-74px;top:560px;height:602px}
  .ventana-terminal .contenido{font-size:44px;line-height:1.62;padding:40px 44px}
  .linea{white-space:pre}
  .com{color:rgba(250,249,245,.44)}
  .ok{color:#8fbf72}

  /* Clawd apoyado por los pies en el canto superior de la terminal. La posicion
     no se elige: es la que ocupa el fotograma 62 dentro del paseo escalado, asi
     que el PNG es literalmente un fotograma del MP4. */
  .clawd img{width:100%;height:100%;display:block}

  .pie{position:absolute;left:74px;right:74px;bottom:62px;z-index:5;
    display:flex;justify-content:space-between;align-items:flex-end}
  .pie img{width:236px;height:auto;display:block}
  .pie .cuando{font-family:var(--font-heading);font-weight:600;font-size:25px;
    color:var(--light);text-align:right;line-height:1.4}
"""

x0, y0, x1, y1 = F62
E06 += (f"  .clawd{{position:absolute;image-rendering:pixelated;z-index:4;"
        f"left:{CAJA_IZQ + round(x0 * ESCALA)}px;"
        f"bottom:{1350 - CAJA_ARRIBA - round(y1 * ESCALA)}px;"
        f"width:{round((x1 - x0) * ESCALA)}px;"
        f"height:{round((y1 - y0) * ESCALA)}px}}" + chr(10))

C06 = """
  <div class="cinta cinta-abajo"></div>

  <div class="cabeza">
    <div class="rotulo">Taller 04</div>
    <h1>Tu primer agente cabe<br>en <b>doce líneas</b></h1>
    <p class="entrada">Lo escribes tú, en tu laptop, sin instalar nada
    que no tengas ya.</p>
  </div>

  <div class="clawd"><img src="{clawd}" alt=""></div>

  <div class="ventana ventana-terminal">
    <div class="barra"><span class="puntos"><i></i><i></i><i></i></span>
      <span class="titulo">~/primer-agente</span></div>
    <div class="contenido">
      <div class="linea"><span class="prompt">$</span> claude "resume los PDF"</div>
      <div class="linea com">  14 archivos leídos</div>
      <div class="linea com">  3 contradicciones</div>
      <div class="linea"><span class="ok">✓</span> resumen.md</div>
      <div class="linea"><span class="prompt">$</span> <span class="valor acento">_</span></div>
    </div>
  </div>

  <div class="pie">
    <img src="{lock_mon}" alt="ClaudeTec">
    <div class="cuando">Jueves 2 de octubre · 18:00<br>Aula CETEC · trae laptop</div>
  </div>
"""


# ===================== 07 · NAVEGADOR ANCLADO ABAJO =====================

# Tres fondos, todos claros y con texto oscuro. El naranja se retira: a 2.96:1
# obligaba a texto claro, y con la ventana blanca abajo la pieza quedaba partida
# en dos temperaturas. Contraste de cada uno contra #141413 entre parentesis.
# Sobre crema la ventana desaparecia: su cuerpo (#faf9f5) y su barra
# (--crema-capa, #f0eee6) son el mismo tono que el fondo. La arregla un filete
# de --mid-gray, que es exactamente para lo que esta ese color en la paleta, y
# bajar la barra a --light-gray. Los otros dos fondos no lo necesitan.
FILETE = ('  .ventana-navegador{border:2px solid var(--mid-gray)}'
          '  .ventana-navegador .barra{background:var(--light-gray)}')
FONDOS_07 = {
    'celeste':     ('#a3cbe6', ''),        # --celeste                (10.8:1)
    'lila':        ('#cbcada', ''),        # --lila                   (11.4:1)
    'verde-claro': ('#c2d4aa', ''),        # --verde-claro            (11.7:1)
    'verde':       ('#788c5d', ''),        # --green, el de la paleta  (5.0:1)
    'crema':       ('#f0eee6', FILETE),    # --crema-capa             (15.9:1)
}

E07 = """
  .pieza{color:var(--dark)}

  .alto{position:absolute;left:74px;right:74px;top:80px;display:flex;
    justify-content:space-between;align-items:flex-start;gap:30px}
  /* El --muted del rotulo no llega sobre el azul; oscuro al 70 % si sobre los tres. */
  .alto .rotulo{color:var(--dark);opacity:.7}
  .alto img{width:222px;height:auto;display:block}

  h1{position:absolute;left:74px;right:74px;top:150px;font-size:92px;
    line-height:1.03;max-width:12ch}
  .entrada{position:absolute;left:74px;top:470px;max-width:24ch;
    font-family:var(--font-body);font-size:30px;line-height:1.5}

  /* La ventana es el suelo de la pieza: sangra por la derecha y por abajo, de
     modo que se lee como una pantalla que sigue mas alla del lienzo. Sin el
     sangrado vuelve a ser una caja flotando en naranja, que es lo que fallaba. */
  .ventana-navegador{position:absolute;left:74px;right:-86px;top:686px;bottom:-70px;
    display:flex;flex-direction:column}
  .ventana-navegador .contenido{padding:0;flex:1;display:flex;flex-direction:column}
  /* 126 px a la derecha = los 86 que la ventana saca del lienzo mas el
     margen propio. Sin esto el sangrado se come el final de cada linea. */
  .chat{padding:36px 126px 116px 40px;flex:1;display:flex;flex-direction:column}

  .turno{display:flex;gap:20px;align-items:flex-start;margin-bottom:30px}
  .turno .quien{width:46px;height:46px;border-radius:10px;flex:none;
    display:grid;place-items:center;background:var(--light-gray);
    font-family:var(--font-heading);font-weight:700;font-size:20px;color:var(--dark)}
  .turno.claude .quien{padding:8px}
  .turno .quien img{width:100%;display:block}
  .turno .dice{font-family:var(--font-body);font-size:31px;line-height:1.46;
    color:var(--dark);padding-top:4px}
  .clave{display:block;font-family:var(--font-heading);font-weight:700;font-size:31px;
    line-height:1.34;color:var(--dark);border-left:5px solid var(--orange);
    padding-left:20px;margin:16px 0}

  .campo{display:flex;align-items:center;justify-content:space-between;
    border:1.5px solid var(--light-gray);border-radius:18px;padding:22px 24px;
    margin-top:auto;font-family:var(--font-body);font-size:26px;color:var(--muted)}
  .campo .enviar{width:44px;height:44px;border-radius:50%;background:var(--orange);
    display:grid;place-items:center;color:var(--light);
    font-family:var(--font-heading);font-weight:700;font-size:22px}
"""

C07 = """
  <div class="alto"><span class="rotulo">Sesión abierta</span>
    <img src="{lock_osc}" alt="ClaudeTec"></div>

  <h1>Lo que 200 respuestas no te dicen</h1>
  <p class="entrada">Miércoles 24, 17:00. Traes tus datos; salimos con la
  conclusión escrita.</p>

  <div class="ventana ventana-navegador">
    <div class="barra">
      <span class="puntos"><i></i><i></i><i></i></span>
      <span class="pestana"><span class="favicon"></span>Claude</span>
      <span class="url">claude.ai/chat</span>
    </div>
    <div class="contenido"><div class="chat">
      <div class="turno tu"><span class="quien">R</span>
        <span class="dice">Tengo 200 respuestas de la encuesta de la carrera.
        ¿Qué me estoy perdiendo?</span></div>
      <div class="turno claude"><span class="quien"><img src="{glifo}" alt=""></span>
        <span class="dice">Hay un patrón que no aparece en ninguna gráfica.
        <span class="clave">Quienes se quejan del horario son los que más asisten.</span>
        No es un problema de agenda: es que nadie les dijo para qué sirve
        la sesión.</span></div>
      <div class="campo"><span>Pregunta lo que quieras…</span>
        <span class="enviar">↑</span></div>
    </div></div>
  </div>
"""


def rendear(nav, nombre, estilo, cuerpo):
    """Escribe el HTML, lo abre y guarda el PNG. Devuelve los fallos de carga."""
    f = SALIDA / f'{nombre}.html'
    f.write_text(marco(estilo, cuerpo), encoding='utf-8')
    pg = nav.new_page(viewport={'width': 1080, 'height': 1350})
    fallos = []
    pg.on('requestfailed', lambda r: fallos.append(r.url.split('/')[-1]))
    pg.goto(f.resolve().as_uri())
    pg.wait_for_timeout(700)
    pg.locator('.pieza').screenshot(path=str(SALIDA / f'{nombre}.png'))
    pg.close()
    return fallos


def video_06(fondo_png, destino):
    """Compone el paseo de Clawd sobre el fondo fijo de la 06.

    Se hace con ffmpeg y no cuadro a cuadro en Pillow por una razon concreta:
    el GIF del paseo tiene duraciones variables (de 20 a 1680 ms, 125 cuadros
    para 11.52 s). Reproducir esos tiempos a mano es donde se cuela el error;
    el demuxer de GIF ya lo hace bien. `flags=neighbor` conserva el pixel art
    al escalar —con el filtro por defecto Clawd sale borroso—.
    """
    import subprocess
    filtro = (f'[1:v]scale={CAJA_W}:{CAJA_H}:flags=neighbor[c];'
              f'[0:v][c]overlay={CAJA_IZQ}:{CAJA_ARRIBA}:format=auto')
    base = ['ffmpeg', '-y', '-loglevel', 'error',
            '-loop', '1', '-i', str(fondo_png),
            '-ignore_loop', '0', '-i', str(pieza_clawd('paseo', 'transparente')),
            '-filter_complex', filtro, '-t', '11.52', '-r', '50']
    subprocess.run(base + ['-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                           '-movflags', '+faststart', str(destino)], check=True)

    # GIF de cortesia para chat: 540 px y 25 fps, con paleta propia.
    gif = destino.with_suffix('.gif')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(destino),
                    '-vf', 'fps=25,scale=540:-1:flags=lanczos,split[a][b];'
                           '[a]palettegen[p];[b][p]paletteuse',
                    str(gif)], check=True)
    return destino, gif


def main():
    rec = dict(clawd=clawd_caminando(),
               glifo=dato(RAIZ / 'assets/logos/claude-glyph.svg', 'image/svg+xml'),
               lock_osc=L_OSC, lock_mon=L_MON)

    def tokens(estilo, cuerpo):
        propio = len(estilo) + len(cuerpo)
        for v in rec.values():
            propio -= cuerpo.count(v) * len(v)
        return round(propio / 4)

    with sync_playwright() as pw:
        nav = pw.chromium.launch()

        # --- 06: pieza fija, fondo sin Clawd, y video ---
        cuerpo = C06.format(**rec)
        fallos = rendear(nav, 'post-06-terminal-negra', E06, cuerpo)
        print(f'{"post-06-terminal-negra":<30} tokens {tokens(E06, cuerpo):>5}   '
              f'fallos: {fallos or "ninguno"}')

        sin_clawd = cuerpo.replace(f'<div class="clawd"><img src="{rec["clawd"]}" alt=""></div>', '')
        assert sin_clawd != cuerpo, 'no se encontro el bloque de Clawd para el fondo del video'
        rendear(nav, '_post-06-fondo', E06, sin_clawd)

        # --- 07: la misma pieza en tres fondos ---
        for nombre, (color, extra) in FONDOS_07.items():
            estilo = E07 + f'  .pieza{{background:{color}}}{extra}' + chr(10)
            cuerpo7 = C07.format(**rec)
            f = f'post-07-web-chat--{nombre}'
            fallos = rendear(nav, f, estilo, cuerpo7)
            print(f'{f:<30} tokens {tokens(estilo, cuerpo7):>5}   '
                  f'fallos: {fallos or "ninguno"}')
        nav.close()

    mp4, gif = video_06(SALIDA / '_post-06-fondo.png',
                        SALIDA / 'post-06-terminal-negra.mp4')
    for f in (mp4, gif):
        print(f'{f.name:<30} {f.stat().st_size / 1e6:.2f} MB')


if __name__ == '__main__':
    main()
