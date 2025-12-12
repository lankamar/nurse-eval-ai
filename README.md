# Nurse Eval AI - Sistema de Evaluación de Desempeño de Enfermería

Sistema conversacional de evaluación de desempeño para personal de enfermería del Hospital de Clínicas José de San Martín (UBA), basado en el Decreto 366/06, con cumplimiento de Ley 25.326 y RENFAMED.

## 🌟 Características Principales

### Backend (FastAPI)
- ✅ **Autenticación JWT** con tokens de acceso y refresh
- ✅ **Autenticación 2FA TOTP** con generación de QR codes
- ✅ **PostgreSQL** como base de datos principal
- ✅ **RBAC** - 4 roles: Admin, Jefe, Supervisora, Enfermero
- ✅ **Chatbot conversacional** para evaluaciones guiadas
- ✅ **25 criterios de evaluación** (11 técnicos + 14 actitudinales) según Decreto 366/06
- ✅ **Cálculo automático** de puntajes técnicos, actitudinales y totales
- ✅ **Generación de PDFs auditables** con hash SHA-256
- ✅ **Integración con Sentry** para monitoreo de errores
- ✅ **Pruebas con pytest** y cobertura de código
- ✅ **Pruebas de carga con k6**

### Frontend (React)
- ✅ **Interfaz responsive** adaptable a móviles y tablets
- ✅ **Sistema de autenticación** completo con 2FA
- ✅ **Dashboard** con visualización de evaluaciones por rol
- ✅ **Integración con Sentry** para tracking de errores del cliente

### DevOps & Compliance
- ✅ **Docker & Docker Compose** para desarrollo y producción
- ✅ **GitHub Actions CI/CD** con testing automático
- ✅ **Cumplimiento Decreto 366/06** - Evaluación de desempeño
- ✅ **Cumplimiento Ley 25.326** - Protección de datos personales
- ✅ **RENFAMED** - Registro Nacional de Profesionales de Salud

## 📋 Requisitos Previos

- Docker & Docker Compose
- Node.js 18+ (para desarrollo frontend local)
- Python 3.11+ (para desarrollo backend local)
- Git

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/lankamar/nurse-eval-ai.git
cd nurse-eval-ai
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus valores
```

### 3. Iniciar con Docker Compose

```bash
docker-compose up -d
```

Los servicios estarán disponibles en:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### 4. Inicializar la base de datos

```bash
docker-compose exec backend python -m app.db.seed
```

Esto creará:
- 25 criterios de evaluación (11 técnicos + 14 actitudinales)
- Usuario admin (username: `admin`, password: `admin123`)

## 📚 Documentación de la API

La documentación interactiva de la API está disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 👥 Roles y Permisos (RBAC)

### Admin
- Acceso total al sistema
- Gestión de usuarios
- Visualización de todas las evaluaciones
- Generación de reportes

### Jefe
- Gestión de evaluaciones
- Visualización de todas las evaluaciones
- Aprobación de evaluaciones

### Supervisora
- Creación de evaluaciones
- Gestión de evaluaciones propias
- Uso del chatbot conversacional
- Generación de PDFs

### Enfermero
- Visualización de evaluaciones propias
- Descarga de PDFs de sus evaluaciones

## 🤖 Sistema de Evaluación con Chatbot

El chatbot conversacional guía el proceso de evaluación:

1. **Inicio de conversación**: El evaluador inicia una nueva evaluación
2. **Preguntas guiadas**: El chatbot presenta cada criterio de forma conversacional
3. **Evaluación progresiva**: 25 competencias evaluadas (escala 1-5)
   - 11 Competencias Técnicas (TEC-01 a TEC-11)
   - 14 Competencias Actitudinales (ACT-01 a ACT-14)
4. **Cálculo automático**: Puntajes calculados en tiempo real
5. **Finalización**: Generación de PDF auditable

## 📄 Criterios de Evaluación (Decreto 366/06)

### Competencias Técnicas (11)
1. Conocimientos Técnicos Específicos
2. Aplicación de Normas de Bioseguridad
3. Administración de Medicamentos
4. Manejo de Equipamiento Médico
5. Cuidados Críticos y Urgencias
6. Registro y Documentación Clínica
7. Control de Signos Vitales
8. Técnicas de Curación y Vendajes
9. Control de Infecciones
10. Educación al Paciente y Familia
11. Actualización y Formación Continua

### Competencias Actitudinales (14)
1. Responsabilidad Profesional
2. Trabajo en Equipo
3. Comunicación Interpersonal
4. Empatía y Contención
5. Ética Profesional
6. Adaptabilidad y Flexibilidad
7. Iniciativa y Proactividad
8. Manejo del Estrés
9. Respeto y Trato Digno
10. Liderazgo y Supervisión
11. Compromiso Institucional
12. Resolución de Conflictos
13. Presentación Personal
14. Disponibilidad y Compromiso Horario

## 🧪 Testing

### Backend Tests

```bash
# Con Docker
docker-compose exec backend pytest

# Local
cd backend
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
# Con Docker
docker-compose exec frontend npm test

# Local
cd frontend
npm test
```

### Load Tests (k6)

```bash
cd backend
k6 run --vus 50 --duration 2m load_test.js
```

## 📊 Generación de PDFs Auditables

Los PDFs generados incluyen:
- Información completa de la evaluación
- Desglose de puntajes por competencia
- Hash SHA-256 para verificación de integridad
- Cumplimiento normativo (Decreto 366/06, Ley 25.326)
- Información de auditoría completa

## 🔒 Seguridad y Cumplimiento

### Ley 25.326 - Protección de Datos Personales
- Consentimiento explícito del evaluado
- Registro de fecha de consentimiento
- Audit logs de todas las acciones
- Hash de PDFs para trazabilidad

### RENFAMED
- Validación de profesionales registrados
- Trazabilidad de evaluaciones
- Cumplimiento de normativas sanitarias

### Seguridad Técnica
- JWT con expiración configurable
- 2FA TOTP opcional por usuario
- Passwords hasheados con bcrypt
- CORS configurado
- Rate limiting (recomendado en producción)

## 🚀 Despliegue en Producción

### Configuración recomendada:

1. **Variables de entorno de producción**
```env
SECRET_KEY=<generar-clave-segura-32-chars>
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SENTRY_DSN=<tu-sentry-dsn>
ENVIRONMENT=production
```

2. **SSL/TLS**
   - Usar nginx o Traefik como reverse proxy
   - Certificados SSL (Let's Encrypt)

3. **Base de datos**
   - PostgreSQL en servidor dedicado
   - Backups automáticos
   - Replicación recomendada

4. **Monitoreo**
   - Sentry para error tracking
   - Logs centralizados
   - Métricas de performance

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 Contacto

Hospital de Clínicas José de San Martín - Universidad de Buenos Aires

---

**Desarrollado con ❤️ para mejorar la gestión del personal de enfermería**
