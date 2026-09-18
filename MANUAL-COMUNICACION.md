# Manual de producción — Dirección de Comunicación

Cómo sacar un post de ClaudeTec, de principio a fin.

El `README.md` explica qué es esta skill. Este manual explica **cómo se usa un
martes por la tarde cuando hay que anunciar un taller**.

No necesitas saber diseño ni programar. Necesitas saber qué quieres comunicar.

---

## El flujo completo

```
1. Escribes el encargo   →  2. Eliges la forma  →  3. Revisas
        (2 min)                  (1 min)            (5 min)
                                                        ↓
                                            4. Publicas con bloque LiFE
```

Los cuatro pasos importan, pero **el paso 1 decide la calidad de todo lo demás**.
Un encargo vago produce una pieza vaga, y arreglarla cuesta más que haberla
pedido bien.

---

## Paso 1 · Escribir el encargo

Abre un chat con la skill activa y escribe qué necesitas. Cinco cosas hacen la
diferencia:

| Qué decir | Por qué |
|---|---|
| **El formato** | «post 4:5 para Instagram», «story», «carrusel de 5 láminas» |
| **Para qué es** | anunciar, explicar, invitar, recapitular, presentar a alguien |
| **A quién le habla** | no es lo mismo primer semestre que la mesa directiva |
| **Los datos duros** | fechas, horas, lugar, cupo, dónde se inscriben |
| **El tono** | accesible, formal, celebratorio, urgente |

Lo que **no** hace falta decir: colores, tipografías, tamaños. Eso ya está
resuelto, y darlo a medias empeora el resultado.

### Un encargo que funciona

> Necesito un post 4:5 para Instagram anunciando el bootcamp Build with Claude.
> Arranca el lunes 18 de agosto, son cuatro sesiones de 18:00 a 20:00 en el aula
> CETEC Sur 3.401, cupo de 60 y el formulario está en la bio. Va para estudiantes
> de cualquier carrera, sobre todo primeros semestres. Que se sienta accesible,
> no técnico. Dame tres opciones.

### El mismo encargo mal escrito

> Hazme un post del bootcamp, bonito, con naranja.

El segundo produce algo genérico y arranca tres rondas de correcciones. El
primero suele acertar a la primera.

### Pide varias opciones de una vez

«Dame tres composiciones distintas» cuesta lo mismo que pedir una y te ahorra dos
rondas. Elegir entre tres es más rápido que corregir una.

---

## Paso 2 · Elegir la forma

Hay catorce composiciones aprobadas. **Los nombres describen cómo se reparte el
lienzo, no de qué habla el ejemplo.** `09-corte-foto-ficha` no es «la plantilla
de perfiles»: es imagen arriba y ficha abajo, y sirve igual para una persona, un
proyecto o una herramienta.

Las catorce láminas de la v1 **se retiraron**: eran un catálogo de formas sin
contenido real detrás. Lo que un carrusel tiene que poder hacer —portada, lista,
cifra, comparación, ficha de persona, índice, cierre— está en
`references/laminas-carrusel.md`.

Mientras se rediseñan, **describe la necesidad en el encargo** en vez de pedir
una lámina por número: «una lámina para presentar a la mesa directiva», «una
para el temario». Es como conviene pedirlo de todos modos — a veces la forma
correcta no es la que tenías en mente.

### Montar un carrusel

**Alterna los fondos.** Dos láminas seguidas con el mismo tratamiento se leen
como una sola y el lector pasa de largo. El orden que funciona es
*fuerte / limpio / fuerte*.

Un carrusel de cinco que funciona: `01` portada con foto → `02` el temario →
`05` la cifra → `08` el horario → `14` el cierre con la inscripción.

---

## Paso 3 · Fotos

Si vas a meter una foto que no está en la biblioteca, **mídela antes**:

```
python3 scripts/tratar_foto.py mi-foto.jpg --recomendar
```

Te dice qué tratamiento aguanta y cuánto velo necesita para que el texto se lea.
Tarda cinco segundos y evita el error más común: subir el velo hasta que la foto
se convierte en una mancha gris.

**La regla que más se malinterpreta:** contraste y visibilidad de la foto no
están reñidos. Lo parecen mientras el texto se apoye *encima* de la foto. Si
necesitas que el texto se lea perfecto **y** que la foto se vea a detalle, no
subas el velo — usa una composición que separe las zonas: `06-lista-con-banda`,
`08-filas-valor`, `09-corte-foto-ficha`.

**El salmón de la marca no es un color.** Es una foto en duotono naranja. Si
quieres ese tono, trata una foto; no pongas un hex parecido, porque cae fuera de
la paleta.

---

## Paso 4 · Revisar antes de publicar

Tres cosas, en este orden.

