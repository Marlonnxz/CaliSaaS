#!/bin/bash
export PATH=$PATH:/opt/keycloak/bin

# Esperamos un poco o nos autenticamos (asumiendo que ya hay credenciales activadas arriba)
kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

# =========================================
# REALM: CaliSaaS (Centralizado)
# =========================================
kcadm.sh create realms -s realm=CaliSaaS -s enabled=true || true

# Cliente Frontend Unificado
cat <<EOF > /tmp/frontend-client.json
{
  "clientId": "angular-frontend",
  "publicClient": true,
  "redirectUris": ["*"],
  "webOrigins": ["*"],
  "directAccessGrantsEnabled": true
}
EOF
kcadm.sh create clients -r CaliSaaS -f /tmp/frontend-client.json

# Cliente Backend Unificado (Para validaciones si se requiere)
cat <<EOF > /tmp/backend-client.json
{
  "clientId": "backend-client",
  "secret": "secret-calisaas",
  "serviceAccountsEnabled": true,
  "publicClient": false,
  "directAccessGrantsEnabled": true
}
EOF
kcadm.sh create clients -r CaliSaaS -f /tmp/backend-client.json

# Roles de Negocio
kcadm.sh create roles -r CaliSaaS -s name=admin_gym || true
kcadm.sh create roles -r CaliSaaS -s name=atleta || true

# Roles de Tenant (Inquilino) - ¡Clave para el enrutamiento dinámico!
kcadm.sh create roles -r CaliSaaS -s name=tenant_norte || true
kcadm.sh create roles -r CaliSaaS -s name=tenant_sur || true

# =========================================
# USUARIOS NORTE
# =========================================
kcadm.sh create users -r CaliSaaS -s username=owner_norte -s enabled=true
kcadm.sh set-password -r CaliSaaS --username owner_norte --new-password owner
kcadm.sh add-roles -r CaliSaaS --uusername owner_norte --rolename admin_gym
kcadm.sh add-roles -r CaliSaaS --uusername owner_norte --rolename tenant_norte

kcadm.sh create users -r CaliSaaS -s username=atleta_norte -s enabled=true
kcadm.sh set-password -r CaliSaaS --username atleta_norte --new-password atleta
kcadm.sh add-roles -r CaliSaaS --uusername atleta_norte --rolename atleta
kcadm.sh add-roles -r CaliSaaS --uusername atleta_norte --rolename tenant_norte

# =========================================
# USUARIOS SUR
# =========================================
kcadm.sh create users -r CaliSaaS -s username=owner_sur -s enabled=true
kcadm.sh set-password -r CaliSaaS --username owner_sur --new-password owner
kcadm.sh add-roles -r CaliSaaS --uusername owner_sur --rolename admin_gym
kcadm.sh add-roles -r CaliSaaS --uusername owner_sur --rolename tenant_sur

kcadm.sh create users -r CaliSaaS -s username=atleta_sur -s enabled=true
kcadm.sh set-password -r CaliSaaS --username atleta_sur --new-password atleta
kcadm.sh add-roles -r CaliSaaS --uusername atleta_sur --rolename atleta
kcadm.sh add-roles -r CaliSaaS --uusername atleta_sur --rolename tenant_sur

echo "Keycloak setup for Centralized CaliSaaS finished successfully."
