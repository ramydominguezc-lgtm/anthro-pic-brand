# Recursos compositivos

Este archivo existe porque el resto de la skill son **prohibiciones** —no
degradados, un acento, márgenes iguales, un gráfico— y con eso solo se puede
producir trabajo correcto y muerto. Aquí están los permisos: movimientos concretos
para que una pieza tenga interés, cada uno sacado de una referencia real y con su
código listo para pegar.

**Regla de uso: toda pieza debe usar al menos dos de estos recursos.** Una pieza
con cero es la que sale plana aunque la paleta y la tipografía estén bien.
`scripts/validar.py` lo revisa.

---

## 1 · Sangrar del lienzo

El más importante y el que más faltaba. Al menos un elemento cruza el borde: una
tarjeta que atraviesa de lado a lado, una foto que se sale, la mascota cortada por
abajo.

Medido: las referencias tocan el borde en 0.64–0.79 de su perímetro; las piezas
propias iban en 0.00–0.09.

```css
.tarjeta{position:absolute; left:-46px; right:-46px; top:150px; bottom:104px}
.clawd{position:absolute; right:-40px; bottom:-30px; width:220px}
```

## 2 · Canto irregular

Una tarjeta clara sobre naranja con el borde ondulado, como papel rasgado, en vez
de `border-radius`. Es la diferencia entre "recuadro de PowerPoint" y "collage".

```css
clip-path:polygon(0 1.2%,18% 0,42% 1.6%,71% .3%,100% 1.4%,
                  100% 98.4%,74% 100%,45% 98.6%,20% 99.8%,0 98.6%);
```

## 3 · Label de carga en la esquina

Una label animada de la biblioteca de Clawd (`✻ Working…`, `Pondering…`), en
inglés y como **detalle mínimo**. Ramses rechazó la versión anterior (chips
blancos rotados, 3–4 por pieza, encima del titular) el 28/10/2026: *"roban
mucho protagonismo"*.

- **Solo la palabra animada.** Sin fondo blanco, sin caja, sin borde ni píldora.
  Sobre foto, una sombra suave (`drop-shadow(0 1px 3px rgba(20,20,19,.45))`)
  basta para que se lea.
- **Siempre horizontal.** Nada de rotarla.
- **En una esquina**, superior o inferior. Nunca centrada, nunca sobre el
  titular ni sobre una cara. En reels, dentro de la zona segura (250 px arriba,
  320 px abajo).
- **Pequeña:** 44–60 px de alto de renglón en 1080 px de ancho.
- **Cuántas:** 1–2 por reel como máximo. En posts y carruseles, de preferencia
  ninguna; una en toda la pieza como mucho.
- **Ante la duda, quítala.** La pieza no la necesita.

```css
.label-carga{position:absolute; top:270px; left:70px; height:60px;
             filter:drop-shadow(0 1px 3px rgba(20,20,19,.45))}  /* GIF/PNG -claro, sin caja */
```

## 4 · Píldora de estado sólida

Arriba a la derecha, en color pleno —naranja o verde— con una palabra: *Nuevo*,
*Última llamada*, *Convocatoria*. Distinta de la píldora de contorno: esta grita.

```css
.estado{background:var(--orange); color:#fff; border-radius:999px;
        padding:11px 30px; font:700 22px 'Poppins',sans-serif}
```

## 5 · Imagen intercalada en el titular

En vez de titular arriba e imagen abajo, las fotos se meten **entre las líneas**
del titular. Es el recurso que más cambia la sensación de una pieza.

```css
h1{font-size:96px; line-height:1.0}
h1 .foto{float:left; width:230px; margin:8px 22px 6px 0}
```

## 6 · Rotación leve

Dos o tres grados en chips, etiquetas o fotos pequeñas. Suficiente para que se lea
como colocado a mano; más de cinco grados se ve a error.

## 7 · Marca dibujada a mano

Una flecha, un subrayado o un círculo trazados a mano alzada, saliendo del cuadro y
sugiriendo continuación. Va en `#141413`, trazo de grosor uniforme.

## 8 · Marco de color

El fondo naranja no como fondo, sino como **marco delgado** alrededor de una
tarjeta casi a sangre. Invierte la jerarquía: el color enmarca, no domina.

## 9 · Palabra en acento dentro del titular

Una sola palabra del titular en naranja, el resto en oscuro. Da un punto focal sin
añadir un elemento más.

```html
<h1>Se abren <b style="color:var(--orange)">convocatorias</b></h1>
```

## 10 · Solape deliberado

Los objetos se montan unos sobre otros: el mockup tapa el pie, el chip cruza el
canto de la tarjeta, la foto invade el titular. **Nada de carriles.** Que cada cosa
tenga su franja limpia es exactamente lo que se lee como plano.

## 11 · Serif grande para el titular

Todas las referencias —Builder Club y @claudeai— usan serif editorial en el titular
grande. Ninguna usa Poppins ahí. Para piezas de comunidad, la serif es el punto de
partida; Poppins queda para etiquetas, datos e interfaz.

---

## Capas, ventanas y fotos

Los recursos 2, 8 y 10 (canto irregular, marco de color, solape) tienen ahora
implementacion lista en `assets/templates/capas.css`, mas cintas, ventanas de
terminal y navegador, y tres patrones de acomodo de imagenes. Estan
explicados en `references/capas.md`.

## Lo que sigue prohibido

Estos permisos no cancelan el sistema. Se mantienen: sin degradados, sin sombras
suaves, sin glow, un solo acento dominante, sentence case, y la jerarquía de logos
del Tec. La personalidad se construye con **capas y ritmo**, no con efectos.
