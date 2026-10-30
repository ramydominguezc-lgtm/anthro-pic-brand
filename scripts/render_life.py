#!/usr/bin/env python3
"""
Renderiza un HTML a PNG con dimensiones exactas, usando Chromium vía Playwright.

Uso:
    python3 scripts/render_life.py pieza.html salida.png --width 1080 --height 1080
    python3 scripts/render_life.py story.html story.png --width 1080 --height 1920
    python3 scripts/render_life.py diploma.html diploma.png --width 3508 --height 2480

Notas que ahorran tiempo:

- El HTML se carga con file:// desde su propio directorio, así que las rutas
  relativas a los logos (../logos/...) funcionan sin base64.
- --scale renderiza a mayor densidad y luego reduce: sirve para impresión o
  cuando el texto pequeño se ve sucio. Para pantalla, 1 basta.
- Las fuentes se toman del sistema. Corre scripts/fuentes_life.sh antes si
  quieres Poppins/Inter/Lora; si no, el CSS cae a los fallbacks.
- Si el PNG sale en blanco: casi siempre es una fuente web o una imagen que no
  cargó y bloqueó el layout. Sube --wait o revisa las rutas.
"""

import argparse
import pathlib
import sys


def render(html_path, out_path, width, height, scale, wait_ms, full_page):
    from playwright.sync_api import sync_playwright

    html_path = pathlib.Path(html_path).resolve()
    if not html_path.exists():
        sys.exit(f"No existe el HTML: {html_path}")

    out_path = pathlib.Path(out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb"])
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=scale,
        )
        page.goto(html_path.as_uri())
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass  # sin recursos externos, networkidle puede no dispararse
        page.wait_for_timeout(wait_ms)
        page.screenshot(path=str(out_path), full_page=full_page)
        browser.close()

    if scale != 1:
        from PIL import Image

        im = Image.open(out_path)
        im.resize((width, height), Image.LANCZOS).save(out_path)

    print(f"OK -> {out_path} ({width}x{height}, scale {scale})")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--scale", type=int, default=1,
                    help="Densidad de render; se reduce al tamaño final (default 1)")
    ap.add_argument("--wait", type=int, default=400,
                    help="ms extra de espera antes del screenshot")
    ap.add_argument("--full-page", action="store_true",
                    help="Captura toda la altura del documento en vez del viewport")
    a = ap.parse_args()
    render(a.html, a.out, a.width, a.height, a.scale, a.wait, a.full_page)


if __name__ == "__main__":
    main()
