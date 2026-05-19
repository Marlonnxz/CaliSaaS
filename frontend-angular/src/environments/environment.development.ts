export const environment = {
  production: false,
  apiUrl: `http://${window.location.hostname}:5000/api`, // Default API, will be overridden by interceptor
  tenant: {
    name: 'CaliSaaS Gym Network',
    keycloakUrl: `http://${window.location.hostname}:8082`,
    keycloakRealm: 'CaliSaaS',
    keycloakClientId: 'angular-frontend'
  }
};
