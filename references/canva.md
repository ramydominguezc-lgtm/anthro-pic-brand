# Canva

Canva es donde el equipo edita, así que el objetivo no es producir la pieza final
fuera y subirla: es que Canva **ya venga configurado** para que cualquiera del
equipo diseñe dentro de marca sin acordarse de un solo hex.

**Estado al 15 de agosto de 2026: un Brand Kit sin configurar, cero Brand
Templates.** El montaje está pendiente y es manual. Los pasos exactos, con los
colores en orden y los campos de autofill, en `references/guia-canva.md`. Los
archivos a subir, ya seleccionados y numerados, en `assets-canva/` (la genera `scripts/preparar_canva.py`).

## Montar el Brand Kit (una vez)

No hay API para crear ni editar un Brand Kit — se configura a mano en Canva y
desde aquí solo se puede leer. Vale la pena hacerlo bien una vez.

**Colores.** Carga los diez de `assets/tokens/brand-kit.json` en este orden, para
que los primeros de la fila sean los que más se usan:

```
#141413  #faf9f5  #d97757  #e8e6dc  #7d7b74
#6a9bcc  #788c5d  #cc785c  #f0eee6  #b0aea5
```

**Fuentes.** Poppins para títulos, Lora para cuerpo. Las dos están en Google
Fonts y salen en Canva gratis, sin subir archivos. Newsreader también, si vas a
componer lockups ahí — aunque es mejor subir el SVG ya hecho.

**Logos y assets.** Sube los SVG, no los PNG: Canva los acepta y escalan sin
pixelearse. Del `assets/` prioriza `logos/`, `lockups/`, `ilustraciones/` (las
cinco base más las variantes `--claro`, `--azul` y `--verde`) y los `clawd/*.svg`
que existan.

## Brand Templates

Un Brand Kit fija colores y fuentes; un **Brand Template** fija la composición,
que es donde más se rompen las piezas. Sube las plantillas de `assets/templates/`
como diseños, ajústalas en Canva y publícalas como Brand Template.

Si además les etiquetas campos de autofill (titular, fecha, lugar, gráfico),
quedan rellenables desde aquí sin abrir Canva: se busca el template, se lee su
esquema de campos y se genera la pieza con los datos del evento. Vale mucho la
pena para series repetitivas como los eventos semanales.

## Trabajar contra Canva desde aquí

Lo que se puede hacer sin salir de la conversación:

- **Leer** qué Brand Kits, templates y diseños existen.
- **Generar** una pieza a partir de una descripción, aplicándole un Brand Kit y
  metiéndole assets ya subidos.
- **Crear** un diseño a partir de un Brand Template, con o sin autofill.
- **Editar, exportar y redimensionar** un diseño existente.
- **Publicar** un diseño como Brand Template nuevo.

Dos cosas que conviene saber antes de intentarlas:

- Los assets se suben **desde una URL pública**, y esa es una pared dura. Un
  archivo local no se puede empujar. Y la salida fácil —subirlo a un servicio de
  hospedaje temporal para tener una URL— **no es una opción**: publicaría
  material del grupo en internet abierto de forma irreversible. Se sube a mano en
  Canva, o se sirve desde un dominio propio que ya sea público.
- Las presentaciones tienen flujo propio: primero se revisa y aprueba un esquema
  de slides, y solo después se genera el diseño. No se puede saltar ese paso.
- La generación devuelve **candidatos**, no un diseño final: hay que elegir uno
  antes de poder editarlo o exportarlo.

## Cuándo Canva y cuándo HTML

| Situación | Ruta |
|---|---|
| La pieza la va a seguir editando el equipo | Canva, sobre Brand Template |
| Serie repetitiva con los mismos campos | Brand Template + autofill |
| Se necesita el archivo ya, con control exacto | HTML de `assets/templates/` → PNG |
| Presentación que alguien más va a retocar | Canva |
| Pieza única que nadie va a volver a tocar | HTML, es más rápido |

La regla práctica: **si va a tener una segunda versión, que nazca en Canva.**
Una pieza generada fuera y subida como imagen es un callejón sin salida — nadie
podrá corregirle una fecha sin volver a pedirla.

## Advertencia sobre el generador de Canva

El generador aplica el Brand Kit pero no conoce las reglas de composición de esta
skill: mete degradados, centra texto, apila varios acentos. Cuando lo uses,
**revisa la pieza contra la checklist del SKILL.md** o pásala por
`scripts/validar.py` después de exportarla. Es más fiable partir de un Brand
Template propio que pedirle una pieza desde cero.
