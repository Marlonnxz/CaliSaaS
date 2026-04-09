#!/bin/bash
export PATH=$PATH:/opt/keycloak/bin

# Esperamos un poco o nos autenticamos (asumiendo que ya hay credenciales activadas arriba)
kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

# Creamos el reino CaliSaaS
kcadm.sh create realms -s realm=CaliSaaS -s enabled=true || true

# Create frontend client
cat <<EOF > /tmp/frontend-client.json
{
  "clientId": "frontend-react",
  "publicClient": true,
  "redirectUris": ["*"],
  "webOrigins": ["*"],
  "directAccessGrantsEnabled": true
}
EOF
kcadm.sh create clients -r CaliSaaS -f /tmp/frontend-client.json

# Create backend client
cat <<EOF > /tmp/backend-client.json
{
  "clientId": "calisaas-backend",
  "secret": "secret",
  "serviceAccountsEnabled": true,
  "publicClient": false,
  "directAccessGrantsEnabled": true
}
EOF
kcadm.sh create clients -r CaliSaaS -f /tmp/backend-client.json

# Create Roles
kcadm.sh create roles -r CaliSaaS -s name=admin_gym || true
kcadm.sh create roles -r CaliSaaS -s name=atleta || true

# Create testing users
kcadm.sh create users -r CaliSaaS -s username=owner -s enabled=true
kcadm.sh set-password -r CaliSaaS --username owner --new-password owner
kcadm.sh add-roles -r CaliSaaS --uusername owner --rolename admin_gym

kcadm.sh create users -r CaliSaaS -s username=athlete -s enabled=true
kcadm.sh set-password -r CaliSaaS --username athlete --new-password athlete
kcadm.sh add-roles -r CaliSaaS --uusername athlete --rolename atleta

echo "Keycloak setup finished successfully."
