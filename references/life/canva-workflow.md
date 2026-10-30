# Ruta B — Producir la pieza en Canva

Se usa cuando la pieza debe quedar editable para el equipo, no solo como PNG final.

## Límite que define todo el flujo

Canva no importa archivos locales del contenedor. `generate-design` crea el diseño a partir de una descripción, y los assets se suben con `upload-asset-from-url` — o sea, desde una URL pública. Los logos oficiales viven en el disco local, así que **no se pueden insertar directamente**.

Dos salidas honestas ante esto, ambas legítimas:

**Opción 1 — Híbrida (recomendada).** Genera la pieza completa por HTML/CSS con los logos oficiales bien puestos, entrégala como PNG, y en paralelo crea el diseño en Canva como base editable **sin** los logos, avisando que los logos hay que subirlos a mano desde la carpeta oficial (el manual incluye un QR de descarga). Es más honesto que entregar un Canva con logos aproximados.

**Opción 2 — Canva puro.** Solo si el usuario acepta pegar los logos él mismo después. Genera la composición, el copy y la estructura; deja marcados los espacios reservados.

## Pasos

1. `search-designs` primero, por si ya existe una plantilla del grupo que convenga copiar con `copy-design` en vez de generar de cero.
2. `generate-design` con `design_type` acorde al formato:
   - post de Instagram → `instagram-post` (o `poster` si se necesita más resolución)
   - story → el tipo vertical de story
   - **`generate-design` no soporta `presentation`**; para presentaciones se usa `generate-design-structured` a partir de un outline aprobado.
3. Describe la pieza en el prompt con la paleta explícita del grupo (acento y fondo en hexadecimal), la tipografía deseada y el espacio reservado en la esquina para el bloque de logos. Canva no adivina la identidad del grupo; pásasela explícita desde el perfil.
4. `read-design` para verificar qué salió, y `edit-design` para corregir textos.
5. `export-design` (revisa antes los formatos disponibles con `get-export-formats`) para obtener el PNG.
6. Entrega el link del diseño **y** el PNG exportado, más el recordatorio de subir los logos oficiales si quedaron pendientes.

## Antes de exportar

Revisa la pieza contra el checklist de `references/life/grupos-estudiantiles.md` igual que en la ruta HTML. Que Canva la haya generado no la exime de las reglas del manual — y el Líder de Portafolio la va a revisar con el mismo criterio.
