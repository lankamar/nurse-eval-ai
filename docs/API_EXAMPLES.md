# API Usage Examples

## Authentication

### Register a new user

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria.garcia",
    "email": "maria.garcia@hospital.uba.ar",
    "full_name": "María García",
    "password": "SecurePass123!",
    "role": "enfermero"
  }'
```

Response:
```json
{
  "id": 1,
  "username": "maria.garcia",
  "email": "maria.garcia@hospital.uba.ar",
  "full_name": "María García",
  "role": "enfermero",
  "is_active": true,
  "totp_enabled": false,
  "created_at": "2024-01-15T10:00:00"
}
```

### Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria.garcia",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "requires_2fa": false
}
```

### Setup 2FA

```bash
curl -X POST "http://localhost:8000/api/auth/2fa/setup" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Response:
```json
{
  "secret": "JBSWY3DPEHPK3PXP",
  "qr_code_uri": "data:image/png;base64,iVBORw0KGgoAAAANS..."
}
```

### Verify 2FA

```bash
curl -X POST "http://localhost:8000/api/auth/2fa/verify" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "123456"
  }'
```

### Get Current User

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Evaluations

### Create Evaluation

```bash
curl -X POST "http://localhost:8000/api/evaluations/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "evaluated_id": 2,
    "period": "2024-Q1",
    "consent_given": true,
    "comments": "Evaluación trimestral"
  }'
```

Response:
```json
{
  "id": 1,
  "evaluator_id": 1,
  "evaluated_id": 2,
  "status": "draft",
  "period": "2024-Q1",
  "technical_score": null,
  "attitudinal_score": null,
  "total_score": null,
  "pdf_generated": false,
  "created_at": "2024-01-15T10:00:00"
}
```

### List Evaluations

```bash
curl -X GET "http://localhost:8000/api/evaluations/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Evaluation Details

```bash
curl -X GET "http://localhost:8000/api/evaluations/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Response:
```json
{
  "id": 1,
  "evaluator_id": 1,
  "evaluated_id": 2,
  "status": "completed",
  "period": "2024-Q1",
  "technical_score": 85.5,
  "attitudinal_score": 92.0,
  "total_score": 88.75,
  "pdf_generated": true,
  "pdf_path": "/path/to/pdf",
  "created_at": "2024-01-15T10:00:00",
  "completed_at": "2024-01-15T11:30:00",
  "evaluator": {
    "id": 1,
    "username": "supervisor.lopez",
    "full_name": "Laura López",
    "role": "supervisora"
  },
  "evaluated": {
    "id": 2,
    "username": "maria.garcia",
    "full_name": "María García",
    "role": "enfermero"
  },
  "responses": [
    {
      "id": 1,
      "criteria_id": 1,
      "score": 4,
      "comments": "Excelente dominio técnico",
      "created_at": "2024-01-15T10:15:00"
    }
  ]
}
```

### Add Response to Evaluation

```bash
curl -X POST "http://localhost:8000/api/evaluations/1/responses" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "criteria_id": 1,
    "score": 4,
    "comments": "Excelente conocimiento de técnicas específicas"
  }'
```

### Complete Evaluation

```bash
curl -X POST "http://localhost:8000/api/evaluations/1/complete" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Chatbot

### Start Conversation

```bash
curl -X POST "http://localhost:8000/api/chatbot/start/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Response:
```json
{
  "message": "¡Bienvenido a la Evaluación de Desempeño!\n\nEvaluemos la competencia técnica: **Conocimientos Técnicos Específicos**\n\nDominio de técnicas y procedimientos específicos de enfermería según área de desempeño\n\n¿Qué puntuación otorgaría del 1 al 5?",
  "is_question": true,
  "criteria_code": "TEC-01",
  "completed": false
}
```

### Send Message

```bash
curl -X POST "http://localhost:8000/api/chatbot/message" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "evaluation_id": 1,
    "message": "Otorgo una puntuación de 4. Demuestra muy buen dominio."
  }'
