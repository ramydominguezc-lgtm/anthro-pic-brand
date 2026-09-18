# Piezas aprobadas

Cinco posts 1080×1350 que Ramses aprobó sin correcciones el 17/09/2026. Salieron
de la tanda de diez de `salida/diez_posts.py`.

**No son láminas oficiales.** No se referencian desde `SKILL.md`, no entran en el
visor y no hay que replicarlas. Están aquí por dos motivos: son material
publicable tal cual, y son el único conjunto medido de lo que sí funciona.

| Archivo | Recurso | De qué va |
|---|---|---|
| `01-foto-capas` | foto de contexto atenuada + foto nítida encima + chip | titular sobre fondo oscuro |
| `02-foto-ficha` | foto con ficha solapada en la esquina | pieza más «documental» |
| `03-foto-sangre` | foto a sangre completa con velo | titular sobre imagen |
| `04-foto-arriba` | foto arriba a sangre, texto abajo | reparto en dos mitades |
| `05-par-fotos` | dos fotos en fila, cada una con su ficha | antes / después |

Cada `.html` es editable y vuelve a rendear tal cual: las rutas `../assets/…`
resuelven igual desde esta carpeta que desde `salida/`.

---

## Qué las separa de las rechazadas

No es el gusto, y se puede medir. `scripts/analizar_referencia.py` sobre las diez:

| | `aire_max` | `sangra` | veredicto |
|---|---|---|---|
| 03 foto a sangre | 0 | 0.70 | aprobada |
| 04 foto arriba | 0 | 0.89 | aprobada |
| 01 foto capas | 0 | 0.35 | aprobada |
| 02 foto ficha | 82 | 0.00 | aprobada |
| 05 par de fotos | 171 | 0.00 | aprobada |
| 06 terminal (v1) | **251** | 0.00 | rechazada |
| 10 Clawd (v1) | **293** | 0.41 | rechazada |
| 07 navegador (v1) | **579** | 0.00 | rechazada |

`aire_max` es la franja horizontal **completamente vacía** más alta del lienzo.
Ninguna aprobada pasa de 171 px; ninguna rechazada por acomodo baja de 251.

> **Regla:** ningún hueco vacío de más de **180 px** en una pieza 1080×1350.
> Si sobra sitio, crece la tipografía, baja el objeto o entra una capa
> —una cinta, una ficha, Clawd—. No se deja el hueco.

Las otras dos rechazadas (08 y 09) no fallaban por aire sino por contenido: una
era una cifra gigante ocupando el lienzo entero y la otra una ilustración sola
en medio. También están descartadas.

---

## Lo que NO hay que aprender de aquí

Ramses señaló, con razón, que estas cinco copian el acomodo de las referencias
que él pasó. Copiar el acomodo no es el encargo.

Lo que se replica es el **número**: cuántas capas, cuánto aire máximo, qué
fracción de tinta es imagen, cuánto salto tipográfico. El acomodo se inventa
cada vez. Una pieza nueva es correcta si da los números de esta tabla **con una
geometría que no esté aquí**, no si se parece a la 03.

El modo de fallo contrario también está documentado: las cinco piezas de
recursos gráficos compartían un mismo esqueleto —rótulo, titular, un objeto
centrado, nota, pie— repetido cinco veces. Ese esqueleto es lo que las hundió,
no el objeto de cada una.
