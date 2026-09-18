#!/usr/bin/env python3
"""Diez piezas 1080x1350 con las capas de `capas.css`, y su coste en tokens.

Cinco con fotografia y cinco solo con recursos graficos. Entre las de recursos
hay una terminal en negro y una herramienta web.

ESTADO (17/09/2026). Ramses aprobo las cinco con foto —copia en
`piezas-aprobadas/`— y rechazo las cinco de recursos graficos. Las 08, 09 y 10
quedan descartadas y sus salidas borradas; las definiciones se dejan aqui solo
como registro de lo que no funciono. Las 06 y 07 se rehicieron con sus
correcciones en `salida/ventanas_67.py`: ese es el script que manda para esas
dos, no este.

    python3 salida/diez_posts.py

Mide, para cada pieza, los tokens del HTML que hay que escribir para producirla.
No mide las fotos ni los SVG: esos se referencian, no se leen (ver el apartado
de tokens en references/assets-index.md).
"""
import base64
import pathlib

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'salida'
FOTOS = SALIDA / 'fotos'


def dato(ruta, mime):
    return f'data:{mime};base64,' + base64.b64encode(pathlib.Path(ruta).read_bytes()).decode()


def marco(estilo, cuerpo, clase=''):
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/templates/_base.css">
<link rel="stylesheet" href="../assets/templates/capas.css">
<style>
  .pieza{{width:1080px;height:1350px;padding:74px;position:relative}}
  .rotulo{{font-family:var(--font-heading);font-weight:600;font-size:19px;
    letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}
  .pie-marca{{position:absolute;left:74px;bottom:56px;display:flex;
    align-items:center;gap:18px;z-index:4}}
  .pie-marca img{{width:232px;height:auto;display:block}}
  .pie-marca span{{font-family:var(--font-heading);font-weight:600;
    font-size:17px;color:var(--muted)}}
{estilo}
</style></head><body><div class="pieza {clase}">{cuerpo}</div></body></html>"""


def construir(rec):
    L_OSC = '../assets/logos-claudetec/claudetec.svg'      # sobre fondo claro
    L_CLA = '../assets/logos-claudetec/claudetec--claro.svg'   # sobre oscuro
    L_MON = '../assets/logos-claudetec/claudetec--monocromo-claro.svg'  # sobre naranja

    piezas = []

    # ============ 1 · FOTO · contexto detras + momento delante ============
    piezas.append(('01-foto-capas', 'foto', 'oscuro', """
  .pieza{padding:0;background:var(--dark)}
  .foto-capas .fondo img{filter:grayscale(1) sepia(.3) brightness(.55)}
  .cabeza{position:absolute;left:74px;right:110px;top:80px;z-index:3}
  .rotulo{color:rgba(250,249,245,.78)}
  h1{font-size:84px;line-height:1.04;color:var(--light);margin-top:18px}
  .foto-capas .encima{left:236px;right:-52px;bottom:196px;height:452px}
  .chip-foto{left:174px;bottom:588px;z-index:4}
  .pie{position:absolute;left:74px;bottom:56px;right:74px;z-index:4;
    display:flex;justify-content:space-between;align-items:flex-end}
  .pie p{font-family:var(--font-heading);font-weight:600;font-size:23px;
    color:var(--light);line-height:1.45}
  .pie p b{color:var(--orange)}
""", f"""
  <div class="foto-capas">
    <div class="fondo"><img src="{rec['f6']}" alt=""></div>
    <div class="cabeza">
      <div class="rotulo">Conectores</div>
      <h1>Un puente entre tus datos y una decisión</h1>
    </div>
    <div class="encima"><img src="{rec['f2']}" alt=""></div>
    <div class="chip-foto"><img src="{rec['glifo']}" alt="">Connecting…</div>
    <div class="pie"><p>Claude lee de donde ya trabajas.<br><b>Sin copiar y pegar.</b></p></div>
  </div>
  <div class="pie-marca" style="position:absolute;right:74px;left:auto;bottom:56px">
    <img src="{L_CLA}" alt="ClaudeTec"></div>
"""))

    # ============ 2 · FOTO · ficha solapada ============
    piezas.append(('02-foto-ficha', 'foto', '', """
  .pieza{display:flex;flex-direction:column;padding-bottom:146px}
  .encabezado{display:grid;grid-template-columns:1.2fr .8fr;gap:42px;
    align-items:start;margin-top:20px}
  h1{font-size:72px;line-height:1.05}
  h1 b{font-weight:600;color:var(--orange)}
  .entrada{font-family:var(--font-body);font-size:24px;line-height:1.46;padding-top:10px}
  .foto-con-ficha{margin-top:56px;margin-right:34px}
  .foto-con-ficha > img{height:690px;object-fit:cover}
  .ficha p{font-size:22px}
""", f"""
  <div class="rotulo">El caso</div>
  <div class="encabezado">
    <h1>Mapear un ecosistema <b>entero</b> en una tarde</h1>
    <p class="entrada">Diecisiete años de registros de campo, dispersos en PDF,
    hojas de cálculo y cuadernos. Ahora responden preguntas.</p>
  </div>
  <div class="foto-con-ficha">
    <img src="{rec['f4']}" alt="">
    <div class="ficha">
      <div class="rotulo">Reserva de la Biosfera</div>
      <p>1,240 especies catalogadas. El equipo pasó de tres semanas de búsqueda
      manual a preguntar en lenguaje natural y recibir la cita exacta.</p>
    </div>
  </div>
  <div class="pie-marca"><img src="{L_OSC}" alt="ClaudeTec"><span>@claude.tec</span></div>
"""))

    # ============ 3 · FOTO · a sangre con titular encima ============
    piezas.append(('03-foto-sangre', 'foto', 'oscuro', """
  .pieza{padding:0}
  .fondo-total{position:absolute;inset:0;overflow:hidden}
  .fondo-total img{width:100%;height:100%;object-fit:cover;
    filter:grayscale(1) sepia(.22) brightness(.58)}
  .texto{position:absolute;left:78px;right:150px;top:150px;z-index:3}
  h1{font-size:88px;line-height:1.07;color:var(--light)}
  .chip-foto{left:78px;top:78px;z-index:4}
  .fuente{position:absolute;right:78px;bottom:60px;z-index:4;text-align:right;
    font-family:var(--font-heading);font-weight:600;font-size:20px;
    color:rgba(250,249,245,.8);letter-spacing:.1em;text-transform:uppercase;
    line-height:1.5}
""", f"""
  <div class="fondo-total"><img src="{rec['f3']}" alt=""></div>
  <div class="chip-foto"><img src="{rec['glifo']}" alt="">Analyzing…</div>
  <div class="texto"><h1>Cómo un servicio forestal predice la niebla que apaga incendios</h1></div>
  <div class="fuente">Sierra de Arteaga<br>Coahuila</div>
  <div class="pie-marca"><img src="{L_CLA}" alt="ClaudeTec"></div>
"""))

    # ============ 4 · FOTO · arriba, chip montando, titular abajo ============
    piezas.append(('04-foto-arriba', 'foto', '', """
  .pieza{padding:0;background:var(--crema-capa)}
  .banda-foto{position:relative;height:640px}
  .banda-foto > img{width:100%;height:100%;object-fit:cover;display:block}
  .chip-foto{left:74px;bottom:-26px;z-index:3}
  .bajo{padding:84px 74px 0}
  h1{font-size:76px;line-height:1.06;margin-top:22px;max-width:15ch}
  h1 b{font-weight:600;color:var(--orange)}
  .entrada{font-family:var(--font-body);font-size:25px;line-height:1.46;
    margin-top:26px;max-width:30ch}
""", f"""
  <div class="banda-foto"><img src="{rec['f1']}" alt="">
    <div class="chip-foto"><img src="{rec['glifo']}" alt="">Researching…</div></div>
  <div class="bajo">
    <div class="rotulo">Convocatoria</div>
    <h1>Buscamos a quien nunca ha escrito <b>una línea de código</b></h1>
    <p class="entrada">Mesa directiva 2027. Cinco puestos abiertos, todas las
    carreras. Postulaciones hasta el 30 de octubre.</p>
  </div>
  <div class="pie-marca"><img src="{L_OSC}" alt="ClaudeTec"><span>claudetec.com</span></div>
"""))

    # ============ 5 · FOTO · par con fichas ============
    piezas.append(('05-par-fotos', 'foto', '', """
  .pieza{display:flex;flex-direction:column;padding-bottom:146px}
  h1{font-size:68px;line-height:1.06;margin-top:16px;max-width:17ch}
  .par-fotos{margin-top:56px;gap:36px}
  .par-fotos .foto-con-ficha > img{height:760px;object-fit:cover}
  .par-fotos .ficha{left:26px;right:-18px;bottom:-30px;padding:20px 22px}
  .par-fotos .ficha .rotulo{font-size:14px;margin-bottom:6px}
  .par-fotos .ficha p{font-size:19px;line-height:1.38}
""", f"""
  <div class="rotulo">Recapitulación</div>
  <h1>Dos días, dos ciudades, la misma pregunta</h1>
  <div class="par-fotos">
    <div class="foto-con-ficha"><img src="{rec['f5']}" alt="">
      <div class="ficha"><div class="rotulo">Sesión 01</div>
      <p>Cuarenta asistentes. Salió el primer prototipo del semestre.</p></div></div>
    <div class="foto-con-ficha"><img src="{rec['f2']}" alt="">
      <div class="ficha"><div class="rotulo">Sesión 02</div>
      <p>Doce equipos. Tres siguen construyendo por su cuenta.</p></div></div>
  </div>
  <div class="pie-marca"><img src="{L_OSC}" alt="ClaudeTec"><span>@claude.tec</span></div>
"""))

    # ============ 6 · GRÁFICO · terminal en negro ============
    piezas.append(('06-terminal-negra', 'grafico', '', """
  .pieza{background:var(--crema-capa);display:flex;flex-direction:column;
    padding-bottom:146px}
  h1{font-size:66px;line-height:1.06;margin-top:16px;max-width:16ch}
  h1 b{font-weight:600;color:var(--orange)}
  .ventana{margin-top:46px}
  .ventana-terminal .contenido{font-size:29px;line-height:2.05;padding:44px 40px 50px}
  .linea{white-space:pre}
  .com{color:rgba(250,249,245,.42)}
  .ok{color:#8fbf72}
  .pie-nota{font-family:var(--font-heading);font-weight:600;font-size:24px;
    color:var(--muted);margin-top:auto;max-width:34ch;line-height:1.45}
""", f"""
  <div class="rotulo">Taller 04</div>
  <h1>Tu primer agente cabe en <b>doce líneas</b></h1>

  <div class="ventana ventana-terminal">
    <div class="barra"><span class="puntos"><i></i><i></i><i></i></span>
      <span class="titulo">~/primer-agente</span></div>
    <div class="contenido">
      <div class="linea"><span class="prompt">$</span> claude "resume estos PDF"</div>
      <div class="linea com">  leyendo 14 archivos…</div>
      <div class="linea com">  encontradas 3 contradicciones</div>
      <div class="linea com">  cruzando con notas de clase…</div>
      <div class="linea"><span class="ok">✓</span> resumen.md escrito</div>
      <div class="linea">&nbsp;</div>
      <div class="linea"><span class="prompt">$</span> <span class="valor acento">_</span></div>
    </div>
  </div>

  <p class="pie-nota">Jueves 2 de octubre, 18:00. Aula CETEC.
  Trae laptop; el resto lo vemos ahí.</p>
  <div class="pie-marca"><img src="{L_OSC}" alt="ClaudeTec"><span>claudetec.com</span></div>
"""))

    # ============ 7 · GRÁFICO · herramienta web ============
    piezas.append(('07-web-chat', 'grafico', '', """
  .pieza{background:var(--orange);display:flex;flex-direction:column;
    padding-bottom:146px}
  .rotulo{color:rgba(250,249,245,.85)}
  .ventana{margin-top:30px}
  .ventana-navegador .contenido{padding:0}
  .chat{padding:34px 36px 40px}
  .turno{display:flex;gap:16px;align-items:flex-start;margin-bottom:26px}
  .turno .quien{width:40px;height:40px;border-radius:9px;flex:none;
    display:grid;place-items:center;font-family:var(--font-heading);
    font-weight:700;font-size:17px}
  .turno.tu .quien{background:var(--light-gray);color:var(--dark)}
  .turno.claude .quien{background:var(--light-gray);padding:7px}
  .turno .quien img{width:100%;display:block}
  .turno .dice{font-family:var(--font-body);font-size:25px;line-height:1.5;
    padding-top:5px}
  .turno.claude .dice b{font-family:var(--font-heading);font-weight:700}
  .campo{display:flex;align-items:center;justify-content:space-between;
    border:1.5px solid var(--light-gray);border-radius:16px;
    padding:20px 22px;margin-top:8px;
    font-family:var(--font-body);font-size:23px;color:var(--muted)}
  .campo .enviar{width:40px;height:40px;border-radius:50%;
    background:var(--orange);display:grid;place-items:center;color:#fff;
    font-family:var(--font-heading);font-weight:700;font-size:20px}
  .pie-nota{font-family:var(--font-heading);font-weight:600;font-size:24px;
    color:var(--light);margin-top:36px;max-width:30ch;line-height:1.45}
  .pie-marca span{color:rgba(250,249,245,.8)}
""", f"""
  <div class="rotulo">Sesión abierta</div>

  <div class="ventana ventana-navegador">
    <div class="barra">
      <span class="puntos"><i></i><i></i><i></i></span>
      <span class="pestana"><span class="favicon"></span>Claude</span>
      <span class="url">claude.ai/chat</span>
    </div>
    <div class="contenido"><div class="chat">
      <div class="turno tu"><span class="quien">R</span>
        <span class="dice">Tengo 200 respuestas de una encuesta. ¿Qué me estoy perdiendo?</span></div>
      <div class="turno claude"><span class="quien"><img src="{rec['glifo']}" alt=""></span>
        <span class="dice">Hay un patrón que no aparece en las gráficas:
        <b>quienes se quejan del horario son los que más asisten.</b>
        No es un problema de agenda.</span></div>
      <div class="campo"><span>Pregunta lo que quieras…</span>
        <span class="enviar">↑</span></div>
    </div></div>
  </div>

  <p class="pie-nota">Traemos tus datos reales. Miércoles 24, 17:00.</p>
  <div class="pie-marca"><img src="{L_MON}" alt="ClaudeTec"><span>@claude.tec</span></div>
"""))

    # ============ 8 · GRÁFICO · cifra con cintas ============
    piezas.append(('08-cifra-cintas', 'grafico', '', """
  .pieza{background:var(--light);display:flex;flex-direction:column;
    padding-bottom:146px}
  .cinta-abajo{height:430px;background:var(--crema-capa)}
  .cinta-arriba{height:14px;background:var(--orange)}
  .cifra{font-family:var(--font-titular);font-weight:600;font-size:340px;
    line-height:.8;letter-spacing:-.05em;color:var(--orange);margin-top:40px}
  h1{font-size:60px;line-height:1.08;margin-top:22px;max-width:16ch}
  .tarjeta{margin-top:auto;margin-bottom:6px}
  .tarjeta .rotulo{margin-bottom:12px}
  .tarjeta p{font-family:var(--font-body);font-size:24px;line-height:1.46}
""", f"""
  <div class="cinta cinta-arriba"></div>
  <div class="cinta cinta-abajo cinta--crema"></div>

  <div class="rotulo">Primer semestre</div>
  <div class="cifra">312</div>
  <h1>personas pasaron por un taller de ClaudeTec</h1>

  <div class="tarjeta tarjeta--alta">
    <div class="rotulo">De dónde vienen</div>
    <p>Ingeniería, 41%. Negocios, 23%. Arquitectura y Diseño, 14%.
    Salud, 11%. Humanidades, 11%. <b>Ninguna carrera queda fuera.</b></p>
  </div>
  <div class="pie-marca"><img src="{L_OSC}" alt="ClaudeTec"><span>claudetec.com</span></div>
"""))

    # ============ 9 · GRÁFICO · ilustración + tarjeta ============
    piezas.append(('09-ilustracion', 'grafico', '', """
  .pieza{background:var(--orange);display:flex;flex-direction:column;
    padding-bottom:146px}
  .rotulo{color:rgba(250,249,245,.85)}
  h1{font-size:74px;line-height:1.05;color:var(--light);margin-top:18px;max-width:12ch}
  .art{position:absolute;right:-66px;top:300px;width:600px;height:600px;z-index:0}
  .tarjeta{margin-top:auto;max-width:560px;position:relative;z-index:2}
  .tarjeta .rotulo{color:var(--muted);margin-bottom:12px}
  .tarjeta p{font-family:var(--font-body);font-size:24px;line-height:1.46}
  .pie-marca span{color:rgba(250,249,245,.8)}
""", f"""
  <div class="rotulo">Qué es MCP</div>
  <h1>El cable que le faltaba a la IA</h1>
  <div class="art">{rec['globo']}</div>

  <div class="tarjeta tarjeta--alta">
    <div class="rotulo">En una frase</div>
    <p>Un estándar abierto para que cualquier modelo hable con cualquier
    herramienta —tu Drive, tu base de datos, tu calendario— sin escribir
    un conector nuevo cada vez.</p>
  </div>
  <div class="pie-marca"><img src="{L_MON}" alt="ClaudeTec"><span>Taller el 9 de octubre</span></div>
"""))

    # ============ 10 · GRÁFICO · Clawd con cinta diagonal ============
    piezas.append(('10-clawd', 'grafico', '', """
  .pieza{background:var(--light);display:flex;flex-direction:column;
    padding-bottom:146px}
  .cinta-abajo{height:520px;background:var(--green);
    clip-path:polygon(0 26%,100% 0,100% 100%,0 100%)}
  h1{font-size:82px;line-height:1.04;margin-top:18px;max-width:11ch}
  h1 b{font-weight:600;color:var(--orange)}
  .entrada{font-family:var(--font-body);font-size:25px;line-height:1.46;
    margin-top:24px;max-width:26ch}
  .art{position:absolute;right:56px;bottom:190px;width:430px;
    image-rendering:pixelated;z-index:2}
  .pie-nota{position:absolute;left:74px;bottom:150px;z-index:3;
    font-family:var(--font-heading);font-weight:700;font-size:26px;
    color:var(--light);max-width:20ch;line-height:1.4}
  .pie-marca span{color:rgba(250,249,245,.85)}
""", f"""
  <div class="cinta cinta-abajo"></div>
  <div class="rotulo">Bienvenida</div>
  <h1>Llegaste al club de los que <b>rompen cosas</b></h1>
  <p class="entrada">Sesión de inducción para nuevos miembros. Sin diapositivas:
  se construye algo el mismo día.</p>
  <img class="art" src="{rec['clawd']}" alt="">
  <p class="pie-nota">Viernes 26 · 16:00<br>Sala de estudiantes</p>
  <div class="pie-marca"><img src="{L_CLA}" alt="ClaudeTec"><span>@claude.tec</span></div>
"""))

    return piezas


def main():
    rec = {f'f{i}': dato(FOTOS / f'f{i}.jpg', 'image/jpeg') for i in range(1, 7)}
    rec['glifo'] = dato(RAIZ / 'assets/logos/claude-glyph.svg', 'image/svg+xml')
    rec['clawd'] = dato(RAIZ / 'assets/clawd/clawd-search.png', 'image/png')
    rec['globo'] = (RAIZ / 'assets/ilustraciones/globo-llaves--verde.svg').read_text(
        encoding='utf-8').replace('<svg', "<svg style='width:100%;height:100%'", 1)

    filas = []
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for nombre, familia, clase, estilo, cuerpo in construir(rec):
            # Lo que cuesta ESCRIBIR la pieza: su CSS y su marcado, sin los
            # data: URI de las fotos, que no pasan por el modelo.
            propio = len(estilo) + len(cuerpo)
            for k, v in rec.items():
                propio -= cuerpo.count(v) * len(v)
            f = SALIDA / f'post-{nombre}.html'
            f.write_text(marco(estilo, cuerpo, clase), encoding='utf-8')
            pg = nav.new_page(viewport={'width': 1080, 'height': 1350})
            fallos = []
            pg.on('requestfailed', lambda r: fallos.append(r.url.split('/')[-1]))
            pg.goto(f.resolve().as_uri())
            pg.wait_for_timeout(700)
            pg.locator('.pieza').screenshot(path=str(SALIDA / f'post-{nombre}.png'))
            pg.close()
            filas.append((nombre, familia, round(propio / 4), fallos))
        nav.close()

    print(f'\n{"pieza":<20}{"tipo":<10}{"tokens":>8}   fallos')
    for n, fam, tok, fallos in filas:
        print(f'{n:<20}{fam:<10}{tok:>8}   {fallos or "—"}')
    foto = [t for _, f, t, _ in filas if f == 'foto']
    graf = [t for _, f, t, _ in filas if f == 'grafico']
    print(f'\n  con foto     media {sum(foto)//len(foto):>5}   total {sum(foto)}')
    print(f'  solo grafico media {sum(graf)//len(graf):>5}   total {sum(graf)}')
    print(f'  TOTAL escrito      {sum(foto)+sum(graf)} tokens')


if __name__ == '__main__':
    main()
