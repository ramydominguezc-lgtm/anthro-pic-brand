#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collage que se va montando solo: piezas que aparecen una a una sobre el fondo.

    python3 scripts/collage_animado.py            demo
    python3 scripts/collage_animado.py mi.json    receta propia

Sale un MP4, un GIF y el PNG del ultimo fotograma, los tres a 1080x1350.

DE DONDE SALE
  Del video "The making of Claude Code" de Anthropic: una tarjeta central fija y,
  alrededor, capturas, fotos y clips que van entrando de uno en uno hasta llenar
  el lienzo. La tarjeta no se mueve; lo que cuenta la historia es el orden en que
  llega lo demas.

LA RECETA LA ESCRIBE LA PERSONA, NO EL SCRIPT
  Nada se coloca "donde quede bien". Cada pieza trae su caja en pixeles y su
  turno, y eso es todo lo que decide donde y cuando aparece:

      {"src": "fotos/f1.jpg", "caja": [0, 70, 360, 270], "turno": 1,
       "pie": "Soba, el perro de Boris"}

  caja   [x, y, ancho, alto] en el lienzo de 1080x1350. Puede salirse por los
         bordes a proposito: los valores negativos sangran.
  turno  1, 2, 3… El orden de entrada. Dos piezas con el mismo turno entran a la
         vez. El 0 es "ya estaba ahi desde el principio".
  desde  solo para video: segundo del clip por el que empieza a reproducirse.
  pie    rotulo opcional debajo, en la pixel monoespaciada.

POR QUE NO SE USAN ANIMACIONES CSS
  Porque habria que capturar "a ojo" confiando en que el reloj del navegador y el
  del capturador coinciden, y no coinciden: salen fotogramas repetidos y saltos.
  Aqui el tiempo es un argumento. El HTML expone `pintar(t)`, que coloca la pieza
  entera en el segundo t, y el capturador llama a `pintar` una vez por fotograma.
  El render es deterministico: dos corridas dan el mismo MP4 byte a byte.

  Lo mismo vale para los clips: `pintar` le fija el `currentTime` a cada <video>
  en vez de dejarlo correr. Un clip dentro del collage avanza al ritmo del
  collage, no al de la maquina que renderiza.

ENTRADA
  0.24 s por pieza: opacidad de 0 a 1 y escala de 0.94 a 1, sin rebote. La marca
  no admite rebotes ni deslizamientos largos; esto es un corte con un respiro.
