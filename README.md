# CaliSaaS - Plataforma Distribuida de Gestión de Gimnasios

¡Bienvenido al repositorio oficial del proyecto **CaliSaaS**! 🚀

Este proyecto implementa una arquitectura distribuida (microservicios) orientada al formato **Multi-Tenant** (múltiples gimnasios bajo la misma infraestructura), utilizando tecnologías modernas para el backend, frontend y gestión de identidades.

---

## 🛠️ Tecnologías Principales

- **Frontend:** Angular 17+ (Standalone Components, sin `AppModule`).
- **Backend Core:** Django (Python) con Django REST Framework y PostgreSQL.
- **Backend Secundario (Ej. Auditoría):** Node.js con MongoDB y MySQL (por implementar).
- **Gestión de Identidad:** Keycloak (OIDC, JWT).
- **Mensajería Asíncrona:** Apache Kafka + Zookeeper.
- **Infraestructura:** Docker & Docker Compose.

---

## 🚀 Requisitos Previos

Asegúrate de tener instalado en tu máquina local:
1. **Docker y Docker Compose:** Para levantar toda la infraestructura.
2. **Node.js (v18 o superior):** Para compilar y levantar el proyecto de Angular.
3. **Git:** Para clonar el repositorio.

---

## ⚙️ Pasos para Levantar la Infraestructura (Docker)

Todo el ecosistema de bases de datos, Kafka y Keycloak está orquestado. Sigue estos pasos exactamente en este orden:

### 1. Clonar y configurar variables de entorno
Crea un archivo llamado `.env` en la raíz del proyecto (basado en el `.env.example`).
**Nota importante:** En el `.env`, la variable `HOST_IP` debe ser tu dirección IP en la red local (ejemplo: `192.168.1.5`). Esto es vital para que Angular y Keycloak se comuniquen correctamente y el profesor pueda conectarse desde otros dispositivos en la universidad.

### 2. Levantar los contenedores
Abre tu terminal en la raíz del proyecto y ejecuta:
```bash
docker-compose up -d --build
```
Espera un par de minutos para que todas las bases de datos y Keycloak se inicialicen correctamente.

### 3. Configurar Keycloak Automáticamente
El script `keycloak-setup.sh` contiene todas las configuraciones necesarias (Reino `CaliSaaS`, Cliente `angular-frontend`, roles y usuarios de prueba).
Como estás en Windows, la forma más fácil de ejecutarlo es inyectándolo directamente al contenedor de Keycloak:
```powershell
docker cp keycloak-setup.sh calisaas_keycloak:/tmp/keycloak-setup.sh
docker exec calisaas_keycloak bash /tmp/keycloak-setup.sh
```
Con esto tendrás listos los siguientes usuarios para hacer pruebas:
- **Usuario:** `owner` | **Contraseña:** `owner` (Rol: admin_gym)
- **Usuario:** `athlete` | **Contraseña:** `athlete` (Rol: atleta)

---

## 🎨 Pasos para Levantar el Frontend (Angular)

El frontend ha sido configurado sin librerías "mágicas". El manejo de tokens y la inyección a través de Interceptors se hace **completamente de forma manual**.

1. Entra a la carpeta de Angular:
   ```bash
   cd frontend-angular
   ```
2. Instala las dependencias:
   ```bash
   npm install
   ```
3. Levanta el servidor con certificados seguros locales:
   ```bash
   npm start
   ```
   > **⚠️ OJO:** Este comando internamente ejecuta `ng serve --host 0.0.0.0 --ssl`. Usamos `--ssl` porque Keycloak 26 utiliza políticas estrictas de seguridad web (PKCE) que **solo funcionan bajo HTTPS**.

4. **Accede a la aplicación:** Abre tu navegador y dirígete a:
   👉 `https://TU_IP_LOCAL:4200` (Ej: `https://192.168.1.5:4200`)
   *(Acepta la advertencia de seguridad del navegador dándole a "Avanzado > Continuar").*

---

## 🏛️ Diseño Multi-Tenant 

1. **Aislamiento en Backend:** Django utiliza un Mixin llamado `GymIsolationMixin`. Cada petición que recibe saca el `gym_id` del token JWT e inyecta un filtro automático. Los modelos **no** tienen claves foráneas directas hacia un modelo `Gym`, cumpliendo la regla estricta de aislamiento.
2. **Branding Dinámico en Frontend:** El componente `AppComponent` lee los colores y logos definidos en `environment.ts` e inyecta variables CSS en tiempo real (`document.documentElement.style.setProperty`).
3. **Autenticación Standalone:** No hay `keycloak-angular`. Se utiliza `keycloak-js` nativo y un Interceptor manual (`auth.interceptor.ts`) que adjunta el `Bearer token` a todas las peticiones hacia Django (puerto 8000) y Node.js (puerto 3000).

