# API Documentation - CONDORIISABEL-H2T9

Proyecto: Sistema de detección de comportamiento sospechoso
Autor: CONDORIISABEL
Repositorio: https://github.com/beljin34/sistema-deteccion-comportamiento-sospechoso

Resumen
-------
Esta documentación describe la API REST implementada en el proyecto. La API permite consultar el estado del servicio, leer y crear eventos detectados por el sistema, y leer/actualizar la configuración del detector.

Base URL
--------
Por defecto para pruebas locales: http://localhost:5000

Endpoints
---------

1) GET /api/health
- Descripción: Devuelve estado y tiempo de actividad del servicio.
- Respuesta 200:
  {
    "status": "ok",
    "uptime_seconds": 123
  }

2) GET /api/events
- Descripción: Lista de eventos recientes (ordenados por más recientes primero). Devuelve el contenido de la cola de eventos.
- Respuesta 200: [ { id, type, x, y, details, ts }, ... ]

3) POST /api/events
- Descripción: Inserta un evento manual (útil para pruebas).
- Body (JSON): { "type": "loitering", "x": 320, "y": 240, "details": "simulado" }
- Respuesta 201: { id, type, x, y, details, ts }
- Errores: 400 si no se envía JSON o faltan campos.

4) GET /api/config
- Descripción: Lee parámetros del detector.
- Respuesta 200: { accum_weight, min_area, loiter_frames, loiter_radius }

5) PUT /api/config
- Descripción: Actualiza parámetros. Valida rangos básicos.
- Body (JSON): algunos o todos los campos: accum_weight (float 0-1), min_area (int>0), loiter_frames (int>0), loiter_radius (int>=0)
- Respuesta 200: mensaje y config actualizada
- Errores: 400 con lista de errores si validación falla.

6) GET /api/video_url
- Descripción: Devuelve la URL local para el stream de video ('/video_feed').
- Respuesta 200: { "url": "/video_feed" }

Pruebas en Postman
------------------
- Importa el archivo CONDORIISABEL-H2T9.json en Postman.
- Crea una variable de entorno base_url con valor http://localhost:5000
- Ejecuta las peticiones en orden: health -> events GET -> events POST -> config GET -> config PUT

Rúbrica
-------
Este entregable aporta: endpoints funcionales y documentados con ejemplos. Valida campos en POST/PUT y responde con códigos HTTP adecuados, cumpliendo criterios de la rúbrica (funcionalidad y documentación).

Conversión a PDF
----------------
Para generar el PDF final (APELLIDOSNOMBRE-H2T9.PDF):
- En Linux/macOS: pandoc CONDORIISABEL-H2T9.md -o CONDORIISABEL-H2T9.pdf
- O usar la opción "Print -> Save as PDF" desde GitHub web view.

