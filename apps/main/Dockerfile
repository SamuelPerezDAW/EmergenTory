FROM node:lts-slim

WORKDIR /app

# Primero copiamos los archivos de dependencias
COPY package*.json ./
RUN npm install

# Copiamos el resto del código
COPY . .

EXPOSE 5173
