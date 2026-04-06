from django.db import models
from django.conf import settings

class Gym(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    # SEGURIDAD MULTI-TENANT: Vinculamos cada gimnasio al usuario real de Django.
    # Esto asegura que todo el árbol de datos dependa de un Tenant autenticado.
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_gyms'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Athlete(models.Model):
    # EL DISCRIMINADOR: Esta llave foránea es la frontera que separa 
    # los atletas de un gimnasio (Tenant A) de los de otro (Tenant B).
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='athletes')
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    weight = models.FloatField(help_text="Peso en kg")
    height = models.FloatField(help_text="Altura en metros")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.gym.name}"