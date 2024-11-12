import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../ui/button';
import { Mail } from 'lucide-react';
import Logo from '../../assets/icons/Mesa de trabajo 55.png';

const EmailVerificationPage = ({ email }) => {
  const navigate = useNavigate();

  return (
    <div className="w-full min-h-screen bg-background flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-lg p-8">
        {/* Container principal con flex y centrado */}
        <div className="flex flex-col items-center space-y-6">
          {/* Logo */}
          <div className="w-32 mb-2">
            <img 
              src={Logo} 
              alt="Pet2Pet Logo" 
              className="w-full h-full object-contain" 
            />
          </div>

          {/* Icono de correo */}
          <div className="p-4 bg-[#f0f0f0] rounded-full">
            <Mail className="h-6 w-6 text-[#d55b49]" />
          </div>

          {/* Título */}
          <h1 className="text-2xl font-bold text-[#0066ff]">
            ¡Registro Exitoso!
          </h1>

          {/* Subtítulo */}
          <p className="text-gray-600 text-center">
            Un paso más para unirte a la comunidad Pet2Pet
          </p>

          {/* Sección de correo */}
          <div className="w-full text-center space-y-1">
            <p className="text-gray-600">
              Hemos enviado un correo a:
            </p>
            <p className="font-medium text-gray-800 break-all">
              {email}
            </p>
          </div>

          {/* Instrucciones */}
          <p className="text-gray-600 text-center">
            Por favor, revisa tu bandeja de entrada y haz clic en 
            el enlace de verificación para comenzar a conectar 
            con otros amantes de las mascotas.
          </p>

          {/* Botón centrado */}
          <div className="w-full px-4">
            <Button 
              onClick={() => navigate('/')}
              className="w-full bg-[#d55b49] hover:bg-[#d55b49]/90 text-white"
            >
              Ir al inicio de sesión
            </Button>
          </div>

          {/* Texto spam */}
          <p className="text-sm text-gray-500 text-center">
            Si no encuentras el correo, revisa tu carpeta de spam
          </p>

          {/* Link reenviar */}
          <button
            type="button"
            onClick={() => {/* Implementar reenvío */}}
            className="text-[#509e9e] hover:text-[#509e9e]/80 text-sm"
          >
            Reenviar correo de verificación
          </button>
        </div>
      </div>
    </div>
  );
};

export default EmailVerificationPage;