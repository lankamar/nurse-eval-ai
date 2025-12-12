# 📋 PRD_COMPLETE.md - Documento de Requisitos del Producto

**NurseEval AI - Evaluación Inteligente de Enfermería**

---

## 1. Resumen Ejecutivo

Este documento especifica los requisitos funcionales y no-funcionales para NurseEval AI, un sistema conversacional de IA que automatiza la evaluación de desempeño del personal de enfermería del Hospital de Clínicas José de San Martín con cumplimiento total de Decreto 366/06 y Ley 25.326.

**Alcance**: Chatbot inteligente + Portal enfermero + Generador PDF auditable  
**Usuarios**: 200+ enfermeros + 5+ jefes + 1 supervisora  
**Presupuesto**: $0 USD (stack gratuito)  
**Timeline**: 4 semanas (05/01/2026 Go Live)  

---

## 2. Historias de Usuario

### 2.1 Chatbot Conversacional

**US-001: Chatbot 2FA Login**
```
Como: Jefe de sala
Quiero: Acceder al sistema con seguridad
Para: Evaluar personal sin riesgos de suplantación

Criterios de Aceptación:
- JWT token + TOTP 2FA
- Códigos de respaldo (10) si pierde TOTP
- Timeout 15 min de inactividad
- Logs de acceso auditables
```

**US-002: Evaluación Conversacional**
```
Como: Jefe evaluador
Quiero: Realizar evaluación mediante chat
Para: Reducir tiempo de evaluación de 45min → 15min

Criterios de Aceptación:
- 25 preguntas (11 técnicas + 14 actitudinales)
- Escala 1-5 por ítem
- Cálculo automático: CT×60% + CA×40%
- Sin sesgo (nó hay prompts sugestivos)
- Guarda progreso auto cada 30seg
```

**US-003: Generación PDF Auditable**
```
Como: Sistema
Quiero: Generar PDF con plantilla intocable
Para: Cumplir con normas de evaluación oficial

Criterios de Aceptación:
- Plantilla hospital oficialmente aprobada (NO CAMBIOS)
- Firma digital jefe + fecha/hora
- QR para validación (hash SHA-256)
- PDF descargable e imprimible
```

### 2.2 Portal Enfermero

**US-004: Transparencia - Ver Evaluación**
```
Como: Enfermero evaluado
Quiero: Ver mi evaluación + rúbrica
Para: Conocer criterios y resultados

Criterios de Aceptación:
- Requiere consentimiento explícito ("He leído la rúbrica")
- Vista read-only del PDF
- Acceso solo a su evaluación (RBAC)
- Puedo descargar constancia
```

**US-005: Observaciones y Recursos**
```
Como: Enfermero
Quiero: Enviar observaciones a jefes
Para: Cuestionar evaluación si considero injusta

Criterios de Aceptación:
- Formulario de observaciones
- Jefes notificados por email
- Jefes responden en el portal
- Trazabilidad completa (logs)
```

### 2.3 Administración

**US-006: Dashboard Admin Supervisora**
```
Como: Supervisora Sandra Guzmán
Quiero: Ver estadísticas de evaluaciones
Para: Supervisar proceso + reportes

Criterios de Aceptación:
- Total evaluaciones por mes/sala
- Promedio puntajes por área
- Descargar reportes (CSV, Excel)
- Ver logs de auditoría
```

---

## 3. Requisitos No-Funcionales

### 3.1 Rendimiento
- Respuesta chatbot: < 2 segundos
- Generación PDF: < 5 segundos
- DB queries: < 100ms (P95)
- Soportar 100+ usuarios concurrentes (load testing)

### 3.2 Disponibilidad
- Uptime: 99.5% SLA
- Backup automático cada 6 horas
- Disaster recovery RTO: 4h, RPO: 1h

### 3.3 Seguridad
- Encriptación AES-256 en reposo
- TLS 1.3 en tránsito
- 2FA obligatorio (jefes)
- OWASP Top 10 testing
- Pentesting antes de Go Live

### 3.4 Compliance
- Ley 25.326: Derechos ARCO implementados
- Decreto 366/06: Evaluaciones auditables
- RENFAMED: Datos profesionales protegidos
- GDPR-like: Derecho al olvido implementado

### 3.5 Usabilidad
- Mobile-responsive (tablets + celulares)
- Interfaz en español
- Accesibilidad WCAG 2.1 AA
- No requiere capacitación técnica avanzada

---

## 4. Requisitos Datos

### 4.1 Modelo de Datos

**Tablas Clave:**
- `users`: ID, email, role, 2fa_secret, activo
- `evaluations`: ID, evaluador_id, evaluado_id, fecha, scores (JSON), estado
- `evaluation_items`: ID, tipo (Técnico/Actitudinal), criterio, puntaje (1-5)
- `audit_logs`: ID, usuario_id, acción, timestamp, datos_modificados
- `observations`: ID, evaluado_id, comentario, estado_recurso

### 4.2 Retención de Datos
- Evaluaciones: 5 años (por ley)
- Logs auditoría: 5 años
- Datos personales: Eliminación en 90 días post-renuncia

---

## 5. Integraciones

- **Email**: Notificaciones (observaciones, recordatorios)
- **Cloud Storage**: PDFs en Google Cloud Storage
- **Autenticación**: TOTP (Google Authenticator, Microsoft Authenticator)

---

## 6. Criterios de Éxito del MVP

✅ 100% de historias usuario implementadas  
✅ Todos los tests pasando (80%+ coverage)  
✅ Performance SLA cumplido  
✅ Auditoría legal validada  
✅ 0 vulnerabilidades críticas (OWASP)  
✅ Personal capacitado + aceptación del usuario  

---

**Versión**: 1.0  
**Fecha**: 12/12/2025
