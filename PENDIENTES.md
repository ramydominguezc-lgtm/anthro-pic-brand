# Pendientes y decisiones abiertas

Lista viva. Se actualiza en cada sesión: lo cerrado se tacha con su versión, lo
nuevo se añade arriba de su bloque. Última revisión: **17 de septiembre de 2026 · v2.15**

Tres estados: **Decisión de Ramses** (no se toca sin su visto bueno porque rompe
algo), **Bloqueado** (falta información que solo él tiene), **Listo para hacer**
(no rompe nada, solo falta tiempo).

---

## Decisión de Ramses — rompen algo que ya funciona

| # | Qué | Por qué no se ha hecho |
|---|---|---|
| 1 | **Confirmar 06, 07 y 08 de la tanda 02** | Las tres se rehicieron con tu veredicto. La 06 y la 07 son versiones nuevas de cero: dijiste que si no convencen quedan descartadas. La 08 solo cambió de acomodo |
| 2 | **Sacar `piezas-aprobadas/` del ZIP** | Son 33 archivos y 14.5 MB de los 195 que caben (el tope son 200). Es material entregable tuyo, no herramienta, y `veredictos.md` ya lleva lo que la sesión necesita de esas piezas. Sin ella la skill baja a 162 archivos y 17.45 MB. No lo toco sin tu visto bueno porque cambia qué recibe una sesión nueva |
| 3 | **Dónde vive el manual interactivo** | El PDF está hecho. La galería viva —piezas nuevas según se aprueban— pide un artifact, que es lo único que se actualiza sin reimprimir |

## Bloqueado — falta información que solo tiene Ramses

| # | Qué | Qué hace falta |
|---|---|---|
| 4 | **Rediseño de las láminas de carrusel** | La lista de lo que tienen que cubrir está en `references/laminas-carrusel.md`. Falta empezar por tres de un carrusel real, con texto de verdad |
| 5 | **Logo LiFE** | No hay archivo. Si una pieza de grupo estudiantil tiene que llevarlo, hace falta el original |

## Listo para hacer — no rompe nada

| # | Qué | Nota |
|---|---|---|
| 6 | **Subir el ZIP a Claude web** | Nada lo bloquea ya. Protocolo en `VERSION.md` |
| 7 | **Montar el Brand Kit en Canva** | Son pasos manuales dentro de Canva, ~40 min. El paquete de subida lo arma `scripts/preparar_canva.py` y el procedimiento está en `references/guia-canva.md` |

---

## Cerrado

- ~~Veredicto de la tanda 02~~ · v2.15 — dado. 01, 02, 04, 05 y 09 aprobadas
  tal cual; 03 y 10 aprobadas con corrección; 06, 07 y 08 rehechas y a la
  espera de confirmación (fila 1)
- ~~Qué pixel usar para titular~~ · v2.15 — **Press Start 2P**. Pixelify Sans
  fuera por ilegible: redondea la esquina y la `D` se lee `O`. No se vuelve a
  proponer una pixel de esquina redondeada
- ~~Qué tramas de fondo se quedan vivas~~ · v2.13 — las once, cerradas. No se
  vuelve a preguntar
- ~~Más colores en la paleta~~ · v2.13 — cerrada. Celeste, verde claro y lila
  como principales; azul y verde como contrapartes fuertes. No se añaden más
- ~~La sombra acotada de `capas.css`~~ · v2.13 — **aprobada por Ramses.** Ya no
  es excepción a debate: es regla. Anotada en `capas.css` y en `capas.md`
- ~~Permiso de las fotos de Conecta Tec~~ · v2.13 — concedido. Anotado en
  `assets/fotos/LEEME.md`
- ~~Las seis versiones de patrocinio~~ · v2.13 — entregadas; los archivos se
  retiraron de `salida/`
- ~~Material real para el primer collage~~ · v2.13 — no hace falta: la
  herramienta está probada y la receta la escribe Ramses cuando toque
- ~~Corpus de `regresion.py` vacío~~ · v2.12 — se retiró el corpus de imágenes
  entero. Lo sustituye `references/veredictos.md`
- ~~Conectar con las skills de animaciones~~ · v2.12 — puente
  `scripts/clawd_biblioteca.py` y referencias cruzadas en las tres
- ~~`flags.json` de la bandera~~ · la animación existe y está aprobada en
  `clawd-biblioteca`
- ~~Contexto de ClaudeTec~~ · v2.6 — en `references/claudetec.md`
- ~~Las 14 láminas obsoletas~~ · v2.6 — su función en `laminas-carrusel.md`
- ~~WebP en la biblioteca~~ · v2.4 — solo PNG y SVG
