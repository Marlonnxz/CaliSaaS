export const environment = {
  production: true,
  tenant: {
    name: 'CaliSaaS Gym',
    apiUrlDjango: 'http://192.168.1.5:8000/api',
    apiUrlNode: 'http://192.168.1.5:3000/api',
    keycloakUrl: 'http://192.168.1.5:8082',
    keycloakRealm: 'CaliSaaS',
    keycloakClientId: 'angular-frontend',
    theme: {
      primaryColor: '#ff4b4b',
      secondaryColor: '#2d3436',
      backgroundColor: '#f8f9fa'
    }
  }
};
