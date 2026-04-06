import React, { createContext, useState, useEffect, useRef, useContext } from 'react';
import keycloak from '../../keycloak'; // 👈 Importas la instancia global

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authenticated, setAuthenticated] = useState(false);
  const isRun = useRef(false);

  useEffect(() => {
    if (isRun.current) return; 
    isRun.current = true;

    // Ya no hacemos "new Keycloak", usamos el importado
    keycloak.init({ 
      onLoad: 'login-required', 
      checkLoginIframe: false 
    }).then((auth) => {
      setAuthenticated(auth);
    }).catch(err => console.error("Error en Keycloak:", err));

  }, []);

  // Mientras no esté autenticado, no mostramos la app
  if (!authenticated) return <div>Cargando la seguridad...</div>;

  return (
    <AuthContext.Provider value={{ keycloak, authenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);