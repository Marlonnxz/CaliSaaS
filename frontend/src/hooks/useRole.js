// src/hooks/useRole.js
import { useAuth } from '../context/AuthContext';

export const useRole = () => {
  const { keycloak } = useAuth();

  const isAtleta = () => keycloak.hasRealmRole('atleta');
  const isAdmin = () => keycloak.hasRealmRole('admin_gym');

  return { isAtleta, isAdmin, role: isAdmin() ? 'Administrador' : 'Atleta' };
};