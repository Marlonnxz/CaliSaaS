import { Injectable } from '@angular/core';
import Keycloak from 'keycloak-js';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AutenticacionService {
  private keycloak: Keycloak | undefined;

  constructor() {}

  /**
   * Inicializa la configuración dinámica del cliente de Keycloak según el entorno (Tenant).
   * Determina si hay una sesión activa y almacena el token JWT de forma segura.
   * @returns {Promise<boolean>} Retorna true si el usuario está autenticado en el sistema.
   */
  async init(): Promise<boolean> {
    this.keycloak = new Keycloak({
      url: environment.tenant.keycloakUrl,
      realm: environment.tenant.keycloakRealm,
      clientId: environment.tenant.keycloakClientId
    });

    try {
      const authenticated = await this.keycloak.init({
        onLoad: 'check-sso',
        checkLoginIframe: false, // Evita errores de iframe en localhost/IPs sin SSL
        pkceMethod: false // Desactiva PKCE para que funcione en HTTP con IP
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

  /**
   * Genera dinámicamente la URL de inicio de sesión hacia el servidor Keycloak centralizado.
   * Redirige al usuario al flujo de autenticación estándar OIDC.
   */
  async login() {
    if (this.keycloak) {
      try {
        // En lugar de depender de la promesa interna de keycloak.login(), 
        // generamos la URL y forzamos la redirección manualmente.
        const url = await this.keycloak.createLoginUrl({
          redirectUri: window.location.origin + '/dashboard'
        });
        window.location.href = url;
      } catch (err) {
        alert("Error generando URL de login: " + err);
      }
    } else {
      alert("La instancia de Keycloak es undefined. El APP_INITIALIZER falló.");
    }
  }

  /**
   * Cierra la sesión activa borrando los tokens locales e invocando el logout de Keycloak.
   * Redirige a la página principal de la plataforma.
   */
  logout() {
    if (this.keycloak) {
      this.keycloak.logout({ redirectUri: window.location.origin });
      localStorage.removeItem('auth_token');
    }
  }

  getToken(): string | null {
    return localStorage.getItem('auth_token');
  }

  /**
   * Verifica la existencia y disponibilidad de la instancia de Keycloak y su sesión.
   */
  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  /**
   * Examina la firma decodificada del JWT para extraer los roles de acceso del usuario (RBAC).
   */
  getRoles(): string[] {
    const token = this.getToken();
    if (!token) return [];
    try {
      const payloadBase64 = token.split('.')[1];
      const decodedPayload = JSON.parse(atob(payloadBase64));
      return decodedPayload?.realm_access?.roles || [];
    } catch (e) {
      console.error('Error decoding JWT for roles', e);
      return [];
    }
  }

  isAdmin(): boolean {
    return this.getRoles().includes('admin_gym');
  }

  isAthlete(): boolean {
    return this.getRoles().includes('atleta');
  }

  getTenant(): 'norte' | 'sur' | null {
    const roles = this.getRoles();
    if (roles.includes('tenant_norte')) return 'norte';
    if (roles.includes('tenant_sur')) return 'sur';
    return null;
  }
}
