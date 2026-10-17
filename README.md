# Calendario UNIR

Calendario del campus de UNIR publicado como suscripción `.ics`.

**Enlace de suscripción:** https://raw.githubusercontent.com/AgustinaLorusso/cal-unir-2089fe4e/main/unir.ics

## Actualización

1. En Chrome, con la sesión de UNIR iniciada, abrir https://campusvirtual.unir.net/p/calendar?mode=month
2. Ejecutar en la página el PASO 1 de `tools/extract.js`, cambiar de mes y ejecutar el PASO 2.
3. Copiar `window.__s` (en trozos) a `eventos.txt`, una fila por línea.
4. `python3 tools/gen_ics.py eventos.txt unir.ics` y subir `unir.ics`.
