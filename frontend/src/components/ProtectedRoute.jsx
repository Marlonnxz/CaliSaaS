import { useAuth } from '../context/AuthContext';

export const ProtectedRoute = ({ children, role }) => {
  const { keycloak } = useAuth();

  // Verifica si el usuario tiene el rol necesario
  const hasRole = keycloak.hasRealmRole(role);

  if (!hasRole) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-100">
        <h1 className="text-2xl text-red-600 font-bold">
          Acceso Denegado: No tienes permisos para ver esto.
        </h1>
      </div>
    );
  }

  return children;
};