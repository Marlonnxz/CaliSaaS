from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Gym, Athlete

User = get_user_model()

class AthleteListCreateTests(APITestCase):

    def setUp(self):
        # Creamos dos dueños diferentes
        self.owner1 = User.objects.create_user(username='owner1', password='pw')
        self.owner2 = User.objects.create_user(username='owner2', password='pw')

        # Creamos dos gimnasios
        self.gym1 = Gym.objects.create(name='Gym 1', slug='gym1', owner=self.owner1)
        self.gym2 = Gym.objects.create(name='Gym 2', slug='gym2', owner=self.owner2)

        # Creamos atletas
        self.athlete1 = Athlete.objects.create(
            gym=self.gym1, first_name='John', last_name='Doe', weight=70, height=1.75
        )
        self.athlete2 = Athlete.objects.create(
            gym=self.gym2, first_name='Jane', last_name='Smith', weight=65, height=1.65
        )

        self.url = '/api/athletes/' # Asegúrate de que esta URL coindice con tu urls.py

    def test_owner_only_sees_own_athletes(self):
        """
        Verifica que al consultar la lista, owner1 solo vea a athlete1 y NO a athlete2
        gracias al aislamiento del TenantManager y TenantMiddleware.
        """
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Solo debe haber 1 atleta en la respuesta (athlete1)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'John')

    def test_cannot_create_athlete_in_other_owners_gym_idor_prevention(self):
        """
        Verifica que owner1 NO puede asignar un atleta a gym2
        """
        self.client.force_authenticate(user=self.owner1)
        data = {
            'gym': self.gym2.id, # Intento de IDOR (asignar al gym del owner2)
            'first_name': 'Hacker',
            'last_name': 'Man',
            'weight': 80,
            'height': 1.80
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('gym', response.data)
        self.assertIn('Acceso denegado: No puedes agregar atletas a un gimnasio que no te pertenece.', str(response.data['gym']))

    def test_owner_can_create_athlete_in_their_gym(self):
        """
        Verifica que owner1 SÍ puede crear un atleta en gym1
        """
        self.client.force_authenticate(user=self.owner1)
        data = {
            'gym': self.gym1.id,
            'first_name': 'Legit',
            'last_name': 'User',
            'weight': 75,
            'height': 1.70
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Athlete.objects.filter(gym=self.gym1).count(), 2)
