---
icon: lucide/box
---

# Dockerizacion

Este documento explica la estrategia de containerización de EmergenTory, detallando la configuración de Docker y Docker Compose tanto para el entorno de desarrollo como para el de producción.

## Arquitectura de Contenedores

La aplicación EmergenTory se ha dividido en dos contenedores principales e independientes para garantizar la modularidad y facilitar el despliegue:

1. **API (Backend):** Proyecto basado en el framework Django.
2. **Frontend:** Proyecto basado en el framework Node.js con el la librería Vue.js .

Ambos componentes cuentan con su propio archivo `Dockerfile` basado en imágenes ligeras específicas de cada tecnología, optimizando el tamaño y la eficiencia del contenedor. Cada Dockerfile deja expuesto el puerto nativo de la aplicación para permitir la posterior conexión desde el host.

En el caso del Frontend, se deja el comando de actualizado de paquetes `npm i` además del comando para levantar el proyecto `npm run dev`.

## Imágenes Públicas

Tras realizar el proceso de construcción (_build_), las imágenes optimizadas se suben y se mantienen actualizadas en los siguientes repositorios públicos de Docker Hub:

- **API:** `samuelpinfo/emergentory-api:latest`
- **Frontend:** `samuelpinfo/emergentory-front:latest`

## Configuración de Docker Compose

El proyecto cuenta con dos archivos `docker-compose` diferenciados según el entorno de ejecución. Ambos mapean los puertos expuestos en los Dockerfile individuales para permitir el tráfico de red.

### Entorno de Producción

Diseñado para un despliegue rápido y estable utilizando las imágenes preconstruidas de Docker Hub.

- **Imágenes:** Descarga y ejecuta directamente `samuelpinfo/emergentory-api:latest` y `samuelpinfo/emergentory-front:latest`.
- **Persistencia:** En el contenedor de la API se configura un volumen persistente hacia el host. Este volumen aloja el archivo de la base de datos `sqlite3`, garantizando que la información no se pierda al detener o reiniciar los contenedores.

### Entorno de Desarrollo

Preparado para facilitar la modificación del código fuente en tiempo real y la construcción de nuevas imágenes locales.

- **Volúmenes adicionales:** Además de los volúmenes base, incorpora un volumen mapeado por cada aplicación que vincula el directorio local del host con el código fuente dentro del contenedor.
- **Comportamiento:** Permite aplicar cambios en el código de la API o del Front y ver los resultados de manera inmediata sin necesidad de reconstruir manualmente el contenedor en cada modificación.

## Variables de Entorno y Ciclo de Vida

El comportamiento de los contenedores se parametriza mediante variables de entorno y comandos de inicialización automatizados.

### Variables del Frontend

El contenedor del Frontend requiere una única variable de entorno:

- `VITE_API_URL` (o equivalente): Define la IP o dominio del servidor que aloja la API, permitiendo que el cliente Vue establezca la conexión con el backend.

### Variables y Comandos de la API

El contenedor de la API cuenta con una lógica de inicialización en cadena mediante la instrucción `command`. Al ejecutarse, realiza automáticamente las siguientes acciones:

1. Instala las dependencias del proyecto Django.
2. Ejecuta las migraciones de la base de datos.
3. Crea el usuario administrador por defecto utilizando los datos de las variables de entorno.
4. Levanta el servidor de desarrollo de Django apuntando a `0.0.0.0:8000`.

| Entorno                     | Variable de Entorno | Uso / Descripción                                                                                                            |
| :-------------------------- | :------------------ | :--------------------------------------------------------------------------------------------------------------------------- |
| **Producción y Desarrollo** | Datos del Admin     | Define las credenciales básicas (usuario, email, contraseña) para la creación del administrador inicial.                     |
| **Solo Desarrollo**         | `DEV`               | Activa el modo de desarrollo interno. Al estar presente, habilita la directiva `DEBUG = True` en la configuración de Django. |

## Recomendaciones de Uso

- **Persistencia en Producción:** Nunca borres el volumen local mapeado para la API en producción si no cuentas con un respaldo de la base de datos SQLite3.
- **Modo Debug:** Asegúrate de que la variable `DEV` no esté expuesta ni activa en entornos de producción para evitar brechas de seguridad con el panel de errores de Django.
- **Actualización de Imágenes:** En entornos de producción, ejecuta `docker compose pull` antes de levantar los contenedores para asegurarte de estar utilizando la versión `:latest` más reciente.
