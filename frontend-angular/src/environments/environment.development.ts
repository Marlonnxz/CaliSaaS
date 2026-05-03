export const environment = {
  production: false,
  tenant: {
    name: 'CaliSaaS Gym (Dev)',
    apiUrlDjango: `http://${window.location.hostname}:8000/api`,
    apiUrlNode: `http://${window.location.hostname}:3000/api`,
    keycloakUrl: `http://${window.location.hostname}:8082`,
    keycloakRealm: 'CaliSaaS',
    keycloakClientId: 'angular-frontend',
    theme: {
      primaryColor: '#ff4b4b',
      secondaryColor: '#2d3436',
      backgroundColor: '#f8f9fa'
    }
  }
};
