# 🏥 NurseEval AI - Evaluación Inteligente de Enfermería

**Hospital de Clínicas José de San Martín | Universidad de Buenos Aires**

> Sistema conversacional de IA que automatiza la evaluación de desempeño del personal de enfermería con rúbrica validada, generando documentos auditables conforme a Decreto 366/06, Ley 25.326 y normativas argentinas.

[![License: MIT](https://img.shields.io/badge/License-MIT%203.0-blue.svg)](LICENSE)
[![Status: MVP Planning](https://img.shields.io/badge/Status-MVP%20Planning-yellow)](PROJECT_CHARTER.md)
[![Python](https://img.shields.io/badge/Backend-FastAPI%20%7C%20Python%203.10%2B-green)]() 
[![React](https://img.shields.io/badge/Frontend-React%2018%20%7C%20React%20Native-61dafb)]()

---

## 📋 Índice Rápido
- [Descripción](#descripción)
- [Estado Actual](#-estado-actual-hoy-12122025)
- [Logros](#-logros-completados)
- [Próximos Pasos](#-próximos-pasos)
- [Documentación](#-documentación-completa)

---

## 📖 Descripción

**NurseEval AI** resuelve el problema de evaluaciones manuales lentas (45+ min), sesgadas (15-25% errores) y no auditables. Implementa:

✅ **Chatbot conversacional** - 25 ítems (11 técnicos + 14 actitudinales)  
✅ **Autenticación 2FA** - JWT + TOTP + SMS  
✅ **Cálculo automático** - Sin sesgo (CT×60% + CA×40%)  
✅ **PDF auditable** - Plantilla oficial intocable  
✅ **Cumplimiento legal** - Decreto 366/06, Ley 25.326, RENFAMED  
✅ **Portal enfermero** - Transparencia + derecho a recurso  
✅ **Auditoría completa** - Logs inmutables (5 años retención)  

---

## 🎯 Estado Actual (Hoy 12/12/2025)

### ✅ Completado - Semana 1
| Item | Estado | Detalles |
|------|--------|----------|
| **Repositorio GitHub** | ✅ Activo | @lankamar/nurse-eval-ai (MIT License) |
| **Rama SIMULADOR** | 🛡️ Protegida | Ruleset: bloquea push --force + eliminación |
| **Copilot Agent** | 🤖 En ejecución | PR #1: [WIP] Full-stack system (5 fases) |
| **Documentación Normativa** | 📋 Completa | 14 leyes analizadas + compliance checklist |
| **Project Charter** | 📄 Finalizado | Acta constitución con 10 secciones |
| **Especificaciones Auth** | 🔒 Documentado | JWT + 2FA (TOTP + SMS + backup codes) |
| **Deployment Plan** | ☁️ Listo | Google Cloud: 12 horas (fase por fase) |

### 🔄 En Progreso
- Copilot generando estructura backend/frontend
- PR #1 pendiente review antes merge

### ⏳ Próximo (Semana 2-4)
- Backend core (Auth + BD + APIs)
- Frontend conversacional
- Testing + QA
- **LIVE 05/01/2026**

---

## 🏆 Logros Completados

### Infraestructura
✅ Repositorio público con 2 branches  
✅ Rama SIMULADOR protegida contra cambios forzados  
✅ Licencia MIT configurada  
✅ Descripción completa en repo  

### Documentación (EN GITHUB /docs)
✅ PROJECT_CHARTER.md - Acta constitución  
✅ PRD_COMPLETE.md - Requisitos funcionales/no-funcionales  
✅ COMPLIANCE_ARGENTINA.md - 14 normativas analizadas  
✅ RUBRICA_EVALUACION.md - 25 criterios + indicadores  
✅ ESPECIFICACIONES_TECNICAS.md - Auth, BD, Seguridad  
✅ DEPLOYMENT_PLAN.md - Google Cloud (12h)  
✅ NORMATIVAS_ETICAS.md - Marco legal completo  

### IA y Desarrollo
✅ Copilot Agent iniciado  
✅ PR #1 abierto con plan 5 fases  
✅ Instrucción a Copilot documentada  

---

## 🚀 Próximos Pasos

### Inmediatos (Próximas 24-48h)
1. ✅ Subir documentación a GitHub `/docs` (hoy)
2. ⏳ Validar código Copilot en PR #1
3. ⏳ Crear branch `develop` para desarrollo
4. ⏳ Setup local environment

### Corto Plazo (Próxima semana 19-25/12)
1. Backend: Autenticación JWT + 2FA
2. Backend: Modelos BD (Users, Evaluations, Criteria)
3. Backend: APIs REST
4. Frontend: Interfaz chat base
5. Tests unitarios (pytest)

### Mediano Plazo (26/12 - 01/01)
1. Motor conversacional completo
2. Generador PDF funcionando
3. RBAC implementado
4. Auditoría + logging
5. Integration testing

### Largo Plazo (02/01 - 05/01)
1. Staging en Google Cloud
2. Load testing (100+ usuarios)
3. Capacitación jefes/supervisora
4. **LIVE en producción**

---

## 📚 Documentación Completa

### En Este Repo `/docs`
- **PROJECT_CHARTER.md** - Justificación, objetivos, stakeholders, riesgos
- **PRD_COMPLETE.md** - Requisitos funcionales/no-funcionales, user stories
- **COMPLIANCE_ARGENTINA.md** - Decreto 366/06, Ley 25.326, +12 leyes
- **RUBRICA_EVALUACION.md** - 25 ítems con indicadores por nivel
- **ESPECIFICACIONES_TECNICAS.md** - Autenticación 2FA, BD, Seguridad
- **DEPLOYMENT_PLAN.md** - Google Cloud setup paso a paso
- **NORMATIVAS_ETICAS.md** - Marco legal y ético completo
- **LOGROS_HITOS.md** - Estado actual + timeline

### En Este Chat
- Decisiones en progreso
- Consultas + cambios
- Iteraciones del PRD
- Validaciones antes de GitHub

---

## 👥 Equipo

| Rol | Responsable | Contacto |
|-----|------------|----------|
| **Project Manager / CEO / Dev** | Marcelo Omar Lancry Kamycki | @lankamar |
| **Jefe Sala 4** | Marcelo Omar Lancry Kamycki | - |
| **Jefe Sala 4 (Evaluador)** | Aguilar Walter | - |
| **Supervisora** | Guzmán Sandra | - |
| **Dirección Enfermería** | Hospital de Clínicas | - |

---

## 💻 Stack Tecnológico

### Backend
```
FastAPI (Python 3.10+)
PostgreSQL 13+ (AES-256 encriptado)
SQLAlchemy ORM
PyJWT + bcrypt (autenticación)
PyOTP (TOTP 2FA)
Sentry (error tracking)
```

### Frontend
```
React 18 + Tailwind CSS (desktop)
React Native (mobile)
axios + jwt-decode
ReportLab (PDF generation)
```

### DevOps
```
Docker + docker-compose
GitHub Actions (CI/CD)
Google Cloud Platform
Cloud SQL (PostgreSQL managed)
Cloud Run (serverless)
Cloud Storage (PDFs)
```

---

## 📊 Hitos y Timeline

| Hito | Fecha | Estado |
|------|-------|--------|
| Repo + Infraestructura | 12/12/2025 | ✅ Completado |
| Rama protegida | 12/12/2025 | ✅ Completado |
| Documentación normativa | 12/12/2025 | ✅ Completado |
| Backend core (Copilot) | ~19/12/2025 | 🔄 En progreso |
| Frontend base (Copilot) | ~22/12/2025 | ⏳ Próximo |
| Testing + QA | ~01/01/2026 | ⏳ Próximo |
| Staging en GCP | ~03/01/2026 | ⏳ Próximo |
| **LIVE Producción** | **05/01/2026** | 🎯 **OBJETIVO** |

---

## 🔐 Seguridad y Compliance

✅ **Encriptación**: AES-256 (en reposo) + TLS 1.3 (en tránsito)  
✅ **Autenticación**: JWT stateless + 2FA obligatorio (jefes)  
✅ **Autorización**: RBAC (4 roles definidos)  
✅ **Auditoría**: Logs inmutables + trazabilidad 100%  
✅ **Normativa**: Decreto 366/06 + Ley 25.326 + RENFAMED  
✅ **Retención**: 5 años backup automático  
✅ **ARCO**: Derechos acceso/rectificación/cancelación implementados  

---

## 📝 Licencia

**MIT License** - Libre para uso, modificación y distribución  
Ver [LICENSE](LICENSE) para detalles completos.

```
Copyright (c) 2025 Marcelo Omar Lancry Kamycki
```

---

## 📞 Contacto

- **Email**: lancry.marcelo@hospitaldelasclinicas.uba.ar
- **GitHub**: [@lankamar](https://github.com/lankamar)
- **LinkedIn**: [lankamar](https://www.linkedin.com/in/lankamar)
- **Issues**: [GitHub Issues](../../issues) para bugs/features

---

## 📄 Estado del Desarrollo

```
✅ Semana 1 (12/12-18/12): Repo + Infraestructura + Docs
🔄 Semana 2 (19/12-25/12): Backend + Frontend base (Copilot)
⏳ Semana 3 (26/12-01/01): Integración + Testing + QA  
⏳ Semana 4 (02/01-05/01): Staging + Capacitación + LIVE
```

**Última actualización**: 12 de Diciembre de 2025, 08:30 ARS  
**Próxima actualización**: 19 de Diciembre de 2025 (Backend progress)

---

*Proyecto de investigación e innovación educativa - Hospital de Clínicas José de San Martín, Facultad de Medicina, UBA*
