// src/App.jsx
import { useAuth } from './context/AuthContext';
import { useRole } from './hooks/useRole';

function App() {
  const { keycloak } = useAuth();
  const { isAdmin, role } = useRole();

  // Sacamos los datos de ese Token que acabas de ver en consola
  const username = keycloak.tokenParsed?.name || keycloak.tokenParsed?.preferred_username;

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        
        {/* Cabecera */}
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

        {/* Tarjeta de Bienvenida */}
        <div className="bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-700 mb-8">
          <h2 className="text-2xl font-bold mb-2">¡Hola, {username}! 👋</h2>
          <p className="text-gray-400">
            Estás autenticado correctamente. Tu rol en el sistema es: 
            <span className="ml-2 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-orange-500/10 text-orange-500 border border-orange-500/20">
              {role}
            </span>
          </p>
        </div>

        {/* Sección Protegida: SOLO PARA ADMINS */}
        {isAdmin() ? (
          <div className="bg-blue-900/20 border border-blue-500/30 rounded-xl p-6 shadow-lg">
            <div className="flex items-center mb-4">
              <span className="text-2xl mr-3">👑</span>
              <h3 className="text-xl font-bold text-blue-400">Zona de Administración</h3>
            </div>
            <p className="text-gray-300 mb-4">
              Como dueño de gimnasio, aquí podrás ver los pagos, métricas y gestionar a tus atletas. 
              (Un atleta normal no puede ver esta caja).
            </p>
            <div className="grid grid-cols-2 gap-4">
              <button className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-medium">
                Gestionar Pagos
              </button>
              <button className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-medium">
                Ver Atletas
              </button>
            </div>
          </div>
        ) : (
          <div className="bg-green-900/20 border border-green-500/30 rounded-xl p-6 shadow-lg">
             <div className="flex items-center mb-4">
              <span className="text-2xl mr-3">💪</span>
              <h3 className="text-xl font-bold text-green-400">Zona de Entrenamiento</h3>
            </div>
            <p className="text-gray-300">
              Aquí verás tus rutinas de calistenia, progreso y asistencia.
            </p>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;