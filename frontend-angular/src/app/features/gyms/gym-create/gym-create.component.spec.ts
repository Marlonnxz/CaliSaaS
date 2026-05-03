import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GymCreateComponent } from './gym-create.component';

describe('GymCreateComponent', () => {
  let component: GymCreateComponent;
  let fixture: ComponentFixture<GymCreateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GymCreateComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GymCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
