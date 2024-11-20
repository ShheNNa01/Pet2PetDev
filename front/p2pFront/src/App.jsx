import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './components/context/AuthContext';
import { PetProvider } from './components/context/PetContext';
import { AuthGuard } from './components/guards/AuthGuard';
import { AdminGuard } from './components/guards/AdminGuard';
import { GuestGuard } from './components/guards/GuestGuard';
import LoginPage from './components/pages/LoginPage';
import RegisterPage from './components/pages/RegisterPage';
import HomePage from './components/pages/HomePage';
import Dashboard from './components/pages/Dashboard';
import WelcomePage from './components/pages/WelcomePage';
import NotFoundPage from './components/pages/NotFoundPage';
import RegisterMascotaPage from './components/pages/RegisterMascotaPage';
import PetProfiles from './components/pages/PetProfiles';
import Verification from './components/pages/Verification';
import PetProfile from './components/pages/PetProfile';
import UserProfile from './components/user/UserProfile';
import PasswordRecovery from './components/pages/PasswordRecovery';
import ResetPassword from './components/pages/ResetPassword';
import CreateVirtualPet from './components/pages/CreateVirtualPet';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Rutas públicas */}
          <Route element={<GuestGuard />}>
            <Route path="/" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/verify-email" element={<Verification />} />
            <Route path="/forgot-password" element={<PasswordRecovery />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            
          </Route>
          
          {/* Rutas protegidas (requieren autenticación) */}
          <Route element={<AuthGuard />}>
            <Route element={<PetProvider />}>
              <Route path="/welcome" element={<WelcomePage />} />
              <Route path="/home" element={<HomePage />} />
              <Route path="/registerPet" element={<RegisterMascotaPage />} />
              <Route path="/pets" element={<PetProfiles />} />
              <Route path="/petProfile" element={<PetProfile />} />
              <Route path="/createVirtualPet" element={<CreateVirtualPet />} />
              {/* <Route path="/userProfile" element={<UserProfile />} /> */}
              <Route path="/userProfile/:user_id" element={<UserProfile />} />
            </Route>
          </Route>
          {/* Ruta del dashboard (solo admin) */}
          <Route element={<AdminGuard />}>
            <Route path="/dashboard" element={<Dashboard />} />
          </Route>
          {/* Ruta 404 */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;