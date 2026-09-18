#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diez piezas con fotografia, cada una con una geometria distinta.

    python3 salida/tanda_fotos.py

Salen en `piezas-aprobadas/tanda-02-imagenes/`, en PNG y HTML.

EL ENCARGO
  Las cinco de `piezas-aprobadas/` gustaron, pero replicaban el acomodo de las
  referencias que paso Ramses. Estas diez tienen que dar la misma calidad
  **inventando el acomodo**. Asi que ninguna repite la geometria de aquellas
  cinco —foto atenuada detras, ficha solapada, foto a sangre, mitad y mitad,
  par de fotos— ni la de otra de esta tanda.

LO QUE SE REPLICA ES EL NUMERO
  De `references/veredictos.md`: `aire_max <= 180 px`, una sola capa de texto
  sobre la foto, y la foto tocando al menos un borde salvo que la geometria
  pida lo contrario. Cada corrida lo mide y lo dice.

LAS DIEZ GEOMETRIAS
  01 rejilla  Tres fotos en retícula irregular; el titular ocupa una celda.
  02 corte    Titular sobre color, foto en el corte diagonal inferior.
  03 circulo  Foto recortada en cuarto de circulo; el texto la rodea en L.
  04 columna  Foto a sangre en una columna de altura completa.
  05 ventana  La foto es el contenido de una ventana de navegador.
  06 cita     La cita partida en dos por una banda de foto a sangre.
  07 cifra    Cifra en pixel arriba, foto a sangre, franja de datos al pie.
  08 tira     Cuatro fotos pequenas en fila; el titular manda debajo.
  09 indice   Lista numerada; la foto ancla la esquina inferior.
  10 pixel    Foto a sangre, tarjeta pixel y Clawd caminando sobre su canto.

VEREDICTO DE RAMSES (17 sep 2026)
  Aprobadas tal cual: 01, 02, 04, 05, 09.
  03  bullets mas grandes.
  06  "no le entiendo" -> rehecha entera. Se revisa de cero.
  07  igual -> rehecha entera. Se revisa de cero.
  08  la idea si, el acomodo no: sobraba hueco.
  10  la pixel redondeada no se lee -> Press Start 2P, y las ventanas tipo
      terminal son buen sitio para meter animaciones de Clawd.

LA 10 SALE TAMBIEN EN MP4
  Clawd camina sobre el canto de la tarjeta. El PNG es el fotograma 62 de ese
  mismo video —misma escala y misma posicion—, no un montaje aparte. Sin ffmpeg
  el PNG sale igual y el MP4 se avisa como pendiente.
"""
import base64
import pathlib
import sys

from playwright.sync_api import sync_playwright

RAIZ0 = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ0 / 'scripts'))
from clawd_biblioteca import pieza as pieza_clawd          # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FOTOS = RAIZ / 'salida' / 'fotos2'
DESTINO = RAIZ / 'piezas-aprobadas' / 'tanda-02-imagenes'

# La caja del paseo sobre la tarjeta de la 10. El lienzo original mide 1008x544;
# a 560 px de ancho Clawd queda en ~178x151, que es lo minimo para que se lea
# como Clawd y no como una mancha. La caja se pega al borde derecho de la
# tarjeta (996-560=436) y su base al canto superior (392-302=90), asi que Clawd
# camina APOYADO en la tarjeta. Comprobado que no pisa nada: el parrafo acaba en
# x~510 por encima de y=241, y el punto mas alto del salto (fotograma 80) cae en
# x 667-845, lejos del rotulo. El fotograma 62 tiene su silueta en
# (384,272)-(704,544), que a esta escala es (649,241) de 178x151.
PASEO_W, PASEO_H = 560, 302
PASEO_X, PASEO_Y = 436, 90
F62 = (384, 272, 704, 544)

L_OSC = '../../assets/logos-claudetec/claudetec.svg'
L_CLA = '../../assets/logos-claudetec/claudetec--claro.svg'
L_MON = '../../assets/logos-claudetec/claudetec--monocromo-claro.svg'


def dato(ruta, mime):
    return f'data:{mime};base64,' + base64.b64encode(pathlib.Path(ruta).read_bytes()).decode()


def marco(estilo, cuerpo, clases='', vars_=''):
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="../../assets/templates/_base.css">
<link rel="stylesheet" href="../../assets/templates/capas.css">
<link rel="stylesheet" href="../../assets/templates/fondos-color.css">
<style>
  .pieza{{width:1080px;height:1350px;position:relative;padding:0;display:block;
    overflow:hidden}}
  .rotulo{{font-family:var(--font-heading);font-weight:600;font-size:21px;
    letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}
  .marca{{position:absolute;z-index:8;display:block}}
  .marca img{{width:236px;height:auto;display:block}}
  .cuerpo{{font-family:var(--font-body);line-height:1.5}}
{estilo}
</style></head><body><div class="pieza {clases}" style="{vars_}">{cuerpo}</div></body></html>"""


