# CaliSaaS - Plataforma Distribuida de Gestión de Gimnasios

¡Bienvenido al repositorio oficial del proyecto **CaliSaaS**! 🚀

Este proyecto implementa una arquitectura distribuida (microservicios) orientada al formato **Multi-Tenant con Aislamiento Físico** (bases de datos y tecnologías separadas para cada gimnasio), comunicados mediante coreografía de eventos.

---

## 🛠️ Tecnologías Principales

- **Frontend:** Angular 17+ (Standalone Components, UI Premium Moderna).
- **Tenant 1 (Gimnasio Norte):** Backend en Python (Flask) + Base de Datos PostgreSQL.
- **Tenant 2 (Gimnasio Sur):** Backend en Node.js (Express) + Base de Datos MySQL.
- **Gestión de Identidad:** Keycloak (OIDC, JWT) configurado con múltiples Realms.
- **Coreografía y Auditoría:** Apache Kafka + Zookeeper consumido por un microservicio en Node.js.
- **Infraestructura Base:** Docker & Docker Compose.

---

## 🚀 Requisitos Previos

Para que el proyecto funcione en tu computadora a la perfección, necesitas:
1. **Docker Desktop** (Asegúrate de que esté abierto y corriendo).
2. **Node.js** (Para correr el Tenant Sur, la Auditoría y el Frontend).
3. **Python 3.13+** (Para correr el Tenant Norte).
4. **Git** (Para clonar).

---

## ⚙️ GUÍA PASO A PASO PARA EJECUTAR EL PROYECTO (A prueba de balas)

Sigue estas instrucciones al pie de la letra. ¡Gracias a Docker, **solo necesitas abrir 1 terminal**!

### PASO 1: Configurar tu IP Local (¡CRÍTICO!)
El proyecto y Apache Kafka necesitan saber la IP de la máquina host en la red local (LAN) para permitir la conexión de dispositivos cliente de forma dinámica.
1. Abre una terminal y escribe `ipconfig` (Windows) o `ifconfig` (Mac/Linux).
2. Anota tu dirección IPv4 (Ejemplo: `192.168.1.5`).
3. En la raíz del proyecto, copia el archivo `.env.example` y renómbralo exactamente a `.env`.
4. Abre `.env` y cambia la variable `HOST_IP` por tu IP real.

### PASO 2: Levantar toda la Plataforma (1 Solo Comando)
Abre tu terminal en la carpeta raíz del proyecto y ejecuta la magia de Docker:
```bash
docker compose up --build -d
```
> **Nota:** Esto descargará e instalará todas las bases de datos, Kafka, Keycloak, y construirá automáticamente los Backends (Python/Node) y Frontends (Angular). La primera vez puede tardar un par de minutos. Al final, todo quedará corriendo silenciosamente en segundo plano.

### PASO 3: Configurar el sistema de Logins (Keycloak)
Aún en la misma terminal, ejecuta el script automático que crea los "Realms", clientes y usuarios de prueba. **Espera unos 20 segundos** después del Paso 2 antes de correr esto, para darle tiempo a Keycloak de encender:
```bash
cmd.exe /c "docker exec -i keycloak /bin/bash < keycloak-setup.sh"
```
*(Si usas Mac/Linux, usa: `docker exec -i keycloak /bin/bash < keycloak-setup.sh`)*

**¡Y LISTO! Ya no tienes que encender nada más.**

---

## 💻 CÓMO PROBAR LA APLICACIÓN Y EL RBAC

El sistema ahora cuenta con **Control de Acceso Basado en Roles (RBAC)** integrado con Keycloak. Dependiendo del usuario con el que ingreses, verás una interfaz diferente.

### 1. El Portal Centralizado (`http://TU_IP_LOCAL:4200`)
La aplicación ahora funciona como un **SaaS de Login Único (SSO)**. Angular leerá tu usuario y te redirigirá mágicamente al backend del Norte (Python) o del Sur (Node.js).

**Para probar el Gimnasio Norte (PostgreSQL - Puerto 5000):**
- **Dueño:** `owner_norte` / **Clave:** `owner` (Verás el panel para crear atletas)
- **Cliente:** `atleta_norte` / **Clave:** `atleta` (Verás el portal de rutinas en modo lectura)

**Para probar el Gimnasio Sur (MySQL - Puerto 3000):**
- **Dueño:** `owner_sur` / **Clave:** `owner`
- **Cliente:** `atleta_sur` / **Clave:** `atleta`
*(Nota que al entrar con los usuarios del sur, la base de datos estará vacía. ¡Aislamiento físico y enrutamiento dinámico exitoso!)*

### 2. Auditoría y Trazabilidad (Apache Kafka)
El archivo `ms_auditoria_simple/auditoria.log` actúa como el registro de eventos centralizado (Event Sourcing). Captura en tiempo real operaciones críticas emitidas por ambos Tenants:
- `USER_LOGIN`: Autenticaciones exitosas.
- `CREATE_ATHLETE` / `DELETE_ATHLETE`: Modificaciones en el registro físico de clientes.
- `CREATE_ROUTINE` / `DELETE_ROUTINE`: Cambios en el catálogo global de rutinas.
- `TRAINING_STARTED`: Trazabilidad de uso de la plataforma por parte de los atletas.

---

## 📚 Diccionario de Endpoints (API REST)

Ambos microservicios backend implementan estricta paridad arquitectónica.

### Endpoints de Atletas
- `GET /api/athletes`: Recupera la lista completa de atletas (Lectura).
- `POST /api/athletes`: Registra un nuevo expediente de atleta y emite a Kafka.
- `DELETE /api/athletes/:id`: Borrado en cascada del expediente.

### Endpoints de Rutinas (Catálogo Global)
- `GET /api/routines`: Recupera las rutinas disponibles.
- `POST /api/routines`: Crea una rutina global y emite a Kafka.
- `DELETE /api/routines/:id`: Elimina una rutina del sistema.

### Endpoints de Auditoría
- `POST /api/audit/login`: Valida el JWT y registra el acceso del usuario.
- `POST /api/audit/training`: Registra el inicio de actividad física de un atleta.
