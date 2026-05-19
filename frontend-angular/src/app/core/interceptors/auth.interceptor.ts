import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AutenticacionService } from '../services/autenticacion.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AutenticacionService);
  const token = authService.getToken();
  const tenant = authService.getTenant();

  let modifiedReq = req;

  // Enrutamiento Dinámico: Cambiar el puerto según el tenant
  if (tenant === 'sur' && req.url.includes('5000')) {
    const newUrl = req.url.replace('5000', '3000');
    modifiedReq = req.clone({ url: newUrl });
  }

  if (token) {
    modifiedReq = modifiedReq.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  return next(modifiedReq);
};
