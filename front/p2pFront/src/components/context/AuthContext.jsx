import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
   
    if (token && storedUser) {
      try {
        const userData = JSON.parse(storedUser);
        console.log('Datos cargados del localStorage:', userData);
        // Aseguramos que role_id y city estén presentes
        userData.role_id = userData.role_id || userData.rol_id;
        userData.city = userData.city || 'global'; // Valor por defecto si no hay ciudad
        setUser({ ...userData, token });
      } catch (error) {
        console.error('Error parsing stored user:', error);
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      }
    }
    setLoading(false);
  }, []);

  const login = (userData) => {
    const { access_token, user: userDetails } = userData;
    console.log('Datos completos recibidos en login:', userData);
    console.log('Datos del usuario:', userDetails);
    
    // Aseguramos que role_id y city estén presentes
    const userToStore = {
      ...userDetails,
      role_id: userDetails.role_id || userDetails.rol_id,
      city: userDetails.city || 'global' // Valor por defecto si no hay ciudad
    };
    
    localStorage.setItem('token', access_token);
    localStorage.setItem('user', JSON.stringify(userToStore));
    setUser({ ...userToStore, token: access_token });
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  // Verificamos ambas posibilidades role_id y rol_id
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
        // Agregamos método helper para obtener la ciudad
        getUserCity: () => user?.city || 'global'
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