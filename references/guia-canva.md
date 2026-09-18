# Montar Canva — guía de una sola vez

Al 15 de agosto de 2026, la cuenta tiene **un Brand Kit sin configurar y cero
Brand Templates**. Esta guía lo deja montado. Es trabajo manual dentro de Canva:
el conector puede leer Brand Kits y templates, y generar diseños, pero **no puede
subir archivos locales**, y hospedarlos en un servicio público para saltarse eso
publicaría material del grupo en internet abierto. Así que se sube a mano.

Calcula 40 minutos la primera vez. Se hace una vez y ya.

Todo lo que hay que subir está en `assets-canva/` (la genera `scripts/preparar_canva.py`), numerado en el orden en que
conviene subirlo.

---

## Paso 1 · Colores del Brand Kit

Canva → Brand → Brand Kit → Colores. Cárgalos **en este orden**, porque Canva
ofrece los primeros de la fila como sugerencia por defecto:

```
#141413   Dark        texto principal, fondos oscuros
#faf9f5   Light       fondo por defecto de casi todo
#d97757   Orange      acento primario
#e8e6dc   Light Gray  tarjetas, bloques, huecos de foto
#7d7b74   Gray        texto secundario
#6a9bcc   Blue        acento alterno
#788c5d   Green       acento alterno
#cc785c   Clay        naranja del dialecto editorial
#f0eee6   Bone        fondo alterno
#b0aea5   Mid Gray    filetes y apoyos
```

Los tres primeros son el 90% de las piezas. Azul y verde existen para rotar entre
series, no para mezclarse dentro de una misma pieza.

## Paso 2 · Fuentes

Brand Kit → Fuentes. **Poppins** para títulos, **Lora** para cuerpo. Las dos están
en el catálogo de Canva y son gratuitas: no hay que subir archivos.

Si defines estilos de texto, estos son los del sistema:

| Estilo | Fuente | Tamaño a 1080×1350 |
|---|---|---|
| Titular | Poppins Bold | 64–86 px |
| Subtítulo | Poppins SemiBold | 27–31 px |
| Cuerpo | Lora Regular | 25–26 px |
| Apoyo / pie | Lora Regular | 19–22 px |

## Paso 3 · Assets

Canva → Uploads. Arrastra las carpetas de `assets-canva/` (la genera `scripts/preparar_canva.py`) en orden.

| Carpeta | Qué es | Nota |
|---|---|---|
| `1-logos/` | Wordmark de Claude y los tres lockups de ClaudeTec | En SVG. No los recolorees dentro de Canva: ya vienen en la variante correcta |
| `2-ilustraciones/` | Cinco line art, versión base y `--claro` | La `--claro` es para fondo oscuro |
| `3-clawd/` | Clawd base y con audífonos, más los dos GIF animados | **Nunca sobre naranja**: Clawd es naranja y desaparece |
| `4-fotos/` | Las cinco fotos y sus versiones tratadas | Los `duo-naranja-*` son el salmón de la marca; no lo imites con un color plano |

Los SVG escalan sin pixelearse; los PNG no. Cuando exista SVG, usa el SVG.

## Paso 4 · Los dos primeros Brand Templates

Aquí está el valor real. Un Brand Kit fija color y tipografía; un Brand Template
fija **la composición**, que es donde de verdad se rompen las piezas.

No hagas los catorce. Haz **dos**, los que más se van a repetir:

**Template A — anuncio de evento.** Copia `01-foto-titular`: foto a sangre, velo
oscuro desde abajo, marca arriba a la izquierda, titular grande abajo, una línea
de bajada, paginador abajo a la izquierda.

**Template B — ficha de persona.** Copia `09-corte-foto-ficha`: bloque de foto
arriba ocupando el 44%, y abajo nombre, cargo en naranja y tres filas de
etiqueta/valor separadas por filete.

Para cada uno: diseño nuevo de 1080×1350 px → reconstruye la composición mirando
el PNG de referencia → Compartir → **Publicar como Brand Template**.

Márgenes del sistema: eje izquierdo a 76 px, margen superior 106 px, paginador a
52 px del borde inferior. La píldora de categoría va arriba a la izquierda, sobre
el mismo eje que todo lo demás — es lo que hace que la serie se lea como sistema.

## Paso 5 · Campos de autofill

Es el paso que convierte esto en algo que se usa desde el chat. En el template,
selecciona cada elemento de texto o imagen y ponle nombre en el panel de datos.

Para el Template A:

| Campo | Tipo | Ejemplo |
|---|---|---|
| `titular` | texto | Build with Claude |
| `bajada` | texto | De cero a un proyecto funcional en cuatro semanas |
| `etiqueta` | texto | Bootcamp |
| `fecha` | texto | Lunes 18 · 18:00 |
| `grafico` | imagen | la foto del evento |

Para el Template B: `nombre`, `cargo`, `descripcion`, `dato_1`…`dato_3`,
`retrato`.

Con los campos puestos, desde aquí se puede buscar el template, leer su esquema y
generar la pieza con los datos del evento sin abrir Canva. Para series
repetitivas —talleres semanales, fichas de la mesa directiva— es la diferencia
entre veinte minutos y treinta segundos por pieza.

---

## Antes de publicar cualquier pieza

**El bloque LiFE.** Ninguna plantilla de la skill lo trae, a propósito: son
composiciones, no piezas publicables. Toda pieza pública de un grupo estudiantil
lo lleva, **más pequeño que el logo de ClaudeTec**, y la pieza debe dejar claro
que ClaudeTec es un grupo estudiantil del Tec de Monterrey y no una activación
oficial de Anthropic. Detalle en la skill `publicaciones-grupos-estudiantiles`.

**Pasa la pieza por el validador.** Exporta el PNG y corre
`python3 scripts/validar.py pieza.png`. Tarda diez segundos y atrapa lo que el
ojo perdona.

## No uses el generador de Canva para piezas desde cero

Aplica el Brand Kit pero no conoce las reglas de composición: mete degradados de
dos colores, centra el texto y apila varios acentos. Partir de un Brand Template
propio da mejor resultado y menos correcciones.

## Cuándo Canva y cuándo HTML

La regla corta: **si va a tener una segunda versión, que nazca en Canva.** Una
pieza generada fuera y subida como imagen es un callejón sin salida — nadie podrá
corregirle una fecha sin volver a pedirla. Para la pieza única y urgente, el HTML
de `assets/templates/` es más rápido.
