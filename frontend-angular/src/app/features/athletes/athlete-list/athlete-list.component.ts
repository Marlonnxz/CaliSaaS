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

  assignRoutine(athleteId: number) {
    if (!this.selectedRoutineId) return;
    this.http.post(`${environment.apiUrl}/athletes/${athleteId}/routines`, { routine_id: this.selectedRoutineId })
      .subscribe({
        next: () => {
          alert('Rutina asignada exitosamente (El evento se emitió a Kafka)');
          this.selectedAthleteForRoutine = null;
          this.selectedRoutineId = null;
        },
        error: (err) => console.error('Error assigning routine', err)
      });
  }
}
