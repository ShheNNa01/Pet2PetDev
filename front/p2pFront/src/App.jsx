import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/pages/LoginPage';
import RegisterPage from './components/pages/RegisterPage';
import HomePage from './components/pages/HomePage';
import Dashboard from './components/pages/Dashboard';
import WelcomePage from './components/pages/WelcomePage';
import NotFoundPage from './components/pages/NotFoundPage'; // Opcional para rutas no encontradas
import 'bootstrap/dist/css/bootstrap.min.css';
import RegisterMascotaPage from './components/pages/RegisterMascotaPage';



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/welcome" element={<WelcomePage />} /> {/* Página de Bienvenida */}
        <Route path="/" element={<LoginPage />} /> {/* Página de inicio de sesión */}
        <Route path="/register" element={<RegisterPage />} /> {/* Página de registro */}
        <Route path="/registerPet" element={<RegisterMascotaPage />} /> {/* Página principal */}
        <Route path="/home" element={<HomePage />} /> {/* Página principal */}
        <Route path="/dashboard" element={<Dashboard />} /> {/* DashBoard */}
        <Route path="*" element={<NotFoundPage />} /> {/* Componente para rutas no encontradas */}
      </Routes>
    </Router>
  );
}

export default App;

