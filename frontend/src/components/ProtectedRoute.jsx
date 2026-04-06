import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useRole } from '../hooks/useRole';

const ProtectedRoute = ({ children, requireAdmin }) => {
  const { authenticated } = useAuth();
  const { isAdmin } = useRole();

  if (!authenticated) {
    return <Navigate to="/" replace />;
  }

  if (requireAdmin && !isAdmin()) {
    return <Navigate to="/training" replace />;
  }

  return children;
};

export default ProtectedRoute;