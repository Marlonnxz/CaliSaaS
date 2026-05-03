import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { environment } from '../environments/environment';
import { AutenticacionService } from './core/services/autenticacion.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = environment.tenant.name;

  constructor(public authService: AutenticacionService) {}

  ngOnInit() {
    // Inyección de estilos dinámica basada en el tenant
    const theme = environment.tenant.theme;
    document.documentElement.style.setProperty('--primary-color', theme.primaryColor);
    document.documentElement.style.setProperty('--secondary-color', theme.secondaryColor);
    document.documentElement.style.setProperty('--bg-color', theme.backgroundColor);
  }

  login() {
    this.authService.login();
  }

  logout() {
    this.authService.logout();
  }
}
