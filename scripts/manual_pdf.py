#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arma el manual de la skill en PDF.

    python3 scripts/manual_pdf.py

Sale `salida/manual-anthro-pic-brand.pdf`: cómo se hace un post, qué decide qué,
y cómo encaja esta skill con las dos de Clawd.

PARA QUIEN ES
  Para una persona del equipo que va a pedir o a revisar una pieza, y para
  cualquier sesión nueva que abra la skill sin contexto. No sustituye a los `.md`
  —esos son la fuente— pero se lee de corrido y se puede mandar por WhatsApp.

COMO ESTA HECHO
  HTML + Chromium, no reportlab. Dos motivos: el manual tiene que verse con la
  tipografia y los colores de la marca, y esos ya estan definidos en CSS; y las
  muestras de piezas son PNG que hay que colocar en rejilla, que es lo que el
  navegador hace bien. `pg.pdf()` con `print_background` da el archivo.

  Las muestras se leen de `piezas-aprobadas/`, asi que el manual se actualiza
  solo: si cambian las piezas, se vuelve a correr y ya.
"""
import base64
import pathlib
import sys

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'salida'
PDF = SALIDA / 'manual-anthro-pic-brand.pdf'


def uri(ruta, ancho=None):
    """`ancho` reduce antes de empotrar. Las muestras se ven a 3 cm en el PDF:
    meterlas a 1080 px daba un archivo de 14 MB para nada."""
    r = pathlib.Path(ruta)
    if ancho:
        import io
        from PIL import Image
        im = Image.open(r).convert('RGB')
        im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, 'JPEG', quality=86)
        return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    return 'data:image/png;base64,' + base64.b64encode(r.read_bytes()).decode()


def muestras(carpeta, n=None):
    fs = sorted(pathlib.Path(RAIZ / carpeta).glob('*.png'))[:n]
    return ''.join(f'<figure><img src="{uri(f, 400)}"><figcaption>{f.stem}</figcaption></figure>'
                   for f in fs)


def html():
    aprobadas = muestras('piezas-aprobadas')
    tanda2 = muestras('piezas-aprobadas/tanda-02-imagenes')
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/tokens/tokens.css">
<style>
  @page {{ size: 210mm 297mm; margin: 0; }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:var(--font-body);color:var(--dark);background:var(--light)}}

  .hoja{{width:210mm;height:297mm;padding:22mm 20mm;position:relative;
    page-break-after:always;overflow:hidden}}
  .hoja:last-child{{page-break-after:auto}}
  .folio{{position:absolute;left:20mm;right:20mm;bottom:12mm;display:flex;
    justify-content:space-between;font-family:var(--font-heading);
    font-weight:600;font-size:8pt;color:var(--muted);
    border-top:1px solid var(--light-gray);padding-top:3mm}}

  h1{{font-family:var(--font-titular);font-weight:600;font-size:34pt;
    line-height:1.08;letter-spacing:-.015em}}
  h2{{font-family:var(--font-titular);font-weight:600;font-size:19pt;
    margin:9mm 0 3mm;line-height:1.15}}
  h2:first-of-type{{margin-top:0}}
  h3{{font-family:var(--font-heading);font-weight:700;font-size:10.5pt;
    margin:6mm 0 2mm}}
  p,li{{font-size:10pt;line-height:1.5;margin-bottom:2.6mm}}
  ul,ol{{padding-left:5mm}}
  li{{margin-bottom:1.6mm}}
  b,strong{{font-family:var(--font-heading);font-weight:700}}
  code{{font-family:var(--font-mono);font-size:9pt;background:var(--light-gray);
    padding:.4mm 1.2mm;border-radius:1mm}}
  pre{{font-family:var(--font-mono);font-size:8.6pt;line-height:1.45;
    background:#2b2a27;color:var(--light);padding:4mm 5mm;border-radius:2mm;
    margin:3mm 0;white-space:pre-wrap}}
  pre b{{color:var(--orange);font-family:var(--font-mono);font-weight:400}}

  .rotulo{{font-family:var(--font-heading);font-weight:600;font-size:8.5pt;
    letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}
  .clave{{border-left:3px solid var(--orange);padding-left:4mm;margin:4mm 0}}
  .clave p{{margin-bottom:0}}

  table{{width:100%;border-collapse:collapse;margin:3mm 0;font-size:9pt}}
  th{{font-family:var(--font-heading);font-weight:700;font-size:8.5pt;
    text-align:left;border-bottom:1.5px solid var(--dark);padding:2mm 2mm 1.6mm 0}}
  td{{border-bottom:1px solid var(--light-gray);padding:2mm 2mm 2mm 0;
    vertical-align:top;line-height:1.4}}

  .rejilla{{display:grid;grid-template-columns:repeat(5,1fr);gap:2.6mm;margin:3mm 0}}
  /* Las diez de la tanda 02 en una sola fila: en dos filas de cinco la pagina
     se pasaba 102 px del alto util y la ultima seccion caia a la pagina
     siguiente. Aqui la miniatura es indice visual, no lamina. */
  .rejilla.diez{{grid-template-columns:repeat(10,1fr);gap:1.6mm}}
  .rejilla.diez figcaption{{font-size:5.2pt;letter-spacing:0}}
  .rejilla figure img{{width:100%;display:block;border-radius:1mm}}
  .rejilla figcaption{{font-family:var(--font-mono);font-size:6.6pt;
    color:var(--muted);margin-top:1mm}}

  .portada{{background:var(--dark);color:var(--light);display:flex;
    flex-direction:column;justify-content:space-between}}
  .portada h1{{font-size:44pt;color:var(--light)}}
  .portada .rotulo{{color:rgba(250,249,245,.7)}}
  .portada p{{font-size:12pt;color:rgba(250,249,245,.88);max-width:34ch}}
  .portada .lock img{{width:58mm;display:block}}
</style></head><body>

<!-- ============ 1 · PORTADA ============ -->
<section class="hoja portada">
  <div><div class="rotulo">Sistema de marca · ClaudeTec</div></div>
  <div>
    <h1>Cómo se<br>hace un post</h1>
    <p style="margin-top:6mm">Manual de la skill <code style="background:none;color:var(--orange)">anthro-pic-brand</code>
    y de cómo encaja con las dos skills de animación.</p>
  </div>
  <div class="lock"><img src="{uri(RAIZ / 'assets/logos-claudetec/claudetec--claro.png')}"></div>
</section>

<!-- ============ 2 · QUE ES Y DONDE CORRE ============ -->
<section class="hoja">
  <div class="rotulo">1</div>
  <h2>Qué es esto y qué no</h2>
  <p>Tres skills se reparten el trabajo de diseño. Ninguna hace lo de la otra.</p>
  <table>
    <tr><th style="width:32%">Skill</th><th>Hace</th></tr>
    <tr><td><b>anthro-pic-brand</b></td><td>Compone piezas: paleta, tipografía, capas, fondos, medición. Es de donde sale el post</td></tr>
    <tr><td><b>clawd-animaciones</b></td><td><b>Genera</b> animaciones de Clawd en pixel art y labels de carga</td></tr>
    <tr><td><b>clawd-biblioteca</b></td><td><b>Almacena y entrega</b> lo ya terminado. Su <code>CATALOGO.md</code> manda</td></tr>
  </table>
  <div class="clave"><p><b>La skill de marca no anima: consume.</b> Cuando una pieza
  necesita a Clawd moviéndose, lo pide a la biblioteca por su puente. Si la
  animación no existe, se encarga a <code>clawd-animaciones</code>, que la deja
  en la biblioteca — y entonces la pieza la usa.</p></div>
  <pre>from clawd_biblioteca import pieza
gif = pieza(<b>'paseo'</b>, <b>'transparente'</b>)      # el GIF con alfa
f62 = pieza(<b>'paseo'</b>, <b>'fotograma'</b>, 62)     # un cuadro suelto</pre>
  <p>El puente busca la biblioteca en varias rutas y, si no está instalada, dice
  qué skill falta en vez de fallar con un error de archivo.</p>

  <h2>Dónde corre</h2>
  <p>Tres sitios, y no son iguales. Lo primero al abrir la skill en uno nuevo:</p>
  <pre>python3 scripts/entorno.py</pre>
  <table>
    <tr><th style="width:36%"></th><th>Code / desktop</th><th>claude.ai web</th></tr>
    <tr><td>HTML de la pieza</td><td>Sí</td><td>Sí, siempre</td></tr>
    <tr><td>PNG y PDF</td><td>Sí</td><td>Solo con Chromium</td></tr>
    <tr><td>MP4 y GIF</td><td>Sí</td><td>Solo con ffmpeg</td></tr>
    <tr><td>Medir la pieza</td><td>Sí</td><td>Necesita numpy y scipy</td></tr>
    <tr><td>Escribir en la skill</td><td>Sí</td><td><b>No</b>, es efímero</td></tr>
  </table>
  <p><b>Sin Chromium la pieza igual se entrega.</b> Todas llevan los assets
  embebidos en <code>data:</code> URI, así que el HTML se abre y se captura en
  cualquier navegador. Lo que no se puede es medirla — y eso se dice, no se
  disimula.</p>
  <div class="folio"><span>Manual · anthro-pic-brand</span><span>1</span></div>
</section>

<!-- ============ 3 · COMO SE HACE UN POST ============ -->
<section class="hoja">
  <div class="rotulo">2</div>
  <h2>Cómo se hace un post</h2>
  <p>No hay plantillas que rellenar. Cada pieza es un HTML que escribe un script
  sobre cuatro hojas de estilo compartidas. El marco canónico son cuatro líneas:</p>
  <pre>&lt;link rel="stylesheet" href="../assets/templates/_base.css"&gt;
&lt;link rel="stylesheet" href="../assets/templates/capas.css"&gt;
&lt;link rel="stylesheet" href="../assets/templates/fondos-color.css"&gt;
&lt;style&gt;.pieza{{width:1080px;height:1350px;position:relative}}&lt;/style&gt;</pre>

  <h3>Los cinco pasos</h3>
  <ol>
    <li><b>Medida.</b> Por defecto <b>1080 × 1350</b> (4:5). Story y reel,
    1080 × 1920. En un carrusel todas las láminas van a la misma proporción.</li>
    <li><b>Fondo.</b> Uno de los colores principales —celeste, verde claro, lila,
    crema— y, si hace falta, una de las once tramas. Fondo oscuro solo si se pide.</li>
    <li><b>Capas.</b> Dos o tres: fondo, una cinta o una foto, y una tarjeta o
    ventana encima. Una sola capa es el modo de fallo de este sistema.</li>
    <li><b>Texto.</b> Titular en serif; Poppins solo en etiquetas y datos; Lora
    en cuerpo. Las dos pixel, solo si la pieza habla de terminal o de producto.</li>
    <li><b>Medir.</b> <code>python3 scripts/validar.py pieza.png</code> y
    comprobar el hueco máximo. Esto no es opcional.</li>
  </ol>

  <h3>El número que manda</h3>
  <div class="clave"><p><b>Ningún hueco vacío de más de 180 px</b> en una pieza
  de 1080 × 1350.</p></div>
  <p>Es el único umbral que separa limpiamente lo que Ramses aprobó de lo que
  rechazó: ninguna aprobada pasa de 171 px, ninguna rechazada por acomodo baja de
  251. Si sobra sitio, crece la tipografía, baja el objeto o entra una capa. No se
  deja el hueco. Lo mide <code>scripts/analizar_referencia.py</code> como
  <code>aire_max</code>.</p>
  <p>Dos cosas que <b>no</b> son el criterio: la densidad —hay piezas vacías
  buenas y piezas llenas buenas— y el número de ejes de alineación por sí solo.</p>

  <h3>Si la pieza lleva animación</h3>
  <p>El entregable es <b>MP4</b>. Salen los tres: <code>.mp4</code> para
  Instagram, <code>.gif</code> para chat y el <code>.png</code> del último
  fotograma, que es literalmente un cuadro del vídeo y no un montaje aparte.</p>
  <div class="folio"><span>Manual · anthro-pic-brand</span><span>2</span></div>
</section>

<!-- ============ 4 · QUE FUNCIONA ============ -->
<section class="hoja">
  <div class="rotulo">3</div>
  <h2>Qué funciona, con evidencia</h2>
  <p>Cada veredicto se anota con sus medidas y <b>su motivo</b> en
  <code>references/veredictos.md</code>. La regla de los 180 px salió de comparar
  esa tabla, no de mirar las piezas.</p>

  <h3>Aprobadas sin correcciones</h3>
  <div class="rejilla">{aprobadas}</div>
  <p style="font-size:9pt">Foto de contexto atenuada con otra nítida encima ·
  ficha solapando la esquina · foto a sangre con velo · lienzo partido en dos ·
  par de fotos con ficha.</p>

  <h3>Diez geometrías distintas, revisadas</h3>
  <div class="rejilla diez">{tanda2}</div>
  <p style="font-size:9pt">Retícula irregular · corte diagonal · cuarto de
  círculo · columna a sangre · la foto dentro de una ventana · cita partida por
  una banda de foto · cifra en pixel con franja de datos · tira de cuatro ·
  índice con la foto de ancla · tarjeta pixel con Clawd caminando encima.</p>

  <h3>Cinco motivos de rechazo que no tienen número</h3>
  <ol>
    <li><b>Todas las piezas de la tanda comparten esqueleto.</b> Rótulo, titular,
    un objeto centrado, nota, pie, repetido cinco veces.</li>
    <li><b>El texto de terminal, pequeño.</b> Mínimo 40 px y cinco líneas
    contadas; leer monoespaciada de 29 px sobre negro da pereza.</li>
    <li><b>La foto no habla de lo que dice el texto.</b> Y si la foto trae
    letras, mete una segunda marca en la pieza. Antes de colocarla, leerla.</li>
    <li><b>Firmar una voz con algo que no es una voz.</b> Si el material no da
    caras, la cita se firma con texto, no con una ficha disimulada.</li>
    <li><b>Una ventana centrada con hueco debajo.</b> Va desplazada y sangrando
    por un borde.</li>
  </ol>
  <div class="folio"><span>Manual · anthro-pic-brand</span><span>3</span></div>
</section>

<!-- ============ 5 · REGLAS Y MANTENIMIENTO ============ -->
<section class="hoja">
  <div class="rotulo">4</div>
  <div class="clave" style="margin-top:0"><p>De una referencia se copia <b>el
  número</b>, no el acomodo: cuántas capas, cuánto aire, qué fracción de tinta es
  imagen. El acomodo se inventa cada vez.</p></div>
  <h2 style="margin-top:7mm">Las reglas que no se rompen</h2>
  <ul>
    <li>Un solo <b>acento dominante</b> por pieza. El naranja es el default.</li>
    <li>Máximo contraste: <code>#141413</code> sobre <code>#faf9f5</code>, o al revés.</li>
    <li>Los fondos claros —celeste, verde claro, lila— <b>solo aguantan texto
    oscuro</b>. Para texto blanco están los tonos medios.</li>
    <li>Nada de degradados de dos tintas, glow ni esquinas muy redondeadas. Velo
    de un hex, duotono, semitono y grano sí.</li>
    <li><b>Excepción aprobada:</b> una tarjeta o una ventana que flota lleva
    sombra, o no se lee como capa. Acotada a dos tokens.</li>
    <li>«ClaudeTec» <b>nunca se escribe como texto</b>: va el SVG del lockup.</li>
    <li>El aviso de que no es una activación oficial de Anthropic solo si lo
    piden, y en la última lámina.</li>
  </ul>

  <h2>Antes de entregar</h2>
  <pre>python3 scripts/entorno.py      <b>qué se puede hacer aquí</b>
python3 scripts/validar.py pieza.png
python3 scripts/enlaces.py      <b>ninguna ruta rota</b></pre>
  <p><code>enlaces.py</code> existe porque renombrar una carpeta a mano rompió
  diez archivos <b>sin dar un solo error</b>: los scripts seguían escribiendo su
  HTML, el navegador no encontraba el SVG y las piezas habrían salido con un
  hueco donde va el logo.</p>

  <h2>Dónde está cada cosa</h2>
  <table>
    <tr><th style="width:42%">Si buscas…</th><th>Abre</th></tr>
    <tr><td>Componer, capas, ventanas, collage</td><td><code>references/capas.md</code></td></tr>
    <tr><td>Qué aprobó y qué rechazó Ramses</td><td><code>references/veredictos.md</code></td></tr>
    <tr><td>Qué es ClaudeTec y cómo se le habla</td><td><code>references/claudetec.md</code></td></tr>
    <tr><td>Elegir un gráfico o un fondo</td><td><code>references/assets-index.md</code>, <code>fondos-color.css</code></td></tr>
    <tr><td>Antes de rehacer algo ya intentado</td><td><code>references/reglas-derivadas.md</code></td></tr>
    <tr><td>Qué hace cada script</td><td><code>references/scripts.md</code></td></tr>
    <tr><td>Qué falta por decidir</td><td><code>PENDIENTES.md</code></td></tr>
  </table>
  <div class="clave"><p>La skill que se entrega <b>no incluye</b>
  <code>salida/</code>: eso es trabajo producido, no la herramienta. Se empaqueta
  con <code>-x '*/salida/*'</code>.</p></div>
  <div class="folio"><span>Manual · anthro-pic-brand</span><span>4</span></div>
</section>
</body></html>"""


