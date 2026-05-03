# CaliSaaS - Plataforma Distribuida de Gestión de Gimnasios

¡Bienvenido al repositorio oficial del proyecto **CaliSaaS**! 🚀

Este proyecto implementa una arquitectura distribuida (microservicios) orientada al formato **Multi-Tenant** (múltiples gimnasios bajo la misma infraestructura), utilizando tecnologías modernas para el backend, frontend y gestión de identidades.

---

## 🛠️ Tecnologías Principales

- **Frontend:** Angular 17+ (Standalone Components, sin `AppModule`).
- **Backend Core:** Django (Python) con Django REST Framework y PostgreSQL.
- **Gestión de Identidad:** Keycloak (OIDC, JWT).
- **Mensajería Asíncrona:** Apache Kafka + Zookeeper.
- **Infraestructura:** Docker & Docker Compose.

---

## 🚀 Requisitos Previos (¡Muy Importante!)

Para que el proyecto funcione en tu computadora, necesitas tener instalado:
1. **Docker Desktop:** [Descárgalo aquí](https://www.docker.com/products/docker-desktop/). ¡Asegúrate de que la aplicación de Docker esté **abierta y corriendo** antes de continuar!
2. **Node.js (v18 o superior):** [Descárgalo aquí](https://nodejs.org/).
3. **Git:** Para clonar el proyecto.

---

## ⚙️ GUÍA PASO A PASO: Cómo levantar el proyecto

Sigue estas instrucciones al pie de la letra (¡es a prueba de fallos!):

### PASO 1: Configurar la IP de tu computadora
El proyecto necesita saber tu IP local para que los servicios se puedan comunicar y Keycloak funcione correctamente.
1. Abre tu terminal (CMD o PowerShell) y escribe `ipconfig` (si usas Windows).
2. Busca la "Dirección IPv4" (ejemplo: `192.168.1.5` o `192.168.0.20`).
3. En la carpeta raíz de este proyecto, haz una copia del archivo `.env.example` y llámala **exactamente** `.env`.
4. Abre ese archivo `.env` y asegúrate de que la primera línea tenga tu IP. Por ejemplo:
   ```env
   HOST_IP=192.168.1.5
   ```
   *(¡No pongas localhost ni 127.0.0.1! Tiene que ser la IP de tu red).*

### PASO 2: Levantar las Bases de Datos y el Backend
1. Abre una terminal en la carpeta principal del proyecto (donde está el archivo `docker-compose.yml`).
2. Escribe el siguiente comando y presiona Enter:
   ```bash
   docker-compose up -d --build
   ```
3. **¡Paciencia!** La primera vez tomará varios minutos en descargar e instalar todo. Espera a que termine.

### PASO 3: Configurar el sistema de Logins (Keycloak)
El servidor de logins arranca vacío, así que debemos inyectarle la configuración de nuestro gimnasio.
1. Abre **otra ventana de terminal** (PowerShell o CMD) en la misma carpeta raíz del proyecto.
2. Pega este primer comando y dale Enter:
   ```powershell
   docker cp keycloak-setup.sh calisaas_keycloak:/tmp/keycloak-setup.sh
   ```
3. Pega este segundo comando y dale Enter (este creará los usuarios y el gimnasio):
   ```powershell
   docker exec calisaas_keycloak bash /tmp/keycloak-setup.sh
   ```
   *Deberías ver un mensaje que dice "Keycloak setup finished successfully."*

Con esto ya tienes tus cuentas de prueba listas:
👉 **Usuario:** `owner` | **Contraseña:** `owner` (Es el administrador)
👉 **Usuario:** `athlete` | **Contraseña:** `athlete` (Es un deportista)

### PASO 4: Encender la Interfaz Gráfica (Frontend Angular)
¡Buenas noticias! El frontend es "inteligente" y detectará tu IP automáticamente, no tienes que cambiar código.

1. Abre una terminal y métete a la carpeta del frontend:
   ```bash
   cd frontend-angular
   ```
2. Instala los paquetes de Node:
   ```bash
   npm install
   ```
3. Enciende el servidor de Angular:
   ```bash
   npm start
   ```
   > **⚠️ NOTA:** Este comando levanta Angular con seguridad SSL. Es obligatorio porque Keycloak bloquea los logins si la página no es HTTPS.

### PASO 5: ¡Entrar a la Plataforma!
1. Abre tu navegador (Google Chrome o Edge) y entra a esta dirección, **usando la misma IP que pusiste en el PASO 1**:
   👉 `https://TU_IP_LOCAL:4200` (Ejemplo: `https://192.168.1.5:4200`)
2. El navegador te lanzará una alerta roja gigante diciendo "La conexión no es privada" (porque es un certificado local).
3. Haz clic en el botón **"Configuración Avanzada"** (Advanced) y luego haz clic en el enlace de abajo que dice **"Continuar a 192.168.X.X (inseguro)"**.
4. ¡Listo! Dale clic al botón rojo de **Login** e ingresa con el usuario `owner`.

---

## 🏛️ Resumen para la Sustentación (Diseño Multi-Tenant)

Si el profesor pregunta cómo logramos que el proyecto soporte múltiples gimnasios sin mezclar los datos:

1. **Aislamiento en Backend (Filtro Invisible):** En Django programamos un `GymIsolationMixin`. Django toma el token JWT del usuario, extrae el `gym_id`, y lo inyecta obligatoriamente en todas las consultas a la base de datos de PostgreSQL. Los datos del gimnasio A jamás se mezclarán con los del B.
2. **Branding Dinámico en Frontend:** Angular lee colores y textos desde el `environment.ts` y cambia las variables CSS en tiempo real con `document.documentElement.style.setProperty`. Esto permite cambiar la "fachada" según el gimnasio.
3. **Seguridad Standalone sin atajos:** No usamos librerías de terceros perezosas como `keycloak-angular`. Implementamos `keycloak-js` nativo y construimos un `auth.interceptor.ts` 100% manual para propagar el Token JWT hacia los microservicios.
