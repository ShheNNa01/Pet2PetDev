import React from 'react';
import gifAnimation from '../../assets/icons/huella.gif'; // Asegúrate de que la ruta sea correcta

const GifAnimation = () => {
  return (
    <div className="flex flex-col justify-center items-center h-screen"> {/* Cambié flex-direction a columna */}
      <img src={gifAnimation} alt="Animación de GIF" className="w-64 h-auto" /> {/* Ajusta el tamaño según sea necesario */}
      <h1 className="mt-4 text-center text-2xl font-bold text-black">
      {/* Cambié text-4xl y font-bold para hacerlo más grande y oscuro */}
      "Un registro para recordar que cada huella deja una historia." 🐾 {/* Usé <br /> para el salto de línea */}
      </h1>

    </div>
  );
};

export default GifAnimation;
