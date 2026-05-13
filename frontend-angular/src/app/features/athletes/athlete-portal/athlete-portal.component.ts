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
}
