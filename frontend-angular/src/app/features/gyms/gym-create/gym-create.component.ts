import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-gym-create',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './gym-create.component.html'
})
export class GymCreateComponent {
  fb = inject(FormBuilder);
  http = inject(HttpClient);
  mensaje = '';

  gymForm = this.fb.group({
    name: ['', Validators.required],
    slug: ['', Validators.required]
  });

  onSubmit() {
    if (this.gymForm.valid) {
      this.http.post(`${environment.apiUrl}/gyms/`, this.gymForm.value)
        .subscribe({
          next: () => this.mensaje = 'Gimnasio creado en Node.js exitosamente',
          error: (err) => this.mensaje = `Fallo esperado (Node.js no está levantado en el puerto 3000): ${err.message}`
        });
    }
  }
}
