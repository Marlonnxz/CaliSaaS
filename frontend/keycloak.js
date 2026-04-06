import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  url: 'http://localhost:8080',
  realm: 'CaliSaaS',
  clientId: 'frontend-react'
});

export default keycloak;