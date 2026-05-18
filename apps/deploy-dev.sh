#!/bin/bash

FILE="docker-compose.yml"
DEVFILE="docker-compose-dev.yml"

sudo rm -R api
sudo rm -R front

sudo mkdir api
sudo mkdir front

echo "=== 1. Apagando contenedores previos ==="
sudo docker compose -f $FILE -f $DEVFILE down

echo "=== 2. Descargando últimas imágenes ==="
sudo docker compose -f $FILE -f $DEVFILE pull

function cleanup {
    echo -e "\n=== Detectado Ctrl+C: Apagando el entorno limpiamente ==="
    sudo docker compose -f $FILE -f $DEVFILE down
    exit 0
}
trap cleanup SIGINT

echo "=== 3. Iniciando contenedores (Mostrando Logs en vivo) ==="
echo "Presiona Ctrl + C para detener el proyecto y apagar los contenedores."
echo "------------------------------------------------------------------"

sudo docker compose -f $FILE -f $DEVFILE up
