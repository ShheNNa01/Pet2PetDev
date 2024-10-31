import React from 'react';
import gifAnimation from '../../assets/icons/huella.gif'; // Asegúrate de que la ruta sea correcta

const GifAnimation = () => {
  return (
    <div className="flex flex-col justify-center items-center h-screen"> {/* Cambié flex-direction a columna */}
      <img src={gifAnimation} alt="Animación de GIF" className="w-64 h-auto" /> {/* Ajusta el tamaño según sea necesario */}
      <h1 className="mt-4 text-center"> {/* Añadí text-center para centrar el texto */}
        "Un registro para recordar <br /> que cada huella deja una historia." 🐾 {/* Usé <br /> para el salto de línea */}
      </h1>
    </div>
  );
};

export default GifAnimation;
