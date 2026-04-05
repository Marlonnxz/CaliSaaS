import React, { createContext, useState, useEffect, useRef, useContext } from 'react';
import Keycloak from 'keycloak-js';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [keycloak, setKeycloak] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);
  const isRun = useRef(false); // 👈 1. Creamos un "candado"

  useEffect(() => {
    // 👈 2. Si ya se ejecutó una vez, detenemos la función aquí
    if (isRun.current) return; 
    isRun.current = true; // 👈 3. Cerramos el candado

    const kc = new Keycloak({
      url: 'http://localhost:8080',
      realm: 'CaliSaaS',
      clientId: 'frontend-react'
    });

    kc.init({ 
      onLoad: 'login-required', 
      checkLoginIframe: false 
    }).then((auth) => {
      setKeycloak(kc);
      setAuthenticated(auth);
    }).catch(err => console.error("Error en Keycloak:", err));

  }, []);

  if (!keycloak) return <div>Cargando la seguridad...</div>;

  return (
    <AuthContext.Provider value={{ keycloak, authenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);