```

Response:
```json
{
  "message": "Evaluemos la competencia técnica: **Aplicación de Normas de Bioseguridad**\n\nCumplimiento riguroso de protocolos de bioseguridad e higiene hospitalaria\n\n¿Qué puntuación otorgaría del 1 al 5?",
  "is_question": true,
  "criteria_code": "TEC-02",
  "completed": false
}
```

## PDF Generation

### Generate PDF

```bash
curl -X POST "http://localhost:8000/api/pdf/generate" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "evaluation_id": 1
  }'
```

Response:
```json
{
  "pdf_path": "generated_pdfs/evaluation_1_20240115_103000.pdf",
  "pdf_hash": "a3d5f6e8b2c1d4e7f9a0b3c5d8e1f4a7b0c3d6e9f2a5b8c1d4e7f0a3b6c9d2e5"
}
```

### Download PDF

```bash
curl -X GET "http://localhost:8000/api/pdf/download/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  --output evaluation_1.pdf
```

## Python Examples

### Using requests library

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Login
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "username": "maria.garcia",
        "password": "SecurePass123!"
    }
)
token = login_response.json()["access_token"]

# Headers for authenticated requests
headers = {
    "Authorization": f"Bearer {token}"
}

# Create evaluation
evaluation = requests.post(
    f"{BASE_URL}/api/evaluations/",
    headers=headers,
    json={
        "evaluated_id": 2,
        "period": "2024-Q1",
        "consent_given": True
    }
)
evaluation_id = evaluation.json()["id"]

# Start chatbot conversation
conversation = requests.post(
    f"{BASE_URL}/api/chatbot/start/{evaluation_id}",
    headers=headers
)
print(conversation.json()["message"])

# Add responses
for criteria_id in range(1, 26):  # 25 criteria
    response = requests.post(
        f"{BASE_URL}/api/evaluations/{evaluation_id}/responses",
        headers=headers,
        json={
            "criteria_id": criteria_id,
            "score": 4,
            "comments": "Desempeño satisfactorio"
        }
    )

# Complete evaluation
complete = requests.post(
    f"{BASE_URL}/api/evaluations/{evaluation_id}/complete",
    headers=headers
)

# Generate PDF
pdf = requests.post(
    f"{BASE_URL}/api/pdf/generate",
    headers=headers,
    json={"evaluation_id": evaluation_id}
)
print(f"PDF generated: {pdf.json()['pdf_path']}")
```

## JavaScript/React Examples

### Using axios

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

// Login
const login = async (username, password) => {
  const response = await api.post('/api/auth/login', {
    username,
    password,
  });
  
  const { access_token } = response.data;
  localStorage.setItem('token', access_token);
  
  // Set default authorization header
  api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
  
  return response.data;
};

// Create evaluation
const createEvaluation = async (evaluatedId, period) => {
  const response = await api.post('/api/evaluations/', {
    evaluated_id: evaluatedId,
    period: period,
    consent_given: true,
  });
  
  return response.data;
};

// Get evaluations
const getEvaluations = async () => {
  const response = await api.get('/api/evaluations/');
  return response.data;
};

// Start chatbot
const startChatbot = async (evaluationId) => {
  const response = await api.post(`/api/chatbot/start/${evaluationId}`);
  return response.data;
};

// Send message
const sendMessage = async (evaluationId, message) => {
  const response = await api.post('/api/chatbot/message', {
    evaluation_id: evaluationId,
    message: message,
  });
  return response.data;
};

// Generate PDF
const generatePDF = async (evaluationId) => {
  const response = await api.post('/api/pdf/generate', {
    evaluation_id: evaluationId,
  });
  return response.data;
};

// Download PDF
const downloadPDF = async (evaluationId) => {
  const response = await api.get(`/api/pdf/download/${evaluationId}`, {
    responseType: 'blob',
  });
  
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `evaluation_${evaluationId}.pdf`);
  document.body.appendChild(link);
  link.click();
  link.remove();
};
```

## Testing with pytest

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login():
    # Register
    register_response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpass123",
            "role": "enfermero"
        }
    )
    assert register_response.status_code == 201
    
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
```
