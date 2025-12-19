# 🤖 Copilot Instructions for NurseEval AI

## Visión General
- **NurseEval AI** automatiza la evaluación de desempeño de enfermería usando un chatbot, rúbrica validada y generación de PDF auditable, cumpliendo normativas argentinas (Decreto 366/06, Ley 25.326).
- Arquitectura full-stack: **Backend** (FastAPI, Python, PostgreSQL, Alembic, JWT+2FA, ReportLab) y **Frontend** (React 18, TypeScript, Tailwind, Vite, react-pdf).
- Cumplimiento legal, seguridad (AES-256, TLS 1.3, RBAC, logs inmutables) y auditoría son requisitos centrales.

## Estructura y Componentes Clave
- **backend/**: API REST, modelos, autenticación, generación de PDFs, migraciones Alembic.
  - Entrypoint: [backend/main.py](../backend/main.py)
  - Modelos: [backend/app/models/](../backend/app/models/)
  - Rúbrica: [backend/app/constants/rubric.py](../backend/app/constants/rubric.py)
  - PDF: [backend/app/services/pdf_generator.py](../backend/app/services/pdf_generator.py)
  - Autenticación: JWT + TOTP ([backend/app/api/auth.py](../backend/app/api/auth.py))
- **frontend/**: Interfaz conversacional, contexto de evaluación, integración API.
  - Entrypoint: [frontend/src/App.tsx](../frontend/src/App.tsx)
  - Chatbot: [frontend/src/pages/ChatbotPage.tsx](../frontend/src/pages/ChatbotPage.tsx)
  - Rúbrica: [frontend/src/data/rubric.ts](../frontend/src/data/rubric.ts)
  - API: [frontend/src/services/api.ts](../frontend/src/services/api.ts)

## Patrones y Convenciones Específicas
- **Evaluación**: 25 ítems (11 técnicos, 14 actitudinales), puntaje 1-5, cálculo automático (CT×60% + CA×40%).
- **PDF**: Generado en backend, incluye hash SHA-256 y QR para auditoría.
- **Autenticación**: JWT stateless, 2FA obligatorio para roles críticos, backup codes.
- **RBAC**: 4 roles (admin, supervisora, jefe, enfermero), control de acceso en endpoints y frontend.
- **Contextos React**: `AuthContext`, `EvaluationContext` para estado global.
- **Feedback educativo**: Chatbot da feedback inmediato según ítem y puntaje ([ChatbotPage.tsx](../frontend/src/pages/ChatbotPage.tsx)).

## Workflows de Desarrollo
- **Backend**: 
  - Ejecutar local: `uvicorn main:app --reload` en [backend/](../backend/)
  - Migraciones: `alembic upgrade head`
  - Tests: `pytest` en [backend/app/tests/](../backend/app/tests/)
- **Frontend**:
  - Ejecutar local: `npm install && npm run dev` en [frontend/](../frontend/)
  - Variables: `VITE_API_URL` para endpoint backend
- **Docker Compose**: Levanta backend, frontend y db con `docker-compose up --build`

## Integraciones y Dependencias
- **API REST**: `/api/v1/auth/*`, `/api/v1/evaluations/*`, `/api/v1/admin/*` (ver [ESPECIFICACIONES_TECNICAS.md](../docs/ESPECIFICACIONES_TECNICAS.md))
- **DB**: PostgreSQL 13+, migraciones Alembic
- **PDF**: reportlab (backend), react-pdf (frontend)
- **Seguridad**: CORS restringido, input validation (Pydantic), rate limiting, logs auditables

## Ejemplos de Uso y Pruebas
- Usuario demo: `demo@hospital.test` / `P@ssw0rd!` (ver [main.py](../backend/main.py))
- Flujo típico: login → 2FA → chatbot → puntuar ítems → PDF generado → firma digital

## Documentación Clave
- [README.md](../README.md), [docs/ESPECIFICACIONES_TECNICAS.md](../docs/ESPECIFICACIONES_TECNICAS.md), [docs/RUBRICA_EVALUACION.md](../docs/RUBRICA_EVALUACION.md)

---

**Sigue estos patrones y flujos para mantener la coherencia y compliance del sistema. Consulta los archivos referenciados para detalles técnicos y legales.**