def clawd_f62():
    """Fotograma 62 del paseo recortado a su silueta, a la escala del video.

    Es el unico cuadro con las cuatro patas separadas; los demas se leen como
    Clawd quieto. Sale por el puente `clawd_biblioteca`, no por ruta absoluta.
    """
    from PIL import Image
    im = Image.open(pieza_clawd('paseo', 'fotograma', 62))
    tmp = RAIZ / 'salida' / '_clawd-f062.png'
    im.crop(F62).save(tmp)
    return dato(tmp, 'image/png')


def video_10(fondo_png, destino):
    """Superpone el paseo sobre el fondo fijo de la 10.

    Con ffmpeg y no cuadro a cuadro: el GIF del paseo tiene duraciones variables
    (20 a 1680 ms, 125 cuadros para 11.52 s) y el demuxer de GIF ya las respeta.
    `flags=neighbor` conserva el pixel art al escalar.
    """
    import shutil
    import subprocess
    if not shutil.which('ffmpeg'):
        print('  (sin ffmpeg: 10-pixel.mp4 queda pendiente; el PNG si salio)')
        return None
    filtro = (f'[1:v]scale={PASEO_W}:{PASEO_H}:flags=neighbor[c];'
              f'[0:v][c]overlay={PASEO_X}:{PASEO_Y}:format=auto')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error',
                    '-loop', '1', '-i', str(fondo_png),
                    '-ignore_loop', '0', '-i', str(pieza_clawd('paseo', 'transparente')),
                    '-filter_complex', filtro, '-t', '11.52', '-r', '50',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart', str(destino)], check=True)
    return destino


