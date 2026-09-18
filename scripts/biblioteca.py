#!/usr/bin/env python3
"""Genera un visor HTML de toda la biblioteca de assets.

Existe porque una hoja de contactos estatica no deja buscar ni copiar rutas, y
elegir asset abriendo carpetas es donde se pierde el tiempo. El archivo que sale
es autonomo: se abre en el navegador, filtra por carpeta y por texto, alterna el
fondo entre claro, naranja y oscuro para ver como se comporta cada pieza, y al
hacer clic copia la ruta relativa al portapapeles.

Uso:
    python3 biblioteca.py                  # escribe assets/biblioteca.html
    python3 biblioteca.py --salida x.html
"""
import argparse, json, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
EXT = {".svg", ".png", ".webp"}
CARPETAS = ["logos", "logos-claudetec", "iconos", "ilustraciones", "clawd"]


def inventario():
    items = []
    for c in CARPETAS:
        d = RAIZ / "assets" / c
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            if f.suffix.lower() not in EXT:
                continue
            variante = f.stem.split("--")[1] if "--" in f.stem else ""
            items.append({
                "carpeta": c,
                "nombre": f.name,
                "base": f.stem.split("--")[0],
                "variante": variante,
                "ruta": f"{c}/{f.name}",
                "kb": round(f.stat().st_size / 1024, 1),
                "vector": f.suffix.lower() == ".svg",
            })
    return items


PLANTILLA = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>Biblioteca — Anthropic / Claude</title>
<style>
:root{--dark:#141413;--light:#faf9f5;--muted:#7d7b74;--orange:#d97757;--linea:#e8e6dc}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--light);color:var(--dark);font:15px/1.5 system-ui,sans-serif;padding:32px 40px}
h1{font-size:26px;font-weight:700;letter-spacing:-.02em}
.sub{color:var(--muted);margin-top:4px;font-size:14px}
.barra{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:22px 0 6px;
       position:sticky;top:0;background:var(--light);padding:12px 0;z-index:5;
       border-bottom:1px solid var(--linea)}
button,input{font:inherit;border:1px solid var(--linea);background:#fff;color:var(--dark);
             border-radius:999px;padding:7px 16px;cursor:pointer}
button.on{background:var(--dark);color:var(--light);border-color:var(--dark)}
input{cursor:text;min-width:200px}
.fondos{margin-left:auto;display:flex;gap:6px}
.sw{width:30px;height:30px;border-radius:50%;border:2px solid var(--linea);cursor:pointer}
.sw.on{border-color:var(--dark)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:16px;margin-top:20px}
.card{border:1px solid var(--linea);border-radius:10px;overflow:hidden;cursor:pointer;
      transition:transform .08s}
.card:hover{transform:translateY(-2px);border-color:var(--muted)}
.lienzo{aspect-ratio:1;display:grid;place-items:center;padding:14px;background:var(--light)}
.lienzo img{max-width:100%;max-height:100%;object-fit:contain}
.pie{padding:8px 10px;border-top:1px solid var(--linea);font-size:11.5px;
     display:flex;justify-content:space-between;gap:6px}
.nom{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tag{color:var(--muted);flex:none}
.vacio{color:var(--muted);padding:40px 0}
#aviso{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(80px);
       background:var(--dark);color:var(--light);padding:10px 20px;border-radius:999px;
       font-size:13px;transition:transform .18s}
#aviso.ver{transform:translateX(-50%) translateY(0)}
</style></head><body>

<h1>Biblioteca de marca</h1>
<p class="sub">__N__ archivos. Clic en cualquiera para copiar su ruta.</p>

<div class="barra">
  <button data-f="" class="on">Todo</button>
  __BOTONES__
  <input id="q" placeholder="buscar…">
  <div class="fondos">
    <div class="sw on" style="background:#faf9f5" data-bg="#faf9f5"></div>
    <div class="sw" style="background:#d97757" data-bg="#d97757"></div>
    <div class="sw" style="background:#141413" data-bg="#141413"></div>
  </div>
</div>

<div class="grid" id="grid"></div>
<div id="aviso">ruta copiada</div>

<script>
const items = __DATOS__;
const grid = document.getElementById('grid');
let filtro = '', texto = '';

function pinta(){
  const vis = items.filter(i =>
    (!filtro || i.carpeta === filtro) &&
    (!texto || (i.nombre + ' ' + i.carpeta).toLowerCase().includes(texto)));
  grid.innerHTML = vis.length ? vis.map(i => `
    <div class="card" data-ruta="${i.ruta}">
      <div class="lienzo"><img src="${i.ruta}" loading="lazy" alt=""></div>
      <div class="pie">
        <span class="nom" title="${i.nombre}">${i.base}${i.variante ? ' · ' + i.variante : ''}</span>
        <span class="tag">${i.vector ? 'SVG' : i.kb + 'k'}</span>
      </div>
    </div>`).join('') : '<p class="vacio">Nada coincide.</p>';
}

document.querySelectorAll('.barra button').forEach(b => b.onclick = () => {
  document.querySelectorAll('.barra button').forEach(x => x.classList.remove('on'));
  b.classList.add('on'); filtro = b.dataset.f; pinta();
});
document.getElementById('q').oninput = e => { texto = e.target.value.toLowerCase(); pinta(); };
document.querySelectorAll('.sw').forEach(s => s.onclick = () => {
  document.querySelectorAll('.sw').forEach(x => x.classList.remove('on'));
  s.classList.add('on');
  document.querySelectorAll('.lienzo').forEach(l => l.style.background = s.dataset.bg);
});
grid.onclick = e => {
  const c = e.target.closest('.card'); if(!c) return;
  navigator.clipboard.writeText(c.dataset.ruta);
  const a = document.getElementById('aviso');
  a.classList.add('ver'); setTimeout(() => a.classList.remove('ver'), 1100);
};
pinta();
</script>
</body></html>
"""

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--salida", default=str(RAIZ / "assets" / "biblioteca.html"))
    a = p.parse_args()

    items = inventario()
    carpetas = sorted({i["carpeta"] for i in items})
    botones = "".join(f'<button data-f="{c}">{c}</button>' for c in carpetas)
    html = (PLANTILLA
            .replace("__DATOS__", json.dumps(items, ensure_ascii=False))
            .replace("__BOTONES__", botones)
            .replace("__N__", str(len(items))))
    pathlib.Path(a.salida).write_text(html)
    print(f"-> {a.salida}  ({len(items)} assets, {len(html)/1024:.0f} KB)")
