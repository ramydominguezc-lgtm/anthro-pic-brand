# Cierre animado — logo ClaudeTec

Réplica cuadro a cuadro del cierre del logo de Claude (el que aparece al final de los
videos de @claudeai), con el logo de ClaudeTec. Pedido por Ramses el 26/10/2026:
"exactamente idéntica, solo que con el logo de ClaudeTec". Va **al final de cada reel**.

## Qué pasa en pantalla (100 cuadros a 30 fps = 3.33 s)

| Cuadros | Qué hace |
|---|---|
| 0 | Un punto naranja en el centro del logo completo |
| 1–12 | Se abre en estrella y crece; el trazo cambia cada 2–3 cuadros (dibujado a mano) |
| 13–19 | Llega a su tamaño máximo (1.35× el final) y empieza a ir a la izquierda |
| 17–24 | Se desliza a su lugar dejando una estela; la palabra se descubre con cortinilla |
| 25–99 | Logo quieto; la estrella sigue "respirando" (cambia de dibujo cada ~3 cuadros) |

Los 43 dibujos de la estrella se extrajeron de la referencia (no se redibujaron) y se
limpiaron a 480 px. El lockup de ClaudeTec tiene la misma proporción estrella/palabra
que el de Claude (1.16 vs 1.18), por eso la animación se transfiere sin deformarse.

## Archivos

| Archivo | Para qué |
|---|---|
| `cierre-claudetec-reel.mp4` | 1080×1920, fondo durazno de la referencia `#e3c9bb` |
| `cierre-claudetec-post.mp4` | 1080×1350 |
| `cierre-claudetec-16x9.mp4` | 1920×1080 |
| `cierre-claudetec-reel-transparente.mov` | ProRes 4444 con alfa, para montarlo sobre video |
| `estrella-sprites.png` | Los 43 dibujos (rejilla de 7, 480 px, solo alfa) |
| `linea.json` | Por cuadro: dibujo, posición de la estrella y avance de la cortinilla |
| `palabra-oscura.png` / `palabra-clara.png` | La palabra del SVG sin la estrella, a 5604×846 |

## Regenerar a otra medida o color

```bash
python scripts/cierre_claudetec.py salida.mp4 --ancho 1080 --alto 1350 --logo 620
python scripts/cierre_claudetec.py salida.mp4 --fondo "#faf9f5" --seg 4    # más largo: la estrella sigue respirando
python scripts/cierre_claudetec.py salida.mov --transparente
python scripts/cierre_claudetec.py salida.mp4 --fondo "#141413" --clara     # fondo oscuro
```

Solo necesita Pillow y ffmpeg.
