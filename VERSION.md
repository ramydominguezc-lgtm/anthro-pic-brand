# Versiones — `anthro-pic-brand`

Este archivo vive en la raíz de la skill. Lo primero que debe hacer cualquier
sesión que abra la skill es leerlo, para saber de cuándo es lo que tiene enfrente
y qué le falta.

---

## Versión instalada

**v2.15** — 17 de septiembre de 2026. Veredicto de la tanda 02 aplicado, la pixel cambia a Press Start 2P y `aire_max` deja de estar ciega.

Las versiones son `MAYOR.MENOR`: la **mayor** sube cuando cambia cómo se usa la
skill (v1 → v2 fue adelgazar el `SKILL.md` y sacar la animación); la **menor**,
en cada tanda de trabajo que se empaqueta. El número del Artifact del visor
—"Versión 6", "Versión 7"— **no es este número**: lo pone la plataforma en cada
publicación y no se puede elegir.

## Límites del formato

Una skill admite **200 archivos como máximo**. Esta versión trae **195**, con 5
de margen: prácticamente no queda sitio. Si vas a añadir, mira antes qué se
puede convertir en script; la lista de abajo son 40 MB y más de doscientos
archivos que salieron de aquí sin perder nada.

**Lo primero que hay que sacar es `piezas-aprobadas/`**: son 33 archivos y
14.5 MB de material entregable, no de herramienta. El modelo no puede mirar esas
piezas sin gastar ~1,900 tokens por imagen —que es justo el motivo por el que se
retiró el corpus de imágenes en la v2.12— y lo que necesita de ellas ya está en
`references/veredictos.md` como números y motivos. Sin esa carpeta la skill
queda en **162 archivos y 17.45 MB**. Está pendiente de tu visto bueno.

Aviso de un error propio: en esta sesión quedó una carpeta `--help/` con 195
archivos, creada al probar `clawd_caminando.py --help` antes de que el script
tuviera guard de ayuda — interpretó `--help` como carpeta de destino y generó la
animación entera dentro. Si un script pide una ruta de salida, verifica que no la
esté escribiendo dentro de la skill.

## Qué no se guarda, y por qué

La skill pesa unos 11 MB. Antes pesaba 57, y la diferencia no era contenido: era
la misma cosa guardada varias veces.

**Nada derivado se versiona.** Si un archivo se puede regenerar con un script en
segundos, el script es la fuente y el archivo no se guarda:

| No está | Se genera con |
|---|---|
| `assets-canva/` | `scripts/preparar_canva.py` |
| `catalogo.pdf` | `scripts/catalogo_pdf.py` |
| `assets/biblioteca.html` | `scripts/biblioteca.py` |
| `visor-veredictos.html` | `scripts/visor.py` |
| `salida/catalogo-fondos.{png,pdf}` | `scripts/catalogo_fondos.py` |
| Los PNG de cada SVG | `scripts/derivar_png.py` |
| Los cuadros sueltos de un collage | `scripts/collage_animado.py` |
| Las animaciones de Clawd | no son de esta skill: `clawd-biblioteca` |

Tres cosas retiradas que conviene no reponer:

- **`v1/`** (14 MB) y **las catorce láminas**: obsoletas desde la v2.6. Su
  función quedó escrita en `references/laminas-carrusel.md`.
- **Las cinco plantillas HTML de `assets/templates/`**: escribían «ClaudeTec»
  como texto plano —el error que Ramses llamó grave— y el handle equivocado.
  Ninguna pieza salía ya de ellas. Lo que queda de `templates/` son las cuatro
  hojas de estilo, que sí son el sistema.
- **`referencias/aprobadas/` y `rechazadas/`**: el corpus de imágenes. Lo
  sustituye `references/veredictos.md` — la razón completa está en la cabecera
  de `scripts/veredictos.py`.

**Lo que sí se mide va sin pérdida.** Los iconos, porque los mide `auditar.py`.
La compresión con pérdida mueve los píxeles lo justo para cambiar qué colores lee
un validador como dominantes, y aparecen hallazgos graves falsos. Lo que nadie
mide admite pérdida: las capturas de `referencias/inspiracion/` van a 900 px y
calidad 82, porque son referencia de gusto — se miran, no se miden.

**La regla:** antes de añadir un archivo, pregunta si algún script lo produce. Si
la respuesta es sí, añade el script.

Cómo verificarlo sin confiar en este texto:

```bash
find /mnt/skills/user/anthro-pic-brand -type f -printf "%T+\n" | sort -u
```

Si sale **una sola fecha**, esa es la versión: las skills se instalan como paquete
extraído de golpe, así que todos los archivos comparten la marca de tiempo de la
subida. Si salen varias, alguien editó en caliente y esos cambios **no van a
sobrevivir** (ver protocolo abajo).

---

## Protocolo — leer antes de tocar nada

