# Fototeca

**Permisos.** Las fotos del Expedition FEMSA vienen de `conecta.tec.mx` y
**Ramses consiguió el permiso el 17/09/2026**: se pueden publicar. Para
cualquier otra foto de terceros, preguntar antes — es parte del trabajo, no un
trámite aparte (ver `references/layout.md`).


Cinco fotos de referencia, medidas con `scripts/tratar_foto.py --recomendar`.
Los percentiles son de luminancia relativa WCAG, no la media: lo que hunde un
texto no es el brillo tipico del fondo sino su peor zona.

| Foto | p05 | mediana | p95 | Saturacion | Le va bien |
|---|---|---|---|---|---|
| `mesa-redonda` | .001 | .032 | .256 | .70 | `fondo-scrim`, `fondo-sangre`. Ya es oscura: con texto crema aguanta solo 20% de velo, asi que se ve casi entera |
| `junta-laptops` | .013 | .400 | .766 | .15 | `fondo-corte`, `fondo-banda`. Rango .75 |
| `oficina-madera` | .010 | .307 | .593 | .40 | `fondo-duotono`, `fondo-semitono`. Saturada: el duotono la unifica |
| `pizarron-equipo` | .021 | .358 | .755 | .27 | `fondo-banda`. Sin velo, a detalle pleno |
| `open-space` | .006 | .173 | .858 | .28 | `fondo-corte`, `fondo-sangre` con velo alto. Rango .85, el mayor |

**Ninguna aguanta texto encima sin velo.** Las cuatro de rango alto piden separar
las zonas —banda, corte o tarjeta— en vez de subir el velo: asi se consigue
contraste maximo y foto a detalle pleno al mismo tiempo. Es la regla de oro de
`fondos.css` y estas mediciones son su evidencia.

Para una foto nueva, midela antes de usarla:

    python3 scripts/tratar_foto.py foto.jpg --recomendar
