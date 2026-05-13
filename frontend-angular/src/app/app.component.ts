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

  constructor(public authService: AutenticacionService) {}

  ngOnInit() {
  }

  login() {
    this.authService.login();
  }

  logout() {
    this.authService.logout();
  }
}