`/mnt/skills/user/` es escribible pero **efímero**. Se repuebla en cada arranque
de contenedor desde la última versión subida. Las escrituras nunca regresan solas.

**Regla: una sesión que toca la skill y no termina en commit y ZIP, no ocurrió.**

Desde la v2.15 hay dos destinos y son cosas distintas:

| | Qué es | Qué lleva |
|---|---|---|
| **El repositorio** | el archivo. `github.com/ramydominguezc-lgtm/anthro-pic-brand`, privado | todo: 225 archivos, 34.9 MB |
| **El ZIP** | la herramienta que se instala | solo lo que el flujo lee: 143 archivos, 14.8 MB comprimido |

Lo que sale del ZIP **no se pierde**, está en el repositorio. Esa es toda la
razón por la que se puede adelgazar sin miedo.

Al cerrar cualquier sesión de trabajo sobre la skill:

1. `git add -A && git commit` — el repositorio primero, siempre. Si se pierde la
   sesión, se pierde de aquí.
2. `python3 scripts/empaquetar.py` — arma el ZIP. Comprueba el tope de 200
   archivos y corre `enlaces.py`; **se niega** si algo no cuadra, en vez de
   dejar un ZIP con una ruta rota que sale a publicar con un hueco.
3. Subir el ZIP a Claude web / desktop.
3. Subirlo en Configuración → Capacidades → Skills, reemplazando la anterior.
4. Añadir la fila al registro de abajo **antes** de empaquetar.

Las otras dos skills del conjunto tienen su propio repositorio, privado también,
porque se instalan por separado: `clawd-animaciones` (genera) y
`clawd-biblioteca` (almacena y entrega). Si regeneras `paseo` en la primera,
cambia la pieza `10-pixel` de esta.

Esto se escribió porque entre el 31 de julio y el 3 de agosto de 2026 se
perdieron cuatro sesiones de trabajo por no hacerlo.

---

## Registro de versiones

Una línea por versión. El detalle está más abajo.

