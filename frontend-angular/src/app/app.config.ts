import { ApplicationConfig, APP_INITIALIZER } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { routes } from './app.routes';
import { AutenticacionService } from './core/services/autenticacion.service';
import { authInterceptor } from './core/interceptors/auth.interceptor';

function initializeKeycloak(authService: AutenticacionService) {
  return () => authService.init();
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([authInterceptor])),
    {
      provide: APP_INITIALIZER,
      useFactory: initializeKeycloak,
      multi: true,
      deps: [AutenticacionService]
    }
  ]
};
