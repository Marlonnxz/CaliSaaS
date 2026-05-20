import { Injectable } from '@angular/core';

interface CacheEntry {
  data: any;
  expiry: number;
}

@Injectable({
  providedIn: 'root'
})
export class CacheService {
  private cache = new Map<string, CacheEntry>();
  private defaultTtl = 30000; // 30 segundos de duración de la caché

  constructor() {}

  /**
   * Almacena datos en caché asociados a una clave (URL)
   */
  put(key: string, data: any, ttlMs: number = this.defaultTtl): void {
    const expiry = Date.now() + ttlMs;
    this.cache.set(key, { data, expiry });
    console.log(`%c[CacheService] Guardado en caché: ${key} (Expira en ${ttlMs / 1000}s)`, 'color: #00bcd4; font-weight: bold;');
  }

  /**
   * Recupera datos de la caché si no han expirado
   */
  get(key: string): any | null {
    const entry = this.cache.get(key);
    if (!entry) return null;

    const isExpired = Date.now() > entry.expiry;
    if (isExpired) {
      console.log(`%c[CacheService] Expiró la caché para: ${key}`, 'color: #ff9800;');
      this.cache.delete(key);
      return null;
    }

    console.log(`%c[CacheService] Servido desde caché (SIN petición de red): ${key}`, 'color: #4caf50; font-weight: bold;');
    return entry.data;
  }

  /**
   * Limpia toda la caché (por ejemplo, tras una mutación como POST/DELETE)
   */
  clear(): void {
    console.log('%c[CacheService] Limpiando toda la caché por mutación de datos (POST/DELETE)', 'color: #e91e63; font-weight: bold;');
    this.cache.clear();
  }
}
