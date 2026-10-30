#!/usr/bin/env bash
# Instala Poppins, Inter y Lora como archivos locales y las registra en el
# sistema, para que el render las use sin depender de Google Fonts (que está
# bloqueado en el contenedor; npm no).
#
# Uso:  bash scripts/fuentes_life.sh
# Corre desde la raíz de la skill. Es idempotente.

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

echo "Instalando fuentes vía npm..."
npm i @fontsource/poppins @fontsource/inter @fontsource/lora \
  --no-audit --no-fund --loglevel=error

FONTDIR="$HOME/.local/share/fonts/ge-tec"
mkdir -p "$FONTDIR"

for f in poppins inter lora; do
  # solo los pesos latinos que usan las plantillas
  find "node_modules/@fontsource/$f/files" -name "*latin-*normal.woff2" \
    -exec cp {} "$FONTDIR/" \; 2>/dev/null || true
done

# fontconfig no lee woff2; para que Chromium las use, las plantillas las cargan
# con @font-face apuntando a node_modules. Este copiado es solo respaldo.
fc-cache -f "$FONTDIR" >/dev/null 2>&1 || true

echo "Listo. Las plantillas cargan las fuentes desde:"
echo "  $DIR/node_modules/@fontsource/<fuente>/files/"
echo "Si moviste las plantillas de lugar, ajusta la ruta en su @font-face."
