# ☁️ DEPLOYMENT_PLAN (GCP Free Tier)

## 1. Pre-requisitos
- Proyecto GCP con facturación habilitada (modo free tier).
- gcloud CLI autenticado.
- Habilitar APIs: Cloud Run, Cloud SQL Admin, Cloud Storage, Secret Manager, Cloud Build.

## 2. Infraestructura
1) **Cloud SQL Postgres 13**
   - Crear instancia db-f1-micro, región `southamerica-east1`.
   - Crear base `nurse_eval`, usuario `app` con contraseña segura.
2) **Cloud Storage**
   - Bucket `nurse-eval-pdfs` (uniform access, no public).
3) **Secret Manager**
   - Guardar `JWT_SECRET`, `DATABASE_URL`, `TOTP_ISSUER`, `TOTP_INTERVAL`, `GCP_BUCKET`.
4) **VPC Serverless Connector** (si se usa conexión privada a Cloud SQL).

## 3. Build & Deploy Backend (Cloud Run)
```
gcloud builds submit --tag gcr.io/$PROJECT_ID/nurse-eval-backend ./backend

gcloud run deploy nurse-eval-backend \
  --image gcr.io/$PROJECT_ID/nurse-eval-backend \
  --region southamerica-east1 \
  --platform managed \
  --allow-unauthenticated \
  --set-secrets JWT_SECRET=JWT_SECRET:latest,DATABASE_URL=DATABASE_URL:latest \
  --set-env-vars TOTP_ISSUER=NurseEval,TOTP_INTERVAL=30,GCP_BUCKET=nurse-eval-pdfs
```

## 4. Base de datos y migraciones
- Ejecutar Alembic migrations conectando a Cloud SQL (pendiente de implementación).
- Opcional: Cloud SQL Auth Proxy para desarrollo local.

## 5. Frontend
- Build estático con `npm run build` y servir en Cloud Run (estático) o en Firebase Hosting.
- Configurar `VITE_API_URL` apuntando a la URL de Cloud Run backend.

## 6. Observabilidad
- Cloud Logging habilitado por defecto en Cloud Run.
- Configurar alertas de disponibilidad (uptime checks) y errores 5xx.

## 7. Seguridad y compliance
- No exponer bucket públicamente.
- Forzar HTTPS en Cloud Run.
- Rotar secretos cada 90 días.

## 8. Plan de rollback
- Mantener última imagen estable en Cloud Run (revisión previa).
- En caso de falla, revertir a revisión anterior desde consola de Cloud Run.
