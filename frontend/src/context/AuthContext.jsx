import { createContext, useState, useEffect, useContext } from 'react';
import Keycloak from 'keycloak-js';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [keycloak, setKeycloak] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    const kc = new Keycloak({
      url: import.meta.env.VITE_KEYCLOAK_URL,
      realm: import.meta.env.VITE_KEYCLOAK_REALM,
      clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID,
    });

    kc.init({ 
      onLoad: 'login-required', 
      checkLoginIframe: false 
    }).then((auth) => {
      setKeycloak(kc);
      setAuthenticated(auth);
    }).catch(err => console.error("Error en Keycloak:", err));
  }, []);

  return (
    <AuthContext.Provider value={{ keycloak, authenticated }}>
      {/* Si no ha cargado Keycloak, mostramos un loading */}
      {keycloak && authenticated ? children : (
        <div className="flex h-screen items-center justify-center bg-gray-900 text-white">
          <p className="text-xl animate-pulse">Cargando CaliSaaS Security...</p>
        </div>
      )}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);