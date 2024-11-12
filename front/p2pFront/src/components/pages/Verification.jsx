import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Check, X, Loader } from 'lucide-react';
import { Button } from '../ui/button';
import { AuthService } from '../services/auth.service';
import Logo from '../../assets/icons/Mesa de trabajo 55.png';

const Verification = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('verifying');
  const token = searchParams.get('token');

  useEffect(() => {
    const verifyToken = async () => {
      if (!token) {
        setStatus('error');
        return;
      }

      try {
        console.log('Verificando token:', token); // Para debugging
        await AuthService.verifyEmail(token);
        setStatus('success');
        // Redirigir al login después de 5 segundos
        setTimeout(() => {
          navigate('/Welcome');
        }, 5000);
      } catch (error) {
        console.error('Error de verificación:', error);
        setStatus('error');
      }
    };

    verifyToken();
  }, [token, navigate]);

  const renderContent = () => {
    switch (status) {
      case 'verifying':
        return (
          <>
            <div className="p-4 bg-[#f0f0f0] rounded-full">
              <Loader className="h-6 w-6 text-[#d55b49] animate-spin" />
            </div>
            <h1 className="text-2xl font-bold text-[#0066ff]">
              Verificando tu correo
            </h1>
            <p className="text-gray-600 text-center">
              Solo tomará un momento...
            </p>
          </>
        );

      case 'success':
        return (
          <>
            <div className="p-4 bg-[#f0f0f0] rounded-full">
              <Check className="h-6 w-6 text-[#d55b49]" />
            </div>
            <h1 className="text-2xl font-bold text-[#0066ff]">
              ¡Verificación Exitosa!
            </h1>
            <p className="text-gray-600 text-center">
              Tu cuenta ha sido verificada correctamente
            </p>
            <p className="text-gray-600 text-center">
              Bienvenido a la comunidad Pet2Pet
            </p>
            <div className="w-full px-4">
              <Button
                onClick={() => navigate('/welcome')}
                className="w-full bg-[#d55b49] hover:bg-[#d55b49]/90 text-white"
              >
                Ir al inicio de sesión
              </Button>
            </div>
            <p className="text-sm text-gray-500 text-center">
              Serás redirigido automáticamente en unos segundos...
            </p>
          </>
        );

      case 'error':
        return (
          <>
            <div className="p-4 bg-[#f0f0f0] rounded-full">
              <X className="h-6 w-6 text-[#d55b49]" />
            </div>
            <h1 className="text-2xl font-bold text-[#0066ff]">
              Error de Verificación
            </h1>
            <p className="text-gray-600 text-center">
              No pudimos verificar tu cuenta. El enlace puede haber expirado o ser inválido.
            </p>
            <div className="w-full px-4">
              <Button
                onClick={() => navigate('/')}
                className="w-full bg-[#d55b49] hover:bg-[#d55b49]/90 text-white"
              >
                Volver al inicio de sesión
              </Button>
            </div>
          </>
        );

      default:
        return null;
    }
  };

  return (
    <div className="w-full min-h-screen bg-background flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-lg p-8">
        <div className="flex flex-col items-center space-y-6">
          {/* Logo */}
          <div className="w-32 mb-2">
            <img
              src={Logo}
              alt="Pet2Pet Logo"
              className="w-full h-full object-contain"
            />
          </div>
          
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default Verification;