| Versión | Fecha | Qué entró |
|---|---|---|
| **v2.15** | 17 sep 2026 | Veredicto de Ramses sobre la tanda 02 aplicado: 03 con bullets más grandes, **06 y 07 rehechas enteras**, 08 con la lista reorganizada, 10 con tipografía nueva y **Clawd caminando sobre la tarjeta** (sale también en MP4). **`--font-pixel` pasa de Pixelify Sans a Press Start 2P**: la redondeada no se lee (la `D` se ve `O`); cotejadas cuatro candidatas. **Bug de `analizar_referencia.py`**: `aire_max` tomaba como fondo el color de la esquina, así que sobre fondo oscuro o bajo una trama daba 0 con 300-400 px muertos a la vista; ahora el fondo es el color más frecuente y hay `aire_fiable` para decir cuándo el número no significa nada. `collage_animado.py` ajusta solo el cuerpo del titular al ancho de la tarjeta |
| **v2.14** | 17 sep 2026 | `salida/tanda_fotos.py`: diez piezas con foto, **ninguna repite geometría** con las cinco aprobadas ni entre sí, en `piezas-aprobadas/tanda-02-imagenes/`. `entorno.py` sondea qué se puede hacer en Claude Code, desktop o web y qué se pierde sin lo que falte. `manual_pdf.py` arma el manual de 5 páginas con muestras vivas. El ZIP deja de llevar `salida/` |
| **v2.13** | 17 sep 2026 | `assets/lockups/` renombrada a **`assets/logos-claudetec/`** y las 33 citas actualizadas. `enlaces.py` ahora también revisa los **nombres sueltos de carpeta** en las listas `CARPETAS` de los scripts: cinco apuntaban al nombre viejo y `biblioteca.py` inventariaba 65 assets en vez de 75 sin fallar. Sombra acotada aprobada. Patrocinios entregados y retirados de `salida/` |
| **v2.12** | 17 sep 2026 | Limpieza: fuera `v1/` (14 MB), las cinco plantillas HTML, el visor derivado y el corpus de imágenes. `references/veredictos.md` + `veredictos.py` sustituyen a `referencias/aprobadas|rechazadas` y a `regresion.py`. `enlaces.py` comprueba que toda ruta citada exista —encontró que `assets/logos-claudetec/` se había renombrado a mano y diez archivos apuntaban al vacío—. Puente `clawd_biblioteca.py` con las dos skills de Clawd. `VERSION.md` de 4,826 a 2,200 tokens |
| **v2.11** | 17 sep 2026 | Pixelify Sans y Departure Mono instaladas (`--font-pixel`, `--font-mono`), sacadas del vídeo «The making of Claude Code». `collage_animado.py`: collage progresivo con imagen y vídeo, caja y turno dictados por quien pide la pieza, salida MP4 + GIF + PNG. Fondos podados a las 11 aprobadas; corte diagonal y esquina pasan a `hueco-diagonal` y `hueco-esquina`; `.tinta-clara` para que cualquier trama funcione sobre cualquier color. `--celeste` y `--verde-claro` pasan a principales |
| **v2.10** | 17 sep 2026 | `--lila`, `--celeste` y `--verde-claro` en `tokens.css` como fondos claros (solo texto oscuro; el porqué va documentado). `fondos-color.css` con 18 tramas —libreta, milimetrado, puntos, semitono, arcos, damero, grano, sellos…— y `catalogo_fondos.py`, que las saca en PNG y PDF. La 07 en cinco fondos |
| **v2.9** | 17 sep 2026 | La 06 sale en MP4 + GIF con el paseo de Clawd compuesto por ffmpeg; la escala se despeja del recorrido del paseo y del ancho de la ventana, no a ojo. La 07 en tres fondos claros (azul, lila `#cbcada`, crema) con texto y lockup oscuros; filete de `--mid-gray` para que la ventana no se pierda sobre crema |
| **v2.8** | 17 sep 2026 | Reglas de terminal (letra ≥ 40 px, cinco líneas, nunca centrada ni sola) y de ventana de navegador (titular arriba, ventana anclada abajo y sangrada). `aire_max` ≤ 180 px como umbral medido. Bug de `capas.css`: la ventana de navegador heredaba color claro sobre `.pieza` naranja. `piezas-aprobadas/` con las cinco piezas con foto |
| **v2.7** | 16 sep 2026 | `capas.css` + `references/capas.md`: cintas, tarjetas flotantes, ventanas de terminal y navegador, y tres patrones de acomodo de fotos. Lockup `--monocromo-claro` (el único que aguanta fondo naranja) y **bug de `lockup_variantes.py`** que dejaba el texto sin recolorear si el asterisco iba claro. Fondo claro por defecto; aviso de Anthropic solo si lo piden |
| **v2.6** | 16 sep 2026 | 14 láminas retiradas (su función queda en `laminas-carrusel.md`). `@font-face` de Newsreader declarado y `h1` en serif. `fotos-demo/` y la bandera fuera. `SKILL.md` 2,034→1,644 y catálogo 4,188→3,741 tokens |
| **v2.5** | 16 sep 2026 | Lockups renombrados a un solo criterio (`claudetec`, `--claro`, `--duotono`); 4 veredictos migrados |
| **v2.4** | 16 sep 2026 | Biblioteca solo PNG + SVG: 17 WebP convertidos, 21 PNG derivados, `derivar_png.py`. Visor agrupado por dibujo |
| **v2.3** | 16 sep 2026 | Glifo de Claude vectorizado. Catálogo saneado: 11 defectos, incluida una regla que se contradecía. Skill instalada en Claude Code |
| **v2.2** | 16 sep 2026 | Renders borrados (13). Variante `proyector-codigo--pantalla-clara` del encargo del visor |
| **v2.1** | 16 sep 2026 | Compatibilidad de fondo medida sobre 53 piezas. Dos reglas de la skill resultaron falsas y se invirtieron |
| **v2.0** | 15 sep 2026 | Reorganización: `SKILL.md` de 3,900 a 1,500 tokens, `gustos.md` partido, animación a skill aparte, visor publicado |
| v1.7 | 15 ago 2026 | `MANUAL-COMUNICACION.md` y reparto de los documentos para personas |
| v1.6 | 15 ago 2026 | `assets-canva/` y `guia-canva.md` con el procedimiento completo |
| v1.5 | 15 ago 2026 | Las catorce láminas replicadas del plano original; corpus de 2 a 16 piezas |
| v1.4 | 15 ago 2026 | Fototeca y láminas recalibradas sobre foto real: cero hallazgos graves |
| v1.3 | 15 ago 2026 | Tres bugs cerrados, `regresion.py` calibrando el validador, corpus separado |
| v1.2 | 15 ago 2026 | Fuentes locales en woff2, `fondos.css`, `tratar_foto.py`, `laminas.py` |
| v1.1 | 15 ago 2026 | Clawd caminando recuperado y verificado byte a byte |
| v1.0 | 25 jul 2026 | Paleta, tipografía, `layout.md`, 67 assets, 5 plantillas, 11 scripts |

### Cómo numerar la siguiente

Sube la **menor** (v2.6, v2.7…) en cada tanda que se empaquete y suba. Sube la
**mayor** solo si cambia cómo se usa la skill: qué se lee, qué se abre, dónde
vive algo. Añade la fila **antes** de empaquetar, en una línea.

---

---

## Historia

El detalle de cada versión, el manifiesto de recuperación de agosto de 2026 y
los bugs que se cerraron por el camino están en `references/bitacora.md`. Esto
es el índice; eso es el relato.
