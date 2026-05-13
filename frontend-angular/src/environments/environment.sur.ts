export const environment = {
  production: false,
  apiUrl: `http://${window.location.hostname}:3000/api`,
  tenant: {
    name: 'Gimnasio Sur',
    keycloakUrl: `http://${window.location.hostname}:8082`,
    keycloakRealm: 'GimnasioSur',
    keycloakClientId: 'angular-frontend'
  }
};
