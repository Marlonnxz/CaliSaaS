FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# We use an argument to determine which tenant configuration to serve
ARG TENANT_CONFIG
ENV TENANT_CONFIG=${TENANT_CONFIG}

EXPOSE 4200
EXPOSE 4201

# Run Angular's dev server directly for maximum development/demonstration compatibility
CMD npm run start -- -c ${TENANT_CONFIG} --host 0.0.0.0 --port 4200 --disable-host-check
