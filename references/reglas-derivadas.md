# Reglas derivadas del corpus

Lo que se aprendió midiendo piezas aprobadas contra rechazadas. Esto es lo
accionable; el cómo se llegó a cada conclusión está en `bitacora.md`, que no
hace falta abrir para trabajar.

Corpus actual: la tabla de `references/veredictos.md`, 23 filas. Las imágenes
que la respaldan **no viajan en la skill**: viven en el repositorio.
Regla del archivo: **nada de adjetivos sin número detrás.**

## Al componer

1. **Sangra del lienzo.** Al menos un elemento cruza el borde: una foto que se
   sale, una tarjeta que atraviesa de lado a lado, la mascota cortada por abajo.
   Las referencias de @claudeai tocan el borde en 0.64–0.79 de su perímetro; las
   primeras piezas propias iban en 0.00–0.09, y esa era la diferencia más limpia
   entre unas y otras. La foto a sangre es la forma barata de conseguirlo.
   *Confianza alta.*

2. **Capas encabalgadas, no carriles.** Los objetos se montan unos sobre otros:
   chips sobre el titular, fotos dentro del texto, un elemento que tapa el pie.
   Que cada cosa tenga su franja limpia es exactamente lo que se lee como plano
   aunque la paleta y la tipografía sean correctas. *Confianza media.*

3. **Nada de bloques macizos grandes.** Las dos piezas peor recibidas son las
   que buscaron personalidad con áreas de color —una banda, una tarjeta— y
   ocupaban 0.86 y 0.90 de bloque macizo. Las aprobadas están en 0.00. Apunta a
   densidad de tinta ≤0.10 y a que ninguna banda o tarjeta pase de un tercio del
   lienzo. Verificable con `analizar_referencia.py`. *Confianza media.*

4. **La personalidad se construye con tipografía y ritmo, no con contenedores.**
   Numeración `01–05`, un titular a 112 px, píldoras de contorno. La variante que
   lo hizo así gustó; las que metieron color plano, no. *Confianza baja: un solo
   par de casos.*

5. **La serif es el default en piezas de comunidad.** Todas las referencias
   —Builder Club y @claudeai— usan serif editorial en el titular grande.
   Ninguna usa Poppins ahí. Poppins queda para etiquetas, datos e interfaz.
   *Confianza media.*

6. **Ninguna zona muerta grande.** Cuando una composición reserva una zona
   limpia, el texto se centra en ESA zona y crece hasta llenarla. Anclarlo
   arriba deja un hueco que se lee como error de maquetación. Ojo con el
   paginador: si la zona limpia acaba en una banda de foto, el paginador va
   ANTES de la banda, no encima.

7. **El color de fondo no predice el veredicto.** Hay aprobadas en crema y en
   naranja, y rechazadas en blanco, crema y naranja. No vale la pena optimizarlo.

## Al elegir el gráfico

7-bis. **El fondo oscuro es el que menos assets admite.** De 65 piezas revisadas,
   sobre oscuro solo funcionan: Clawd, el glifo, las variantes `--claro` de
   ilustración y los lockups claros. Ningún icono, ninguna ilustración base.
   Si la pieza va en oscuro, el gráfico se elige **antes** que el fondo.
   *Confianza alta: medido pieza por pieza, no deducido.*

## Al tratar fotos

8. **El duotono útil de esta marca es PÁLIDO.** Mapear linealmente produce un
   bloque de tinta llena que compite con el texto. Por eso `tratar_foto.py`
   tiene `--claridad`: los valores que funcionaron van de **4.6 a 5.0**.

9. **El semitono tampoco va al 100% de cobertura.** Al máximo es una mancha
   plana y pierde la textura que justifica el tratamiento.

10. **El gris de las descripciones secundarias no puede ser `--mid-gray`:**
    sobre crema queda apagado. Usa `#6f6d66`.

## Trampas técnicas (cada una costó una sesión)

11. **No fuerces `position:relative` a los hijos de `.pieza`.** Pisa el
    `position:absolute` de la píldora y del pie, que salen como bloques de ancho
    completo. *Síntoma: píldora estirada de canto a canto.* La corrección buena
    es hundir las capas de fondo a z-index negativo dentro de un
    `isolation:isolate`, sin tocar `position` de nada.

12. **`url()` dentro de una custom property se resuelve contra la hoja donde se
    USA, no contra el HTML que la declara.** Aunque `--foto` se declare inline en
    el HTML, Chromium la resuelve contra `fondos.css`. Con rutas relativas al
    HTML no encuentra nada, **no da error**, y las piezas salen grises y
    plausibles. Las rutas van relativas a `assets/templates/fondos.css`.

13. **Todo lo que un script mida se guarda sin pérdida.** Los iconos los mide
    `auditar.py`: van sin pérdida. La
    compresión con pérdida mueve los píxeles lo justo para cambiar qué colores
    lee el validador como dominantes, y aparecen hallazgos graves falsos. Solo
    lo que nadie mide —las capturas de inspiración— admite pérdida.

14. **De una referencia se copia el número, no el acomodo.** Las cinco piezas
    con foto de `piezas-aprobadas/` salieron aprobadas replicando la geometría de
    las referencias que pasó Ramses, y su reproche fue exacto: *"lo único que
    hiciste fue copiar el diseño"*. Lo que se replica es cuántas capas hay, cuánto
    aire máximo (`aire_max` ≤ 180 px), qué fracción de tinta es imagen y cuánto
    salto tipográfico. El acomodo se inventa cada vez. Señal de que se está
    calcando: varias piezas de una tanda comparten esqueleto —rótulo, titular, un
    objeto centrado, nota, pie—. Eso hundió las cinco de recursos gráficos.

## Lo que no se puede medir

Gracia, ritmo, si un chiste visual funciona, calidad de la ilustración, si el
tono suena bien para la audiencia, adecuación cultural. Para eso hace falta el
juicio de la persona: el analizador acota el espacio de búsqueda, no decide.

## Cómo anotar una pieza

```bash
python3 scripts/veredictos.py salida/mi-pieza.png --veredicto aprobada         --porque "la razón, en una frase"
```

Escribe la fila en `references/veredictos.md` con las medidas ya calculadas.
**Una pieza rechazada no se guarda como archivo, solo su fila.** Hasta la v2.11
esto era un corpus de imágenes en `referencias/`; el porqué del cambio está en la
cabecera de `scripts/veredictos.py`.

Cuando una fila nueva contradiga una regla de aquí, gana la fila: estas reglas
salieron de esa tabla.
