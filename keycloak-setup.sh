#!/bin/bash
export PATH=$PATH:/opt/keycloak/bin

# Esperamos un poco o nos autenticamos (asumiendo que ya hay credenciales activadas arriba)
kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

# =========================================
# REALM: GimnasioNorte
# =========================================
kcadm.sh create realms -s realm=GimnasioNorte -s enabled=true || true

# Cliente Frontend Norte
cat <<EOF > /tmp/norte-frontend-client.json
{
  "clientId": "angular-frontend",
  "publicClient": true,
  "redirectUris": ["*"],
  "webOrigins": ["*"],
  "directAccessGrantsEnabled": true
}
EOF
kcadm.sh create clients -r GimnasioNorte -f /tmp/norte-frontend-client.json

# Cliente Backend Norte
cat <<EOF > /tmp/norte-backend-client.json
{
  "clientId": "backend-client",
  "secret": "secret-norte",
  "serviceAccountsEnabled": true,
  "publicClient": false,
  "directAccessGrantsEnabled": true
}
EOF
kcadm.sh create clients -r GimnasioNorte -f /tmp/norte-backend-client.json

# Roles Norte
kcadm.sh create roles -r GimnasioNorte -s name=admin_gym || true
kcadm.sh create roles -r GimnasioNorte -s name=atleta || true

# Usuarios Norte
kcadm.sh create users -r GimnasioNorte -s username=owner_norte -s enabled=true
kcadm.sh set-password -r GimnasioNorte --username owner_norte --new-password owner
kcadm.sh add-roles -r GimnasioNorte --uusername owner_norte --rolename admin_gym

kcadm.sh create users -r GimnasioNorte -s username=atleta_norte -s enabled=true
kcadm.sh set-password -r GimnasioNorte --username atleta_norte --new-password atleta
kcadm.sh add-roles -r GimnasioNorte --uusername atleta_norte --rolename atleta

# =========================================
# REALM: GimnasioSur
# =========================================
kcadm.sh create realms -s realm=GimnasioSur -s enabled=true || true

# Cliente Frontend Sur
cat <<EOF > /tmp/sur-frontend-client.json
{
  "clientId": "angular-frontend",
  "publicClient": true,
  "redirectUris": ["*"],
  "webOrigins": ["*"],
  "directAccessGrantsEnabled": true
}
EOF
kcadm.sh create clients -r GimnasioSur -f /tmp/sur-frontend-client.json

# Cliente Backend Sur
cat <<EOF > /tmp/sur-backend-client.json
{
  "clientId": "backend-client",
  "secret": "secret-sur",
  "serviceAccountsEnabled": true,
  "publicClient": false,
  "directAccessGrantsEnabled": true
}
EOF
kcadm.sh create clients -r GimnasioSur -f /tmp/sur-backend-client.json

# Roles Sur
kcadm.sh create roles -r GimnasioSur -s name=admin_gym || true
kcadm.sh create roles -r GimnasioSur -s name=atleta || true

# Usuarios Sur
kcadm.sh create users -r GimnasioSur -s username=owner_sur -s enabled=true
kcadm.sh set-password -r GimnasioSur --username owner_sur --new-password owner
kcadm.sh add-roles -r GimnasioSur --uusername owner_sur --rolename admin_gym

kcadm.sh create users -r GimnasioSur -s username=atleta_sur -s enabled=true
kcadm.sh set-password -r GimnasioSur --username atleta_sur --new-password atleta
kcadm.sh add-roles -r GimnasioSur --uusername atleta_sur --rolename atleta

echo "Keycloak setup for GimnasioNorte and GimnasioSur finished successfully."
