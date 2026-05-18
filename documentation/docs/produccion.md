---
icon: lucide/server
---

# Configuración en Producción

Este documento detalla la configuración del servidor de producción para EmergenTory, explicando el funcionamiento del servidor web Nginx y el proceso automatizado de despliegue.

## Configuración de Nginx (Virtual Host)

Para gestionar el tráfico web en la máquina de producción se utiliza **Nginx** como proxy inverso a través de un _Virtual Host_. Este se encarga de recibir las peticiones externas y derivarlas al contenedor correspondiente de Docker.

```bash
server {
    listen       80;
    server_name  emergentory.arkania.es;

    access_log  /var/log/nginx/host.access.log  main;

    location / {
        proxy_pass http://localhost:5173;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /api/ {
        proxy_pass http://localhost:7000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 90s;
        proxy_read_timeout 90s;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```

La configuración principal del _Virtual Host_ cumple con las siguientes reglas:

- **Puerto de escucha:** `80` (HTTP).
- **Dominio asignado (`server_name`):** `emergentory.arkania.es`

### Enrutamiento de Peticiones

Nginx divide el tráfico entrante de manera inteligente según la ruta de la URL:

| Ruta (Location)                     | Destino            | Dirección de Acceso                              |
| :---------------------------------- | :----------------- | :----------------------------------------------- |
| Enrutamiento general (Raíz)         | **Frontend (Vue)** | `emergentory.arkania.es` o `IP_SERVIDOR`         |
| Peticiones que comienzan por `/api` | **API (Django)**   | `emergentory.arkania.es/api` o `IP_SERVIDOR/api` |

---

## Proceso de Despliegue Automatizado

El repositorio principal incluye un script en Bash diseñado para automatizar por completo el proceso de actualización y puesta en marcha en el servidor de producción.

- **Ubicación del script:** `apps/deploy-prod.sh`

A este script es necesario pasarle como parámetro el **usuario** y la **IP o dominio** del servidor remoto al momento de ejecutarlo.

```bash
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
```

Un ejemplo podría ser:

```bash
source deploy-prod.sh user@domain
```

### Flujo de Trabajo Interno

Al ejecutarse, el script realiza de forma automática las siguientes acciones en el servidor:

1. Se conecta mediante SSH a la máquina de producción.
2. Realiza un `git pull` en el directorio del proyecto para descargar los últimos cambios del repositorio.
3. Levanta y actualiza los servicios utilizando el archivo `docker-compose.yml` de producción.

---

## Recomendaciones de Uso

- **Llaves SSH:** Asegúrate de tener configurada tu clave pública SSH en el servidor de producción para que el script `deploy-prod.sh` pueda conectarse sin solicitar contraseña interactivamente.
- **Configuración de Vite:** Recuerda que el dominio `emergentory.arkania.es` debe estar correctamente declarado en la propiedad `allowedHosts` del archivo `vite.config.ts` del Frontend para evitar bloqueos de peticiones.
- **Logs de Nginx:** En caso de errores de conexión (como un error _502 Bad Gateway_), revisa si los contenedores de Docker están activos antes de modificar la configuración del _Virtual Host_.
