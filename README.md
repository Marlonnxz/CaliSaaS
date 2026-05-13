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
El proyecto y Apache Kafka necesitan saber la IP de tu computadora en tu red local (LAN) para permitir que el profesor y tu celular se conecten.
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

### 1. Probar el Gimnasio Norte (`http://TU_IP_LOCAL:4200`)
- **Como Administrador (Dueño):**
  - **Login:** `owner_norte` / **Clave:** `owner`
  - *Verás el Panel de Control completo para crear atletas y rutinas.*
- **Como Cliente (Atleta):**
  - **Login:** `atleta_norte` / **Clave:** `atleta`
  - *Verás el Portal del Atleta con diseño premium (Solo lectura).*

### 2. Probar el Gimnasio Sur (`http://TU_IP_LOCAL:4201`)
- **Como Administrador:**
  - **Login:** `owner_sur` / **Clave:** `owner`
  - *Comprueba que la base de datos está vacía. ¡Aislamiento físico (Postgres vs MySQL) exitoso!*
- **Como Cliente:**
  - **Login:** `atleta_sur` / **Clave:** `atleta`

### 3. Probar la Auditoría (Apache Kafka)
Abre el archivo `ms_auditoria_simple/auditoria.log` en Visual Studio Code. Crea una rutina desde el panel de dueño y verás cómo Kafka captura el evento en tiempo real en ese archivo de texto.
