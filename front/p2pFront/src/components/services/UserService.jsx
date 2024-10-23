// Función para manejar el login del usuario
export const loginUser = async (userData) => {
    try {
      const response = await fetch("http://localhost/loginApi/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });
      if (!response.ok) {
        throw new Error("Error during login");
      }
      return await response.json();
    } catch (error) {
      console.error(error);
      throw error;
    }
  };
  
  // Función para manejar el registro del usuario
  export const registerUser = async (userData) => {
    try {
      const response = await fetch("http://localhost/registerApi/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });
      if (!response.ok) {
        throw new Error("Error during registration");
      }
      return await response.json();
    } catch (error) {
      console.error(error);
      throw error;
    }
  };
  