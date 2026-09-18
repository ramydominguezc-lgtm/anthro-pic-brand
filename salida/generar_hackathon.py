#!/usr/bin/env python3
"""Anuncio del hackathon, 1080x1350, con las capas nuevas de `capas.css`.

Tres piezas, cada una estrenando un recurso distinto:
  A - ventana de terminal sobre cinta de color
  B - foto con ficha solapada (el acomodo de "La sede")
  C - foto a sangre atenuada + foto nitida encima + chip de estado

Todas dicen lo mismo: faltan 17 dias, equipos de 4.
"""
import base64
import pathlib

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'salida'
DIAS = 17


def dato(rel, mime):
    return f'data:{mime};base64,' + base64.b64encode((RAIZ / rel).read_bytes()).decode()


def marco(cuerpo, estilo, clase=''):
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/templates/_base.css">
<link rel="stylesheet" href="../assets/templates/capas.css">
<style>
  .pieza{{width:1080px;height:1350px;padding:74px;position:relative}}
  .rotulo-sup{{font-family:var(--font-heading);font-weight:600;font-size:19px;
    letter-spacing:.14em;text-transform:uppercase}}
  .marca-pie{{position:absolute;left:74px;bottom:58px;display:flex;
    align-items:center;gap:20px}}
  .marca-pie img{{width:250px;height:auto;display:block}}
  .marca-pie span{{font-family:var(--font-heading);font-weight:600;
    font-size:18px;color:var(--muted)}}
{estilo}
</style></head><body><div class="pieza {clase}">{cuerpo}</div></body></html>"""


def main():
    rec = {
        'glifo': dato('assets/logos/claude-glyph.svg', 'image/svg+xml'),
        'foto': dato('assets/fotos/expedition-femsa.png', 'image/png'),
        'foto2': dato('assets/fotos/expedition-interior.png', 'image/png'),
        'lock_claro': '../assets/logos-claudetec/claudetec--claro.svg',
        'lock_osc': '../assets/logos-claudetec/claudetec.svg',
        'lock_mono': '../assets/logos-claudetec/claudetec--monocromo-claro.svg',
    }

    # ---------------------------------------------------------------- A
    # La informacion como salida de terminal: las filas clave-valor alinean
    # por los dos puntos y se leen de un vistazo, que es lo que fallaba
    # cuando iban como <dl> suelto en medio del lienzo.
    a_estilo = """
  .pieza{background:var(--orange);color:var(--light);
         display:flex;flex-direction:column;padding-bottom:150px}
  .rotulo-sup{color:rgba(250,249,245,.82)}
  .ventana{margin-top:34px}
  .cabecera-vent{background:var(--crema-capa);padding:40px 40px 34px}
  .cabecera-vent h1{font-family:ui-monospace,Menlo,Consolas,monospace;
    font-weight:700;font-size:96px;line-height:1;letter-spacing:-.03em;
    color:var(--dark)}
  .cabecera-vent .cuenta{font-family:var(--font-heading);font-weight:700;
    font-size:25px;color:var(--orange);margin-top:14px}
  .ventana-terminal--clara .contenido{padding:44px 40px 48px;position:relative;font-size:29px;line-height:1.85}
  .ventana-terminal--clara .fila{margin-bottom:10px}
  .boton{display:inline-block;margin-top:30px;background:var(--orange);
    color:var(--light);border-radius:999px;padding:18px 46px;
    font-family:var(--font-heading);font-weight:700;font-size:28px;
    letter-spacing:.06em;text-transform:uppercase}
  .sello{position:absolute;right:38px;bottom:44px;width:158px;opacity:.9}
  .marca-pie span{color:rgba(250,249,245,.78)}
"""
    a_cuerpo = f"""
  <div class="rotulo-sup">ClaudeTec &middot; Tec de Monterrey</div>

  <div class="ventana ventana-terminal ventana-terminal--clara">
    <div class="barra"><span class="puntos"><i></i><i></i><i></i></span>
      <span class="titulo">claudetec &mdash; hackathon</span></div>
    <div class="cabecera-vent">
      <h1>build with<br>claude</h1>
      <div class="cuenta">faltan {DIAS} dias</div>
    </div>
    <div class="contenido">
      <img class="sello" src="{rec['glifo']}" alt="">
      <div class="fila"><span class="clave">fecha</span><span>:</span><span class="valor">sabado 3 de octubre</span></div>
      <div class="fila"><span class="clave">hora</span><span>:</span><span class="valor">9:00 &mdash; 20:00</span></div>
      <div class="fila"><span class="clave">sede</span><span>:</span><span class="valor acento">Expedition FEMSA</span></div>
      <div class="fila"><span class="clave">equipos</span><span>:</span><span class="valor">4 personas</span></div>
      <div class="fila"><span class="clave">abierto a</span><span>:</span><span class="valor">todas las carreras</span></div>
      <div class="fila"><span class="clave">requisito</span><span>:</span><span class="valor">ninguno</span></div>
      <div class="boton">Registrate</div>
    </div>
  </div>

  <div class="marca-pie"><img src="{rec['lock_mono']}" alt="ClaudeTec">
    <span>claudetec.com</span></div>
