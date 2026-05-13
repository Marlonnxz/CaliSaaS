export const environment = {
  production: false,
  apiUrl: `http://${window.location.hostname}:5000/api`,
  tenant: {
    name: 'Gimnasio Norte',
    keycloakUrl: `http://${window.location.hostname}:8082`,
    keycloakRealm: 'GimnasioNorte',
    keycloakClientId: 'angular-frontend'
  }
};
