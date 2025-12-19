# 🚀 DEPLOY NURSEEVAL AI A RENDER - PRÓXIMOS PASOS

**Fecha**: 19/12/2025  
**Estado**: Código listo en GitHub, necesita deploy final a Render  
**Rama**: `SIMULADOR`

---

## ⚠️ PROBLEMA ENCONTRADO

Render rechazó el Blueprint porque hay error en `render.yaml`:

```
Error: fromDatabase reference incorrect
```

---

## ✅ PASO 1: CORREGIR render.yaml (EN CODESPACES)

1. **Abrí Codespaces** de nurse-eval-ai
2. **Abrí el archivo**: `render.yaml`
3. **Buscá esta línea** (alrededor de línea 18):

```yaml
envVars:
  - key: DATABASE_URL
    fromDatabase: nurse-eval-db
```

4. **Reemplazalo con ESTO**:

```yaml
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: nurse-eval-db
      property: connectionString
```

5. **Guardá el archivo** (Ctrl+S)
6. **En la terminal de Codespaces**:

```bash
git add render.yaml
git commit -m "Fix render.yaml database connection reference"
git push origin SIMULADOR
```

**Espera a que termine el push** (debería decir "1 file changed").

---

## ✅ PASO 2: RETRY EN RENDER

1. **Volvé a**: https://dashboard.render.com/blueprint/new
2. **Hacé clic en el botón** `Retry` (abajo)
3. **Render debería validar el render.yaml correctamente** (sin errores en rojo)

---

## ✅ PASO 3: CONFIGURE JWT_SECRET

Una vez que valide, Render te mostrará un formulario con variables de entorno.

**Para el Backend (`nurse-eval-api`)**:

- Buscá la variable `JWT_SECRET`
- Si no existe, creá una nueva
- **Value**: Pegá esto:

```
a7f3e2b9c1d4a6e8f0b2c4d6e8f0a2b4c6d8e0f2a4b6c8e0a2b4d6e8f0a2b4
```

---

## ✅ PASO 4: DEPLOY

1. **Hacé clic en el botón principal** `Deploy` o `Apply`
2. **Render comenzará a**:
   - ✅ Crear BD PostgreSQL
   - ✅ Compilar Backend (FastAPI)
   - ✅ Compilar Frontend (React)

**Esto tarda ~10 minutos**. Podés ver el progreso en los logs.

---

## ✅ PASO 5: VERIFICAR DEPLOY

Una vez que termine:

### Backend Health Check

Abrí en el navegador:
```
https://nurse-eval-api.onrender.com/health
```

**Deberías ver**:
```json
{"status":"ok"}
```

### Frontend

Abrí:
```
https://nurse-eval-frontend.onrender.com
```

**Deberías ver** la pantalla de login de NurseEval

### Probar Login

- **Email**: `demo@hospital.test`
- **Password**: `P@ssw0rd!`
- **2FA Code**: Usa `BACKUP-0001` (o el código que Google Authenticator genere)

---

## 🎯 URLS FINALES

Cuando todo esté listo:

| Servicio | URL |
|----------|-----|
| Frontend | https://nurse-eval-frontend.onrender.com |
| Backend API | https://nurse-eval-api.onrender.com |
| API Docs | https://nurse-eval-api.onrender.com/docs |
| Health Check | https://nurse-eval-api.onrender.com/health |

---

## 📝 RESUMEN

✅ Código backend + frontend: **COMPLETO**  
✅ Documentación: **COMPLETA**  
❌ Render deploy: **BLOQUEADO por error en render.yaml**

**Acción necesaria**: Corregir render.yaml y reintentar en Render.

---

## 💡 PRÓXIMAS MEJORAS (después de deploy)

- [ ] Integrar Gemini API para feedback inteligente
- [ ] Agregar gráficos de progreso
- [ ] Panel administrativo para jefes
- [ ] Link en tu portafolio de Hostinger

---

**¡LO TIENES! 🚀 Solo corregir render.yaml y deploy automático en Render.**
