from django.db import models

class Gym(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True) # Para la URL (ej: calisaas.com/duitama-fit)
    owner_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Athlete(models.Model):
    # Esta es la clave del Multi-tenant: el discriminador
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='athletes')
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    weight = models.FloatField(help_text="Peso en kg")
    height = models.FloatField(help_text="Altura en metros")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.gym.name}"
