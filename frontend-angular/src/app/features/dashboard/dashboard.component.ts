import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { AutenticacionService } from '../../core/services/autenticacion.service';
import { AthleteListComponent } from '../athletes/athlete-list/athlete-list.component';
import { AthletePortalComponent } from '../athletes/athlete-portal/athlete-portal.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, AthleteListComponent, AthletePortalComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  authService = inject(AutenticacionService);
  http = inject(HttpClient);

  ngOnInit() {
    // Disparar evento de auditoría de login a Kafka a través del backend
    if (this.authService.isLoggedIn()) {
      this.http.post(`${environment.apiUrl}/audit/login`, {}).subscribe({
        next: () => console.log('Auditoría de login registrada'),
        error: (err) => console.error('Error registrando login', err)
      });
    }
  }
}
