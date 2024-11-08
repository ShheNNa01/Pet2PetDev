import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthService } from '../services/auth.service';
import { useAuth } from '../context/AuthContext';
import '../styles/LoginPage.css';
import MesaDeTrabajo50 from '../../assets/icons/Mesa de trabajo 50.png';

const LoginPage = () => {
    const navigate = useNavigate();
    const { login, isAuthenticated } = useAuth();
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (isAuthenticated) {
            navigate('/home');
        }
    }, [isAuthenticated, navigate]);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.id]: e.target.value
        });
        if (error) setError('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
    
        if (!formData.username.trim() || !formData.password.trim()) {
            setError('Por favor, completa todos los campos');
            setLoading(false);
            return;
        }
    
        try {
            const response = await AuthService.login({
                username: formData.username,
                password: formData.password
            });
    
            if (response.access_token) {
                await login(response);
                // La redirección la maneja el useEffect
            }
        } catch (error) {
            if (error.response?.status === 401) {
                setError('Usuario o contraseña incorrectos');
            } else if (error.response?.status === 422) {
                setError('Por favor, verifica tus credenciales');
            } else {
                setError('Error al iniciar sesión. Por favor, intenta más tarde');
            }
            console.error('Error de login:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div id="contenedor">
            <div id="contenedorcentrado">
                {/* Sección de login */}
                <div id="login">
                    <h2 className="titulo">Iniciar Sesión</h2>
                    
                    {/* Mostrar mensaje de error si existe */}
                    {error && (
                        <div className="error-mensaje">
                            {error}
                        </div>
                    )}

                    <form className='form-login' onSubmit={handleSubmit}>
                        <label htmlFor="username">Usuario:</label>
                        <input
                            type="text"
                            id="username"
                            placeholder="Introduce tu usuario"
                            value={formData.username}
                            onChange={handleChange}
                            disabled={loading}
                        />
                        
                        <label htmlFor="password">Contraseña:</label>
                        <input
                            type="password"
                            id="password"
                            placeholder="Introduce tu contraseña"
                            value={formData.password}
                            onChange={handleChange}
                            disabled={loading}
                        />
                        
                        <button 
                            type="submit" 
                            disabled={loading}
                            className={loading ? 'button-loading' : ''}
                        >
                            {loading ? 'Ingresando...' : 'Ingresar'}
                        </button>
                    </form>

                    <div className="pie-form">
                        <Link to="/forgot-password">¿Olvidaste tu contraseña?</Link>
                        <Link to="/register">Regístrate</Link>
                    </div>
                </div>

                {/* Sección de la derecha */}
                <div id="derecho">
                    <div className="logo-empresa">
                        <img src={MesaDeTrabajo50} alt="Logo Empresa" />
                    </div>
                    <hr />
                    <div className="pie-form">
                        <p>
                            ¡Bienvenido! <br />
                            Aquí, las mejores conexiones entre mascotas y dueños comienzan. <br />
                            ¡Explora lo que tenemos para ti!
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
