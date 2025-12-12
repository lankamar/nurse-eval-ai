# 🛠️ DEVELOPER_GUIDE

Guía rápida para levantar el MVP conversacional (FastAPI + React) en local.

## 1. Prerrequisitos
- Python 3.10+
- Node.js 18+
- Docker + docker-compose

## 2. Clonar y preparar
```
git clone https://github.com/lankamar/nurse-eval-ai.git
cd nurse-eval-ai
git checkout SIMULADOR
cp .env.example .env
```

## 3. Servicios base
```
docker-compose up -d  # PostgreSQL 13 + Redis 7
```

## 4. Backend (FastAPI)
```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Base de datos y migraciones
- Alembic incluido. Para generar tablas desde metadata (dev rápido): se crea en startup.
- Para aplicar migraciones: `alembic upgrade head` (usa DATABASE_URL).

### Endpoints clave
- POST /api/v1/auth/login (email, password, code opcional, backup_code opcional)
- POST /api/v1/auth/refresh
- GET  /api/v1/auth/me
- POST /api/v1/evaluations
- PUT  /api/v1/evaluations/{id}
- POST /api/v1/evaluations/{id}/sign
- POST /api/v1/admin/import-staff (CSV: email, role) → crea usuarios con password temporal + TOTP

**Demo user:**
- email: demo@hospital.test
- password: P@ssw0rd!
- primer login devuelve `provisioning_uri` + encabezado `X-TOTP-Secret` para configurar Google Authenticator.

## 5. Frontend (React + Vite + Tailwind)
```
cd ../frontend
cp .env.example .env
npm install
npm run dev
```
URL: http://localhost:3000 (usa VITE_API_URL)

## 6. Flujo mínimo para probar
1) Ir a frontend, realizar login con demo user.
2) Usar código TOTP generado con el secreto provisto (o backup code).
3) Crear evaluación demo en "Evaluación Conversacional" (CT1 / CA1) y ver total.

## 7. Próximos pasos sugeridos
- Sustituir store en memoria por repositorio SQLAlchemy + migrations.
- Añadir RBAC real y protección de rutas.
- Integrar PDF real con plantilla oficial.
- Añadir tests (pytest) y linters (ruff/black).
