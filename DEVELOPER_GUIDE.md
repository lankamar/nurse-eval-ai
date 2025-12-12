# 👨‍💻 DEVELOPER_GUIDE.md - Guía de Desarrollo para NurseEval AI

**Hospital de Clínicas José de San Martín | Sistema de Evaluación Inteligente**

---

## ⚡ INICIO RÁPIDO (15 MINUTOS)

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/lankamar/nurse-eval-ai.git
cd nurse-eval-ai
git checkout SIMULADOR
```

### Paso 2: Setup ambiente local
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### Paso 3: Configurar variables de entorno
```bash
# backend/.env
DATABASE_URL=postgresql://user:password@localhost/nurse_eval
JWT_SECRET=your_secret_key_here
TOTP_ISSUER=NurseEval
GCP_PROJECT_ID=your_gcp_project

# frontend/.env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### Paso 4: Levantar servicios
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm start  # abre http://localhost:3000

# Terminal 3: BD (Docker)
docker-compose up -d
```

---

## 📋 ARQUITECTURA COMPLETA

### Backend (FastAPI)
```
backend/
├── main.py                 # Punto de entrada
├── app/
│   ├── api/
│   │   ├── auth.py         # JWT + 2FA
│   │   ├── evaluations.py  # CRUD evaluaciones
│   │   ├── observations.py # Recursos
│   │   └── admin.py        # Dashboard admin
│   ├── models/
│   │   ├── user.py
│   │   ├── evaluation.py
│   │   └── audit_log.py
│   ├── schemas/
│   │   └── (Pydantic models)
│   ├── services/
│   │   ├── pdf_generator.py    # ReportLab
│   │   ├── evaluator.py        # Lógica evaluación
│   │   └── encryption.py       # AES-256
│   └── middleware/
│       ├── auth.py
│       └── error_handler.py
├── requirements.txt
└── docker-compose.yml
```

### Frontend (React 18)
```
frontend/
├── src/
│   ├── pages/
│   │   ├── LoginPage.tsx
│   │   ├── ChatbotPage.tsx
│   │   ├── ResultsPage.tsx
│   │   └── AdminDashboard.tsx
│   ├── components/
│   │   ├── ChatBot/
│   │   ├── PDFViewer/
│   │   ├── ObservationForm/
│   │   └── RBACGuard.tsx
│   ├── context/
│   │   ├── AuthContext.tsx
│   │   └── EvaluationContext.tsx
│   ├── services/
│   │   └── api.ts          # axios client
│   └── App.tsx
└── package.json
```

---

## 🔐 FLUJOS PRINCIPALES

### 1️⃣ AUTENTICACIÓN (JWT + 2FA)

```
USUARIO
   |
   v
[1] POST /auth/login (email, password)
   |
   v
[Backend: Validar bcrypt]
   |
   v
[2] Generar JWT token (exp: 24h)
   |
   v
[3] Generar TOTP secret → QR (Google Authenticator)
   |
   v
[Frontend: Mostrar QR]
   |
   v
[Usuario escanea + verifica TOTP]
   |
   v
[4] POST /auth/2fa/verify (token_jwt, totp_code)
   |
   v
[Backend: Validar TOTP]
   |
   v
[5] Generar REFRESH TOKEN
   |
   v
[✅ ACCESO TOTAL]
```

**Endpoints**:
- `POST /api/v1/auth/login` → JWT + TOTP secret
- `POST /api/v1/auth/2fa/verify` → Verificar TOTP
- `POST /api/v1/auth/refresh` → Renovar JWT

---

### 2️⃣ EVALUACIÓN CONVERSACIONAL

```
[Jefe inicia evaluación]
   |
   v
[1] POST /evaluations (evaluado_id, sala, turno)
   |
   v
[Backend: Crea evaluación en BORRADOR]
   |
   v
[2] Frontend: Carga 25 preguntas en ORDEN
   - Preguntas 1-11: Competencias Técnicas
   - Preguntas 12-25: Competencias Actitudinales
   |
   v
[Usuario selecciona puntajes 1-5]
   |
   v
[3] PUT /evaluations/{id} (scores: JSON)
   |
   v
[Backend: Calcula CT y CA]
   |
   v
[4] POST /evaluations/{id}/sign (firma_digital)
   |
   v
[Backend: Genera PDF + QR con hash SHA-256]
   |
   v
[✅ Evaluación COMPLETADA y FIRMADA]
```

---

### 3️⃣ GENERACIÓN PDF (INTOCABLE)

```python
# backend/services/pdf_generator.py

