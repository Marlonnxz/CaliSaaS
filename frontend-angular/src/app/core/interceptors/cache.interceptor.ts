import { HttpInterceptorFn, HttpResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { of } from 'rxjs';
import { tap } from 'rxjs/operators';
import { CacheService } from '../services/cache.service';

export const cacheInterceptor: HttpInterceptorFn = (req, next) => {
  const cacheService = inject(CacheService);

  // Solo cacheamos peticiones GET a endpoints de datos de negocio (/athletes o /routines)
  const isCacheable = req.method === 'GET' && 
    (req.url.includes('/athletes') || req.url.includes('/routines'));

  if (isCacheable) {
    const cachedResponse = cacheService.get(req.urlWithParams);
    if (cachedResponse !== null) {
      // Retornamos una respuesta simulada de éxito (200 OK) con los datos cacheados
      return of(new HttpResponse({ body: cachedResponse, status: 200 }));
    }

    // Si no está en caché, procedemos con la petición de red y guardamos la respuesta
    return next(req).pipe(
      tap(event => {
        if (event instanceof HttpResponse) {
          cacheService.put(req.urlWithParams, event.body);
        }
      })
    );
  }

  // Si es una petición de modificación (POST, PUT, DELETE) sobre los mismos recursos, invalidamos la caché
  const isMutation = ['POST', 'PUT', 'DELETE'].includes(req.method) &&
    (req.url.includes('/athletes') || req.url.includes('/routines'));

  if (isMutation) {
    return next(req).pipe(
      tap(event => {
        if (event instanceof HttpResponse) {
          cacheService.clear();
        }
      })
    );
  }

  // Por defecto, dejar pasar
  return next(req);
};
