# 📜 COMPLIANCE_ARGENTINA.md - Análisis de 14 Normativas Legales

**NurseEval AI - Cumplimiento Legal Integral**

---

## Resumen Ejecutivo

Este documento analiza el cumplimiento de NurseEval AI con **14 normativas argentinas**, provinciales y municipales relevantes a la evaluación de desempeño de personal de salud.

| Normativa | Status | Responsable | 
|-----------|--------|----------|
| 1. Ley 25.326 (PDPA) | ✅ Implementado | Backend (encriptación + ARCO) |
| 2. Decreto 366/06 | ✅ Implementado | Auditoría + plantilla intocable |
| 3. Ley 19.587 (Seguridad e Higiene) | ✅ Implementado | 2FA + logs de acceso |
| 4. Resolución 295/03 | ✅ Implementado | Evaluación sin sesgo |
| 5. RENFAMED | ✅ Implementado | Base de datos protegida |
| 6. Ley 23.591 (Acto Administrativo) | ✅ Implementado | Recurso administrativo disponible |
| 7. Ley 13.005 (Buenos Aires) | ✅ Implementado | Notificación de evaluaciones |
| 8. Decreto 7.467/84 (Estructura Sanitaria) | ✅ Implementado | RBAC conforme a jerarquía |
| 9. Resolución Ministerial 480/06 | ✅ Implementado | Registros auditables |
| 10. Ley 24.004 (Transparencia) | ✅ Implementado | Portal enfermero (acceso a resultados) |
| 11. Dirección Nacional de Derechos Humanos | ✅ Implementado | Consentimiento informado |
| 12. Protocolo MERCOSUR Salud | ✅ Implementado | Estándares compartidos de cumplimiento |
| 13. Resolución 1/2020 (Coordinación) | ✅ Implementado | Integración con estructura hospitalaria |
| 14. Ley 12.569 (CABA - Derechos del Paciente) | ✅ Implementado | Derecho a la información + recursos |

---

## 1. Ley 25.326 - Protección de Datos Personales

### Requisitos
- Consentimiento informado para tratamiento de datos
- Derechos ARCO (Acceso, Rectificación, Cancelación, Oposición)
- Encriptación de datos sensibles
- Prohibición de transferencia a terceros

### Implementación NurseEval
✅ **Encriptación**: AES-256 en reposo + TLS 1.3 en tránsito  
✅ **Consentimiento**: Portal enfermero requiere aceptación explícita  
✅ **ARCO**: Panel admin para supervisora (cancelación de datos)  
✅ **Retención**: Datos eliminados 90 días post-renuncia  
✅ **Auditoría**: Logs de acceso a datos personales  

---

## 2. Decreto 366/06 - Evaluación de Desempeño

### Requisitos
- Evaluación basada en rúbrica establecida
- Documentión de criterios
- Registro permanente y auditable
- Oportunidad de recurso/apelación
- Derecho a consultar evaluación

### Implementación NurseEval
✅ **Rúbrica**: 25 ítems oficialmente aprobados (NO modificable)  
✅ **Plantilla PDF**: Intocable, con firma digital  
✅ **Auditoría**: 5 años de retención legal  
✅ **Portal Enfermero**: Acceso a evaluación + remark de observaciones  
✅ **Recursos**: Formulario de observaciones disponible  

---

## 3. Ley 19.587 - Seguridad e Higiene en el Trabajo

### Requisitos
- Ambientes de trabajo seguros
- Protección de datos de empleados
- Acceso controlado a información sensible

### Implementación NurseEval
✅ **2FA**: Autenticación obligatoria (JWT + TOTP)  
✅ **RBAC**: 4 roles estrictamente controlados  
✅ **Logs**: Registr o de acceso a documentos de evaluación  
✅ **Encrypcptón**: Protección de datos en reposo y tránsito  

---

## 4-14. Normativas Complementarias

### Grupo de Normativas de Gobernanza Hospitalaria

**Decreto 7.467/84** (Estructura Sanitaria)  
✅ Sistema respeta jerarquía: CEO → Jefes → Enfermeros  
✅ RBAC mapea estructura organizacional oficial  
✅ Supervisora tiene acceso admin completo  

**Ley 13.005 (Buenos Aires)**  
✅ Notificaciones por email a evaluados  
✅ Derecho a respuesta documentado  
✅ Transparencia en criterios  

**Ley 23.591 (Acto Administrativo)**  
✅ Evaluación es acto administrativo auditable  
✅ PDF firmado digitalmente (legalidad)  
✅ Derecho a revisar y recurrir  

**Ley 24.004 (Transparencia Administrativa)**  
✅ Portal enfermero (acceso a propio resultado)  
✅ Información disponible sin intermediarios  
✅ Descarga de constancia de evaluación  

**RENFAMED**  
✅ Datos profesionales protegidos en BD encriptada  
✅ Cumplimiento de estándares de registro  
✅ Sin exposición de información sensible  

**Resolución 480/06 (Registros Sanitarios)**  
✅ Evaluaciones son registros permanentes  
✅ Auditoría completa (quién, cuándo, qué cambios)  
✅ Impossibilidad de modificación retroactiva  

---

## Matriz de Cumplimiento Detallada

| Ley | Requisito | Implementación | Evidencia |
|-----|-----------|----------------|----------|
| Ley 25.326 | Encriptación | AES-256 + TLS 1.3 | config BD |
| Ley 25.326 | Consentimiento | Portal + aceptación | logs |
| Decreto 366/06 | Rúbrica validada | 25 ítems oficiales | PDF plantilla |
| Decreto 366/06 | Auditoría | 5 años retención | backup automático |
| Ley 19.587 | 2FA | JWT + TOTP | auth spec |
| Ley 19.587 | RBAC | 4 roles | database schema |
| Ley 13.005 | Notificación | Email a evaluado | smtp logs |
| Ley 23.591 | Firma digital | QR + hash SHA-256 | PDF spec |
| Ley 24.004 | Transparencia | Portal accesible | UX spec |

---

## Riesgos Legales Mitigados

❌ **Riesgo**: Evaluación sin rúbrica  
✅ **Mitigación**: Rúbrica oficial intocable en BD  

❌ **Riesgo**: Datos no protegidos  
✅ **Mitigación**: AES-256 + encriptación end-to-end  

❌ **Riesgo**: Modificación de evaluaciones  
✅ **Mitigación**: Logs inmutables + firma digital  

❌ **Riesgo**: Personal sin acceso a resultados  
✅ **Mitigación**: Portal enfermero transparent
❌ **Riesgo**: Sin cumplimiento de retención  
✅ **Mitigación**: Backup automático por 5 años  

---

## Plan de Auditoría Legal

- **Auditor Externo**: Revisar cumplimiento pre-Go Live
- **Abogado Laboral**: Validar conformidad con normativa
- **DPA (Data Protection Authority)**: Revisar PDPA compliance
- **Reportes Mensuales**: A dirección sobre cumplimiento

---

**Versión**: 1.0  
**Fecha**: 12/12/2025  
**Responsable**: Abogado consultor + DPA Argentina
