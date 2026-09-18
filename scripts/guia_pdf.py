#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arma la guia de uso de las tres skills en PDF.

    python3 scripts/guia_pdf.py

Sale `salida/guia-tres-skills.pdf`: como se instala, como se pide una pieza y
como se hablan `anthro-pic-brand`, `clawd-animaciones` y `clawd-biblioteca`.

QUE LA DIFERENCIA DE `manual_pdf.py`
  El manual ensena a COMPONER: geometrias, recursos, veredictos, con muestras de
  piezas reales. Esta guia ensena a USAR el conjunto: que se instala donde, en
  que orden se piden las cosas y por donde se hablan las tres skills.

  Consecuencia practica: esta guia **no abre `piezas-aprobadas/`**, y por eso se
  puede armar desde un clon limpio de `main` —donde esa carpeta ya no esta, vive
  en la rama `piezas`—. El manual si las necesita.

  Es la que se manda junto con el ZIP a quien va a instalar la skill.
"""
import base64
import pathlib

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'salida'
PDF = SALIDA / 'guia-tres-skills.pdf'


def uri(ruta):
    """Los assets van empotrados: el PDF tiene que viajar por WhatsApp solo."""
    r = pathlib.Path(ruta)
    tipo = 'image/svg+xml' if r.suffix == '.svg' else 'image/png'
    return f'data:{tipo};base64,' + base64.b64encode(r.read_bytes()).decode()


def html():
    logo = uri(RAIZ / 'assets/logos-claudetec/claudetec--claro.png')
    clawd = uri(RAIZ / 'assets/clawd/clawd-base.png')
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
    margin:8mm 0 3mm;line-height:1.15}}
  h2:first-of-type{{margin-top:0}}
  h3{{font-family:var(--font-heading);font-weight:700;font-size:10.5pt;
    margin:4mm 0 2mm}}
  p,li{{font-size:10pt;line-height:1.5;margin-bottom:2.4mm}}
  ul,ol{{padding-left:5mm}}
  li{{margin-bottom:1.5mm}}
  b,strong{{font-family:var(--font-heading);font-weight:700}}
  code{{font-family:var(--font-mono);font-size:9pt;background:var(--light-gray);
    padding:.4mm 1.2mm;border-radius:1mm}}
  pre{{font-family:var(--font-mono);font-size:8.4pt;line-height:1.45;
    background:#2b2a27;color:var(--light);padding:4mm 5mm;border-radius:2mm;
    margin:3mm 0;white-space:pre-wrap}}
  pre b{{color:var(--orange);font-family:var(--font-mono);font-weight:400}}
  pre i{{color:var(--mid-gray);font-style:normal}}

  .rotulo{{font-family:var(--font-heading);font-weight:600;font-size:8.5pt;
    letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}
  .clave{{border-left:3px solid var(--orange);padding-left:4mm;margin:3mm 0}}
  .clave p{{margin-bottom:0}}

  table{{width:100%;border-collapse:collapse;margin:3mm 0;font-size:9pt}}
  th{{font-family:var(--font-heading);font-weight:700;font-size:8.5pt;
    text-align:left;border-bottom:1.5px solid var(--dark);padding:2mm 2mm 1.6mm 0}}
  td{{border-bottom:1px solid var(--light-gray);padding:2mm 2mm 2mm 0;
    vertical-align:top;line-height:1.4}}

  /* El diagrama de las tres skills se dibuja con cajas, no con una imagen: asi
     se corrige editando texto y no vuelve a quedar desfasado del hecho. */
  .mapa{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;margin:3mm 0 2mm}}
  .caja{{border:1.5px solid var(--dark);border-radius:2mm;padding:4mm;
    display:flex;flex-direction:column;gap:2mm}}
  .caja.marca{{background:var(--orange);color:var(--light);border-color:var(--orange)}}
  .caja .n{{font-family:var(--font-mono);font-size:8.4pt;font-weight:700}}
  .caja .q{{font-size:8.6pt;line-height:1.35;margin:0}}
  .flechas{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;
    font-family:var(--font-heading);font-weight:600;font-size:7.4pt;
    color:var(--muted);text-align:center}}

  .portada{{background:var(--dark);color:var(--light);display:flex;
    flex-direction:column;justify-content:space-between}}
  .portada h1{{font-size:44pt;color:var(--light)}}
  .portada p{{font-size:12pt;color:rgba(250,249,245,.88);max-width:36ch}}
  .portada .rotulo{{color:rgba(250,249,245,.7)}}
  .portada .lock img{{width:58mm;display:block}}
  .portada .titulo{{margin-top:auto;margin-bottom:14mm}}
  .portada .bicho{{position:absolute;right:18mm;top:30mm;width:34mm;
    image-rendering:pixelated;opacity:.92}}
  /* La portada dejaba 86 mm muertos entre el subtitulo y el logo. El indice los
     ocupa y ademas dice de que va el documento, que es mejor que un hueco. */
  .indice{{display:flex;flex-direction:column;gap:0;margin-bottom:10mm}}
  .indice div{{display:flex;gap:5mm;font-size:9.5pt;
    color:rgba(250,249,245,.82);padding:2.6mm 0;
    border-top:1px solid rgba(250,249,245,.18)}}
  .indice div:last-child{{border-bottom:1px solid rgba(250,249,245,.18)}}
  .indice span{{font-family:var(--font-mono);font-size:8.4pt;
    color:var(--orange);padding-top:.6mm}}
</style></head><body>

<!-- ============ 1 - PORTADA ============ -->
<section class="hoja portada">
  <div><div class="rotulo">ClaudeTec &middot; Tec de Monterrey</div></div>
  <img class="bicho" src="{clawd}">
  <div class="titulo">
    <h1>Tres skills,<br>un sistema</h1>
    <p style="margin-top:6mm">C&oacute;mo se instalan, c&oacute;mo se pide una pieza y por
    d&oacute;nde se hablan <code style="background:none;color:var(--orange)">anthro-pic-brand</code>,
    <code style="background:none;color:var(--orange)">clawd-animaciones</code> y
    <code style="background:none;color:var(--orange)">clawd-biblioteca</code>.</p>
  </div>
  <div>
    <div class="indice">
      <div><span>1</span>Qui&eacute;n hace qu&eacute;, y por d&oacute;nde se hablan las tres</div>
      <div><span>2</span>C&oacute;mo se instalan, y qu&eacute; hace falta tener</div>
      <div><span>3</span>C&oacute;mo se pide una pieza</div>
      <div><span>4</span>Cu&aacute;ndo entra Clawd, y c&oacute;mo</div>
      <div><span>5</span>D&oacute;nde queda guardado qu&eacute;, y si algo falla</div>
    </div>
    <div class="lock"><img src="{logo}"></div>
  </div>
</section>

<!-- ============ 2 - EL MAPA ============ -->
<section class="hoja">
  <div class="rotulo">1</div>
  <h2>Qui&eacute;n hace qu&eacute;</h2>
  <p>Tres skills se reparten el trabajo y <b>ninguna hace lo de la otra</b>. Si
  una hace el trabajo de la vecina, deja de haber una sola fuente de verdad.</p>

  <div class="mapa">
    <div class="caja marca">
      <div class="n">anthro-pic-brand</div>
      <p class="q"><b>Compone.</b> Paleta, tipograf&iacute;a, capas, fondos, fotos y la
      medici&oacute;n de la pieza. De aqu&iacute; sale el post.</p>
    </div>
    <div class="caja">
      <div class="n">clawd-animaciones</div>
      <p class="q"><b>Genera.</b> Pixel art de Clawd por fotogramas y labels de
      carga. No guarda nada terminado.</p>
    </div>
    <div class="caja">
      <div class="n">clawd-biblioteca</div>
      <p class="q"><b>Almacena y entrega.</b> Lo ya hecho, en GIF, WebP, MP4, SVG
      y bloque HTML. No dibuja.</p>
    </div>
  </div>
  <div class="flechas">
    <div>pide una animaci&oacute;n &rarr;</div>
    <div>escribe lo generado &rarr;</div>
    <div>&larr; entrega el archivo</div>
  </div>

  <div class="clave"><p><b>La skill de marca no anima: consume.</b> Cuando una
  pieza necesita a Clawd movi&eacute;ndose, lo pide a la biblioteca. Si no existe, se
  encarga a <code>clawd-animaciones</code>, que lo deja en la biblioteca &mdash; y
  entonces la pieza lo usa.</p></div>

  <h3>El puente, en c&oacute;digo</h3>
  <p>Las dos skills de Clawd se ven desde la de marca por un solo archivo,
  <code>scripts/clawd_biblioteca.py</code>. Si la biblioteca no est&aacute; instalada,
  dice qu&eacute; skill falta en vez de reventar con un error de archivo:</p>
  <pre>from clawd_biblioteca import pieza
gif = pieza(<b>'paseo'</b>, <b>'transparente'</b>)      <i># el GIF con alfa</i>
f62 = pieza(<b>'paseo'</b>, <b>'fotograma'</b>, 62)     <i># un cuadro suelto</i></pre>

  <h3>D&oacute;nde vive cada una</h3>
  <table>
    <tr><th style="width:32%">Skill</th><th>Carpeta</th><th style="width:28%">Repositorio</th></tr>
    <tr><td><b>anthro-pic-brand</b></td><td><code>Desktop\\anthro-pic-brand</code></td><td>privado: <code>main</code> + rama <code>piezas</code></td></tr>
    <tr><td><b>clawd-animaciones</b></td><td><code>Desktop\\Animaciones - Clawd</code></td><td>privado</td></tr>
    <tr><td><b>clawd-biblioteca</b></td><td><code>Desktop\\Clawd - Biblioteca</code></td><td>privado</td></tr>
  </table>
  <p>Los tres repositorios est&aacute;n en <code>github.com/ramydominguezc-lgtm</code>.
  Son <b>tres y no uno</b> porque las skills se instalan por separado: juntarlas
  obligar&iacute;a a mover carpetas y rehacer los enlaces cada vez.</p>

  <h3>A cu&aacute;l le pido qu&eacute;</h3>
  <table>
    <tr><th style="width:54%">Lo que quieres</th><th>Con cu&aacute;l empiezas</th></tr>
    <tr><td>Un post, un flyer, un carrusel, una portada</td><td><b>anthro-pic-brand</b></td></tr>
    <tr><td>Una pieza con Clawd movi&eacute;ndose</td><td><b>anthro-pic-brand</b>; ella pide la animaci&oacute;n</td></tr>
    <tr><td>Un GIF de Clawd suelto, para WhatsApp o Notion</td><td><b>clawd-biblioteca</b></td></tr>
    <tr><td>Una animaci&oacute;n nueva, u otra versi&oacute;n de una que ya hay</td><td><b>clawd-animaciones</b></td></tr>
  </table>
  <div class="folio"><span>Gu&iacute;a &middot; tres skills</span><span>1</span></div>
</section>

<!-- ============ 3 - INSTALAR ============ -->
<section class="hoja">
  <div class="rotulo">2</div>
  <h2>C&oacute;mo se instalan</h2>
  <p>Hay dos formas y dependen de d&oacute;nde vayas a trabajar.</p>

  <h3>En Claude Code, en la PC</h3>
  <p>No se copia nada: se enlaza la carpeta real, as&iacute; no hay dos versiones que
  se desincronicen. En Windows, una vez por skill:</p>
  <pre>mklink /J "%USERPROFILE%\\.claude\\skills\\anthro-pic-brand" ^
          "%USERPROFILE%\\OneDrive\\Desktop\\anthro-pic-brand"</pre>
  <p>Y lo mismo para <code>clawd-animaciones</code> y <code>clawd-biblioteca</code>
  apuntando a sus carpetas. Lo que edites en el escritorio es lo que ve Claude.</p>

  <h3>En claude.ai web o en la app de escritorio</h3>
  <p>Ah&iacute; se sube un ZIP, en <b>Configuraci&oacute;n &rarr; Capacidades &rarr; Skills</b>. El
  de la skill de marca se arma solo:</p>
  <pre>python3 scripts/empaquetar.py</pre>
  <p>Deja el ZIP en el escritorio, comprueba el tope de <b>200 archivos</b> que
  admite una skill y verifica que ninguna ruta citada apunte al vac&iacute;o.
  <b>Se niega a escribir</b> si algo no cuadra, en vez de dejar un ZIP que sale a
  publicar con un hueco donde iba el logo.</p>
  <div class="clave"><p>En la web las skills son de <b>solo lectura</b>. Lo que
  Claude genere ah&iacute; no se guarda en la skill: hay que descargarlo. Para que algo
  quede, se trabaja en Claude Code o se vuelve a subir el ZIP.</p></div>

  <h3>Qu&eacute; hace falta tener instalado</h3>
  <pre>pip install playwright pillow numpy scipy
python3 -m playwright install chromium</pre>
  <table>
    <tr><th style="width:36%"></th><th>Code / escritorio</th><th>claude.ai web</th></tr>
    <tr><td>HTML de la pieza</td><td>S&iacute;</td><td>S&iacute;, siempre</td></tr>
    <tr><td>PNG y PDF</td><td>S&iacute;</td><td>Solo con Chromium</td></tr>
    <tr><td>MP4 y GIF</td><td>S&iacute;</td><td>Solo con ffmpeg</td></tr>
    <tr><td>Medir la pieza</td><td>S&iacute;</td><td>Necesita numpy y scipy</td></tr>
    <tr><td>Escribir en la skill</td><td>S&iacute;</td><td><b>No</b>, es ef&iacute;mero</td></tr>
  </table>
  <p>Para saber qu&eacute; hay antes de prometer nada, lo primero al abrir la skill en
  un sitio nuevo: <code>python3 scripts/entorno.py</code></p>
  <p><b>Sin Chromium la pieza igual se entrega.</b> Todas llevan los assets
  empotrados en <code>data:</code> URI, as&iacute; que el HTML se abre y se captura en
  cualquier navegador. Lo que no se puede es medirla &mdash; y eso se avisa, no se
  disimula.</p>
  <div class="folio"><span>Gu&iacute;a &middot; tres skills</span><span>2</span></div>
</section>

<!-- ============ 4 - PEDIR UNA PIEZA ============ -->
<section class="hoja">
  <div class="rotulo">3</div>
  <h2>C&oacute;mo se pide una pieza</h2>
  <p>No hay formulario: el encargo se escribe en una frase. Pero <b>cuatro cosas
  cambian el resultado</b> y conviene decirlas siempre.</p>
  <table>
    <tr><th style="width:24%">Qu&eacute;</th><th>Por qu&eacute; importa</th></tr>
    <tr><td><b>De qu&eacute; habla</b></td><td>El texto exacto que va en la pieza. Si no lo das, sale texto de relleno que habr&aacute; que cambiar</td></tr>
    <tr><td><b>D&oacute;nde se publica</b></td><td>Post 1080&times;1350, story 1080&times;1920, carrusel, slide. Decide la proporci&oacute;n y cu&aacute;nto texto cabe</td></tr>
    <tr><td><b>Si se va a reeditar</b></td><td>Si el equipo le va a cambiar la fecha despu&eacute;s, <b>tiene que nacer en Canva</b>. Una imagen exportada es un callej&oacute;n sin salida</td></tr>
    <tr><td><b>Si lleva foto</b></td><td>Cu&aacute;l. Y si no hay, se dice: se compone sin foto antes que con una que no hable del tema</td></tr>
  </table>

  <h3>Qu&eacute; pasa por dentro</h3>
  <ol>
    <li><b>Medida.</b> Por defecto 1080 &times; 1350. En un carrusel, todas las
    l&aacute;minas a la misma proporci&oacute;n.</li>
    <li><b>Fondo.</b> Uno de los colores principales y, si hace falta, una trama.
    Fondo oscuro solo si se pide.</li>
    <li><b>Capas.</b> Dos o tres: fondo, una cinta o una foto, y una tarjeta o
    ventana encima. <b>Una sola capa es el modo de fallo de este sistema</b>: la
    pieza sale correcta y plana.</li>
    <li><b>Texto.</b> Titular en serif; Poppins solo en etiquetas y datos; Lora
    en cuerpo. La pixel, solo si la pieza habla de terminal o de producto.</li>
    <li><b>Medir.</b> <code>python3 scripts/validar.py pieza.png</code>. No es
    opcional.</li>
  </ol>

  <h3>El n&uacute;mero que manda</h3>
  <div class="clave"><p><b>Ning&uacute;n hueco vac&iacute;o de m&aacute;s de 180 px</b> en una pieza
  de 1080 &times; 1350.</p></div>
  <p>Es el &uacute;nico umbral que separa limpiamente lo aprobado de lo rechazado:
  ninguna aprobada pasa de <b>177 px</b>, ninguna rechazada por acomodo baja de
  <b>251</b>. Si sobra sitio, crece la tipograf&iacute;a, baja el objeto o entra una
  capa. No se deja el hueco.</p>
  <p>Las medidas y el motivo de cada veredicto est&aacute;n en
  <code>references/veredictos.md</code>, una fila por pieza. <b>Eso es lo que se
  lee al componer, no las im&aacute;genes</b>: mirar un PNG cuesta unos 1,900 tokens y
  la tabla entera cuesta 700.</p>

  <h3>Un encargo que funciona</h3>
  <pre>Post de Instagram para la convocatoria de nuevos miembros.
Titular: <b>"Entra al club"</b>. Bajada: cierre de registro el
<b>30 de septiembre</b>, cupo de 40 lugares. Va el logo de ClaudeTec.
Foto: la del taller de agosto. <b>Lo va a reeditar el equipo.</b></pre>
  <p>Cuatro l&iacute;neas y est&aacute;n las cuatro decisiones: qu&eacute; dice, d&oacute;nde va, si lleva
  foto y si se va a reeditar &mdash;esto &uacute;ltimo manda la pieza a Canva en vez de a un
  PNG&mdash;. Lo que no se diga, se decide sin ti.</p>
  <div class="folio"><span>Gu&iacute;a &middot; tres skills</span><span>3</span></div>
</section>

<!-- ============ 5 - CUANDO ENTRA CLAWD ============ -->
<section class="hoja">
  <div class="rotulo">4</div>
  <h2>Cu&aacute;ndo entra Clawd, y c&oacute;mo</h2>
  <p>Clawd es <b>registro informal</b>: comunidad, merch, bienvenidas. No va en
  material institucional, no va junto al wordmark y <b>no sustituye al logo</b>.
  Dentro de esos l&iacute;mites, se anima.</p>

  <h3>El orden, que no se salta</h3>
  <ol>
    <li><b>Mirar el cat&aacute;logo primero.</b> <code>CATALOGO.md</code> de
    <code>clawd-biblioteca</code>, una fila por animaci&oacute;n. Hoy hay
    <code>caminando</code>, <code>saltando</code>, <code>confeti</code>,
    <code>paseo</code>, <code>paseo-arriba</code>, <code>pesas</code>,
    <code>bandera</code> y los labels de carga.</li>
    <li><b>Si existe, se entrega.</b> Y no se gasta nada m&aacute;s.</li>
    <li><b>Si no existe o hay que cambiarla</b> &mdash;otro tama&ntilde;o, otro fondo, otro
    ritmo&mdash;, se encarga a <code>clawd-animaciones</code>. <b>No se edita a mano en
    la biblioteca.</b></li>
  </ol>
  <div class="clave"><p>Clawd se anima <b>por cuadros, no por interpolaci&oacute;n</b>:
  entre dos formas de pixel art no hay tween posible. Por eso la receta est&aacute; en
  el generador y los archivos en la biblioteca &mdash; regenerar es barato, editar un
  GIF a mano no tiene vuelta atr&aacute;s.</p></div>

  <h3>Qu&eacute; archivo seg&uacute;n d&oacute;nde va</h3>
  <table>
    <tr><th style="width:46%">Destino</th><th>Archivo</th></tr>
    <tr><td>Web, landing</td><td><code>&lt;n&gt;.webp</code> &mdash; alfa real</td></tr>
    <tr><td>WhatsApp, correo, Notion</td><td><code>&lt;n&gt;.gif</code> &mdash; fondo crema horneado</td></tr>
    <tr><td>Fondo claro que no es crema</td><td><code>&lt;n&gt;-transparente.gif</code></td></tr>
    <tr><td>Reel, story, post de Instagram</td><td><code>&lt;n&gt;.mp4</code></td></tr>
    <tr><td>Canvas, artifact, Claude Design</td><td><code>&lt;n&gt;-bloque.html</code> &mdash; aut&oacute;nomo</td></tr>
    <tr><td>Una pose suelta</td><td><code>svg/&lt;n&gt;-&lt;pose&gt;.svg</code></td></tr>
  </table>

  <h3>D&oacute;nde ponerlo dentro de la pieza</h3>
  <p>Cualquier ventana sirve de repisa: el canto de una terminal, el borde de una
  tarjeta, el marco de un navegador. Dos reglas que salieron de hacerlo mal:</p>
  <ul>
    <li><b>Nunca por debajo de ~170 px de alto.</b> M&aacute;s peque&ntilde;o, Clawd deja de
    leerse como un personaje y se ve como una silueta recortada.</li>
    <li><b>Si no cabe, se mueve la caja, no se encoge a Clawd.</b> El texto de la
    ventana se aparta; la animaci&oacute;n mantiene su tama&ntilde;o.</li>
  </ul>
  <div class="clave"><p><b>Aviso entre skills:</b> la pieza <code>10-pixel</code>
  de la skill de marca usa <code>paseo</code>, en PNG fijo y en MP4. Regenerar
  <code>paseo</code> cambia esa pieza. Avisar antes.</p></div>
  <div class="folio"><span>Gu&iacute;a &middot; tres skills</span><span>4</span></div>
</section>

<!-- ============ 6 - MANTENIMIENTO ============ -->
<section class="hoja">
  <div class="rotulo">5</div>
  <h2>D&oacute;nde queda guardado qu&eacute;</h2>
  <p>Tres destinos con tres trabajos distintos. Confundirlos es lo que llenaba el
  paquete de material que nadie abr&iacute;a.</p>
  <table>
    <tr><th style="width:24%"></th><th>Qu&eacute; es</th><th style="width:22%">Qu&eacute; lleva</th></tr>
    <tr><td><b>rama <code>main</code></b></td><td>La skill. Lo que se lee al componer: <code>SKILL.md</code>, <code>references/</code>, <code>scripts/</code>, <code>assets/</code></td><td>176 archivos</td></tr>
    <tr><td><b>rama <code>piezas</code></b></td><td>El archivo visual: las piezas aprobadas y la inspiraci&oacute;n. La evidencia detr&aacute;s de las reglas</td><td>51 archivos</td></tr>
    <tr><td><b>El ZIP</b></td><td>La herramienta que se instala en la web</td><td>143 archivos</td></tr>
  </table>
  <p>Lo que sale del ZIP no se pierde: est&aacute; en <code>main</code>. Lo que sali&oacute; de
  <code>main</code> est&aacute; en <code>piezas</code>. Esa cadena es la raz&oacute;n por la que
  se puede adelgazar en cada paso sin miedo.</p>
  <div class="clave"><p>Para ver las im&aacute;genes <b>no cambies de rama</b> en tu
  carpeta de trabajo: te las quitar&iacute;a del escritorio. Se abren en una carpeta
  hermana con <code>git worktree add ../piezas-archivo piezas</code>.</p></div>

  <h2>Al cerrar una sesi&oacute;n de trabajo</h2>
  <ol>
    <li><code>git add -A &amp;&amp; git commit</code> &mdash; <b>el repositorio
    primero, siempre</b>. Si se pierde la sesi&oacute;n, se pierde de aqu&iacute;.</li>
    <li>A&ntilde;adir la fila de la versi&oacute;n en <code>VERSION.md</code>.</li>
    <li><code>python3 scripts/empaquetar.py</code> &mdash; arma el ZIP y comprueba.</li>
    <li>Subirlo a Claude, reemplazando el anterior.</li>
  </ol>
  <div class="clave"><p><b>Una sesi&oacute;n que toca la skill y no termina en commit y
  ZIP, no ocurri&oacute;.</b></p></div>

  <h2>Si algo falla</h2>
  <table>
    <tr><th style="width:44%">S&iacute;ntoma</th><th>Qu&eacute; mirar</th></tr>
    <tr><td>La pieza sale con un hueco donde iba el logo</td><td><code>scripts/enlaces.py</code>: una ruta citada apunta al vac&iacute;o</td></tr>
    <tr><td>El texto sale en Arial y se ve fuera de marca</td><td>Las fuentes van por <code>@font-face</code> local desde <code>assets/tokens/tokens.css</code>. La red est&aacute; bloqueada y la ca&iacute;da a Arial es silenciosa</td></tr>
    <tr><td>Clawd no aparece y salta un error de ruta</td><td>La biblioteca no est&aacute; instalada. El puente lo dice por su nombre</td></tr>
    <tr><td>El ZIP se niega a armarse</td><td>Pasa de 200 archivos o hay una ruta rota. El script dice cu&aacute;l de las dos</td></tr>
    <tr><td><code>aire_max = 0</code> pero la pieza se ve vac&iacute;a</td><td>Mirar <code>aire_fiable</code>: bajo una trama que cubre el lienzo o una foto a sangre, el 0 no significa nada</td></tr>
  </table>
  <p style="margin-top:5mm">La fuente de verdad son los <code>.md</code> de cada
  skill. Esta gu&iacute;a se lee de corrido; ellos son los que mandan.</p>
  <div class="folio"><span>Gu&iacute;a &middot; tres skills</span><span>5</span></div>
</section>

</body></html>"""


