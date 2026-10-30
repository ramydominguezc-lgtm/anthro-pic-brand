# Perfiles de grupo

Cada grupo estudiantil tiene su propia identidad visual. Las reglas del manual LiFE no cambian; lo que cambia es la paleta, la tipografía y el tono. Aquí se guardan esos perfiles para que las piezas de un mismo grupo salgan consistentes entre sí.

## Cómo se ve un perfil

Un perfil útil cabe en pocas líneas y responde: qué colores, qué tipografía, qué tono, y dónde está el logo.

```markdown
## [Nombre del grupo]

- **Logo**: assets/life/logos/grupos/[archivo].png  (o "sin logo — wordmark tipográfico")
- **Paleta**:
  --acento:    #XXXXXX
  --fondo:     #XXXXXX
  --texto:     #XXXXXX
  --apoyo:     #XXXXXX
- **Tipografía**: titulares [fuente], texto [fuente]
- **Tono**: [dos o tres adjetivos, y qué evitar]
- **Handle IG**: @xxxx
```

## Cómo construir uno cuando el grupo no lo tiene

La mayoría de los grupos no tienen manual de marca — tienen un logo y un color que "siempre usan". Con eso basta:

1. **Del logo salen los colores.** Toma el color dominante como acento. Si el logo es monocromático, el acento puede ser un color que el grupo ya use en sus redes.
2. **Un solo acento por pieza.** Si necesitas jerarquía extra, cámbiale peso o tamaño al texto antes de meter otro color. Los flyers estudiantiles se arruinan casi siempre por exceso de colores, no por falta.
3. **Fondo claro o fondo oscuro, no ambos en la misma campaña.** El fondo define qué variante del logo LiFE toca: fondo claro → logo negro; fondo oscuro → logo blanco.
4. **Contraste real.** Texto sobre fondo con contraste suficiente para leerse en un celular a plena luz. Si dudas, oscurece el texto.
5. **Confirma antes de producir.** Enseña la paleta propuesta y espera visto bueno; es más rápido que rehacer tres piezas.

Al terminar, ofrece agregar el perfil a este archivo.

## Paletas de arranque

Si el grupo no tiene nada y hay que proponer, estas combinaciones funcionan y no se parecen a la plantilla genérica de Canva. Son puntos de partida para adaptar, no una identidad prefabricada:

**Vino**
```css
--acento:#8C3A4A; --fondo:#F7F3F0; --texto:#22181A; --apoyo:#E7D3D6;
```

**Azul profundo**
```css
--acento:#2B5FAB; --fondo:#F5F7FA; --texto:#0E1B2E; --apoyo:#CFE0F5;
```

**Verde bosque**
```css
--acento:#3E7C59; --fondo:#F3F5F0; --texto:#16241B; --apoyo:#D7E4D3;
```

**Oscura / alto contraste**
```css
--acento:#E4B33C; --fondo:#16171A; --texto:#FFFFFF; --apoyo:#333333;
```

Dos advertencias:

- El azul institucional del Tec pertenece a la universidad, no al grupo. Úsalo solo donde el manual lo pida, nunca como color de marca propio.
- Si el grupo lleva en su nombre la marca de una empresa, su paleta corporativa tampoco es de uso libre. Esa identidad se maneja aparte, con los lineamientos de su dueño; este módulo solo cubre las reglas del Tec.

## Tipografías disponibles

`scripts/fuentes_life.sh` instala Poppins (titulares, geométrica), Inter (interfaz y datos) y Lora (serif, para piezas con tono editorial o constancias). Se pueden instalar otras del mismo modo: `npm i @fontsource/<nombre>` y apuntar el `@font-face` a `node_modules/@fontsource/<nombre>/files/`. Google Fonts por CDN no carga en el contenedor; npm sí.

Combinaciones que funcionan:

| Tono del grupo | Titulares | Texto |
|---|---|---|
| Técnico, directo | Inter 700 | Inter 400 |
| Cálido, humano | Poppins 700 | Inter 400 |
| Editorial, formal | Lora 600 | Inter 400 |

---

# Perfiles guardados

*(vacío — los perfiles se van agregando conforme se trabaje con cada grupo)*

Formato: usa la plantilla del inicio de este archivo. Un perfil por grupo, con su
logo, paleta, tipografía y tono.