def generate_evaluation_pdf(evaluation_id: UUID) -> bytes:
    eval = db.get(Evaluation, evaluation_id)
    
    # Template oficial (NO MODIFICABLE)
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch
    )
    
    # Contenido fijo
    story = [
        Paragraph("<b>EVALUACIÓN DE DESEMPEÑO</b>", styles['Title']),
        Paragraph(f"Enfermero: {eval.evaluated_nurse.name}", styles['Normal']),
        Paragraph(f"Sala: {eval.sala}", styles['Normal']),
        Spacer(1, 0.3*inch),
        # Tabla de rúbrica (25 ítems)
        # Puntajes
        # QR con firma digital
    ]
    
    doc.build(story)
    return buffer.getvalue()
```

---

## 🗄️ BD SCHEMA CRÍTICO

### Users (Autenticación)
```sql
id UUID PRIMARY KEY
email VARCHAR(255) UNIQUE
password_hash VARCHAR (bcrypt)
role ENUM('admin', 'supervisora', 'jefe', 'enfermero')
2fa_secret VARCHAR(32) ENCRYPTED
2fa_enabled BOOLEAN
backup_codes TEXT[] (10 códigos)
```

### Evaluations (Core)
```sql
id UUID PRIMARY KEY
evaluador_id UUID → users
evaluado_id UUID → users
sala VARCHAR(50)
turno ENUM('Noche A', 'Noche B', 'Mañana', 'Tarde', 'SADOFE')
scores JSON {"1": 4, "2": 5, ...}  # 25 ítems
puntaje_final DECIMAL(3,2)  # CT × 60% + CA × 40%
estado ENUM('borrador', 'completada', 'firmada')
pdf_url VARCHAR(512)  # Cloud Storage
firma_digital VARCHAR(256)  # SHA-256 hash
timestamp_firma TIMESTAMP
```

### AuditLogs (Inmutable, 5 años retención)
```sql
id UUID PRIMARY KEY
usuario_id UUID → users
accion VARCHAR(100)  # 'CREATE_EVALUATION', 'SIGN_EVALUATION'
tabla VARCHAR(50)
registro_id UUID
antes JSON  # Valores previos
despues JSON  # Nuevos valores
ip_address INET
timestamp TIMESTAMP NOT NULL
retencion_hasta TIMESTAMP
```

---

## 🔒 SEGURIDAD OBLIGATORIA

### Encriptación
```python
# backend/app/services/encryption.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

class EncryptionService:
    def encrypt_aes256(data: str, key: str) -> str:
        # AES-256 para datos sensibles
        pass
    
    def hash_password(password: str) -> str:
        # bcrypt para passwords
        pass
    
    def generate_signature(evaluation_id: UUID) -> str:
        # SHA-256 para firma digital de PDFs
        pass
```

### Headers de Seguridad
```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hospital.ar"],  # SOLO hospital
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Authorization"],
)

# Agregar headers
response.headers["X-Content-Type-Options"] = "nosniff"
response.headers["X-Frame-Options"] = "DENY"
response.headers["Strict-Transport-Security"] = "max-age=31536000"
```

---

## ✅ CHECKLIST ANTES DE GO LIVE

- [ ] Backend:
  - [ ] Todas las APIs testadas (pytest)
  - [ ] 2FA funcionando con Google Authenticator
  - [ ] PDF generados con plantilla oficial
  - [ ] AuditLogs registrando todo
  - [ ] Encriptación AES-256 activa
  
- [ ] Frontend:
  - [ ] Chatbot conversacional fluido
  - [ ] Portal enfermero mostrando su evaluación
  - [ ] Dashboard admin con estadísticas
  - [ ] Formulario de observaciones funcional
  
- [ ] Cloud (GCP):
  - [ ] Cloud SQL PostgreSQL activa
  - [ ] Cloud Run deploying backend
  - [ ] Cloud Storage para PDFs
  - [ ] Cloud Logging registrando
  
- [ ] Legal:
  - [ ] Auditor validó compliance
  - [ ] 14 normativas verificadas
  - [ ] RGPD-like (derechos ARCO) implementados
  - [ ] Consentimiento enfermero integrado

---

## 📞 CONTACTO & SOPORTE

**CEO/Dev Principal**: Marcelo Omar Lancry Kamycki (@lankamar)  
**Email**: lancry.marcelo@hospitaldelasclinicas.uba.ar  
**GitHub Issues**: Reportar bugs en `/lankamar/nurse-eval-ai/issues`  
**PR Review**: Crear PR a rama `develop` para review

---

**Última actualización**: 12 Diciembre 2025, 10:00 ARS  
**Versión**: 1.0  
**Estado**: LISTO PARA DESARROLLO