"""
import base64
import json
import mimetypes
import pathlib
import subprocess
import sys

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'salida'
FPS = 30
ENTRADA = 0.24          # cuanto tarda una pieza en aparecer, en segundos


# --------------------------------------------------------------- la receta ---

DEMO = {
    'nombre': 'collage-demo',
    'fondo': '--dark',
    'trama': 'fondo-puntos-fundidos tinta-clara',
    'ritmo': 0.40,          # segundos entre turno y turno
    'cola': 1.8,            # reposo al final, para que el bucle respire
    'tarjeta': {
        'titulo': 'ASI SE HIZO\nCLAUDETEC',
        'pie': 'POR EL CLUB',
        'caja': [96, 430, 888, 500],
    },
    'piezas': [
        {'src': 'salida/fotos/f1.jpg', 'caja': [-40, 64, 430, 300], 'turno': 1,
         'pie': 'Primera junta'},
        {'src': 'salida/fotos/f4.jpg', 'caja': [640, 40, 480, 330], 'turno': 2,
         'pie': 'Taller 01'},
        {'src': 'salida/post-06-terminal-negra.mp4', 'caja': [720, 960, 400, 500],
         'turno': 5, 'desde': 1.2},
        {'src': 'salida/fotos/f3.jpg', 'caja': [-30, 980, 400, 300], 'turno': 4,
         'pie': 'Expedition FEMSA'},
        {'src': 'assets/clawd/clawd-skateboard.png', 'caja': [430, 250, 210, 180],
         'turno': 3, 'pixel': True},
        {'src': 'salida/fotos/f6.jpg', 'caja': [330, 1010, 340, 260], 'turno': 6,
         'pie': 'Cierre de semestre'},
    ],
}


# ----------------------------------------------------------------- montaje ---

def uri(ruta):
    r = (RAIZ / ruta) if not pathlib.Path(ruta).is_absolute() else pathlib.Path(ruta)
    mime = mimetypes.guess_type(r.name)[0] or 'application/octet-stream'
    return f'data:{mime};base64,' + base64.b64encode(r.read_bytes()).decode(), mime


def marcado(receta):
    trozos, datos = [], []
    for i, p in enumerate(receta['piezas']):
        src, mime = uri(p['src'])
        x, y, w, h = p['caja']
        pie = (f'<span class="pie-pieza">{p["pie"]}</span>') if p.get('pie') else ''
        clase = 'pieza-col' + (' pixelado' if p.get('pixel') else '')
        if mime.startswith('video'):
            medio = f'<video src="{src}" muted preload="auto"></video>'
        else:
            medio = f'<img src="{src}" alt="">'
        trozos.append(f'<div class="{clase}" data-i="{i}" '
                      f'style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
                      f'{medio}{pie}</div>')
        datos.append({'turno': p['turno'], 'desde': p.get('desde', 0),
                      'video': mime.startswith('video')})
    return ''.join(trozos), datos


def html(receta):
    trozos, datos = marcado(receta)
    t = receta['tarjeta']
    tx, ty, tw, th = t['caja']
    titulo = t['titulo'].replace('\n', '<br>')

    # Press Start 2P es monoespaciada y avanza ~1 em por caracter, asi que el
    # renglon mas largo decide el cuerpo. Con un tamano fijo, un titulo de mas
    # de diez letras se salia de la tarjeta sin avisar —el texto se recortaba
    # contra `overflow:hidden` y la pieza salia plausible y mal—. Se calcula:
    # ancho util de la tarjeta entre el renglon mas largo, con tope en 76.
    largo = max(len(l) for l in t['titulo'].split(chr(10)))
    cuerpo = min(76, int((tw - 80) / max(1, largo)))
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/templates/_base.css">
<link rel="stylesheet" href="../assets/templates/capas.css">
<link rel="stylesheet" href="../assets/templates/fondos-color.css">
<style>
  body{{margin:0;background:#000}}
  .pieza{{width:1080px;height:1350px;position:relative;overflow:hidden;padding:0;
    display:block;isolation:isolate}}

  /* Cada pieza del collage arranca invisible y ligeramente encogida. `pintar`
     solo toca opacidad y escala: nada de layout, para que el navegador no
     recalcule la pagina en cada fotograma. */
  .pieza-col{{position:absolute;opacity:0;transform:scale(.94);
    transform-origin:center center;will-change:opacity,transform}}
  .pieza-col img,.pieza-col video{{width:100%;height:100%;object-fit:cover;
    display:block;border-radius:6px}}
  .pieza-col.pixelado img{{object-fit:contain;image-rendering:pixelated;
    border-radius:0}}
  .pie-pieza{{position:absolute;left:4px;top:calc(100% + 10px);
    font-family:var(--font-mono);font-size:22px;color:rgba(250,249,245,.62);
    white-space:nowrap}}

  /* La tarjeta central: es la unica que no entra, ya esta. Lleva la barra de
     tres puntos de capas.css y las dos pixel de tokens.css — la gruesa para el
     titular, la monoespaciada para el pie. */
  .tarjeta-col{{position:absolute;left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px;
    background:#2b2a27;border-radius:14px;box-shadow:var(--sombra-alta);
    display:flex;flex-direction:column;z-index:5;overflow:hidden}}
  .tarjeta-col .barra{{display:flex;gap:9px;padding:18px 22px}}
  .tarjeta-col .barra i{{width:14px;height:14px;border-radius:50%;display:block}}
  .tarjeta-col .barra i:nth-child(1){{background:#ed6a5e}}
  .tarjeta-col .barra i:nth-child(2){{background:#f4bf4f}}
  .tarjeta-col .barra i:nth-child(3){{background:#61c554}}
  .tarjeta-col .centro{{flex:1;display:flex;flex-direction:column;
    align-items:center;justify-content:center;gap:34px;padding:0 40px 30px}}
  .tarjeta-col h1{{font-family:var(--font-pixel);font-weight:400;font-size:{cuerpo}px;
    line-height:1.30;color:var(--light);text-align:center;letter-spacing:0}}
  .tarjeta-col .pie{{font-family:var(--font-mono);font-size:26px;
    letter-spacing:.30em;color:rgba(250,249,245,.55);text-align:center}}
</style></head><body>
<div class="pieza {receta['trama']}" style="--fondo:var({receta['fondo']})">
  {trozos}
  <div class="tarjeta-col">
    <div class="barra"><i></i><i></i><i></i></div>
    <div class="centro"><h1>{titulo}</h1><div class="pie">{t['pie']}</div></div>
  </div>
</div>
<script>
  const DATOS = {json.dumps(datos)};
  const RITMO = {receta['ritmo']}, ENTRADA = {ENTRADA};
  const CAJAS = [...document.querySelectorAll('.pieza-col')];

  // t en segundos -> estado de la pieza entera. Es la unica funcion que mueve
  // algo; el capturador la llama una vez por fotograma.
  window.pintar = function (t) {{
    CAJAS.forEach((el, i) => {{
      const d = DATOS[i];
      const inicio = d.turno * RITMO;
      let k = (t - inicio) / ENTRADA;              // 0 = aun no, 1 = ya entera
      k = k < 0 ? 0 : (k > 1 ? 1 : k);
      const s = 1 - Math.pow(1 - k, 3);            // ease-out cubica
      el.style.opacity = s;
      el.style.transform = 'scale(' + (0.94 + 0.06 * s) + ')';
      if (d.video) {{
        const v = el.querySelector('video');
        const avance = Math.max(0, t - inicio);
        if (v.duration) v.currentTime = (d.desde + avance) % v.duration;
      }}
    }});
    return true;
  }};

  // Los clips tienen que estar decodificados ANTES del primer fotograma, o los
  // primeros salen en negro. El capturador espera a esta promesa.
  window.listo = Promise.all([...document.querySelectorAll('video')].map(
    v => v.readyState >= 2 ? Promise.resolve()
         : new Promise(r => v.addEventListener('loadeddata', r, {{once: true}}))));
</script></body></html>"""


