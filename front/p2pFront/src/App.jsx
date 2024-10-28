import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/pages/LoginPage';
import RegisterPage from './components/pages/RegisterPage';
import HomePage from './components/pages/HomePage';
import WelcomePage from './components/pages/WelcomePage';
import NotFoundPage from './components/pages/NotFoundPage'; // Opcional para rutas no encontradas
import 'bootstrap/dist/css/bootstrap.min.css';



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} /> {/* Página de inicio de sesión */}
        <Route path="/home" element={<HomePage />} /> {/* Página principal */}
        <Route path="/register" element={<RegisterPage />} /> {/* Página de registro */}
        <Route path="/welcome" element={<WelcomePage />} /> {/* Página de Bienvenida */}
        <Route path="*" element={<NotFoundPage />} /> {/* Componente para rutas no encontradas */}
      </Routes>
    </Router>
  );
}

export default App;

