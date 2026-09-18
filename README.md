# anthro-pic-brand — léeme antes de usarla

> **Este repositorio es el archivo, no la skill que se instala.** Lleva de más
> las piezas terminadas (`piezas-aprobadas/`), la inspiración (`referencias/`) y
> el banco de trabajo (`salida/`), que son la evidencia detrás de las reglas
> pero que **ningún paso del flujo abre**. Para instalarla se arma un ZIP con
> `python3 scripts/empaquetar.py`, que deja fuera todo eso: 143 archivos y
> 16.6 MB, frente a los 225 y 34.9 MB de aquí.
>
> Las otras dos skills del conjunto, en repositorios aparte porque se instalan
> por separado:
> [`clawd-animaciones`](https://github.com/ramydominguezc-lgtm/clawd-animaciones)
> genera las animaciones de Clawd ·
> [`clawd-biblioteca`](https://github.com/ramydominguezc-lgtm/clawd-biblioteca)
> las guarda y las entrega. Esta skill **consume** de la biblioteca a través de
> `scripts/clawd_biblioteca.py`; si regeneras `paseo`, la pieza `10-pixel`
> cambia.

## Cómo se instala

```bash
git clone https://github.com/ramydominguezc-lgtm/anthro-pic-brand.git
cd anthro-pic-brand
python3 scripts/entorno.py        # dice qué se puede hacer aquí y qué falta
python3 scripts/empaquetar.py     # arma el ZIP que se sube a Claude web
```

En **Claude Code** basta con enlazar la carpeta a `~/.claude/skills/`; en
Windows, `mklink /J "%USERPROFILE%\.claude\skills\anthro-pic-brand" "ruta"`.
En **claude.ai web** y en **desktop** se sube el ZIP.

Sistema de identidad visual de Claude y Anthropic para las piezas de ClaudeTec.
Este archivo es para **personas**. El `SKILL.md` de al lado es para Claude: es más
largo, más técnico, y no hace falta que lo leas.

---

## Qué hace y qué no

**Sí:** posts, stories, flyers, carteles, carruseles, portadas, slides, banners y
plantillas de correo con marca Claude — en Canva, Claude Design, Figma, HTML o
PowerPoint. También revisa piezas ya hechas y dice qué está fuera de marca.

**No:** no es un generador automático. No decide qué comunicar. Y **no sustituye
la aprobación de nadie**: sigue haciendo falta el visto bueno de Comunicación y,
en piezas institucionales, el de la Dirección de Liderazgo.

---

## Cómo se pide una pieza

Con la skill activa, en un chat normal. La diferencia entre un encargo que sale
bien y uno que sale regular está en cuánto contexto das:

> Necesito un post 4:5 para Instagram anunciando el bootcamp Build with Claude.
> Arranca el 18 de agosto, son cuatro sesiones, el cupo es de 60 y el formulario
> está en la bio. Va dirigido a estudiantes de cualquier carrera, sobre todo de
> primeros semestres. Quiero que se sienta accesible, no técnico.

Lo que sirve: **formato, para qué es, a quién le habla, los datos duros y el
tono**. Lo que no hace falta: decirle los colores ni las tipografías — eso ya lo
sabe, y si se lo dices a medias sale peor.

Si quieres varias opciones, pídelas de una vez: «dame tres composiciones
distintas» ahorra tres rondas.

## Lo que no decidas por tu cuenta

Estas cosas ya están resueltas y cambiarlas rompe el sistema:

- **Los colores y las tipografías.** Poppins en títulos, Lora en cuerpo, y la
  paleta de siete colores. Si una pieza necesita un color nuevo, eso se discute,
  no se improvisa.
- **El logo.** No se recolorea, no se deforma, no se le quita aire.
- **El bloque LiFE.** Su tamaño y su posición los fija el Tec, no nosotros. Toda
  pieza pública de un grupo estudiantil lo lleva, y va **más pequeño** que el
  logo de ClaudeTec.
- **Que ClaudeTec es un grupo estudiantil del Tec de Monterrey**, no una
  activación oficial de Anthropic. En piezas públicas tiene que quedar claro.

---

## Si vas a producir una pieza hoy

Ve directo a **`MANUAL-COMUNICACION.md`**: el flujo completo de un post, cómo
escribir el encargo, qué composición elegir según lo que necesitas decir, y qué
revisar antes de publicar. Este archivo es el contexto; ese es el instructivo.

## Empieza por aquí

1. Corre `python3 scripts/biblioteca.py` y abre `assets/biblioteca.html` en el
   navegador. Es el catálogo visual: filtra
   por tipo, prueba cada asset sobre los tres fondos y copia la ruta con un clic.
2. Para una pieza suelta, parte de `assets/templates/`: `poster` 1:1,
   `story` 9:16, `carrusel` 4:5, `slide` 16:9.
3. Para revisar algo hecho: `python3 scripts/validar.py mi-pieza.png`.

**Las catorce láminas de carrusel se retiraron en v2.6.** Eran un catálogo de
formas sin contenido real detrás. Lo que tiene que poder hacer un carrusel
—portada, lista, cifra, ficha de persona, cierre— está en
`references/laminas-carrusel.md`, que es la lista a cubrir al rediseñarlas.

---

## Tres reglas que se rompen seguido

1. **Al montar un carrusel, alterna los fondos.** Dos láminas seguidas con el
   mismo se leen como una sola. El orden que funciona es fuerte / limpio /
   fuerte.
2. **Clawd nunca sobre naranja.** Es naranja y desaparece. Crema, blanco u
   oscuro.
3. **Píldora naranja con texto crema da 3.0:1 y no pasa accesibilidad.** Sobre
   naranja, el texto va en `#141413`. Esto sorprende porque la propia guía de
   marca sugiere lo contrario.

## Si el validador marca algo

Tiene tres niveles. **Alta** es un error real de marca o accesibilidad y hay que
arreglarlo. **Media** merece que lo mires. **Baja** es una sugerencia —
concretamente, la de sangrado te está comparando con los posts oficiales de
@claudeai, que son más atrevidos que los nuestros. No es un error; es la
distancia que falta.

Si crees que el validador se equivoca, probablemente tengas razón: dilo en vez de
cambiar la pieza. Por eso cada veredicto se anota con sus medidas en
`references/veredictos.md`: la regla que funciona sale de comparar la tabla.

---

## Cómo se mantiene

**Lo más importante de este archivo:** las ediciones a la skill son efímeras. Si
una sesión modifica algo y no termina exportando un ZIP que alguien vuelve a
subir en Configuración → Capacidades → Skills, ese trabajo se pierde al cerrar.
Ya pasó una vez y costó cuatro sesiones. El protocolo completo está en
`VERSION.md`.

**Quién decide qué.** Los veredictos de diseño —qué se aprueba y qué no— los
registra Vicepresidencia en `references/bitacora.md`, y lo que sale de ellos
se destila en `references/reglas-derivadas.md`. Cuando apruebes o rechaces
una pieza, dilo con la razón: «no me gusta» no se puede codificar, «el titular
compite con la foto» sí.

**Qué falta hoy.** Canva: los assets están seleccionados y la guía escrita, pero
subirlos y publicar los dos primeros Brand Templates es trabajo manual que aún no
se ha hecho — unos 40 minutos, en `references/guia-canva.md`. Hasta entonces, la
ruta que Comunicación tiene disponible es el HTML de `assets/templates/`.
El resto de pendientes, en `VERSION.md`.
