import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [
    { duration: '30s', target: 10 },  // Ramp up to 10 users
    { duration: '1m', target: 50 },   // Ramp up to 50 users
    { duration: '2m', target: 50 },   // Stay at 50 users
    { duration: '30s', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
    errors: ['rate<0.1'],              // Error rate must be below 10%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

// Test scenarios
export default function () {
  // Test 1: Health check
  let healthRes = http.get(`${BASE_URL}/health`);
  check(healthRes, {
    'health check status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  sleep(1);

  // Test 2: Root endpoint
  let rootRes = http.get(`${BASE_URL}/`);
  check(rootRes, {
    'root status is 200': (r) => r.status === 200,
    'root has compliance info': (r) => r.json().compliance !== undefined,
  }) || errorRate.add(1);

  sleep(1);

  // Test 3: Register user
  const username = `user_${Date.now()}_${__VU}`;
  const registerPayload = JSON.stringify({
    username: username,
    email: `${username}@example.com`,
    full_name: 'Load Test User',
    password: 'testpass123',
    role: 'enfermero',
  });

  const registerParams = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  let registerRes = http.post(
    `${BASE_URL}/api/auth/register`,
    registerPayload,
    registerParams
  );
  
  check(registerRes, {
    'register status is 201': (r) => r.status === 201,
    'register returns user id': (r) => r.json().id !== undefined,
  }) || errorRate.add(1);

  sleep(1);

  // Test 4: Login
  const loginPayload = JSON.stringify({
    username: username,
    password: 'testpass123',
  });

  let loginRes = http.post(
    `${BASE_URL}/api/auth/login`,
    loginPayload,
    registerParams
  );

  let authToken = '';
  const loginCheck = check(loginRes, {
    'login status is 200': (r) => r.status === 200,
    'login returns token': (r) => r.json().access_token !== undefined,
  });

  if (loginCheck) {
    authToken = loginRes.json().access_token;
  } else {
    errorRate.add(1);
  }

  sleep(1);

  // Test 5: Get current user (authenticated)
  if (authToken) {
    const authParams = {
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    };

    let meRes = http.get(`${BASE_URL}/api/auth/me`, authParams);
    check(meRes, {
      'me endpoint status is 200': (r) => r.status === 200,
      'me endpoint returns username': (r) => r.json().username === username,
    }) || errorRate.add(1);
  }

  sleep(2);
}
