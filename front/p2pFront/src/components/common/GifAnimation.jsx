import React from 'react';
import gifAnimation from '../../assets/icons/huella.gif';

const GifAnimation = () => {
  return (
    <div className="flex flex-col justify-center items-center text-center space-y-2">
      <div className="relative">
        <img
          src={gifAnimation}
          alt="Animación de GIF"
          className="w-32 h-auto" 
        />
      </div>
      <p className="text-lg font-medium text-[#509ca2] italic">
        "Un registro para recordar que cada huella deja una historia."
      </p>
    </div>
  );
};

export default GifAnimation;