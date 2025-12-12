# 🚀 DEPLOYMENT_RUNBOOK

Guía rápida para poner NurseEval AI en producción/evaluación. Incluye opciones con créditos de estudiante y sin tarjeta (demo local + túnel).

## 0) Opciones de cuenta
- **Google Cloud student/edu**: si tu cuenta Pro Student tiene créditos, úsalos para activar billing. Necesitas facturación habilitada para Cloud Run/Cloud SQL/Storage aunque te mantengas en free tier.
- **GitHub Student Pack**: revisa si tienes cupones para Google Cloud u otros proveedores. Si obtienes código de créditos, actívalo en GCP y habilita billing.
- **Sin tarjeta**: usa demo local con túnel (ver sección 6).

## 1) Prerrequisitos
- gcloud instalado y autenticado: `gcloud auth login` y `gcloud config set project <PROJECT_ID>`
- Habilitar APIs: `gcloud services enable run.googleapis.com sqladmin.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com storage.googleapis.com`

## 2) Infra mínima (GCP Free Tier)
1. **Cloud SQL Postgres 13**: instancia db-f1-micro, DB `nurse_eval`, usuario `app` + password. Guarda la cadena de conexión completa.
2. **Cloud Storage**: bucket privado (ej. `nurse-eval-pdfs`).
3. **Secret Manager**: crea secretos `JWT_SECRET` (string fuerte) y `DATABASE_URL` (cadena a Cloud SQL). Vars planas: `TOTP_ISSUER=NurseEval`, `TOTP_INTERVAL=30`, `GCP_BUCKET=<tu_bucket>`.
4. (Opcional) **VPC Serverless Connector** si quieres conexión privada a Cloud SQL.

## 3) Build y deploy backend (Cloud Run)
```
cd backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/nurse-eval-backend .

gcloud run deploy nurse-eval-backend \
  --image gcr.io/$PROJECT_ID/nurse-eval-backend \
  --region southamerica-east1 \
  --platform managed \
  --allow-unauthenticated \
  --set-secrets JWT_SECRET=JWT_SECRET:latest,DATABASE_URL=DATABASE_URL:latest \
  --set-env-vars TOTP_ISSUER=NurseEval,TOTP_INTERVAL=30,GCP_BUCKET=<tu_bucket>
```
- Si usas Cloud SQL privado: agrega `--add-cloudsql-instances <INSTANCE_CONN_NAME>` y un Serverless VPC Connector.

## 4) Frontend (estático)
```
cd frontend
npm install
npm run build
```
Opción A (Cloud Run estático):
```
gcloud run deploy nurse-eval-frontend --source . \
  --region southamerica-east1 --platform managed --allow-unauthenticated \
  --set-env-vars VITE_API_URL=https://<backend-url>/api/v1
```
Opción B: Firebase Hosting sirviendo la carpeta `dist/`.

## 5) Cargar personal y probar
- Importar CSV `email,role`: `POST /api/v1/admin/import-staff` (usa `docs/staff_import_example.csv`). La respuesta trae password temporal, secreto TOTP y backup codes.
- Login: usuario demo `demo@hospital.test` / `P@ssw0rd!` (primer login devuelve `provisioning_uri` + header `X-TOTP-Secret`).
- Crear evaluación (25 ítems), firmar, descargar PDF (con hash/QR).

## 6) Demo sin tarjeta (local + túnel)
- Local: `docker-compose up -d`; backend: `uvicorn main:app --reload`; frontend: `npm install && npm run dev` (env `VITE_API_URL=http://localhost:8000/api/v1`).
- Exponer temporalmente: instala ngrok (o similar) y publica el puerto 8000 (backend) y/o 3000 (frontend) para compartir URL de demo. Ej.: `ngrok http 8000`.

## 7) Checklist de verificación
- Cloud Run backend: `/health` responde 200.
- Cloud SQL: conexión desde Cloud Run OK (logs sin errores de conexión).
- Importación CSV: retorna `created > 0` y lista `provisioned`.
- Login TOTP: flujo devuelve 200 con tokens.
- Evaluación: se crea, calcula total y clasificación, PDF generado.

## 8) Costos y límites
- Usa db-f1-micro y tráfico bajo en Cloud Run para permanecer en free tier. Monitorea en Billing -> Budgets/alerts.

## 9) Si algo falla
- Revisa logs de Cloud Run.
- Verifica secretos/vars y cadena `DATABASE_URL`.
- Asegura que la instancia Cloud SQL permita conexión (privada o pública con IP autorizada).
