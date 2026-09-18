#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Catalogo visual de los fondos de `assets/templates/fondos-color.css`.

    python3 scripts/catalogo_fondos.py

Saca `salida/catalogo-fondos.png` y `salida/catalogo-fondos.pdf`: dieciocho
fondos, cada uno con su clase, su color y una pieza de verdad encima.

POR QUE CADA MUESTRA ES UNA PIEZA Y NO UNA MANCHA DE COLOR
  Una trama se juzga con texto encima o no se juzga. La cuadricula de libreta
  parece preciosa en una muestra de 4x4 cm y se come un titular de 80 px. Asi
  que cada casilla renderiza una pieza completa a 1080x1350 y la reduce con
  `transform:scale`, en vez de dibujar un rectangulo a tamano de casilla: lo que
  se ve es exactamente lo que saldria publicado.

  De ahi tambien que ninguna casilla repita color. Con dieciocho tramas sobre el
  mismo crema no se decide nada; el catalogo existe para elegir la pareja
  trama+color, no la trama sola.

COMO SE LEE
  Debajo de cada casilla van la clase y el token de color. Eso es lo unico que
  hace falta para replicar cualquiera:

      <div class="pieza fondo-cuadricula" style="--fondo:var(--ivory)">
"""
import base64
import pathlib
import sys

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'salida'

# --- BLOQUE 1: las once tramas aprobadas, cada una sobre un color distinto ---
# (clase, etiqueta, token de fondo, variables extra, tinta clara?)
FONDOS = [
    ('fondo-plano', 'Plano', '--celeste', '', False),
    ('fondo-plano', 'Plano oscuro', '--dark', '', True),
    ('fondo-cuadricula', 'Cuadrícula de libreta', '--ivory', '--paso:54px', False),
    ('fondo-milimetrado', 'Papel milimetrado', '--verde-claro', '', False),
    ('fondo-puntos', 'Retícula de puntos', '--light', '--paso:50px', False),
    ('fondo-puntos-fundidos', 'Puntos que se apagan', '--dark', '', True),
    ('fondo-semitono', 'Semitono', '--orange', '', False),
    ('fondo-diagonales', 'Rayado diagonal', '--lila', '', False),
    ('fondo-arcos', 'Arcos concéntricos', '--green', '', True),
    ('fondo-grano', 'Grano', '--ivory', '', False),
    ('fondo-velo', 'Velo de un solo hex', '--celeste', '', False),
]

# --- BLOQUE 2: la misma trama en seis colores ---
# Existe para zanjar la duda de Ramses: ninguna trama esta atada a su muestra.
# Es siempre `fondo-puntos`; lo unico que cambia es --fondo y, en los oscuros,
# el modificador .tinta-clara.
PRUEBA_COLOR = [
    ('--celeste', 'celeste', False), ('--verde-claro', 'verde claro', False),
    ('--lila', 'lila', False), ('--ivory', 'crema', False),
    ('--orange', 'naranja', False), ('--dark', 'oscuro', True),
]

# --- BLOQUE 3: los dos huecos de imagen ---
# No son fondo: recortan una foto contra el color del lienzo.
HUECOS = [
    ('hueco-diagonal', '', 'Corte diagonal', '--celeste', 'f2.jpg', '--corte:56%'),
    ('hueco-diagonal', 'al-reves', 'Corte diagonal, espejado', '--verde-claro', 'f5.jpg', '--corte:52%'),
    ('hueco-esquina', 'abajo-izq', 'Esquina abajo izquierda', '--lila', 'f3.jpg', '--radio:600px'),
    ('hueco-esquina', 'arriba-der', 'Esquina arriba derecha', '--ivory', 'f6.jpg', '--radio:540px'),
]

ESCALA = 0.42
ANCHO, ALTO = round(1080 * ESCALA), round(1350 * ESCALA)


def dato(ruta, mime):
    return f'data:{mime};base64,' + base64.b64encode(pathlib.Path(ruta).read_bytes()).decode()


def casilla(cuerpo, clases, estilo, etiqueta, pie, oscuro):
    lock = '../assets/logos-claudetec/claudetec--claro.svg' if oscuro else '../assets/logos-claudetec/claudetec.svg'
    return f"""
  <figure>
    <div class="marco"><div class="pieza {clases} {'inv' if oscuro else ''}" style="{estilo}">
      {cuerpo}
      <img class="lock" src="{lock}" alt="ClaudeTec">
    </div></div>
    <figcaption><b>{etiqueta}</b><span>{pie}</span></figcaption>
  </figure>"""


def texto(n):
    return f"""<div class="rot">Muestra {n}</div>
      <h1>El fondo<br>se juzga con<br>texto encima</h1>
      <p class="txt">Poppins en la etiqueta, Newsreader en el titular, Lora aquí.
      Si la trama se come alguno, se ve a este tamaño.</p>"""


def ayuda():
    """`--help` tiene que funcionar en los diecinueve scripts: es como se
    averigua que hace uno sin abrirlo. Estos tres no usan argparse porque no
    tienen opciones, asi que el guard va a mano."""
    if any(a in ('-h', '--help') for a in sys.argv[1:]):
        print(__doc__)
        raise SystemExit(0)


def main():
    ayuda()
    fotos = {f: dato(SALIDA / 'fotos' / f, 'image/jpeg')
             for _, _, _, _, f, _ in HUECOS}

    uno = ''.join(
        casilla(texto(f'{i:02d}'), f'{c} {"tinta-clara" if inv else ""}',
                f'--fondo:var({tok});{extra}', et, f'.{c} · {tok}', inv)
        for i, (c, et, tok, extra, inv) in enumerate(FONDOS, 1))

    dos = ''.join(
        casilla(f'<div class="rot">{nom}</div><h1>La misma<br>trama</h1>',
                f'fondo-puntos {"tinta-clara" if inv else ""}',
                f'--fondo:var({tok});--paso:50px', nom.capitalize(),
                f'.fondo-puntos · {tok}', inv)
        for tok, nom, inv in PRUEBA_COLOR)

    tres = ''.join(
        casilla(f'<div class="{c} {mod}" style="--foto:url({fotos[f]});{extra}"></div>'
                f'<div class="rot">Hueco</div><h1>La foto<br>entra por<br>el recorte</h1>',
                'fondo-plano', f'--fondo:var({tok})', et, f'.{c}{"." + mod if mod else ""} · {tok}', False)
        for c, mod, et, tok, f, extra in HUECOS)

    html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/templates/_base.css">
<link rel="stylesheet" href="../assets/templates/fondos-color.css">
<style>
  body{{display:block;background:#b6b4ac;padding:56px;
    font-family:var(--font-heading);width:max-content}}
  h2{{font-family:var(--font-titular);font-weight:600;font-size:46px;color:#141413}}
  h3{{font-family:var(--font-heading);font-weight:700;font-size:23px;color:#141413;
    margin:44px 0 6px;letter-spacing:.02em}}
  .intro,.nota{{font-family:var(--font-body);font-size:20px;color:#3a3a36;
    max-width:88ch;line-height:1.5}}
  .intro{{margin-bottom:14px}}
  .nota{{font-size:18px;margin-bottom:24px}}
  .rejilla{{display:grid;grid-template-columns:repeat(6,{ANCHO}px);gap:34px 26px}}

  /* La casilla no dibuja la trama a su tamano: mete una pieza de 1080x1350 y la
     reduce. Asi lo que se ve es el render real, no una aproximacion. */
  .marco{{width:{ANCHO}px;height:{ALTO}px;overflow:hidden;position:relative}}
  .marco .pieza{{width:1080px;height:1350px;position:absolute;top:0;left:0;
    transform:scale({ESCALA});transform-origin:top left;padding:78px;display:block;
    position:absolute;isolation:isolate}}

  .pieza .rot{{font-family:var(--font-heading);font-weight:600;font-size:22px;
    letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}
  .pieza h1{{font-size:82px;line-height:1.05;margin-top:22px;color:var(--dark)}}
  .pieza .txt{{font-family:var(--font-body);font-size:29px;line-height:1.5;
    margin-top:30px;max-width:22ch;color:var(--dark)}}
  .pieza .lock{{position:absolute;left:78px;bottom:70px;width:250px;display:block;z-index:2}}
  .pieza.inv h1,.pieza.inv .txt{{color:var(--light)}}
  .pieza.inv .rot{{color:rgba(250,249,245,.72)}}

  figcaption{{margin-top:11px;display:flex;flex-direction:column;gap:3px}}
  figcaption b{{font-size:17px;font-weight:700;color:#141413}}
  figcaption span{{font-size:14px;color:#4d4c47;font-family:ui-monospace,Consolas,monospace}}
</style></head><body>
  <h2>Fondos de color · anthro-pic-brand</h2>
  <p class="intro">Las once tramas aprobadas de
  <code>assets/templates/fondos-color.css</code>, a 0.42 del tamaño real. Ninguna
  usa degradado de dos tintas: los desvanecidos son un solo hex con máscara. Para
  replicar cualquiera basta la clase y el token del pie.</p>

  <h3>1 · Las once tramas</h3>
  <p class="nota">Cada una sobre un color distinto, porque lo que se elige es la
  pareja trama + color, no la trama sola.</p>
  <div class="rejilla">{uno}</div>

  <h3>2 · La misma trama en seis colores</h3>
  <p class="nota">Ninguna trama está atada a su muestra. Aquí es siempre
  <code>.fondo-puntos</code>; lo único que cambia es <code>--fondo</code> y, en el
  oscuro, el modificador <code>.tinta-clara</code>, que invierte el signo de la
  tinta. El mismo par vale para las once.</p>
  <div class="rejilla">{dos}</div>

  <h3>3 · Huecos de imagen</h3>
  <p class="nota">El corte diagonal y la esquina no son fondo: recortan una foto
  contra el color del lienzo. La imagen entra por <code>--foto</code>.</p>
  <div class="rejilla">{tres}</div>
</body></html>"""

    f = SALIDA / 'catalogo-fondos.html'
    f.write_text(html, encoding='utf-8')

    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pg = nav.new_page(viewport={'width': 2400, 'height': 1800})
        fallos = []
        pg.on('requestfailed', lambda r: fallos.append(r.url.split('/')[-1]))
        pg.goto(f.resolve().as_uri())
        pg.wait_for_timeout(1400)
        caja = pg.evaluate("() => ({w: document.body.scrollWidth, h: document.body.scrollHeight})")
        pg.set_viewport_size({'width': caja['w'], 'height': caja['h']})
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(SALIDA / 'catalogo-fondos.png'), full_page=True)
        pg.pdf(path=str(SALIDA / 'catalogo-fondos.pdf'), print_background=True,
               width=f"{caja['w']}px", height=f"{caja['h']}px",
               margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        nav.close()

    print('fallos de carga:', fallos or 'ninguno')
    print('lienzo:', caja['w'], 'x', caja['h'])
    for n in ('catalogo-fondos.png', 'catalogo-fondos.pdf'):
        print(f'  {n:<24} {(SALIDA / n).stat().st_size / 1e6:.2f} MB')


if __name__ == '__main__':
    main()
