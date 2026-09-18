# Rama `piezas` — el archivo visual

Esta rama **no es la skill**. Es lo que la skill produjo y lo que se le dio de
referencia. Está separada de `main` a propósito.

| Rama | Qué es | Para qué sirve |
|---|---|---|
| `main` | la skill: `SKILL.md`, `references/`, `scripts/`, `assets/` | se instala y se lee al componer una pieza |
| `piezas` | las imágenes | se miran cuando hace falta ver una decisión, no se leen al trabajar |

## Por qué están separadas

Las piezas pesan ~15 MB y **ningún paso de composición las abre**. Se comprobó
buscando cada referencia a estas carpetas en los 25 scripts: sólo
`scripts/manual_pdf.py` las toca, y sólo para hacer las miniaturas del PDF.

Lo que una sesión de trabajo necesita saber de ellas está en
`references/veredictos.md` (en `main`): una fila por pieza, con sus medidas y el
motivo del veredicto. Mirar una imagen de 1080×1350 cuesta ~1,900 tokens; las 23
filas de la tabla cuestan ~700 en total. La tabla es la que se lee; las imágenes
son la prueba detrás de la tabla.

## Qué hay aquí

- **`piezas-aprobadas/`** — las 15 piezas aprobadas por Ramses, cada una con su
  PNG y el HTML que la generó. `tanda-02-imagenes/` son las diez con fotografía;
  la `10-pixel` trae además el MP4 con Clawd caminando.
- **`referencias/inspiracion/`** — capturas de material real de Anthropic y de
  Claude que Ramses cargó como dirección. No las lee ningún script: se citan en
  prosa y se miran.

## Cómo mirarlas

Desde GitHub, con el selector de rama. En local, **sin cambiar de rama** en tu
carpeta de trabajo (te borraría los archivos del escritorio):

```bash
git worktree add ../piezas-archivo piezas
```

Eso te deja las imágenes en una carpeta hermana. Para quitarla:
`git worktree remove ../piezas-archivo`.

## Cómo se actualiza

Cuando se apruebe una pieza nueva:

```bash
git worktree add ../piezas-archivo piezas
cp salida/la-pieza.png ../piezas-archivo/piezas-aprobadas/
cd ../piezas-archivo && git add -A && git commit -m "pieza nueva" && git push
```

Y su fila en `references/veredictos.md`, que va en `main`, con
`scripts/veredictos.py`.
