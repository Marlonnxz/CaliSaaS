import { Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useRole } from '../hooks/useRole';

const Layout = () => {
  const { keycloak } = useAuth();
  const { role } = useRole();
  const username = keycloak.tokenParsed?.name || keycloak.tokenParsed?.preferred_username;

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-3xl font-extrabold text-orange-500">CaliSaaS</h1>
            <p className="text-gray-400">Panel Principal</p>
          </div>
          <button 
            onClick={() => keycloak.logout()}
            className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
          >
            Cerrar Sesión
          </button>
        </div>

        <div className="bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-700 mb-8">
          <h2 className="text-2xl font-bold mb-2">¡Hola, {username}! 👋</h2>
          <p className="text-gray-400">
            Estás autenticado correctamente. Tu rol en el sistema es: 
            <span className="ml-2 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-orange-500/10 text-orange-500 border border-orange-500/20">
              {role}
            </span>
          </p>
        </div>
        
        <Outlet />
      </div>
    </div>
  );
};

export default Layout;