def construir(f):
    p = []

    # ============ 01 · REJILLA IRREGULAR ============
    # El titular no va encima de ninguna foto: ocupa una celda de la retícula,
    # que es lo que hace que la pieza se lea como tablero y no como cartel.
    p.append(('01-rejilla', 'fondo-plano', '--fondo:var(--ivory)', """
  .rej{position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr;
    grid-template-rows:436px 1fr 340px}
  .rej img{width:100%;height:100%;object-fit:cover;display:block}
  .alta{grid-row:1 / span 2}
  .txt{padding:60px 56px 0 60px}
  .txt h1{font-size:72px;line-height:1.05;margin-top:20px}
  .txt h1 b{font-weight:600;color:var(--orange)}
  .pie{grid-column:1 / -1;padding:52px 60px;display:flex;
    justify-content:space-between;align-items:flex-end}
  .pie p{flex:1;font-family:var(--font-body);font-size:30px;line-height:1.45;
    max-width:30ch;padding-right:40px}
  .pie .marca img{width:206px}
  .marca{position:static}
""", f"""
  <div class="rej">
    <img class="alta" src="{f['p625']}" alt="">
    <div class="txt"><div class="rotulo">Convocatoria abierta</div>
      <h1>Primera generación,<br><b>agosto 2026</b></h1></div>
    <img src="{f['p20']}" alt="">
    <div class="pie">
      <p>Cualquier carrera. No hace falta saber programar: hace falta querer
      construir algo.</p>
      <span class="marca"><img src="{L_OSC}" alt="ClaudeTec"></span>
    </div>
  </div>
"""))

    # ============ 02 · CORTE DIAGONAL ============
    p.append(('02-corte', 'fondo-plano', '--fondo:var(--celeste)', """
  .hueco-diagonal{--corte:43%}
  .alto{position:absolute;left:74px;right:74px;top:84px}
  h1{font-size:88px;line-height:1.04;margin-top:22px;max-width:13ch}
  .entrada{font-family:var(--font-body);font-size:30px;line-height:1.5;
    margin-top:28px;max-width:26ch}
  .ficha{position:absolute;left:74px;top:548px;right:200px;z-index:6;
    background:var(--light);border-radius:14px;padding:30px 34px;
    box-shadow:var(--sombra-alta)}
  .ficha dl{display:grid;grid-template-columns:auto 1fr;gap:10px 26px;
    font-family:var(--font-heading);font-size:26px}
  .ficha dt{font-weight:600;color:var(--muted)}
  .ficha dd{font-weight:700}
  .marca{left:74px;bottom:62px}
""", f"""
  <div class="hueco-diagonal" style="--foto:url({f['p180']})"></div>
  <div class="alto"><div class="rotulo">Taller 05</div>
    <h1>Tu primer agente, de principio a fin</h1>
    <p class="entrada">Tres horas. Sales con algo corriendo, no con apuntes.</p></div>
  <div class="ficha"><dl>
    <dt>Cuándo</dt><dd>Sábado 11, 10:00</dd>
    <dt>Dónde</dt><dd>Aula CETEC 204</dd>
    <dt>Traer</dt><dd>Laptop y un problema tuyo</dd>
  </dl></div>
  <span class="marca"><img src="{L_OSC}" alt="ClaudeTec"></span>
"""))

    # ============ 03 · CUARTO DE CIRCULO ============
    # El texto rodea el recorte en L. La foto no lleva texto encima en ningun
    # punto: el circulo es forma, no fondo.
    p.append(('03-circulo', 'fondo-plano', '--fondo:var(--ivory)', """
  .hueco-esquina{--radio:760px}
  .alto{position:absolute;left:74px;right:74px;top:90px}
  h1{font-size:82px;line-height:1.05;margin-top:22px;max-width:12ch}
  h1 b{font-weight:600;color:var(--orange)}
  /* Ramses, v2.14: los bullets se leian chicos. 26 -> 32 px y la columna se
     ensancha de 330 a 386 para que ninguno parta en dos lineas. El circulo no
     estorba: con radio 760 desde la esquina inferior izquierda solo alcanza
     x=514 a la altura en que acaba la lista. */
  .lado{position:absolute;right:74px;top:508px;width:386px;z-index:6;
    font-family:var(--font-body);font-size:30px;line-height:1.5}
  .lado .rotulo{margin-bottom:14px}
  .lado ul{list-style:none;margin-top:20px}
  .lado li{padding:19px 0;border-top:2px solid var(--light-gray);
    font-family:var(--font-heading);font-weight:600;font-size:32px;
    line-height:1.25}
  .marca{right:74px;bottom:70px}
""", f"""
  <div class="hueco-esquina abajo-izq" style="--foto:url({f['p201']})"></div>
  <div class="alto"><div class="rotulo">Mentorías</div>
    <h1>Una hora,<br>tu proyecto y<br><b>alguien que ya pasó por ahí</b></h1></div>
  <div class="lado"><div class="rotulo">Se apuntan</div>
    <ul><li>Idea sin empezar</li><li>Proyecto atorado</li>
    <li>Prototipo que no escala</li></ul></div>
  <span class="marca"><img src="{L_OSC}" alt="ClaudeTec"></span>
"""))

    # ============ 04 · COLUMNA A SANGRE ============
    p.append(('04-columna', 'fondo-plano', '--fondo:var(--dark)', """
  .col{position:absolute;right:0;top:0;bottom:0;width:430px}
  .col img{width:100%;height:100%;object-fit:cover;display:block;
    filter:grayscale(1) sepia(.3) brightness(.78)}
  .txt{position:absolute;left:74px;top:96px;right:500px}
  .txt .rotulo{color:rgba(250,249,245,.7)}
  h1{font-size:80px;line-height:1.04;color:var(--light);margin-top:22px}
  h1 b{font-weight:600;color:var(--orange)}
  .cuerpo{font-size:29px;color:rgba(250,249,245,.86);margin-top:32px}
  .cifras{position:absolute;left:74px;bottom:170px;right:500px;
    display:grid;gap:26px}
  .cifras div{border-top:2px solid rgba(250,249,245,.22);padding-top:14px}
  .cifras b{font-family:var(--font-titular);font-weight:600;font-size:52px;
    color:var(--light);display:block}
  .cifras span{font-family:var(--font-heading);font-weight:600;font-size:22px;
    color:rgba(250,249,245,.62)}
  .marca{left:74px;bottom:70px}
""", f"""
  <div class="col"><img src="{f['p667']}" alt=""></div>
  <div class="txt"><div class="rotulo">Qué es ClaudeTec</div>
    <h1>Un club para <b>usar bien</b> la IA</h1>
    <p class="cuerpo">Grupo estudiantil del Tec de Monterrey. Formamos usuarios
    competentes, críticos y éticos — no espectadores.</p></div>
  <div class="cifras">
    <div><b>1,000+</b><span>Comunidad</span></div>
    <div><b>Todas</b><span>Las carreras</span></div>
  </div>
  <span class="marca"><img src="{L_CLA}" alt="ClaudeTec"></span>
"""))

    # ============ 05 · LA FOTO DENTRO DE UNA VENTANA ============
    # La ventana de capas.css deja de enmarcar texto y enmarca una imagen: lo
    # que se anuncia vive en una URL, asi que la pieza lo ensena como pantalla.
    p.append(('05-ventana', 'fondo-puntos', '--fondo:var(--verde-claro);--paso:52px', """
  .alto{position:absolute;left:74px;right:74px;top:88px}
  h1{font-size:84px;line-height:1.04;margin-top:22px;max-width:13ch}
  .ventana-navegador{position:absolute;left:74px;right:-70px;top:520px;bottom:-60px}
  .ventana-navegador .contenido{padding:0;height:100%}
  .ventana-navegador .marco-foto{height:620px;overflow:hidden}
  .ventana-navegador img.foto{width:100%;height:100%;object-fit:cover;display:block}
  .bajo{padding:34px 160px 40px 40px;display:flex;gap:40px;align-items:baseline}
  .bajo h2{font-family:var(--font-titular);font-weight:600;font-size:38px}
  .bajo p{font-family:var(--font-body);font-size:25px;color:var(--muted);line-height:1.45}
  .marca{right:74px;top:92px}
  .marca img{width:210px}
""", f"""
  <div class="alto"><div class="rotulo">Ya está en línea</div>
    <h1>Todo el club, en una página</h1></div>
  <span class="marca"><img src="{L_OSC}" alt="ClaudeTec"></span>
  <div class="ventana ventana-navegador">
    <div class="barra"><span class="puntos"><i></i><i></i><i></i></span>
      <span class="pestana"><span class="favicon"></span>ClaudeTec</span>
      <span class="url">claudetec.com</span></div>
    <div class="contenido">
      <div class="marco-foto"><img class="foto" src="{f['p392']}" alt=""></div>
      <div class="bajo"><h2>Calendario</h2>
        <p>Talleres, mentorías y convocatorias, con las fechas reales.</p></div>
    </div>
  </div>
"""))

    # ============ 06 · LA CITA ATRAVIESA LA FOTO ============
    # SEGUNDA VERSION. La primera la descarto Ramses: "no le entiendo". Tenia
    # tres fallos y los tres eran de lectura, no de gusto:
    #   1. La "ficha de quien habla" era un retrato, pero en el banco de fotos
    #      no hay una sola persona: salia una cita firmada por un portatil.
    #   2. La comilla de 170 px caia encima del rotulo y se comian entre si.
    #   3. Entre la cita y la firma quedaban ~420 px muertos que `aire_max` no
    #      vio porque la trama de grano tapa el lienzo entero (ver
    #      `aire_fiable` en analizar_referencia.py).
    # Esta version quita el retrato —la voz se firma con texto, que es lo unico
    # que el material soporta—, y parte la frase en dos con la foto en medio a
    # sangre. La banda obliga a que las dos mitades esten llenas: el hueco no
    # cabe. Fondo plano, ademas, para que el aire vuelva a ser medible.
    p.append(('06-cita', 'fondo-plano', '--fondo:var(--celeste)', """
  .arriba{position:absolute;left:74px;right:74px;top:86px}
  .banda{position:absolute;left:0;right:0;top:486px;height:352px;overflow:hidden}
  .banda img{width:100%;height:100%;object-fit:cover;display:block}
  .abajo{position:absolute;left:74px;right:74px;top:900px}
  blockquote{font-family:var(--font-titular);font-weight:600;font-size:62px;
    line-height:1.14;margin-top:24px;max-width:17ch}
  /* La comilla cuelga fuera del eje: dentro empujaria la primera linea y la
     cita dejaria de alinear con el rotulo y con el logo. */
  blockquote.entra{text-indent:-.44em}
  blockquote i{font-style:normal;color:var(--orange)}
  .firma{position:absolute;left:74px;right:74px;bottom:72px;
    display:flex;justify-content:space-between;align-items:flex-end;
    border-top:2px solid rgba(20,20,19,.2);padding-top:26px}
  .firma b{font-family:var(--font-heading);font-weight:700;font-size:29px;display:block}
  .firma span{font-family:var(--font-heading);font-weight:600;font-size:23px;
    color:var(--muted)}
  .marca{position:static}
  .marca img{width:216px}
""", f"""
  <div class="arriba"><div class="rotulo">Voces del club</div>
    <blockquote class="entra"><i>&ldquo;</i>Entré pensando que esto era
    para los de sistemas.</blockquote></div>
  <div class="banda"><img src="{f['p180']}" alt=""></div>
  <div class="abajo">
    <blockquote>Salí con la mitad de mi tesis hecha.</blockquote></div>
  <div class="firma">
    <div><b>Ana, generación 01</b>
      <span>Ingeniería Industrial · 6.º semestre</span></div>
    <span class="marca"><img src="{L_OSC}" alt="ClaudeTec"></span>
  </div>
"""))

    # ============ 07 · LA CIFRA MANDA ============
    # SEGUNDA VERSION. La primera no se entendia por el material, no por el
    # acomodo: la foto era la portada de un libro que pone "Symbol" en grande,
    # o sea una segunda marca dentro de la pieza, y no tenia nada que ver con
    # "312 personas". Ademas el parrafo de porcentajes acababa pegado al logo.
    # Aqui la cifra es lo primero y va en pixel —es un dato de producto, no un
    # titular de comunidad—, la foto es un aula vacia (que SI habla de cuanta
    # gente cabe) y los porcentajes bajan a una franja oscura maciza al pie,
    # donde el contraste esta garantizado y no pueden tocar al logo.
    p.append(('07-cifra', 'fondo-plano', '--fondo:var(--light)', """
  .alto{position:absolute;left:74px;right:74px;top:84px}
  /* Press Start 2P avanza ~1 em por caracter: tres cifras a 168 px son 504 px
     de los 932 utiles. Cuatro cifras cabrian; cinco no. */
  .cifra{font-family:var(--font-pixel);font-weight:400;font-size:168px;
    line-height:1;color:var(--orange);margin-top:26px}
  .glosa{font-family:var(--font-heading);font-weight:600;font-size:38px;
    line-height:1.3;margin-top:30px;max-width:18ch}
  .foto{position:absolute;left:0;right:0;top:522px;bottom:0;overflow:hidden}
  .foto img{width:100%;height:100%;object-fit:cover;display:block;
    filter:saturate(.55) brightness(.96)}
  .pie{position:absolute;left:0;right:0;bottom:0;height:186px;
    background:var(--dark);z-index:4;display:grid;
    grid-template-columns:repeat(5,1fr);align-items:center;padding:0 74px}
  .pie b{font-family:var(--font-mono);font-size:33px;color:var(--orange);
    display:block}
  .pie span{font-family:var(--font-heading);font-weight:600;font-size:19px;
    color:rgba(250,249,245,.72);display:block;margin-top:8px}
  .marca{right:74px;top:92px}
  .marca img{width:206px}
""", f"""
  <div class="alto"><div class="rotulo">Primer semestre</div>
    <div class="cifra">312</div>
    <p class="glosa">personas pasaron por un taller de ClaudeTec</p></div>
  <span class="marca"><img src="{L_OSC}" alt="ClaudeTec"></span>
  <div class="foto"><img src="{f['p625']}" alt=""></div>
  <div class="pie">
    <div><b>41%</b><span>Ingeniería</span></div>
    <div><b>23%</b><span>Negocios</span></div>
    <div><b>14%</b><span>Arq. y Diseño</span></div>
    <div><b>11%</b><span>Salud</span></div>
    <div><b>11%</b><span>Humanidades</span></div>
  </div>
"""))

    # ============ 08 · TIRA DE CUATRO ============
    p.append(('08-tira', 'fondo-plano', '--fondo:var(--dark)', """
  /* Ramses, v2.14: "sigue habiendo espacio vacio". Lo habia: 337 px muertos
     entre el titular y la lista, que la metrica no vio porque sobre fondo
     oscuro tomaba el color de la esquina —dentro de la foto— como fondo y
     entonces TODA la pieza contaba como tinta. Corregida la metrica, la pieza
     medía 337 y el umbral son 180.
     El arreglo no es estirar el hueco: la lista pasa de dos columnas apretadas
     abajo del todo a UNA columna de cuatro renglones que ocupa el tercio
     central. Cada renglon respira, el numero se lee, y no queda banda muerta
     porque la lista nace donde acaba el titular. */
  .tira{position:absolute;left:0;right:0;top:0;height:352px;display:grid;
    grid-template-columns:repeat(4,1fr);gap:6px}
  .tira img{width:100%;height:100%;object-fit:cover;display:block}
  .bajo{position:absolute;left:74px;right:74px;top:428px}
  .bajo .rotulo{color:rgba(250,249,245,.7)}
  h1{font-size:88px;line-height:1.04;color:var(--light);margin-top:24px;max-width:11ch}
  h1 b{font-weight:600;color:var(--orange)}
  /* Cada renglon llega hasta el margen derecho con su dato. Antes la regla
     cruzaba la pieza entera y el texto moria a media anchura: la mitad derecha
     de cada fila era hueco disfrazado de alineacion. */
  .lista{position:absolute;left:74px;right:74px;top:726px}
  .lista div{display:flex;gap:26px;align-items:baseline;
    border-top:2px solid rgba(250,249,245,.2);padding:26px 0}
  .lista i{font-family:var(--font-mono);font-size:27px;
    color:var(--orange);font-style:normal}
  .lista span{font-family:var(--font-heading);font-weight:600;font-size:33px;
    color:rgba(250,249,245,.92);line-height:1.25}
  .lista em{margin-left:auto;font-style:normal;font-family:var(--font-mono);
    font-size:25px;color:rgba(250,249,245,.55)}
  .marca{left:74px;bottom:64px}
""", f"""
  <div class="tira">
    <img src="{f['p20']}" alt=""><img src="{f['p48']}" alt="">
    <img src="{f['p366']}" alt=""><img src="{f['p625']}" alt="">
  </div>
  <div class="bajo"><div class="rotulo">Recap</div>
    <h1>Lo que hicimos <b>este semestre</b></h1></div>
  <div class="lista">
    <div><i>01</i><span>Nueve talleres abiertos</span><em>312 asistentes</em></div>
    <div><i>02</i><span>Un hackathon de un día</span><em>14 equipos</em></div>
    <div><i>03</i><span>Cuatro proyectos vivos</span><em>en curso</em></div>
    <div><i>04</i><span>Dos alianzas firmadas</span><em>2 empresas</em></div>
  </div>
  <span class="marca"><img src="{L_CLA}" alt="ClaudeTec"></span>
"""))

    # ============ 09 · INDICE DE CARRUSEL ============
    p.append(('09-indice', 'fondo-milimetrado', '--fondo:var(--lila)', """
  .alto{position:absolute;left:74px;right:74px;top:92px}
  h1{font-size:78px;line-height:1.04;margin-top:22px;max-width:12ch}
  ol{position:absolute;left:74px;right:430px;top:400px;list-style:none;
    counter-reset:i}
  ol li{counter-increment:i;padding:26px 0;
    border-bottom:2px solid rgba(20,20,19,.16);
    font-family:var(--font-heading);font-weight:600;font-size:30px;
    display:flex;gap:22px;align-items:baseline}
  ol li::before{content:counter(i,decimal-leading-zero);
    font-family:var(--font-mono);font-size:24px;color:var(--orange)}
  /* La foto ancla la esquina y sangra: sin eso la pieza se queda en lista. */
  .ancla{position:absolute;right:-40px;bottom:-40px;width:470px;height:470px;
    border-radius:14px;overflow:hidden;box-shadow:var(--sombra-alta)}
  .ancla img{width:100%;height:100%;object-fit:cover;display:block}
  .marca{left:74px;bottom:76px}
""", f"""
  <div class="alto"><div class="rotulo">Carrusel · 5 láminas</div>
    <h1>Cinco cosas que aprendes el primer mes</h1></div>
  <ol>
    <li>Pedir bien, que no es pedir mucho</li>
    <li>Cuándo NO usar un modelo</li>
    <li>Conectar tus propios datos</li>
    <li>Revisar lo que te devuelve</li>
    <li>Entregar algo, no una demo</li>
  </ol>
  <div class="ancla"><img src="{f['p160']}" alt=""></div>
  <span class="marca"><img src="{L_OSC}" alt="ClaudeTec"></span>
"""))

    # ============ 10 · TARJETA PIXEL SOBRE FOTO ============
    p.append(('10-pixel', 'fondo-plano', '--fondo:var(--dark)', """
  .fondo{position:absolute;inset:0}
  .fondo img{width:100%;height:100%;object-fit:cover;display:block;
    filter:grayscale(1) brightness(.5) contrast(1.1)}
  .tarjeta-px{position:absolute;left:84px;right:84px;top:392px;height:566px;
    background:#2b2a27;border-radius:14px;box-shadow:var(--sombra-alta);
    display:flex;flex-direction:column;overflow:hidden;z-index:4}
  .tarjeta-px .barra{display:flex;gap:9px;padding:18px 22px}
  .tarjeta-px .barra i{width:14px;height:14px;border-radius:50%;display:block}
  .tarjeta-px .barra i:nth-child(1){background:#ed6a5e}
  .tarjeta-px .barra i:nth-child(2){background:#f4bf4f}
  .tarjeta-px .barra i:nth-child(3){background:#61c554}
  .tarjeta-px .centro{flex:1;display:flex;flex-direction:column;
    align-items:center;justify-content:center;gap:30px;padding:0 44px 26px}
  /* Press Start 2P, no Pixelify Sans: Ramses descarto la redondeada por
     ilegible (la D se leia O). Esta es monoespaciada y avanza ~1 em por
     caracter, asi que el renglon mas largo manda el cuerpo: "WITH CLAUDE"
     son 11 caracteres y el ancho util de la tarjeta 824 px -> 58 px maximo.
     Sin letter-spacing: la fuente ya lo trae en la rejilla. */
  .tarjeta-px h1{font-family:var(--font-pixel);font-weight:400;font-size:58px;
    line-height:1.32;color:var(--light);text-align:center;letter-spacing:0}
  .tarjeta-px .sub{font-family:var(--font-mono);font-size:25px;
    letter-spacing:.26em;color:rgba(250,249,245,.55);text-align:center}
  /* Clawd camina sobre el canto de la tarjeta. La caja del paseo ocupa la
     mitad derecha (516 -> 996) para no cruzarse con el parrafo, que acaba en
     x~510. La imagen fija es el fotograma 62 puesto EXACTAMENTE donde lo deja
     el video, no un montaje aparte: misma escala, misma posicion. */
  .clawd{position:absolute;left:649px;top:241px;width:178px;height:151px;
    z-index:5;image-rendering:pixelated}
  .clawd img{width:100%;height:100%;display:block}
  .alto{position:absolute;left:84px;right:84px;top:110px;z-index:4}
  .alto .rotulo{color:rgba(250,249,245,.78)}
  .alto p{font-family:var(--font-body);font-size:31px;line-height:1.45;
    color:var(--light);margin-top:18px;max-width:22ch}
  .abajo{position:absolute;left:84px;right:84px;bottom:76px;z-index:4;
    display:flex;justify-content:space-between;align-items:flex-end}
  .abajo .cuando{font-family:var(--font-heading);font-weight:600;font-size:25px;
    color:var(--light);text-align:right;line-height:1.4}
  .marca{position:static}
""", f"""
  <div class="fondo"><img src="{f['p536']}" alt=""></div>
  <div class="clawd"><img src="{f['clawd62']}" alt=""></div>
  <div class="alto"><div class="rotulo">Hackathon</div>
    <p>Un reto real de una empresa, resuelto en un día por equipos de cuatro.</p></div>
  <div class="tarjeta-px">
    <div class="barra"><i></i><i></i><i></i></div>
    <div class="centro"><h1>BUILD<br>WITH CLAUDE</h1>
      <div class="sub">3 DE OCTUBRE</div></div>
  </div>
  <div class="abajo">
    <span class="marca"><img src="{L_CLA}" alt="ClaudeTec"></span>
    <div class="cuando">Expedition FEMSA<br>Campus Monterrey</div>
  </div>
"""))
    return p


