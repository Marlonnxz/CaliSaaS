import { Routes } from '@angular/router';
import { AthleteListComponent } from './features/athletes/athlete-list/athlete-list.component';
import { GymCreateComponent } from './features/gyms/gym-create/gym-create.component';

export const routes: Routes = [
  { path: 'athletes', component: AthleteListComponent },
  { path: 'gyms/new', component: GymCreateComponent },
  { path: '', redirectTo: '/athletes', pathMatch: 'full' }
];
