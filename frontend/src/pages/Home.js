import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="container">
      <div className="card">
        <h1 style={{ color: '#1a5490' }}>
          Sistema de Evaluación de Desempeño de Enfermería
        </h1>
        <h2>Hospital de Clínicas José de San Martín - UBA</h2>
        <p>
          Sistema conversacional de evaluación basado en inteligencia artificial
          con cumplimiento normativo completo.
        </p>

        <div style={{ marginTop: '30px' }}>
          <h3>Características Principales:</h3>
          <ul>
            <li>🔐 Autenticación segura con JWT y 2FA TOTP</li>
            <li>🤖 Chatbot conversacional para evaluaciones</li>
            <li>📊 Evaluación basada en 25 competencias (Decreto 366/06)</li>
            <li>📄 Generación automática de PDFs auditables</li>
            <li>👥 Control de acceso basado en roles (RBAC)</li>
            <li>⚖️ Cumplimiento normativo (Ley 25.326 + RENFAMED)</li>
          </ul>
        </div>

        <div style={{ marginTop: '30px' }}>
          <h3>Marco Normativo:</h3>
          <ul>
            <li>📋 Decreto 366/06 - Evaluación de Desempeño del Personal de Enfermería</li>
            <li>🔒 Ley 25.326 - Protección de Datos Personales</li>
            <li>🏥 RENFAMED - Registro Nacional de Profesionales de Salud</li>
          </ul>
        </div>

        <div style={{ marginTop: '40px', display: 'flex', gap: '20px' }}>
          <Link to="/login">
            <button className="btn btn-primary">Iniciar Sesión</button>
          </Link>
          <Link to="/register">
            <button className="btn btn-secondary">Registrarse</button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;
