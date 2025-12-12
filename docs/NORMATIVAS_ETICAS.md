# ⚖️ NORMATIVAS_ETICAS

Principios éticos aplicados al desarrollo y operación de NurseEval AI.

## 1. Transparencia
- Explicar criterios de evaluación (rúbrica oficial) a todo evaluado.
- Portal permite ver resultados y descargar PDF.

## 2. No discriminación
- Preguntas neutras, sin sesgos sugeridos.
- Algoritmo de cálculo determinístico (CT×0.6 + CA×0.4), sin ponderaciones ocultas.

## 3. Privacidad y datos personales
- Cumplimiento Ley 25.326 (ARCO). Consentimiento explícito antes de mostrar evaluaciones.
- Minimización: solo se almacenan datos necesarios para el acto administrativo.

## 4. Seguridad
- 2FA obligatorio para jefes/supervisora.
- Datos en tránsito cifrados (TLS 1.3) y en reposo (AES-256 en BD administrada).

## 5. Trazabilidad y auditoría
- Logs inmutables 5 años (política de retención declarada).
- Firma digital de evaluaciones con hash y QR en PDF.

## 6. Derecho a recurso
- Canal de observaciones habilitado; respuestas documentadas.

## 7. Supervisión humana
- Decisiones finales recaen en jefes/supervisora; la IA es asistente conversacional.

## 8. Deber de confidencialidad
- Acceso por rol; restricciones para evitar exposición de datos clínicos o sensibles.
