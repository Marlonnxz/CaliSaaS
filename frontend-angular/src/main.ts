import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import * as CryptoJS from 'crypto-js';
import { v4 as uuidv4 } from 'uuid';

// Polyfill for Web Crypto API on insecure contexts (HTTP + IP)
if (typeof window !== 'undefined') {
  if (!window.crypto) {
    (window as any).crypto = {};
  }
  if (!window.crypto.randomUUID) {
    window.crypto.randomUUID = () => {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      }) as any;
    };
  }
  if (!window.crypto.subtle) {
    (window.crypto as any).subtle = {
      digest: async (algo: string, data: Uint8Array) => {
        const wordArr = CryptoJS.lib.WordArray.create(data as any);
        const hash = CryptoJS.SHA256(wordArr);
        const hex = hash.toString(CryptoJS.enc.Hex);
        const typedArray = new Uint8Array(hex.match(/[\da-f]{2}/gi)!.map(h => parseInt(h, 16)));
        return typedArray.buffer;
      }
    };
  }
  if (!window.crypto.getRandomValues) {
    window.crypto.getRandomValues = (array: any) => {
      for (let i = 0; i < array.length; i++) {
        array[i] = Math.floor(Math.random() * 256);
      }
      return array;
    };
  }
}

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
