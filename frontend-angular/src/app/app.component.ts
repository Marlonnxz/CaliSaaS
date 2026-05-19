import { Component, OnInit } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';
import { environment } from '../environments/environment';
import { AutenticacionService } from './core/services/autenticacion.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = environment.tenant.name;
  logoUrl = 'assets/logo-default.png';

  constructor(public authService: AutenticacionService) {}

  ngOnInit() {
    this.applyTheme();
  }

  applyTheme() {
    const tenant = this.authService.getTenant();
    const root = document.documentElement;

    if (tenant === 'norte') {
      this.title = 'Gimnasio Norte';
      this.logoUrl = 'assets/logo-norte.png';
      // Azul Corporativo
      root.style.setProperty('--primary-color', '#2563eb'); 
      root.style.setProperty('--primary-hover', '#1d4ed8');
    } else if (tenant === 'sur') {
      this.title = 'Gimnasio Sur';
      this.logoUrl = 'assets/logo-sur.png';
      // Verde Esmeralda
      root.style.setProperty('--primary-color', '#10b981'); 
      root.style.setProperty('--primary-hover', '#059669');
    } else {
      this.title = 'CaliSaaS Gym Network';
      this.logoUrl = 'assets/logo-default.png';
      // Gris Neutro (Por defecto)
      root.style.setProperty('--primary-color', '#475569');
      root.style.setProperty('--primary-hover', '#334155');
    }
  }

  login() {
    this.authService.login();
  }

  logout() {
    this.authService.logout();
    // Restaurar tema por defecto al salir
    this.applyTheme();
  }
}
