import { Component, OnInit, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-athlete-list',
  standalone: true,
  templateUrl: './athlete-list.component.html'
})
export class AthleteListComponent implements OnInit {
  athletes: any[] = [];
  http = inject(HttpClient);

  ngOnInit() {
    // El token JWT se inyectará manualmente gracias a nuestro auth.interceptor
    this.http.get<any>(`${environment.tenant.apiUrlDjango}/athletes/`)
      .subscribe({
        next: (response) => {
          this.athletes = response.results || response;
        },
        error: (err) => console.error('Error fetching athletes', err)
      });
  }
}
