import { Component, OnInit, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { environment } from '../../../../environments/environment';

interface Athlete {
  id: number;
  first_name: string;
  last_name: string;
  weight: number;
  height: number;
}

interface Routine {
  id: number;
  name: string;
  description: string;
  difficulty: string;
}

@Component({
  selector: 'app-athlete-list',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './athlete-list.component.html',
  styleUrl: './athlete-list.component.css'
})
export class AthleteListComponent implements OnInit {
  athletes: Athlete[] = [];
  routines: Routine[] = [];
  http = inject(HttpClient);
  
  // Forms
  newAthlete = { first_name: '', last_name: '', weight: null, height: null };
  newRoutine = { name: '', description: '', difficulty: 'Media' };
  
  // State
  loadingAthletes = false;
  loadingRoutines = false;
  submittingAthlete = false;
  submittingRoutine = false;
  selectedAthleteForRoutine: number | null = null;
  selectedRoutineId: number | null = null;

  ngOnInit() {
    this.loadAthletes();
    this.loadRoutines();
  }

  /**
   * Carga la lista global de atletas desde el backend actual (Norte o Sur).
   */
  loadAthletes() {
    this.loadingAthletes = true;
    this.http.get<Athlete[]>(`${environment.apiUrl}/athletes`)
      .subscribe({
        next: (data) => {
          this.athletes = data;
          this.loadingAthletes = false;
        },
        error: (err) => {
          console.error('Error fetching athletes', err);
          this.loadingAthletes = false;
        }
      });
  }

  /**
   * Carga el catálogo global de rutinas.
   */
  loadRoutines() {
    this.loadingRoutines = true;
    this.http.get<Routine[]>(`${environment.apiUrl}/routines`)
      .subscribe({
        next: (data) => {
          this.routines = data;
          this.loadingRoutines = false;
        },
        error: (err) => {
          console.error('Error fetching routines', err);
          this.loadingRoutines = false;
        }
      });
  }

  /**
   * Envía el formulario para crear un nuevo atleta en la base de datos física.
   */
  createAthlete() {
    if (!this.newAthlete.first_name || !this.newAthlete.last_name) return;
    this.submittingAthlete = true;
    this.http.post(`${environment.apiUrl}/athletes`, this.newAthlete)
      .subscribe({
        next: () => {
          this.loadAthletes();
          this.newAthlete = { first_name: '', last_name: '', weight: null, height: null };
          this.submittingAthlete = false;
        },
        error: (err) => {
          console.error('Error creating athlete', err);
          this.submittingAthlete = false;
        }
      });
  }

  /**
   * Elimina un atleta del sistema tras confirmación del usuario.
   */
  deleteAthlete(id: number) {
    if (confirm('¿Estás seguro de eliminar este atleta? Esta acción no se puede deshacer.')) {
      this.http.delete(`${environment.apiUrl}/athletes/${id}`)
        .subscribe({
          next: () => this.loadAthletes(),
          error: (err) => console.error('Error deleting athlete', err)
        });
    }
  }

  /**
   * Crea una nueva rutina y la añade al catálogo global.
   */
  createRoutine() {
    if (!this.newRoutine.name) return;
    this.submittingRoutine = true;
    this.http.post(`${environment.apiUrl}/routines`, this.newRoutine)
      .subscribe({
        next: () => {
          this.loadRoutines();
          this.newRoutine = { name: '', description: '', difficulty: 'Media' };
          this.submittingRoutine = false;
        },
        error: (err) => {
          console.error('Error creating routine', err);
          this.submittingRoutine = false;
        }
      });
  }

  /**
   * Elimina una rutina del catálogo tras confirmación.
   */
  deleteRoutine(routineId: number) {
    if (confirm('¿Estás seguro de que deseas eliminar esta rutina? Esto la quitará de los entrenamientos de todos los atletas.')) {
      this.http.delete(`${environment.apiUrl}/routines/${routineId}`)
        .subscribe({
          next: () => this.loadRoutines(),
          error: (err) => console.error('Error deleting routine', err)
        });
    }
  }
}
