import { Component, OnInit, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

interface Routine {
  id: number;
  name: string;
  description: string;
  difficulty: string;
}

@Component({
  selector: 'app-athlete-portal',
  standalone: true,
  imports: [],
  templateUrl: './athlete-portal.component.html',
  styleUrl: './athlete-portal.component.css'
})
export class AthletePortalComponent implements OnInit {
  routines: Routine[] = [];
  loading = false;
  http = inject(HttpClient);

  ngOnInit() {
    this.loadRoutines();
  }

  /**
   * Carga el catálogo global de rutinas disponibles desde el backend.
   * La vista de atleta es únicamente de lectura sobre estas rutinas.
   */
  loadRoutines() {
    this.loading = true;
    this.http.get<Routine[]>(`${environment.apiUrl}/routines`)
      .subscribe({
        next: (data) => {
          this.routines = data;
          this.loading = false;
        },
        error: (err) => {
          console.error('Error fetching routines', err);
          this.loading = false;
        }
      });
  }

  showMotivationalModal = false;
  activeRoutineName = '';
  motivationalMessage = '';

  motivationalQuotes = [
    "¡El dolor de hoy es la fuerza de mañana! 💪",
    "No te detengas cuando estés cansado, detente cuando hayas terminado. 🔥",
    "La disciplina es el puente entre tus metas y tus logros. 🏆",
    "Cada gota de sudor te acerca un paso más a tu mejor versión. 💧"
  ];

  /**
   * Inicia el flujo de entrenamiento:
   * 1. Despliega un modal motivacional dinámico.
   * 2. Envía un evento asíncrono al backend para registrar la acción en Kafka.
   * @param routine La rutina seleccionada por el atleta.
   */
  startTraining(routine: Routine) {
    this.activeRoutineName = routine.name;
    this.motivationalMessage = this.motivationalQuotes[Math.floor(Math.random() * this.motivationalQuotes.length)];
    this.showMotivationalModal = true;

    this.http.post(`${environment.apiUrl}/audit/training`, { routine_name: routine.name })
      .subscribe({
        next: () => console.log('Training logged'),
        error: (err) => console.error('Error logging training', err)
      });
  }

  /**
   * Cierra el modal interactivo de entrenamiento.
   */
  closeModal() {
    this.showMotivationalModal = false;
  }
}
