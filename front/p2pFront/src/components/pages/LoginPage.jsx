import React from 'react';
import '../styles/LoginPage.css'; // Asegúrate de importar el archivo CSS
import MesaDeTrabajo50 from '../../assets/icons/Mesa de trabajo 50.png'
import { Link } from 'react-router-dom';

<Link to="/register">Regístrate</Link>

const LoginPage = () => {
    return (
        <div id="contenedor" >
            <div id="contenedorcentrado">
                {/* Sección de login */}
                <div id="login">
                    <h2 className="titulo">Iniciar Sesión</h2>
                    <form>
                        <label htmlFor="usuario">Usuario</label>
                        <input type="text" id="usuario" placeholder="Introduce tu usuario" />
                        
                        <label htmlFor="password">Contraseña</label>
                        <input type="password" id="password" placeholder="Introduce tu contraseña" />
                        
                        <button type="submit">Ingresar</button>
                    </form>
                    <div className="pie-form">
                        <a href="#">¿Olvidaste tu contraseña?</a>
                        <Link to="/register">Regístrate</Link>
                    </div>
                </div>

                {/* Sección de la derecha */}
                <div id="derecho">
                    <div className="logo-empresa">
                        <img src={MesaDeTrabajo50 } alt="Logo Empresa" />
                    </div>
                    <hr />
                    <div className="pie-form">
                        <p>Bienvenido a nuestra plataforma.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LoginPage;