def main():
    SALIDA.mkdir(exist_ok=True)
    f = SALIDA / '_guia.html'
    f.write_text(html(), encoding='utf-8')
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(viewport={'width': 1240, 'height': 1754})
        fallos = []
        pg.on('requestfailed', lambda r: fallos.append(r.url.split('/')[-1]))
        pg.goto(f.resolve().as_uri())
        pg.wait_for_timeout(1200)
        pg.pdf(path=str(PDF), format='A4', print_background=True,
               margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        hojas = pg.locator('.hoja').count()
        # Mismo control que el manual: una hoja que se pasa del alto util tira su
        # ultima seccion a la pagina siguiente y el PDF sale con una hoja coja.
        altos = pg.evaluate('''() => [...document.querySelectorAll('.hoja')].map(h => {
            const ultimo = [...h.children].filter(c => !c.classList.contains('folio')).pop();
            return Math.round(ultimo.getBoundingClientRect().bottom
                              - h.getBoundingClientRect().top);
        })''')
        limite = pg.evaluate("() => document.querySelector('.hoja').clientHeight")
        nav.close()
    print('fallos de carga:', fallos or 'ninguno')
    print(f'{PDF.name}: {hojas} páginas · {PDF.stat().st_size / 1e6:.2f} MB')
    tope = limite - 60
    for i, alto in enumerate(altos, 1):
        aviso = f'  <-- SE PASA POR {alto - tope}px' if alto > tope else ''
        print(f'  página {i}: contenido {alto} / {tope}{aviso}')


if __name__ == '__main__':
    main()