# ------------------------------------------------------------------ render ---

def render(receta):
    nombre = receta['nombre']
    f = SALIDA / f'{nombre}.html'
    f.write_text(html(receta), encoding='utf-8')

    ultimo = max(p['turno'] for p in receta['piezas'])
    dur = ultimo * receta['ritmo'] + ENTRADA + receta['cola']
    n = round(dur * FPS)
    cuadros = SALIDA / f'_{nombre}-cuadros'
    cuadros.mkdir(exist_ok=True)
    for viejo in cuadros.glob('*.png'):
        viejo.unlink()

    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pg = nav.new_page(viewport={'width': 1080, 'height': 1350})
        fallos = []
        pg.on('requestfailed', lambda r: fallos.append(r.url.split('/')[-1]))
        pg.goto(f.resolve().as_uri())
        pg.wait_for_function('window.listo !== undefined')
        pg.evaluate('window.listo')
        pg.wait_for_timeout(500)
        lienzo = pg.locator('.pieza')
        for k in range(n):
            pg.evaluate('t => window.pintar(t)', k / FPS)
            lienzo.screenshot(path=str(cuadros / f'c{k:04d}.png'))
        nav.close()

    mp4 = SALIDA / f'{nombre}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS),
                    '-i', str(cuadros / 'c%04d.png'), '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(mp4)],
                   check=True)
    gif = SALIDA / f'{nombre}.gif'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(mp4),
                    '-vf', 'fps=20,scale=540:-1:flags=lanczos,split[a][b];'
                           '[a]palettegen[p];[b][p]paletteuse', str(gif)], check=True)
    png = SALIDA / f'{nombre}.png'
    (cuadros / f'c{n - 1:04d}.png').replace(png)

    # Los cuadros sueltos se borran: 133 PNG de 1080x1350 son ~100 MB, y el MP4
    # los reconstruye. Nada derivado se queda en el proyecto (ver VERSION.md).
    for x in cuadros.glob('*.png'):
        x.unlink()
    cuadros.rmdir()

    print('fallos de carga:', fallos or 'ninguno')
    print(f'{n} cuadros · {dur:.2f} s · {FPS} fps')
    for x in (mp4, gif, png):
        print(f'  {x.name:<26} {x.stat().st_size / 1e6:.2f} MB')
    return mp4


def ayuda():
    """`--help` tiene que funcionar en los diecinueve scripts: es como se
    averigua que hace uno sin abrirlo. Estos tres no usan argparse porque no
    tienen opciones, asi que el guard va a mano."""
    if any(a in ('-h', '--help') for a in sys.argv[1:]):
        print(__doc__)
        raise SystemExit(0)


def main():
    ayuda()
    receta = DEMO
    if len(sys.argv) > 1:
        receta = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
    render(receta)


if __name__ == '__main__':
    main()
