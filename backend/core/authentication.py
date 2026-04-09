from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

class KeycloakJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Intercepta la obtención de usuario a partir del token JWT.
        Si el usuario ("preferred_username") existe en Keycloak y el token es válido,
        pero el usuario no ha sido clonado en la tabla interna de Django (Auth User),
        lo auto-crea silenciosamente para que la petición no fracase.
        """
        username = validated_token.get('preferred_username')
        
        # Si por alguna razón el token no trae el username, delegamos a la lógica por defecto
        if not username:
            return super().get_user(validated_token)
        
        # Obtenemos o creamos mágicamente a nuestro usuario
        user, created = User.objects.get_or_create(username=username)
        return user
