import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <nav className="navbar">
      <div className="container">
        <Link to="/" className="navbar-brand">
          Nurse Eval AI
        </Link>
        <div className="navbar-menu">
          {isAuthenticated ? (
            <>
              <span style={{ color: 'white' }}>
                {user?.full_name} ({user?.role})
              </span>
              <Link to="/dashboard" className="navbar-link">
                Dashboard
              </Link>
              {(user?.role === 'admin' || user?.role === 'jefe') && (
                <Link to="/admin" className="navbar-link">
                  Administración
                </Link>
              )}
              <button
                onClick={logout}
                className="btn btn-secondary"
                style={{ padding: '5px 15px' }}
              >
                Cerrar Sesión
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-link">
                Iniciar Sesión
              </Link>
              <Link to="/register" className="navbar-link">
                Registrarse
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
