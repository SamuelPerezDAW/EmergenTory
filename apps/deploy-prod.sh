#!/bin/bash

if [ -z $1 ]; then
    echo "❌ Error: Debes pasar el usuario y la IP del servidor remoto."
    echo "Uso correcto: ./deploy-prod.sh usuario@ip_del_servidor"
    exit 1
fi

DESTINO="$1"
SERVIDOR=$(echo "$DESTINO" | cut -d'@' -f2)

FILE="docker-compose.yml"

echo "🚀 Iniciando despliegue remoto en: $DESTINO"
echo "📂 Carpeta remota: $REMOTE_DIR"
echo "------------------------------------------------------------------"

ssh -t $1 "
    cd EmergenTory &&
    git pull &&

    cd apps &&

    echo '=== 1. Apagando contenedores previos ===' &&
    sudo docker compose -f ${FILE} down &&
    
    echo '=== 2. Descargando últimas imágenes ===' &&
    sudo docker compose -f ${FILE} pull &&
    
    echo '=== 3. Iniciando contenedores en segundo plano ===' &&
    export PROD_SERVER='${SERVIDOR}' &&
    sudo -E PROD_SERVER=\${PROD_SERVER} docker compose -f ${FILE} up -d &&
    
    echo '------------------------------------------------------------------' &&
    echo '✅ Despliegue completado con éxito.' &&
    echo 'Mostrando logs en vivo. Presiona Ctrl + C para SALIR de los logs.' &&
    echo '(El servidor seguirá encendido de fondo)' &&
    echo '------------------------------------------------------------------' &&
    
    sudo docker compose -f ${FILE} logs -f
"
