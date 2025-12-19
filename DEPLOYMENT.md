# 🚀 Guía de Deployment - NurseEval AI

## 🎯 Estado Actual

**Backend**: Configurado para Render.com (PostgreSQL gratuito)  
**Frontend**: React + Vite (Static Site)

---

## 🔧 Deployment en Render.com (GRATIS)

### Paso 1: Crear cuenta en Render

1. Ve a [render.com](https://render.com)
2. Registrate con tu cuenta de GitHub
3. Autoriza acceso a tus repositorios

---

### Paso 2: Conectar el repositorio

1. En el dashboard de Render, click en **"New +"**
2. Selecciona **"Blueprint"**
3. Busca el repo: `lankamar/nurse-eval-ai`
4. Selecciona la rama: **`SIMULADOR`**
5. Click en **"Apply"**

Render detectará automáticamente el archivo `render.yaml` y creará:
- ✅ Base de datos PostgreSQL (`nurse-eval-db`)
- ✅ Backend API (`nurse-eval-api`)
- ✅ Frontend (`nurse-eval-frontend`)

---

### Paso 3: Configurar variables de entorno

#### Backend (`nurse-eval-api`)

En el dashboard del servicio backend, ve a **"Environment"** y agrega:

```bash
JWT_SECRET=<genera_un_secreto_aleatorio_seguro>
# Ejemplo: openssl rand -hex 32
```

Las demás variables ya están configuradas en `render.yaml`.

#### Frontend (`nurse-eval-frontend`)

La variable `VITE_API_URL` ya está configurada automáticamente en `render.yaml` apuntando a:
```
https://nurse-eval-api.onrender.com
```

---

### Paso 4: Deploy automático

Cada vez que hagas push a la rama `SIMULADOR`, Render desplegará automáticamente:

```bash
git push origin SIMULADOR
```

⏳ El deploy tarda ~5-7 minutos la primera vez.

---

## 🌐 URLs de Acceso

Una vez deployado, tendrás:

- **Frontend**: `https://nurse-eval-frontend.onrender.com`
- **Backend API**: `https://nurse-eval-api.onrender.com`
- **Docs API**: `https://nurse-eval-api.onrender.com/docs`
- **Health Check**: `https://nurse-eval-api.onrender.com/health`

---

## 💻 Desarrollo Local

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend corriendo en: `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend corriendo en: `http://localhost:5173`

---

## 🔐 Usuario Demo

Para probar el sistema deployado:

- **Email**: `demo@hospital.test`
- **Password**: `P@ssw0rd!`
- **TOTP Secret** (para 2FA): `JBSWY3DPEHPK3PXP`
  - Usa Google Authenticator o similar

**Backup Codes**:
```
BACKUP-0001
BACKUP-0002
BACKUP-0003
BACKUP-0004
BACKUP-0005
```

---

## ✅ Verificar Deployment

### 1. Backend Health Check
```bash
curl https://nurse-eval-api.onrender.com/health
# Respuesta esperada: {"status":"ok"}
```

### 2. Frontend
Abre en el navegador:
```
https://nurse-eval-frontend.onrender.com
```

Deberías ver la página de login de NurseEval AI.

---

## 🔄 Troubleshooting

### Error: "Application failed to respond"

**Causa**: El backend no inició correctamente.

**Solución**:
1. Ve a los logs del servicio en Render
2. Verifica que la variable `DATABASE_URL` esté configurada
3. Verifica que `JWT_SECRET` esté configurado

### Error: "Failed to fetch"

**Causa**: El frontend no puede conectarse al backend.

**Solución**:
1. Verifica que `VITE_API_URL` apunte a la URL correcta del backend
2. Verifica que el backend tenga CORS habilitado (ya configurado)

### Error: "Database connection failed"

**Causa**: PostgreSQL no está disponible.

**Solución**:
1. Espera 2-3 minutos (Render está iniciando la BD)
2. Verifica que el servicio de BD esté en estado "Available"

---

## 📊 Monitoreo

Render provee:
- ✅ Logs en tiempo real
- ✅ Métricas de CPU/RAM
- ✅ Health checks automáticos
- ✅ Reinicio automático en caso de falla

---

## 🔒 Backups

Render hace backups automáticos de la base de datos PostgreSQL (plan free: 7 días retención).

---

## 💰 Costos

**Plan Free de Render incluye**:
- ✅ 750 horas/mes de compute (suficiente para 1 servicio 24/7)
- ✅ PostgreSQL con 1GB storage
- ✅ 100GB bandwidth/mes
- ✅ SSL/HTTPS gratis
- ⚠️ El servicio se duerme después de 15 min de inactividad (primer request tarda ~30 seg)

**Costo total**: **$0 USD/mes** ✅

---

## 🚀 Próximos Pasos

1. ✅ Deploy en Render (siguiendo esta guía)
2. ✅ Probar login con usuario demo
3. ✅ Crear evaluación de prueba
4. ✅ Capacitar a jefes/supervisora
5. ✅ **GO LIVE**: 05/01/2026

---

**Última actualización**: 19 de Diciembre de 2025  
**Versión**: 1.0 (MVP)
