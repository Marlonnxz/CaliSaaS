import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import Dashboard from './features/dashboard/Dashboard';
import Training from './features/training/Training';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          {/* Ruta default basada en roles o un redirect */}
          <Route index element={<Navigate to="/dashboard" replace />} />
          
          <Route 
            path="dashboard" 
            element={
              <ProtectedRoute requireAdmin={true}>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="training" 
            element={
              <ProtectedRoute>
                <Training />
              </ProtectedRoute>
            } 
          />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;