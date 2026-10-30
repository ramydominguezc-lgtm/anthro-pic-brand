# Módulo LiFE — publicaciones de grupos estudiantiles del Tec

**Complementario.** Este módulo no se abre en cada pieza. Antes vivía como skill
aparte (`publicaciones-grupos-estudiantiles`); desde la v2.18 está dentro de
`anthro-pic-brand` para que haya una sola skill que instalar.

## Cuándo se abre y cuándo no

| Se abre | No se abre |
|---|---|
| Pieza **pública** de un grupo estudiantil: post, story, flyer de WhatsApp o correo, cartel de evento, invitación | Recursos gráficos internos, pruebas, exploraciones de composición |
| Diploma o constancia de participación | Slides, banners o UI que no se publican como difusión del grupo |
| El mensaje de difusión que acompaña al flyer | Piezas con marca Claude que no son de un grupo estudiantil |
| Preguntas sobre dónde va el logo LiFE o si una pieza cumple con el Tec | Cuando el encargo dice explícitamente que no lleva LiFE |

Si no está claro, **pregunta** si la pieza es publicidad del grupo. No metas el
bloque LiFE «por si acaso»: en una pieza que no lo pide sobra.

## Cómo se combina con la marca Claude

Este módulo define **la reglamentación**. El lenguaje visual sigue siendo el de
`anthro-pic-brand`. En una pieza de ClaudeTec:

- **De la skill principal** salen paleta, tipografías, capas, recursos
  compositivos, formato (4:5 por defecto) y el validador. El perfil de ClaudeTec
  es la propia marca: no hace falta construirle uno en `perfiles-de-grupo.md`.
- **De este módulo** salen el bloque LiFE, la jerarquía de logos, el contenido
  obligatorio, las reglas del diploma, el texto de difusión y la validación con
  el Líder de Portafolio.
- **Ante conflicto, gana la regla del Tec.**

**Conflicto abierto, sin resolver:** el manual pide el logo del grupo **arriba**,
y la regla de reels del 28/10 (`references/reglas-derivadas.md`, «En video y
reels» §2) pone ClaudeTec y el bloque LiFE **abajo** para no tapar a la gente.
Mientras Ramses no decida, en reels avisa del conflicto al entregar; en posts y
flyers el logo del grupo va arriba.

Para otros grupos que no son ClaudeTec, las plantillas de `assets/life/plantillas/`
y los perfiles de `perfiles-de-grupo.md` siguen siendo el punto de partida.

---

## Paso 1 — Identificar el grupo y su perfil

Antes de diseñar, determina de qué grupo es la pieza y consulta `references/life/perfiles-de-grupo.md`:

- **Si es ClaudeTec**, su identidad es la de `anthro-pic-brand`. Salta al paso 2.
- **Si el grupo ya tiene perfil ahí**, úsalo tal cual: paleta, tipografía, tono. No lo reinventes en cada pieza; la consistencia entre publicaciones es la mitad del valor de una identidad.
- **Si no tiene perfil**, constrúyelo antes de abrir el editor. Pregunta por el logo (pide el archivo, idealmente PNG con transparencia o SVG), los colores oficiales si los hay, y el tono del grupo. Si no tiene paleta definida, propón una a partir de su logo y confírmala antes de producir. Al terminar, ofrece guardar el perfil nuevo en ese archivo para que la próxima pieza salga consistente.

Los valores de color que traen las plantillas son placeholders neutros, no una paleta sugerida. Producir una pieza sin haber definido antes la identidad del grupo no es un atajo: es entregarle a un grupo la identidad de otro.

Un grupo sin logo propio no es un bloqueo: se compone un wordmark tipográfico con el nombre del grupo, que es lo que traen las plantillas por defecto.

## Paso 2 — Reunir el contenido

Toda pieza necesita datos concretos; si faltan, pídelos en una sola tanda en vez de inventarlos:

- Nombre del evento
- Fecha, hora y lugar (salón o edificio exacto)
- Link o QR de registro
- Contacto: IG del grupo o persona responsable
- ¿Colaboración con otro grupo estudiantil o patrocinador?

## Paso 3 — Reglas no negociables

Están completas en `references/life/guia-logos-ge.md`. **Léelo antes de componer la primera pieza** — es corto y trae las reglas exactas de área de respeto, variantes permitidas y prohibiciones. El resumen operativo:

1. **Jerarquía**: el logo del grupo va arriba y es el logo más grande de la pieza. El bloque LiFE + Grupos Estudiantiles va siempre presente, más chico, en una esquina.
2. El bloque LiFE **nunca** se separa, se estira, se gira, ni se le pone transparencia. Se usa tal cual sale del archivo.
3. Debe verse completo, incluyendo los colores de la flor. Si el fondo lo traga, mete una cintilla (franja sólida) detrás.
4. Respeta el área libre alrededor del logo: nada del diseño lo toca ni se le encima.
5. En colaboraciones, los logos de los grupos van del **mismo tamaño y alineados** entre sí.
6. Cierra siempre recordando validar con el Líder de Portafolio antes de publicar. No es opcional y es donde más piezas se caen.

