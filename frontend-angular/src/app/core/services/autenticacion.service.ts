import { Injectable } from '@angular/core';
import Keycloak from 'keycloak-js';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AutenticacionService {
  private keycloak: Keycloak | undefined;

  constructor() {}

  async init(): Promise<boolean> {
    this.keycloak = new Keycloak({
      url: environment.tenant.keycloakUrl,
      realm: environment.tenant.keycloakRealm,
      clientId: environment.tenant.keycloakClientId
    });

    try {
      const authenticated = await this.keycloak.init({
        onLoad: 'check-sso',
        checkLoginIframe: false // Evita errores de iframe en localhost/IPs sin SSL
      });

      if (authenticated) {
        // Guardado manual del token
        localStorage.setItem('auth_token', this.keycloak.token || '');
      } else {
        localStorage.removeItem('auth_token');
      }

      return authenticated;
    } catch (error) {
      console.error('Error al inicializar Keycloak', error);
      return false;
    }
  }

  async login() {
    if (this.keycloak) {
      try {
        // En lugar de depender de la promesa interna de keycloak.login(), 
        // generamos la URL y forzamos la redirección manualmente.
        const url = await this.keycloak.createLoginUrl({
          redirectUri: window.location.origin + '/athletes'
        });
        window.location.href = url;
      } catch (err) {
        alert("Error generando URL de login: " + err);
      }
    } else {
      alert("La instancia de Keycloak es undefined. El APP_INITIALIZER falló.");
    }
  }

  logout() {
    if (this.keycloak) {
      this.keycloak.logout({ redirectUri: window.location.origin });
      localStorage.removeItem('auth_token');
    }
  }

  getToken(): string | null {
    return localStorage.getItem('auth_token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}
