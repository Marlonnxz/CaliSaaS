export const environment = {
  production: false,
  apiUrl: `http://${window.location.hostname}:3000/api`,
  tenant: {
    name: 'Default Dev',
    keycloakUrl: `http://${window.location.hostname}:8082`,
    keycloakRealm: 'Default',
    keycloakClientId: 'angular-frontend'
  }
};
