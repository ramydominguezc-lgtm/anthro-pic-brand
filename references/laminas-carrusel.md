# Láminas de carrusel — qué hace falta que exista

Las catorce láminas v1 se retiraron en v2.6 por obsoletas. Este archivo guarda
**para qué servía cada una**, que es lo único que valía la pena conservar: el
inventario de trabajos que un carrusel tiene que poder hacer.

No es una especificación de diseño. Es la lista de necesidades que el rediseño
tiene que cubrir, para que no se olvide ninguna al rehacerlas.

Formato de carrusel: **1080 × 1350** (4:5).

## Las catorce funciones

| # | Trabajo | Para qué se usa | Lleva |
|---|---|---|---|
| 01 | **Portada con foto** | Anuncio, apertura de serie | Foto a sangre, titular abajo |
| 02 | **Lista numerada** | Temario, reglas, top 5 | Filas numeradas que reparten el alto |
| 03 | **Titular suelto** | Una idea, un mito, una pregunta | Un titular grande y una línea |
| 04 | **Texto sobre foto** | Cita, testimonio, definición | Bloque de texto largo sobre foto |
| 05 | **Cifra** | Meta, resultado, precio, aforo | Una cifra gigante y su contexto |
| 06 | **Lista con banda** | Pasos, requisitos, qué traer | Lista arriba, banda de foto abajo |
| 07 | **Dos columnas** | Antes/después, mito/realidad, A/B | Dos columnas enfrentadas |
| 08 | **Filas de valor** | Horario, precios, especificaciones | Etiqueta izquierda, valor derecha |
| 09 | **Ficha de persona** | Mesa directiva, ponente, proyecto | Imagen arriba, ficha abajo |
| 10 | **Solape** | Persona, producto, captura | Cuadro que solapa una tarjeta que sangra |
| 11 | **Tarjeta con ilustración** | Concepto, recurso, anuncio | Tarjeta que sangra, dibujo cruzando el canto |
| 12 | **Ilustración centrada** | Concepto, resumen, cierre suave | Ilustración despegada del borde |
| 13 | **Índice** | Índice de la serie, recapitulación | Lista de lo que trae el carrusel |
| 14 | **Cierre** | Inscripción, fecha límite, CTA | Llamada a la acción sobre fondo fuerte |

## Lo que se agrupa al rehacerlas

Catorce son demasiadas y varias hacían el mismo trabajo. Al rediseñar,
**02, 08 y 13 son la misma lámina** —una lista con dos niveles— y **09 y 10**
también: una ficha con imagen. Con siete u ocho bien resueltas se cubre todo.

## Por qué se retiraron

Nacieron como catálogo de formas abstractas, sin contenido real detrás. De ahí
sus defectos: zonas muertas donde nadie sabía qué iba a ir, titulares en Poppins
cuando la evidencia pedía serif, y texto de relleno. Ninguna llegó a votarse en
el visor.

**El método para las nuevas:** empezar por tres láminas de un carrusel que se
vaya a publicar de verdad, con el texto real. La forma sale del contenido, no al
revés.

## Fondos que tenían

Los tratamientos de foto siguen disponibles en `assets/templates/fondos.css` y no
dependían de las láminas: `fondo-scrim`, `fondo-sangre`, `fondo-banda`,
`fondo-duotono`, `fondo-semitono`, `fondo-rayas`, `fondo-desenfoque`,
`fondo-papel`. Son doce en total y se aplican a cualquier `.pieza`.
