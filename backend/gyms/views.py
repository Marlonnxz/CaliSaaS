from rest_framework import generics, serializers
from .models import Gym, Athlete
from .serializers import GymSerializer, AthleteSerializer

class GymListCreate(generics.ListCreateAPIView):
    serializer_class = GymSerializer

    def get_queryset(self):
        # AISLAMIENTO DE DATOS: Interceptamos la consulta a la BD.
        # El usuario solo puede ver los gimnasios que le pertenecen.
        return Gym.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # INYECCIÓN DE CONTEXTO: Asignamos el dueño automáticamente basado en el 
        # Token JWT de Keycloak. Previene que el usuario falsifique este dato.
        serializer.save(owner=self.request.user)

class AthleteListCreate(generics.ListCreateAPIView):
    serializer_class = AthleteSerializer

    def get_queryset(self):
        # SEGURIDAD DE LECTURA: Solo permitimos ver atletas si su gimnasio 
        # pertenece al usuario que hace la petición.
        return Athlete.objects.filter(gym__owner=self.request.user)

    def perform_create(self, serializer):
        gym = serializer.validated_data.get('gym')
        
        # PREVENCIÓN DE VULNERABILIDAD IDOR:
        # Verificamos que el usuario no intente inyectar un atleta en el 
        # gimnasio de otro cliente. Si no es el dueño, bloqueamos la petición.
        if gym.owner != self.request.user:
            raise serializers.ValidationError(
                {"gym": "Acceso denegado: No puedes agregar atletas a un gimnasio que no te pertenece."}
            )
            
        serializer.save()