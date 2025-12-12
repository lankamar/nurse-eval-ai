# 🔉 ESPECIFICACIONES_TECNICAS.md - Arquitectura Completa

**NurseEval AI - Stack Tecnológico Full-Stack**

---

## 1. BACKEND (FastAPI + Python 3.10+)

### 1.1 Autenticación JWT + 2FA

```python
# Authentication Flow
1. Login: Email + Password
2. Validar credenciales (bcrypt)
3. Generar JWT token (exp: 24h)
4. Enviar TOTP code
5. Usuario escanea QR (Google Authenticator)
6. Validar TOTP
7. Generar refresh token
8. Acceso a APIs

# 2FA Specs
- TOTP: Time-based OTP (30 seg)
- SMS: Opcional para backup
- Backup codes: 10 códigos aleatorios
- Secret almacenado encriptado en BD
```

### 1.2 Base de Datos PostgreSQL

```sql
-- Tabla Users
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin', 'supervisora', 'jefe', 'enfermero'),
  2fa_secret VARCHAR(32),
  2fa_enabled BOOLEAN DEFAULT FALSE,
  backup_codes TEXT[] (10 códigos),
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  activo BOOLEAN DEFAULT TRUE
);

-- Tabla Evaluations
CREATE TABLE evaluations (
  id UUID PRIMARY KEY,
  evaluador_id UUID REFERENCES users(id),
  evaluado_id UUID REFERENCES users(id),
  sala VARCHAR(50),
  turno ENUM('Noche A', 'Noche B', 'Mañana', 'Tarde', 'SADOFE'),
  fecha TIMESTAMP,
  scores JSON (25 ítems 1-5),
  puntaje_final DECIMAL(3,2),
  estado ENUM('borrador', 'completada', 'firmada'),
  pdf_url VARCHAR(512),
  firma_digital VARCHAR(256),
  timestamp_firma TIMESTAMP,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Tabla Audit Logs
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  usuario_id UUID REFERENCES users(id),
  accion VARCHAR(100),
  tabla VARCHAR(50),
  registro_id UUID,
  antes JSON,
  despues JSON,
  ip_address INET,
  timestamp TIMESTAMP NOT NULL,
  retencion_hasta TIMESTAMP -- 5 años
);
```

### 1.3 Encriptación

```
- En REPOSO: AES-256 (datos sensibles)
- En TRÁNSITO: TLS 1.3 (HTTPS forzado)
- Hashing: bcrypt (passwords)
- Firma digital: SHA-256 + RSA (PDFs)
- Algoritmo JWT: HS256 (HMAC-SHA256)
```

### 1.4 APIs REST

```
AUTHENTICATION
POST   /api/v1/auth/login          # Login con email/password
POST   /api/v1/auth/2fa/verify     # Verificar TOTP
POST   /api/v1/auth/logout         # Logout
POST   /api/v1/auth/refresh        # Refresh JWT
GET    /api/v1/auth/2fa/qr         # QR para autenticador

EVALUATIONS
POST   /api/v1/evaluations         # Crear evaluación
GET    /api/v1/evaluations/{id}    # Obtener evaluación
PUT    /api/v1/evaluations/{id}    # Actualizar evaluación
POST   /api/v1/evaluations/{id}/sign # Firmar y completar
GET    /api/v1/evaluations         # Listar (con RBAC)

PDF GENERATION
POST   /api/v1/evaluations/{id}/pdf # Generar PDF
GET    /api/v1/evaluations/{id}/pdf # Descargar PDF

OBSERVATIONS (Recursos)
POST   /api/v1/observations        # Enviar observación
GET    /api/v1/observations/{id}   # Ver observación
PUT    /api/v1/observations/{id}   # Responder observación

ADMIN
GET    /api/v1/admin/stats         # Estadísticas
GET    /api/v1/admin/audit-logs    # Logs auditables
GET    /api/v1/admin/users         # Listar usuarios
```

---

## 2. FRONTEND (React 18 + TypeScript)

### 2.1 Componentes Principales

```tsx
// Pages
- LoginPage: Autenticación + 2FA
- ChatbotPage: Evaluación conversacional
- ResultsPage: Ver evaluación completada
- PortalEnfermero: Ver propia evaluación
- DashboardAdmin: Estadísticas

// Components
- ChatBot: Motor conversacional
- PDFGenerator: Exportar evaluación
- ObservationForm: Formulario de observaciones
- RBACGuard: Control de acceso por rol
```

### 2.2 Estados (React Context)

```
- AuthContext: JWT, usuario, 2FA
- EvaluationContext: Evaluación actual, scores
- UIContext: Temas, idioma, notificaciones
```

### 2.3 Librerías

```
- axios: HTTP client
- jwt-decode: Decodificar JWT
- react-router: Navegación
- tailwindcss: Estilos responsive
- react-pdf: Visualizar PDFs
- zustand: State management
```

---

## 3. GENERACIÓN DE PDF

### 3.1 Plantilla Intocable

```
- Logo Hospital
- Títulos: "EVALUACIÓN DE DESEMPEÑO"
- Datos: Nombre enfermero, sala, fecha
- Rúbrica: 25 ítems (11 Técnicos + 14 Actitudinales)
- Puntajes: CT, CA, FINAL
- Firma digital: QR + hash SHA-256
- Pie de página: "Documento auditable - Decreto 366/06"

# Generación
- Backend: reportlab (Python)
- Frontend: react-pdf (visualización)
```

---

## 4. CLOUD (Google Cloud Platform)

### 4.1 Arquitectura

```
Frontend:     Cloud Run + Cloud Storage
Backend:      Cloud Run (FastAPI)
BD:           Cloud SQL (PostgreSQL)
PDFs:         Cloud Storage
DNS:          Cloud DNS
Logs:         Cloud Logging
Monitor:      Cloud Monitoring
```

### 4.2 Configuración

```dockerfile
# Dockerfile backend
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:pass@db/nurse_eval
      JWT_SECRET: ${JWT_SECRET}
  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
```

---

## 5. SEGURIDAD

- CORS configurado: solo hospital.ar
- Rate limiting: 100 req/min
- Input validation: schemas Pydantic
- OWASP Top 10 testing
- Pentesting pre-Go Live
- Headers: CSP, X-Frame-Options, HSTS

---

## 6. PERFORMANCE

- Respuesta chatbot: < 2s
- Generación PDF: < 5s
- DB queries: < 100ms (P95)
- Caching: Redis (opcional)
- CDN: Google Cloud CDN para assets

---

**Versión**: 1.0  
**Aprobada por**: Equipo técnico  
**Fecha**: 12/12/2025