def main():
    if any(a in ('-h', '--help') for a in sys.argv[1:]):
        print(__doc__)
        return
    DESTINO.mkdir(parents=True, exist_ok=True)
    f = {r.stem: dato(r, 'image/jpeg') for r in FOTOS.glob('p*.jpg')}
    f['clawd62'] = clawd_f62()

    # La 07 cambio de geometria y de nombre: la version de cinta ya no existe.
    for viejo in DESTINO.glob('07-cinta.*'):
        viejo.unlink()

    filas = []
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for nombre, clases, vars_, estilo, cuerpo in construir(f):
            arch = DESTINO / f'{nombre}.html'
            arch.write_text(marco(estilo, cuerpo, clases, vars_), encoding='utf-8')
            pg = nav.new_page(viewport={'width': 1080, 'height': 1350})
            fallos = []
            pg.on('requestfailed', lambda r: fallos.append(r.url.split('/')[-1]))
            pg.goto(arch.resolve().as_uri())
            pg.wait_for_timeout(700)
            pg.locator('.pieza').screenshot(path=str(DESTINO / f'{nombre}.png'))
            if nombre == '10-pixel':
                # Mismo HTML sin Clawd: es el fondo fijo sobre el que ffmpeg
                # superpone el paseo. Asi el video y el PNG no pueden
                # descuadrarse, porque comparten el fondo exacto.
                pg.add_style_tag(content='.clawd{display:none}')
                pg.locator('.pieza').screenshot(path=str(DESTINO / '_10-fondo.png'))
            pg.close()
            propio = len(estilo) + len(cuerpo)
            for v in f.values():
                propio -= cuerpo.count(v) * len(v)
            filas.append((nombre, round(propio / 4), fallos))
        nav.close()

    mp4 = video_10(DESTINO / '_10-fondo.png', DESTINO / '10-pixel.mp4')
    (DESTINO / '_10-fondo.png').unlink()
    if mp4:
        print(f'\n{mp4.name}  {mp4.stat().st_size / 1e6:.2f} MB')

    # El unico umbral medido que separa aprobadas de rechazadas.
    sys.path.insert(0, str(RAIZ / 'scripts'))
    from analizar_referencia import props
    print(f'\n{"pieza":<14}{"tokens":>7}{"aire_max":>10}{"sangra":>8}   fallos')
    for nombre, tok, fallos in filas:
        m = props(DESTINO / f'{nombre}.png')
        if not m['aire_fiable']:
            aviso = '  <-- AIRE NO MEDIBLE (trama a lienzo completo)'
        elif m['aire_max'] > 180:
            aviso = '  <-- PASA DE 180'
        else:
            aviso = ''
        print(f'{nombre:<14}{tok:>7}{m["aire_max"]:>10}{m["sangra"]:>8}   '
              f'{fallos or "-"}{aviso}')


if __name__ == '__main__':
    main()
