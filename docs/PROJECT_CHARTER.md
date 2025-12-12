# 📋 PROJECT_CHARTER.md - Acta Constitutiva del Proyecto

**NurseEval AI - Evaluación Inteligente de Enfermería**

---

## 1. Información del Proyecto

| Aspecto | Descripción |
|--------|-------------|
| **Nombre** | NurseEval AI - Evaluación Inteligente de Enfermería |
| **Institución** | Hospital de Clínicas José de San Martín, UBA |
| **Objetivo** | Automatizar evaluaciones de desempeño del personal de enfermería |
| **Licencia** | MIT |
| **Estado** | MVP Planning (Semana 1) |
| **Fecha Inicio** | 12 de Diciembre de 2025 |
| **Fecha Objetivo** | 05 de Enero de 2026 (GO LIVE) |

---

## 2. Justificación del Proyecto

### Problema
- **Evaluaciones manuales lentas**: 45+ minutos por evaluación
- **Errores humanos**: 15-25% de inconsistencias en evaluaciones
- **Sin auditoría**: Falta trazabilidad legal requerida por Decreto 366/06 y Ley 25.326
- **Falta de transparencia**: Enfermeros sin acceso a resultados de evaluación
- **Enfoque subjetivo**: Ausencia de rúbrica validada para todas las sesiones

### Oportunidad
- Implementar **chatbot conversacional** que automatice evaluaciones
- Generar **documentos auditables** con trazabilidad 100%
- Cumplir **normativa legal argentina** (Decreto 366/06, Ley 25.326, RENFAMED)
- Permitir **recursos al personal** y **derecho de apelación**
- Reducir **sesgos** mediante cálculo automático de puntuaciones

---

## 3. Objetivos SMART

### Objetivo Principal
✅ Desarrollar e implementar en PRODUCCIÓN un sistema conversacional de IA que automatice la evaluación de desempeño de personal de enfermería con rúbrica validada, cumpliendo Decreto 366/06 y Ley 25.326, antes del 05/01/2026.

### Objetivos Secundarios
1. **Reducir tiempo de evaluación**: De 45 min → 15 min (67% reducción)
2. **Eliminar errores**: Implementar cálculo automático sin sesgo (CT×60% + CA×40%)
3. **Garantizar cumplimiento legal**: 14 normativas analizadas + checklist
4. **Transparencia**: Portal enfermero con acceso a evaluaciones + derecho de recurso
5. **Auditoría completa**: 5 años de retención de logs inmutables

---

## 4. Stakeholders (Interesados)

| Rol | Nombre | Responsabilidad | Contacto |
|-----|--------|-----------------|----------|
| **Project Manager / CEO / Dev** | Marcelo Omar Lancry Kamycki | Liderazgo técnico + desarrollo | @lankamar |
| **Jefe Sala 4** | Marcelo Omar Lancry Kamycki | Evaluador principal | - |
| **Jefe Sala 4 (Evaluador)** | Aguilar Walter | Validación de rúbrica | - |
| **Supervisora** | Guzmán Sandra | Supervisión + acceso admin | - |
| **Dirección Enfermería** | Hospital de Clínicas | Sponsor institucional | - |
| **Usuario Final** | Personal de enfermería | Participantes en evaluaciones | - |

---

## 5. Roles y Responsabilidades (RACI)

### Matriz RACI

| Tarea | Marcelo (CEO) | Aguilar | Guzmán | Dirección |
|------|--------------|--------|--------|----------|
| Desarrollar código | **R/A** | C | C | I |
| Validar rúbrica | C | **R/A** | **R/A** | C |
| Testing | **R/A** | C | C | I |
| Capacitación | **R/A** | C | **R/A** | C |
| Deployment GCP | **R/A** | I | C | I |
| Go Live | **A** | **R** | **R** | **A** |

**R**: Responsible | **A**: Accountable | **C**: Consulted | **I**: Informed

---

## 6. Alcance

### Incluido ✅
- Chatbot conversacional con 25 ítems (11 técnicos + 14 actitudinales)
- Autenticación 2FA (JWT + TOTP + SMS)
- Cálculo automático de puntuaciones
- Generador de PDF auditable (plantilla intocable)
- Portal enfermero (transparencia + derecho de recurso)
- RBAC con 4 roles (Admin, Supervisora, Jefes, Enfermeros)
- Auditoría completa (logs inmutables, 5 años retención)
- Cumplimiento Decreto 366/06 + Ley 25.326 + normativas
- Despliegue en Google Cloud (serverless)
- Documentación completa + capacitación

### Excluido ❌
- Mobile app nativa (solo responsive web)
- Gamificación/Badges
- Integraciones con otros sistemas (EPIC, SAP, etc.)
- Analytics avanzado (BI/Dashboards)
- SMS real (solo TOTP + códigos respaldo)
- Traducción a idiomas adicionales

---

## 7. Restricciones

### Restricción CRÍTICA
- **"ESTO DEBE RODAR TOTALMENTE GRATIS BAJO RECURSOS GRATUITOS PORQUE NO HAY PLATA"**
  - Google Cloud Free Tier + Cloud Run + Cloud SQL
  - Herramientas open-source solamente
  - Stack gratuito: FastAPI + React + PostgreSQL + GitHub

### Restricción de Diseño
- **NO PUEDEN SUGERIRSE CAMBIOS EN LA PÁGINA DE EVALUACIÓN**
- **RESPECTARSE EL FORMATO, TIPOGRAFÍA E IDENTIDAD ORGANIZACIONAL**
- La rúbrica es intocable (aprobada por Hospital)

