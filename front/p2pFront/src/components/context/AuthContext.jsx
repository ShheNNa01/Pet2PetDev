import { createContext, useContext, useState, useEffect } from 'react';
import AuthService from '../services/auth.service';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [tokenRefreshInterval, setTokenRefreshInterval] = useState(null);

  // Función para refrescar el token
  const refreshUserToken = async () => {
    try {
      const response = await AuthService.refreshToken();
      const { access_token } = response;
      
      // Actualizar el token en el estado del usuario
      setUser(prevUser => ({
        ...prevUser,
        token: access_token
      }));
    } catch (error) {
      console.error('Error refreshing token:', error);
      logout(); // Si falla el refresh, desloguear al usuario
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (token && storedUser) {
      try {
        const userData = JSON.parse(storedUser);
        userData.role_id = userData.role_id || userData.rol_id;
        userData.city = userData.city || 'global';
        setUser({ ...userData, token });

        // Iniciar el intervalo de refresh del token
        const interval = setInterval(refreshUserToken, 25 * 60 * 1000); // 25 minutos
        setTokenRefreshInterval(interval);
      } catch (error) {
        console.error('Error parsing stored user:', error);
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
      }
    }
    setLoading(false);

    // Cleanup del intervalo
    return () => {
      if (tokenRefreshInterval) {
        clearInterval(tokenRefreshInterval);
      }
    };
  }, []);

  const login = (userData) => {
    const { access_token, refresh_token, user: userDetails } = userData;

    const userToStore = {
      ...userDetails,
      role_id: userDetails.role_id || userDetails.rol_id,
      city: userDetails.city || 'global'
    };

    localStorage.setItem('token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('user', JSON.stringify(userToStore));
    setUser({ ...userToStore, token: access_token });

    // Iniciar el intervalo de refresh del token
    const interval = setInterval(refreshUserToken, 25 * 60 * 1000); // 25 minutos
    setTokenRefreshInterval(interval);
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    localStorage.removeItem('currentPet');
    setUser(null);

    // Limpiar el intervalo de refresh
    if (tokenRefreshInterval) {
      clearInterval(tokenRefreshInterval);
      setTokenRefreshInterval(null);
    }
  };

  const isAdmin = user?.role_id === 2 || user?.rol_id === 2;

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        loading,
        isAdmin,
        isAuthenticated: !!user,
        getUserCity: () => user?.city || 'global',
        refreshToken: refreshUserToken // Exponemos la función de refresh
      }}
    >
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de un AuthProvider');
  }
  return context;
};