Los logos están en `assets/life/logos/`: sobre fondo claro, `life-ge_negro_flor-color.png`; sobre fondo oscuro, `life-ge_blanco_flor-color.png`. Los de la flama del Tec, en `assets/life/logos/tec/`, solo para diplomas o cuando el Líder de Portafolio lo autoriza.

## Paso 4 — Producir

Dos rutas, ambas válidas. Si no se especifica, produce el PNG por HTML y al final ofrece pasarla a Canva.

| Ruta | Cuándo |
|---|---|
| **HTML/CSS → PNG** (por defecto) | Se quiere el archivo final ya, con control pixel-perfect y los logos oficiales embebidos |
| **Canva MCP** | La pieza debe quedar editable para el equipo. Flujo y límites en `references/life/canva-workflow.md` |

**Si la pieza es de ClaudeTec**, se compone como cualquier pieza de la skill
principal y solo se le añade el bloque LiFE desde `assets/life/logos/`. Las
plantillas de abajo son para otros grupos.

Ruta HTML con las plantillas del módulo, paso a paso:

1. Corre `bash scripts/fuentes_life.sh` (instala Poppins, Inter y Lora vía npm en `node_modules/`; sin eso el render sale con fuentes genéricas y se nota).
2. Parte de la plantilla del formato correspondiente en `assets/life/plantillas/` — no arranques de cero:
   - `post-1080.html` — post cuadrado de Instagram, 1080×1080
   - `story-1080x1920.html` — story/reel, con zona segura marcada
   - `diploma.html` — constancia de participación, A4 horizontal
3. Ajusta el bloque `:root` de la plantilla con la paleta del grupo y sustituye el wordmark por su logo. Las plantillas están construidas sobre variables CSS justo para esto: cambiar cuatro valores reidentifica la pieza completa.
4. Renderiza:
   ```bash
   python3 scripts/render_life.py entrada.html salida.png --width 1080 --height 1080
   ```
5. **Abre el PNG y revísalo tú mismo** antes de entregarlo. Los errores que solo se ven mirando: texto desbordado, logo LiFE encimado con el fondo, flor invisible sobre fondo claro, jerarquía invertida (LiFE más grande que el logo del grupo).
6. Entrega el archivo.

## Formatos

| Pieza | Medidas | Nota |
|---|---|---|
| Post IG | 1080×1080 en las plantillas del módulo; 1080×1350 en piezas de ClaudeTec | La info clave no va en los bordes; IG recorta en la retícula del perfil |
| Story / Reel | 1080×1920 | Zona segura: 250px arriba y 320px abajo libres de texto |
| Cartel impreso | Según el espacio, a 300dpi | Confirma medidas antes de componer |
| Diploma / constancia | 3508×2480 (A4 horizontal, 300dpi) | Reglas distintas: ver abajo |

**El diploma es la excepción.** Solo puede llevar el logo del Tec (la flama), el nombre del grupo estudiantil y las firmas de presidencia y asesor/a. **No** lleva el bloque LiFE ni el logo gráfico del grupo. Si alguien lo pide "con el logo del grupo", corrígelo: el formato editable se le pide al Líder de Portafolio.

## Texto de difusión

Cuando la pieza va por WhatsApp o correo, el flyer no viaja solo. Genera también el mensaje:

```
El Grupo Estudiantil [NOMBRE] te invita a [emoji] ¡[Nombre del evento]!

[Una línea de qué es y a quién le sirve.]

📅 [Fecha] | [Gancho corto]
📍 [Lugar y hora]

🎟️ ¡Regístrate aquí! 👉 [link]

Para más información síguenos en IG [@handle]

Grupos Estudiantiles | LiFE
```

El cierre "Grupos Estudiantiles | LiFE" va siempre. Si el mensaje no cabe en una pantalla de celular sin scroll, sobra texto.

## Revisar piezas ajenas

Si te piden revisar un flyer ya hecho, no des un veredicto genérico: recórrelo contra esta lista y señala qué falla y cómo se arregla.

- [ ] Nombre del evento, fecha, hora, lugar
- [ ] Link o QR de registro
- [ ] Contacto (IG o persona responsable)
- [ ] Logo del grupo arriba y como logo más grande
- [ ] Bloque LiFE + Grupos Estudiantiles presente, completo y sin deformar
- [ ] Flor del logo LiFE visible sobre el fondo
- [ ] Área de respeto libre alrededor del logo
- [ ] Logos de colaboradores del mismo tamaño y alineados
- [ ] Texto legible en miniatura (reduce el PNG a 200px de ancho y compruébalo)

## Marcas de terceros

Si el grupo lleva en su nombre o identidad la marca de una empresa — una herramienta, un patrocinador, una comunidad de producto — aplican dos capas de reglas: la del Tec y la del dueño de esa marca. No deformes ni recolorees logotipos ajenos, y no compongas piezas que sugieran que el evento es oficial o patrocinado por esa empresa si no lo es. Cuando la pieza se acerque a esa línea, sobre todo en merch o cualquier cosa que se produzca físicamente, dilo explícitamente en vez de asumir que está bien.