"""

    # ---------------------------------------------------------------- B
    # El acomodo de "La sede": rotulo, titular grande a la izquierda, texto
    # corto a la derecha, y la foto con una ficha que SOLAPA su esquina.
    b_estilo = """
  .pieza{background:var(--light);display:flex;flex-direction:column;
         padding-bottom:150px}
  .rotulo-sup{color:var(--muted)}
  .encabezado{display:grid;grid-template-columns:1.15fr .85fr;gap:44px;
    align-items:start;margin-top:22px}
  h1{font-size:76px;line-height:1.04;letter-spacing:-.015em}
  h1 b{font-weight:600;color:var(--orange)}
  .entrada{font-family:var(--font-body);font-size:25px;line-height:1.45;
    color:var(--dark);padding-top:12px}
  .foto-con-ficha{margin-top:58px;margin-right:34px}
  .foto-con-ficha > img{height:700px;object-fit:cover}
  .ficha p{font-size:23px}
  .cuenta-pill{display:inline-block;background:var(--orange);color:var(--light);
    border-radius:999px;padding:11px 28px;font-family:var(--font-heading);
    font-weight:700;font-size:23px;margin-bottom:20px}
"""
    b_cuerpo = f"""
  <div class="rotulo-sup">La sede</div>

  <div class="encabezado">
    <div>
      <div class="cuenta-pill">Faltan {DIAS} dias</div>
      <h1>Build with <b>Claude</b></h1>
    </div>
    <p class="entrada">Un sabado entero construyendo, en equipos de cuatro.
    Abierto a todas las carreras: no hace falta saber programar.</p>
  </div>

  <div class="foto-con-ficha">
    <img src="{rec['foto']}" alt="Expedition FEMSA">
    <div class="ficha">
      <div class="rotulo">Expedition FEMSA</div>
      <p>Sabado 3 de octubre, de 9:00 a 20:00. En el Distrito de Innovacion
      del campus Monterrey. Registro en claudetec.com.</p>
    </div>
  </div>

  <div class="marca-pie"><img src="{rec['lock_osc']}" alt="ClaudeTec">
    <span>@claude.tec</span></div>
"""

    # ---------------------------------------------------------------- C
    # Foto a sangre atenuada de fondo, foto nitida encima y chip de estado
    # montando su canto: el recurso de las piezas de @claudeai.
    c_estilo = """
  .pieza{background:var(--dark);padding:0}
  .foto-capas .fondo img{filter:grayscale(1) sepia(.35) brightness(.62)}
  .texto{position:absolute;left:74px;right:74px;top:84px;z-index:2}
  .rotulo-sup{color:rgba(250,249,245,.8)}
  h1{font-size:82px;line-height:1.05;color:var(--light);margin-top:20px;
     max-width:13ch;text-shadow:none}
  h1 b{font-weight:600;color:var(--light)}
  .foto-capas .encima{left:210px;right:-44px;bottom:172px;height:430px}
  .chip-foto{left:150px;bottom:552px;z-index:3}
  .datos{position:absolute;left:74px;bottom:62px;z-index:3;
    font-family:var(--font-heading);font-weight:600;font-size:24px;
    color:var(--light);line-height:1.5}
  .datos b{color:var(--orange)}
"""
    c_cuerpo = f"""
  <div class="foto-capas">
    <div class="fondo"><img src="{rec['foto']}" alt=""></div>

    <div class="texto">
      <div class="rotulo-sup">Faltan {DIAS} dias</div>
      <h1>Build with <b>Claude</b></h1>
    </div>

    <div class="encima"><img src="{rec['foto2']}" alt="Expedition FEMSA"></div>
    <div class="chip-foto"><img src="{rec['glifo']}" alt="">Expedition FEMSA</div>

    <div class="datos">Sabado 3 de octubre &middot; 9:00&ndash;20:00<br>
      Equipos de <b>4 personas</b> &middot; claudetec.com</div>
  </div>
"""

    piezas = [('A-terminal', a_cuerpo, a_estilo, ''),
              ('B-foto-ficha', b_cuerpo, b_estilo, ''),
              ('C-foto-capas', c_cuerpo, c_estilo, 'oscuro')]

    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for nombre, cuerpo, estilo, clase in piezas:
            f = SALIDA / f'hack-{nombre}.html'
            f.write_text(marco(cuerpo, estilo, clase), encoding='utf-8')
            pg = nav.new_page(viewport={'width': 1080, 'height': 1350})
            fallos = []
            pg.on('requestfailed', lambda r: fallos.append(r.url.split('/')[-1]))
            pg.goto(f.resolve().as_uri())
            pg.wait_for_timeout(800)
            pg.locator('.pieza').screenshot(path=str(SALIDA / f'hack-{nombre}.png'))
            pg.close()
            print(f'  hack-{nombre}.png · fallos:', fallos or 'ninguno')
        nav.close()


if __name__ == '__main__':
    main()
