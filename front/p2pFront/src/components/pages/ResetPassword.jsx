import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Check, X, Loader, AlertTriangle, Eye, EyeOff } from 'lucide-react';
import { Button } from '../ui/button';
import { Alert, AlertTitle, AlertDescription } from '../ui/alert';
import { AuthService } from '../services/auth.service';
import Logo from '../../assets/icons/Mesa de trabajo 55.png';

// Componente de input de contraseña con toggle
const PasswordInput = ({ label, value, onChange, placeholder }) => {
    const [showPassword, setShowPassword] = useState(false);

    return (
        <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
                {label}
            </label>
            <div className="relative">
                <input
                    type={showPassword ? "text" : "password"}
                    value={value}
                    onChange={onChange}
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#509ca2] focus:border-transparent transition-all bg-white/50 backdrop-blur-sm pr-10"
                    placeholder={placeholder}
                />
                <div 
                    className="absolute inset-y-0 right-0 flex items-center pr-2 cursor-pointer"
                    onClick={() => setShowPassword(!showPassword)}
                >
                    {showPassword ? (
                        <Eye className="h-5 w-5 text-gray-400 hover:text-gray-500" />
                    ) : (
                        <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-500" />
                    )}
                </div>
            </div>
        </div>
    );
};

const ResetPassword = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const [status, setStatus] = useState('validating');
    const [passwords, setPasswords] = useState({
        newPassword: '',
        confirmPassword: ''
    });
    const [error, setError] = useState('');
    const token = searchParams.get('token');

    useEffect(() => {
        if (!token) {
            setStatus('error');
            return;
        }
        setStatus('inputting');
    }, [token]);

    const validatePasswords = () => {
        if (passwords.newPassword.length < 8) {
            setError('La contraseña debe tener al menos 8 caracteres');
            return false;
        }
        if (passwords.newPassword !== passwords.confirmPassword) {
            setError('Las contraseñas no coinciden');
            return false;
        }
        return true;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!validatePasswords()) return;

        try {
            setStatus('resetting');
            await AuthService.resetPassword(token, passwords.newPassword);
            setStatus('success');
            setTimeout(() => {
                navigate('/');
            }, 5000);
        } catch (error) {
            setError(error.detail || 'Ocurrió un error al restablecer la contraseña');
            setStatus('inputting');
        }
    };

    const renderContent = () => {
        switch (status) {
            case 'validating':
                return (
                    <>
                        <div className="p-4 bg-[#509ca2]/10 rounded-full">
                            <Loader className="h-6 w-6 text-[#509ca2] animate-spin" />
                        </div>
                        <h1 className="text-2xl font-bold text-[#509ca2]">
                            Validando enlace
                        </h1>
                        <p className="text-gray-600 text-center">
                            Solo tomará un momento...
                        </p>
                    </>
                );

            case 'inputting':
                return (
                    <>
                        <h1 className="text-2xl font-bold text-[#509ca2] mb-6">
                            Restablecer Contraseña
                        </h1>
                        
                        {error && (
                            <Alert variant="destructive" className="mb-6">
                                <AlertTriangle className="h-4 w-4" />
                                <AlertTitle>Error</AlertTitle>
                                <AlertDescription>{error}</AlertDescription>
                            </Alert>
                        )}

                        <form onSubmit={handleSubmit} className="w-full space-y-6 max-w-sm mx-auto">
                            <div className="space-y-4">
                                <PasswordInput
                                    label="Nueva Contraseña"
                                    value={passwords.newPassword}
                                    onChange={(e) => setPasswords(prev => ({
                                        ...prev,
                                        newPassword: e.target.value
                                    }))}
                                    placeholder="Ingresa tu nueva contraseña"
                                />

                                <PasswordInput
                                    label="Confirmar Contraseña"
                                    value={passwords.confirmPassword}
                                    onChange={(e) => setPasswords(prev => ({
                                        ...prev,
                                        confirmPassword: e.target.value
                                    }))}
                                    placeholder="Confirma tu nueva contraseña"
                                />
                            </div>

                            <Button
                                type="submit"
                                className="w-full py-3 bg-[#d55b49] hover:bg-[#509ca2] text-white rounded-lg transition-all transform hover:scale-[1.02] active:scale-[0.98]"
                            >
                                Cambiar Contraseña
                            </Button>
                        </form>
                    </>
                );

            case 'resetting':
                return (
                    <>
                        <div className="p-4 bg-[#509ca2]/10 rounded-full">
                            <Loader className="h-6 w-6 text-[#509ca2] animate-spin" />
                        </div>
                        <h1 className="text-2xl font-bold text-[#509ca2]">
                            Cambiando contraseña
                        </h1>
                        <p className="text-gray-600 text-center">
                            Estamos procesando tu solicitud...
                        </p>
                    </>
                );

            case 'success':
                return (
                    <>
                        <div className="p-4 bg-[#509ca2]/10 rounded-full">
                            <Check className="h-6 w-6 text-[#509ca2]" />
                        </div>
                        <h1 className="text-2xl font-bold text-[#509ca2]">
                            ¡Contraseña Actualizada!
                        </h1>
                        <p className="text-gray-600 text-center">
                            Tu contraseña ha sido actualizada exitosamente
                        </p>
                        <Button
                            onClick={() => navigate('/')}
                            className="mt-6 w-full max-w-sm bg-[#d55b49] hover:bg-[#d55b49]/90 text-white rounded-lg transition-all transform hover:scale-[1.02] active:scale-[0.98]"
                        >
                            Ir al inicio de sesión
                        </Button>
                        <p className="text-sm text-gray-500 text-center mt-4">
                            Serás redirigido automáticamente en unos segundos...
                        </p>
                    </>
                );

            case 'error':
                return (
                    <>
                        <div className="p-4 bg-[#509ca2]/10 rounded-full">
                            <X className="h-6 w-6 text-[#d55b49]" />
                        </div>
                        <h1 className="text-2xl font-bold text-[#509ca2]">
                            Error de Validación
                        </h1>
                        <p className="text-gray-600 text-center">
                            El enlace para restablecer la contraseña no es válido o ha expirado.
                        </p>
                        <Button
                            onClick={() => navigate('/forgot-password')}
                            className="mt-6 w-full max-w-sm bg-[#d55b49] hover:bg-[#d55b49]/90 text-white rounded-lg transition-all transform hover:scale-[1.02] active:scale-[0.98]"
                        >
                            Solicitar nuevo enlace
                        </Button>
                    </>
                );

            default:
                return null;
        }
    };

    return (
        <div className="relative w-full min-h-screen bg-[#eeede8] flex flex-col items-center justify-center p-4 overflow-hidden">
            {/* Huellitas decorativas */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                {[...Array(20)].map((_, i) => (
                    <div 
                        key={i} 
                        className="absolute text-[#d55b49]/5 text-4xl md:text-6xl"
                        style={{
                            top: `${Math.random() * 100}%`,
                            left: `${Math.random() * 100}%`,
                            transform: `rotate(${Math.random() * 360}deg)`
                        }}
                    >
                        🐾
                    </div>
                ))}
            </div>
            
            <div className="relative w-full max-w-md bg-white/90 backdrop-blur-sm rounded-xl shadow-xl p-8 border border-gray-100">
                <div className="flex flex-col items-center space-y-6">
                    {/* Logo */}
                    <div className="w-32 mb-2 transform hover:scale-105 transition-transform">
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

export default ResetPassword;