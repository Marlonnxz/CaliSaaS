#!/bin/bash
export PATH=$PATH:/opt/keycloak/bin

# Esperamos un poco o nos autenticamos (asumiendo que ya hay credenciales activadas arriba)
kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

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

# Create testing users
kcadm.sh create users -r CaliSaaS -s username=owner -s enabled=true -s "attributes.role=admin"
kcadm.sh set-password -r CaliSaaS --username owner --new-password owner

kcadm.sh create users -r CaliSaaS -s username=athlete -s enabled=true -s "attributes.role=athlete"
kcadm.sh set-password -r CaliSaaS --username athlete --new-password athlete

echo "Keycloak setup finished successfully."
