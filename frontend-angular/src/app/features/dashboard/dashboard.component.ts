import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
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
export class DashboardComponent {
  authService = inject(AutenticacionService);
}
