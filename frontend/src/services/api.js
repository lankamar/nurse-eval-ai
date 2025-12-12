import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth services
export const authService = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', data),
  getCurrentUser: () => api.get('/api/auth/me'),
  setup2FA: () => api.post('/api/auth/2fa/setup'),
  verify2FA: (token) => api.post('/api/auth/2fa/verify', { token }),
  disable2FA: (token) => api.post('/api/auth/2fa/disable', { token }),
};

// Evaluation services
export const evaluationService = {
  createEvaluation: (data) => api.post('/api/evaluations/', data),
  listEvaluations: (params) => api.get('/api/evaluations/', { params }),
  getEvaluation: (id) => api.get(`/api/evaluations/${id}`),
  addResponse: (evaluationId, data) => 
    api.post(`/api/evaluations/${evaluationId}/responses`, data),
  completeEvaluation: (id) => api.post(`/api/evaluations/${id}/complete`),
};

// Chatbot services
export const chatbotService = {
  startConversation: (evaluationId) => 
    api.post(`/api/chatbot/start/${evaluationId}`),
  sendMessage: (data) => api.post('/api/chatbot/message', data),
};

// PDF services
export const pdfService = {
  generatePDF: (evaluationId) => 
    api.post('/api/pdf/generate', { evaluation_id: evaluationId }),
  downloadPDF: (evaluationId) => 
    api.get(`/api/pdf/download/${evaluationId}`, { responseType: 'blob' }),
};

export default api;
