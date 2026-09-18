# Inspiración — capturas de @claudeai

Trece capturas de pantalla de posts oficiales de la cuenta de Claude, guardadas
como referencia de gusto.

**No son piezas de ClaudeTec y no se validan.** Son capturas de Instagram: traen
cromo de la app, proporción de pantalla de teléfono y colores fotográficos fuera
de la paleta. Pasarlas por `validar.py` produce fallos graves que no significan
nada, y de paso hunde el test de regresión.

Estaban en `aprobadas/` y se movieron aquí el 15 de agosto de 2026. La distinción
que importa:

- `aprobadas/` y `rechazadas/` — **piezas producidas por este sistema**, con
  veredicto de Ramses. Son el patrón contra el que se calibra `validar.py`.
- `inspiracion/` — trabajo ajeno que sirve de referencia de gusto. Se mira, no
  se mide.

De aquí sale, entre otras cosas, el rango de sangrado de 0.64 a 0.79 que cita
`validar.py`: es el nivel de @claudeai, no el nivel actual de ClaudeTec.
