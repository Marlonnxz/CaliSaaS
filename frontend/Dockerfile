# Etapa de construcción
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Etapa de producción con Nginx
# Etapa de producción con Nginx
FROM nginx:alpine
# Copiamos el build de Vite a la carpeta de Nginx
COPY --from=build /app/dist /usr/share/nginx/html
# Copiamos la configuración de SPA fallback a Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]