**1. El bloque LiFE.** Ninguna plantilla de la skill lo trae, a propósito: son
composiciones, no piezas publicables. Toda pieza pública de un grupo estudiantil
lo lleva, **más pequeño que el logo de ClaudeTec**, y debe quedar claro que
ClaudeTec es un grupo estudiantil del Tec de Monterrey, no una activación oficial
de Anthropic. Pídelo explícitamente: «añade el bloque LiFE».

**2. El validador.** Exporta el PNG y corre:

```
python3 scripts/validar.py mi-pieza.png
```

Tres niveles:

- **alta** — error real de marca o accesibilidad. Se arregla antes de publicar.
- **media** — míralo. A veces es una decisión deliberada, como una foto a sangre
  con margen cero.
- **baja** — sugerencia. La de sangrado te compara con los posts oficiales de
  @claudeai, que son más atrevidos que los nuestros. No es un error.

**Si crees que el validador se equivoca, probablemente tengas razón.** Dilo en
vez de cambiar la pieza para complacerlo. Ha pasado dos veces ya, y las dos veces
el mal calibrado era el script.

**3. Los ojos.** El validador mide color, contraste y márgenes. No sabe si el
titular dice lo que quieres decir, ni si la foto elegida es la correcta. Eso lo
ves tú.

---

## Recetas rápidas

### Anuncio de taller (lo más frecuente)

> Post 4:5 anunciando el taller de [tema] del [fecha] a las [hora] en [lugar].
> Cupo [n], inscripción en la bio. Público: [quién]. Usa la 01 si tengo foto del
> lugar, o la 03 si no.

### Ficha de la mesa directiva

> Ficha con la 09 para [nombre], [cargo]. Datos: en ClaudeTec hace [x], también
> es [y], busca [z]. Todavía no tengo el retrato, deja el hueco rotulado.

El hueco rotulado dice qué medida y qué encuadre necesitas: llévaselo así al
fotógrafo.

### Recapitulación de evento

> Carrusel de cuatro: portada con foto del evento, la cifra de asistentes,
> dos testimonios y un cierre invitando al siguiente.

### Story

> Story 9:16 con [mensaje]. Sin texto pequeño: en story nadie lee menos de 28 px.

---

## Cuando algo sale mal

**«No me gusta pero no sé por qué.»** Descríbelo por partes: ¿el titular compite
con la foto? ¿sobra aire abajo? ¿el gris se pierde? Cada una tiene arreglo
distinto. «No me gusta» no se puede codificar; «el titular compite con la foto»
sí, y además queda anotado para que no se repita.

**La pieza salió plausible pero sin foto.** Casi siempre es una ruta rota. Las
rutas de `--foto` van relativas a `fondos.css`, no al HTML. No da error: sale
gris y creíble.

**Las tipografías se ven raras.** Si algo se ve en Arial o Times, las fuentes no
cargaron. Poppins y Lora están en `assets/fonts/` como archivos locales; si la
pieza se mueve de carpeta, se rompen.

**El generador de Canva metió un degradado.** No lo uses para piezas desde cero.
Aplica el Brand Kit pero no conoce las reglas de composición: mete degradados de
dos colores, centra el texto y apila acentos. Parte siempre de un Brand Template
propio.

---

## Las cinco cosas que se rompen más seguido

1. **Clawd sobre naranja.** Clawd es naranja y desaparece. Crema, blanco u
   oscuro.
2. **Píldora naranja con texto crema.** Da 3.0:1 y no pasa accesibilidad. Sobre
   naranja, el texto va en `#141413`. Sorprende porque la guía de marca sugiere
   lo contrario.
3. **Dos láminas seguidas con el mismo fondo** en un carrusel.
4. **Publicar sin el bloque LiFE.**
5. **Mezclar el Clawd caminando con el Clawd base.** Son dibujos distintos —
   cuerpo de 8 celdas contra 12. Los dos son válidos; juntos parecen un error.

---

## Qué no decidas por tu cuenta

Estas cosas ya están resueltas y cambiarlas rompe el sistema. Si una pieza
parece necesitarlas, se discute — no se improvisa:

- Los colores y las tipografías.
- El logo: no se recolorea, no se deforma, no se le quita aire.
- El tamaño y la posición del bloque LiFE, que los fija el Tec.
- La declaración de que ClaudeTec es un grupo estudiantil, no una activación de
  Anthropic.

---

## Y lo más importante para que esto siga funcionando

**Cuando apruebes o rechaces una pieza, dilo con la razón.** Los veredictos se
registran en `references/bitacora.md` y son lo que hace que el sistema mejore. El
corpus tiene hoy dieciséis piezas aprobadas y tres rechazadas; cada veredicto
nuevo lo hace más preciso.

Y si alguien modifica la skill, la sesión tiene que terminar exportando el ZIP y
volviéndolo a subir en Configuración → Capacidades → Skills. **Una sesión que
toca la skill y no acaba en subida, no ocurrió.** Ya se perdieron cuatro
sesiones de trabajo por saltarse esto. El protocolo está en `VERSION.md`.
