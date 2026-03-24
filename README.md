# Gemailla AI Backend

Backend FastAPI preparado para integrarse con Firebase Authentication, Firestore y Firebase Storage sin romper una arquitectura por capas.

## Estructura

- `backend/app/api/routes`: endpoints HTTP.
- `backend/app/dependencies`: dependencias de autenticación.
- `backend/app/core`: configuración, logging y clientes Firebase.
- `backend/app/services`: servicios de autenticación, persistencia y storage.
- `backend/app/schemas`: modelos de respuesta y dominio.

## Variables de entorno

Copia `.env.example` a `.env` y completa:

- `FIREBASE_PROJECT_ID`
- `FIREBASE_STORAGE_BUCKET`
- `FIREBASE_SERVICE_ACCOUNT_PATH` o `FIREBASE_SERVICE_ACCOUNT_JSON`
- `FIRESTORE_USERS_COLLECTION`
- `FIRESTORE_DOCUMENTS_COLLECTION`

## Instalación

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Seguridad aplicada

- Validación de Firebase ID token con verificación del Admin SDK y comprobación explícita de `issuer`, `audience` y `subject`.
- `/api/me` y `/api/documents` están protegidos con `Authorization: Bearer <firebase-id-token>`.
- Los archivos ya no se exponen como públicos; se genera una signed URL temporal para acceso controlado.
- Los errores de autenticación, persistencia y storage se devuelven con códigos consistentes y logging estructurado.

## Endpoints

- `GET /health`: healthcheck.
- `GET /api/me`: endpoint protegido que valida el Firebase ID token y devuelve el usuario autenticado.
- `POST /api/documents`: endpoint protegido que sube archivos a Firebase Storage y guarda metadatos en Firestore.

## Persistencia en Firestore

- La colección de usuarios se actualiza automáticamente al validar un token.
- La colección de documentos almacena propietario, tenant, proyecto, tipo de contexto, ruta en storage, signed URL y vencimiento de acceso.
