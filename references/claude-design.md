# Claude Design

Claude Design construye un sistema de diseño para el equipo leyendo archivos de
código y de diseño durante el onboarding, y a partir de ahí aplica esos colores,
tipografía y componentes de forma automática en cada proyecto. La superficie de
trabajo produce HTML y CSS.

Eso hace que esta skill encaje directo: `assets/tokens/tokens.css` y las
plantillas de `assets/templates/` **son** el sistema de diseño, ya escrito en el
formato que espera. No hay que traducir nada.

## Qué darle en el onboarding

En orden de importancia:

1. **`assets/tokens/tokens.css`** — los tokens de color y tipografía. Es el
   archivo que define la marca.
2. **`assets/templates/_base.css`** — los componentes: lockup, píldora, bloque de
   datos, pie. Aquí está la composición, no solo el color.
3. **Las plantillas** (`poster`, `story`, `carrusel`, `slide`, `banner`) como
   ejemplos de uso de esos componentes en cada formato.
4. **`references/layout.md`** — las reglas que el CSS no puede expresar: un solo
   acento por pieza, un solo gráfico, sentence case, sin degradados.

Los assets de imagen se suben aparte según los vaya pidiendo la pieza; prioriza
los SVG de `ilustraciones/`, `lockups/` y `clawd/`.

## Cómo pedir

El sistema resuelve el color y la tipografía solo. Lo que sí hay que decir en
cada pieza:

- **Formato y medida exacta** — "post 1080×1080", no "un post".
- **Modo de fondo** — claro, acento u oscuro. Es la variable que más cambia el
  resultado.
- **Qué gráfico** — nombra el archivo. Si lo dejas abierto, mete cualquier cosa.
- **El contenido literal** — titular, bajada, datos, cierre. Los textos
  inventados por el modelo casi nunca sobreviven a la revisión.

Un ejemplo de encargo que funciona:

> Post 1080×1080, fondo claro. Titular "Construye tu primer MCP" en Poppins Bold,
> máximo dos líneas. Bajada en naranja. Gráfico: `documento-nodos.svg` a la
> izquierda, 290px. A la derecha el bloque de datos en dos columnas con Cuándo,
> Dónde, Traer y Registro. Cierre en Lora itálica al pie. Márgenes de 78px.

## A dónde va después

Claude Design exporta a Canva, PDF, PPTX y HTML suelto, y arma un paquete de
handoff para Claude Code.

Para el flujo del equipo eso significa una cosa concreta: **explorar en Claude
Design, aterrizar en Canva.** Se generan tres o cuatro direcciones en la
conversación, se elige una, y esa se manda a Canva para que quede editable por
quien no está en la conversación. Terminar en un PNG exportado es el mismo
callejón sin salida que se describe en `canva.md`.

## Esta skill sí carga en Claude Design

Comprobado en producción: `anthro-pic-brand` está disponible dentro de Claude
Design, así que se puede nombrar un asset por su ruta —`assets/clawd/clawd-base.svg`,
`assets/ilustraciones/globo-red.svg`— sin subirlo a mano en cada sesión.

Con una salvedad que no es obvia: **una ruta local nunca resuelve dentro de un
navegador.** Que el archivo esté en la skill significa que la herramienta lo
puede leer e incrustar, no que un `<img src="assets/...">` vaya a pintar algo.
Si aparece el hueco de imagen rota, el asset tiene que viajar como data URI o
como código en línea.

## Piezas animadas

El canvas produce HTML y CSS, así que **los `@keyframes` corren nativos**: una
animación entra igual que cualquier otro elemento y se ve en vivo mientras se
edita.

Dónde sobrevive y dónde no:

| Salida | La animación |
|---|---|
| Canvas en vivo | se mueve |
| URL compartido | se mueve |
| HTML autónomo | se mueve |
| Canva (importa HTML) | se mueve |
| PDF, PPTX | **se congela** |

La consecuencia práctica pesa más de lo que parece: **Instagram no acepta HTML.**
Para un post animado que se pueda publicar hay que salir por MP4 o GIF, no por la
exportación de Claude Design. La ruta que funciona es armar la pieza como HTML y
renderizarla a video con Playwright, igual que se hace con los reels.

Para meter la mascota animada hay un bloque autónomo de 5.9 KB —SVG en línea más
keyframes, sin archivos externos— que se pega tal cual en el encargo, junto con
un prompt ya validado. Los dos están en la skill `clawd-biblioteca`, en
`caminando/` (`clawd-caminando-bloque.html` y `prompt-claude-design.md`). Las
demás animaciones y los labels de carga (`labels/`) traen su propio
`-bloque.html` en su carpeta. En los labels, el tema se cambia con
`data-tema="oscuro"`.

## Límites que conviene tener presentes

Está en research preview, así que el detalle cambia seguido; verifica contra el
producto en vivo antes de casarte con un flujo. Un editor a la vez. Y no
sustituye a Canva ni a Figma — Anthropic lo plantea como complemento.

Lo importante para esta skill: **nada de lo anterior se contradice con el
sistema.** Si Claude Design produce algo que se sale de marca, la pieza se pasa
por `scripts/validar.py` igual que cualquier otra, y las reglas de
`references/layout.md` siguen mandando.
