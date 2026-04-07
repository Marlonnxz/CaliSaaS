# CaliSaaS - Plataforma Multi-Tenant

¡Bienvenido a CaliSaaS! Esta aplicación está totalmente contenerizada en Docker, por lo que **no necesitas instalar Node.js ni Python** en tu máquina para correrla. Solo necesitas tener **Docker y Docker Compose** instalados.

## Cómo levantar el proyecto por primera vez

Dado que la base de datos es local de tu propia máquina, al descargar este código por primera vez tu base de datos y tu servidor de autenticación (Keycloak) estarán vacíos. Solo debes seguir estos 3 pasos para ponerlo en marcha:

### 1. Levantar los contenedores
Abre una terminal en esta carpeta y ejecuta:
```bash
docker-compose up --build -d
```
*Espera un par de minutos a que descargue las dependencias y construya la aplicación.*

### 2. Configurar la Base de Datos (Django)
Una vez que el backend esté arriba, necesitamos crear las tablas y un par de usuarios iniciales para que el sistema reconozca a quién le pertenecen los gimnasios. En la misma terminal, ejecuta:

```bash
# Migrar la base de datos (aplica las 4 tablas de entrenamiento y seguridad)
docker-compose exec backend python manage.py migrate

# Crear usuarios base (owner superadmin y athlete)
docker-compose exec backend python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); u, _ = User.objects.get_or_create(username='owner'); u.set_password('owner'); u.is_staff=True; u.is_superuser=True; u.save(); a, _ = User.objects.get_or_create(username='athlete'); a.set_password('athlete'); a.save()"
```

### 3. Configurar la Seguridad (Keycloak)
El proyecto utiliza Keycloak para emitir Interceptores JWT y proteger las rutas de React. Para auto-crear el Reino de CaliSaaS y los clientes, ejecuta el script de configuración.

Si estás usando **Windows (PowerShell)**:
```powershell
cmd.exe /c "type keycloak-setup.sh | docker-compose exec -T keycloak bash"
```

Si estás usando **Mac / Linux**:
```bash
cat keycloak-setup.sh | docker-compose exec -T keycloak bash
```

---

## 🎯 Probar la aplicación
¡Listo! Todo está configurado. 
Abre tu navegador en: **http://localhost:5173**

Puedes iniciar sesión con cualquiera de los dos usuarios de prueba que el script creó mágicamente para ti:
- **Usuario Panel de Administración**: `owner` / `owner`
- **Usuario Panel Atleta**: `athlete` / `athlete`

> **Nota:** La primera vez que inicies sesión con un usuario, Keycloak te pedirá rellenar "Email", "First Name" y "Last Name". Puedes poner cualquier cosa (ej. `mi@email.com`), es solo un proceso de seguridad estándar una vez por cuenta.