### Restricción Legal
- Cumplimiento obligatorio Ley 25.326 (Protección Datos Personales Argentina)
- Cumplimiento Decreto 366/06
- Normativas provincia Buenos Aires + municipio
- RGPD-like: Derechos ARCO (Acceso, Rectificación, Cancelación, Oposición)

### Restricción Técnica
- Encriptación AES-256 en reposo
- TLS 1.3 en tránsito
- Sin envío de datos a terceros
- Infraestructura 100% en Argentina (Google Cloud Argentina región)

---

## 8. Riesgos y Mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|-----------|
| Cambios de alcance en último momento | ALTA | CRÍTICO | Change Control + Sign-off Dirección |
| Falta de datos training para IA | MEDIA | ALTO | Usar rúbrica conocida + templates |
| Rechazo del personal a usar sistema | BAJA | ALTO | Capacitación previa + transparencia |
| Problemas de cumplimiento legal | BAJA | CRÍTICO | Abogado consultor + auditoría |
| Downtime en producción | BAJA | CRÍTICO | Backup automático + disaster recovery |
| Recursos insuficientes ($ limitado) | BAJA | CRÍTICO | Stack 100% gratuito + CI/CD optimizado |

---

## 9. Dependencias

- **Autenticación**: Validación de Guzmán sobre flujo de evaluación
- **Infraestructura**: Google Cloud Account activo (hospital)
- **Datos**: Plantilla rúbrica oficial + indicadores por nivel
- **Legal**: Análisis de 14 normativas completado ✅
- **Capacitación**: Disponibilidad de jefes para training (19-20/12)

---

## 10. Entregables (Deliverables)

### Documentación ✅ COMPLETADA
- [x] PROJECT_CHARTER.md (este archivo)
- [x] PRD_COMPLETE.md
- [x] COMPLIANCE_ARGENTINA.md (14 leyes)
- [x] RUBRICA_EVALUACION.md
- [x] ESPECIFICACIONES_TECNICAS.md
- [x] DEPLOYMENT_PLAN.md
- [x] NORMATIVAS_ETICAS.md
- [x] LOGROS_HITOS.md
- [x] README.md (completo)

### Código
- Backend FastAPI (JWT + 2FA + APIs REST)
- Frontend React + React Native
- Base de datos PostgreSQL encriptada
- CI/CD con GitHub Actions
- Dockerfile + docker-compose

### Infraestructura
- Google Cloud Project configurado
- Cloud Run para backend serverless
- Cloud SQL para datos (AES-256)
- Cloud Storage para PDFs

### Testing
- Unit tests (pytest)
- Integration tests
- Security tests (OWASP)
- Load testing (100+ usuarios)

### Capacitación
- Documentación de usuario
- Video tutoriales
- Manual de administrador
- Soporte durante Go Live

---

## 11. Presupuesto

| Item | Cantidad | Costo Unitario | Total |
|------|----------|-----| -------|
| **INFRAESTRUCTURA** | | |
| Google Cloud (Free Tier) | 1 | $0 | **$0** |
| Dominio (opcional) | 1 | $0 (hospital.ar) | **$0** |
| **DESARROLLO** | | | |
| Horas Dev (donas Marcelo) | - | $0 (project interno) | **$0** |
| Herramientas (GitHub, VS Code) | - | $0 (free/open-source) | **$0** |
| **TOTAL** | | | **$0 USD** ✅ |

---

## 12. Timeline y Hitos

```
📅 SEMANA 1 (12/12-18/12): Repo + Infraestructura + Docs
  ✅ Repo GitHub creado
  ✅ Rama SIMULADOR protegida
  ✅ Documentación normativa completa
  ✅ PROJECT_CHARTER finalizado

📅 SEMANA 2 (19/12-25/12): Backend + Frontend Base
  ⏳ Backend core (Copilot)
  ⏳ Frontend conversacional base
  ⏳ BD schema definido
  ⏳ APIs REST implementadas

📅 SEMANA 3 (26/12-01/01): Integración + Testing
  ⏳ Motor conversacional completo
  ⏳ Generador PDF funcionando
  ⏳ RBAC implementado
  ⏳ Testing + QA

📅 SEMANA 4 (02/01-05/01): Staging + Go Live
  ⏳ Deployment a Staging GCP
  ⏳ Load testing
  ⏳ Capacitación
  🎯 **GO LIVE 05/01/2026**
```

---

## 13. Criteria de Éxito (Definition of Done)

✅ Sistema en PRODUCCIÓN y accesible
✅ 100% de 14 normativas analizadas cumplidas
✅ Todos los tests pasando (unit + integration + security)
✅ Documentación completa + video tutoriales
✅ Personal capacitado en uso + administración
✅ 0 downtime en primer mes
✅ Evaluaciones generadas en < 15 min
✅ Logs auditables 5 años retention
✅ Derecho de recurso habilitado para enfermeros

---

## 14. Autorización y Firma

**Aprobación:**

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| Project Manager | Marcelo Omar Lancry Kamycki | 12/12/2025 | ✅ |
| Supervisor | Guzmán Sandra | - | ⏳ |
| Dirección | Hospital de Clínicas | - | ⏳ |

---

**Última actualización**: 12 de Diciembre de 2025, 09:00 ARS
**Próxima revisión**: 19 de Diciembre de 2025
**Versión**: 1.0 (Inicial)
