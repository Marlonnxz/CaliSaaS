import axios from 'axios';
import keycloak from '../../keycloak';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

// Interceptor de peticiones
api.interceptors.request.use(
  async (config) => {
    try {
      // Si el token va a expirar en los próximos 30 segundos, se actualiza
      if (keycloak.token) {
        await keycloak.updateToken(30);
        config.headers.Authorization = `Bearer ${keycloak.token}`;
      }
    } catch (error) {
      console.error('Error actualizando el token:', error);
      keycloak.login();
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
