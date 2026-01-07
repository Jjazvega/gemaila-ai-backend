# Gemaila AI Backend

Backend para generar correos electrónicos automatizados con IA — rama refactor/scale-2025.

Este README documenta la arquitectura, la estructura de datos, instrucciones de desarrollo y despliegue, pruebas, optimizaciones de rendimiento y recomendaciones para escalado.

Resumen ejecutivo
- Arquitectura: API REST en Express con separación de responsabilidades (routes, controllers, services, middleware, utils).
- Integraciones principales: OpenAI (modelo configurable), PostgreSQL (pg Pool) para persistencia, Redis (ioredis) para cache y rate-limiter.
- Objetivos: baja latencia, escalabilidad horizontal, control de costes de OpenAI (cache), logging estructurado y pruebas automatizadas.

Estructura del repositorio
- server.js - Entrypoint que arranca la app y gestiona shutdown
- migrations/ - SQL de migraciones (001_create_emails.sql)
- src/
  - app.js
  - routes/
  - controllers/
  - services/ (openaiService, cache, db)
  - middleware/ (errorHandler)
  - utils/ (logger)
- tests/ - Jest + Supertest
- .github/workflows/ci.yml - CI básica

Variables de entorno (.env)
- PORT=3000
- NODE_ENV=development
- OPENAI_API_KEY=sk_...
- DATABASE_URL=postgres://user:pass@host:5432/dbname
- REDIS_URL=redis://:password@host:6379
- LOG_LEVEL=info
- RATE_LIMIT_POINTS=100
- RATE_LIMIT_DURATION=60
- CACHE_TTL_SECONDS=3600

Instalación y uso (desarrollo)
1. Clona el repositorio y cambia a la rama:
   git clone https://github.com/Jjazvega/gemaila-ai-backend.git
   cd gemaila-ai-backend
   git checkout refactor/scale-2025
2. Copia .env.example a .env y rellena las variables.
3. Instala dependencias:
   npm ci
4. Ejecuta en modo desarrollo:
   npm run dev
5. Ejecuta tests:
   npm test

Endpoints principales
- GET /health
  - Retorna { "status": "ok" }
- POST /api/v1/email/generate
  - Body (application/json):
    {
      "to": "user@example.com",
      "subject": "Opcional",
      "context": "Contexto adicional",
      "tone": "formal|informal",
      "length": "short|medium|long"
    }
  - Response 200:
    {
      "success": true,
      "data": { "subject": "...", "body": "..." },
      "meta": { "latencyMs": 123 }
    }
  - Errores comunes: 400 (payload), 429 (rate limit), 502/503 (servicio externo), 500 (interno)

Diseño y algoritmos
- Cacheo: Redis con key pattern gemail:email:{sha256(payload)}. TTL configurable. cache hit evita llamada a OpenAI.
- Hash: sha256(JSON.stringify({to,subject,context,tone,length})) para garantizar determinismo en cache.
- Llamada a OpenAI: openaiService reutiliza cliente OpenAIApi. Model, max_tokens y temperature configurables.
- Persistencia: insertEmail en PostgreSQL mediante pg Pool. Persistencia asíncrona (fire-and-forget) desde el controller para mantener baja latencia.
- Rate limiting: rate-limiter-flexible con Redis. Limit configurable por entorno.

Migraciones
- migrations/001_create_emails.sql crea tabla emails e índices:
  - id, recipient, subject, body, tone, length, created_at
  - índices: recipient, created_at
- En entorno de producción usar herramienta de migraciones (node-pg-migrate, knex, Flyway) para versionado y rollback.

Estrategias de rendimiento y escalado
- Pooling DB: usar pg.Pool y en producción combinar con pgbouncer para evitar exceso de conexiones.
- Cache: usar Redis para respuestas repetidas; ajustar TTL según patrones de uso.
- Workers: mover persistencia y envíos reales a workers (BullMQ) para desacoplar latencia.
- Rate-limit y autenticación: aplicar por API key/usuario para control de uso y costes.
- Observabilidad: agregar métricas (Prometheus) y tracing (OpenTelemetry) si se necesita trazabilidad end-to-end.

Pruebas y CI
- Tests unitarios y de integración con Jest y Supertest (tests/email.generate.test.js incluido) y mock de openaiService.
- CI: GitHub Actions configurado para ejecutar tests con servicios Postgres y Redis.

Seguridad
- No cometas .env con secrets
- Usa roles restringidos para la DB
- En producción guarda secretos en un secret manager (AWS Secrets Manager, GitHub Secrets)

Siguientes pasos recomendados
- Implementar workers (BullMQ) para persistencia y envío de emails
- Añadir métricas y dashboards (Grafana)
- Habilitar tracing con OpenTelemetry
- Añadir autenticación (API keys) y cuota por usuario para control de costes OpenAI

Contacto
- Para cambios adicionales, abre un issue o PR en la rama refactor/scale-2025.

---

Este README ha sido generado automáticamente por Copilot y contiene la documentación completa y depurada para la rama refactor/scale-2025.