def main():
    if any(a in ('-h', '--help') for a in sys.argv[1:]):
        print(__doc__)
        return
    f = SALIDA / 'manual-anthro-pic-brand.html'
    f.write_text(html(), encoding='utf-8')
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pg = nav.new_page(viewport={'width': 1240, 'height': 1754})
        fallos = []
        pg.on('requestfailed', lambda r: fallos.append(r.url.split('/')[-1]))
        pg.goto(f.resolve().as_uri())
        pg.wait_for_timeout(1200)
        pg.pdf(path=str(PDF), format='A4', print_background=True,
               margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        hojas = pg.locator('.hoja').count()
        altos = pg.evaluate('''() => [...document.querySelectorAll('.hoja')].map(h => {
            const ultimo = [...h.children].filter(c => !c.classList.contains('folio')).pop();
            return Math.round(ultimo.getBoundingClientRect().bottom
                              - h.getBoundingClientRect().top);
        })''')
        limite = pg.evaluate("() => document.querySelector('.hoja').clientHeight")
        nav.close()
    print('fallos de carga:', fallos or 'ninguno')
    print(f'{PDF.name}: {hojas} páginas · {PDF.stat().st_size / 1e6:.2f} MB')
    tope = limite - 60          # deja sitio al folio
    for i, alto in enumerate(altos, 1):
        aviso = f'  <-- SE PASA POR {alto - tope}px' if alto > tope else ''
        print(f'  página {i}: contenido {alto} / {tope}{aviso}')


if __name__ == '__main__':
    main()
