import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { evaluationService } from '../services/api';

const Dashboard = () => {
  const { user } = useAuth();
  const [evaluations, setEvaluations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadEvaluations();
  }, []);

  const loadEvaluations = async () => {
    try {
      const response = await evaluationService.listEvaluations();
      setEvaluations(response.data);
    } catch (err) {
      setError('Error al cargar evaluaciones');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      draft: { color: '#6c757d', text: 'Borrador' },
      in_progress: { color: '#ffc107', text: 'En Progreso' },
      completed: { color: '#28a745', text: 'Completada' },
      approved: { color: '#007bff', text: 'Aprobada' },
      rejected: { color: '#dc3545', text: 'Rechazada' },
    };

    const badge = badges[status] || { color: '#6c757d', text: status };

    return (
      <span
        style={{
          backgroundColor: badge.color,
          color: 'white',
          padding: '4px 8px',
          borderRadius: '4px',
          fontSize: '12px',
        }}
      >
        {badge.text}
      </span>
    );
  };

  if (loading) {
    return <div className="loading">Cargando...</div>;
  }

  return (
    <div className="container">
      <div className="card">
        <h1 style={{ color: '#1a5490' }}>Dashboard</h1>
        <p>
          Bienvenido, <strong>{user?.full_name}</strong> ({user?.role})
        </p>
      </div>

      <div className="card">
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '20px',
          }}
        >
          <h2>Mis Evaluaciones</h2>
          {(user?.role === 'supervisora' ||
            user?.role === 'jefe' ||
            user?.role === 'admin') && (
            <Link to="/evaluations/new">
              <button className="btn btn-primary">
                Nueva Evaluación
              </button>
            </Link>
          )}
        </div>

        {error && <div className="error-message">{error}</div>}

        {evaluations.length === 0 ? (
          <p>No hay evaluaciones disponibles.</p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table
              style={{
                width: '100%',
                borderCollapse: 'collapse',
              }}
            >
              <thead>
                <tr
                  style={{
                    backgroundColor: '#f8f9fa',
                    borderBottom: '2px solid #dee2e6',
                  }}
                >
                  <th style={{ padding: '10px', textAlign: 'left' }}>ID</th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>
                    Evaluado
                  </th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>
                    Período
                  </th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>
                    Estado
                  </th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>
                    Puntaje
                  </th>
                  <th style={{ padding: '10px', textAlign: 'left' }}>
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody>
                {evaluations.map((evaluation) => (
                  <tr
                    key={evaluation.id}
                    style={{ borderBottom: '1px solid #dee2e6' }}
                  >
                    <td style={{ padding: '10px' }}>{evaluation.id}</td>
                    <td style={{ padding: '10px' }}>
                      Evaluación #{evaluation.evaluated_id}
                    </td>
                    <td style={{ padding: '10px' }}>{evaluation.period}</td>
                    <td style={{ padding: '10px' }}>
                      {getStatusBadge(evaluation.status)}
                    </td>
                    <td style={{ padding: '10px' }}>
                      {evaluation.total_score
                        ? `${evaluation.total_score.toFixed(2)}%`
                        : '-'}
                    </td>
                    <td style={{ padding: '10px' }}>
                      <Link to={`/evaluations/${evaluation.id}`}>
                        <button className="btn btn-primary" style={{ padding: '5px 10px', fontSize: '12px' }}>
                          Ver Detalles
                        </button>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
