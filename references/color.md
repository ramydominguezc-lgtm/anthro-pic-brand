# Color

## Paleta principal

| Nombre | Hex | RGB | Uso |
|---|---|---|---|
| Dark | `#141413` | 20, 20, 19 | Texto principal, fondos oscuros |
| Light | `#faf9f5` | 250, 249, 245 | Fondo por defecto, texto sobre oscuro |
| Mid Gray | `#b0aea5` | 176, 174, 165 | Texto secundario, líneas, bordes |
| Light Gray | `#e8e6dc` | 232, 230, 220 | Fondos sutiles, tarjetas, badges |

## Acentos

| Nombre | Hex | RGB | Uso |
|---|---|---|---|
| Orange | `#d97757` | 217, 119, 87 | Acento primario — CTAs, fondos completos, formas |
| Blue | `#6a9bcc` | 106, 155, 204 | Acento secundario — links, estados informativos |
| Green | `#788c5d` | 120, 140, 93 | Acento terciario — estados positivos, categorías |

El naranja es *el* color de Claude. Azul y verde existen para dar aire a un
sistema que de otro modo sería monocromo; se rotan **entre** piezas de una serie,
no dentro de una pieza. Tres acentos juntos en la misma composición se ven a
desorden, no a variedad.

## Combinaciones aprobadas

| Fondo | Texto | Acento | Notas |
|---|---|---|---|
| `#faf9f5` | `#141413` | naranja | Default. El 80% de las piezas. |
| `#141413` | `#faf9f5` | naranja | Modo oscuro, slides de cierre, banners. |
| `#d97757` | `#faf9f5` | — | Pieza de acento completo. Sin más color encima. |
| `#e8e6dc` | `#141413` | naranja | Tarjetas y bloques dentro de fondo claro. |

Nunca: naranja sobre naranja, texto gris medio sobre claro para lectura, acento
sobre acento, o dos acentos distintos tocándose.

## Jerarquía tipo (web/UI)

```
Fondo de página     #faf9f5
Texto principal     #141413
Título de sección   Poppins Bold, #141413
Subtítulo           Poppins SemiBold, #b0aea5
Cuerpo              Lora Regular, #141413
Botón primario      fondo #d97757, texto #faf9f5
Link / acento       #6a9bcc
Badge               fondo #e8e6dc, texto #141413
Borde / divisor     #b0aea5 a 1px, o #e8e6dc para separadores suaves
```

## Tokens CSS

```css
:root {
  --dark:       #141413;
  --light:      #faf9f5;
  --mid-gray:   #b0aea5;
  --light-gray: #e8e6dc;
  --orange:     #d97757;
  --blue:       #6a9bcc;
  --green:      #788c5d;

  /* dialecto editorial / Builder Club */
  --clay:       #cc785c;
  --ivory:      #f0eee6;
}
```

## Accesibilidad

- `#141413` sobre `#faf9f5` → contraste ~17:1. Cumple AAA.
- `#faf9f5` sobre `#d97757` → ~3.2:1. Solo para texto de 24pt+ o bold; **no**
  para cuerpo pequeño.
- `#141413` sobre `#d97757` → ~5.9:1. Es la opción segura para texto chico sobre naranja.
- `#b0aea5` sobre `#faf9f5` → ~2:1. Decorativo y subtítulos grandes únicamente,
  jamás párrafos.
