// src/guards/AdminGuard.jsx
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const AdminGuard = () => {
  const { isAuthenticated, isAdmin, loading, user } = useAuth();

  // Debug
  console.log('AdminGuard - Estado de autenticación:', {
    isAuthenticated,
    isAdmin,
    loading,
    userData: user,
    userRolId: user?.rol_id
  });

  if (loading) {
    return <div>Cargando...</div>;
  }

  if (!isAuthenticated || !isAdmin) {
    console.log('Acceso denegado:', {
      isAuthenticated,
      isAdmin,
      userRolId: user?.rol_id
    });
    return <Navigate to="/" replace />;
  }

  console.log('Acceso permitido a ruta admin');
  return <Outlet />;
};