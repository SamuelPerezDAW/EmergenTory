# EmergenTory

Bienvenido/a al repositorio de EmergenTory, un proyecto desarrollado para gestionar de manera cómoda el inventariado de vehículos de emergencias.

## Requisitos Previos

Para poder ejecutar correctamente todos los scripts y servicios del repositorio, es necesario tener instaladas las siguientes herramientas:

- `uv`
- `docker`
- `docker-compose-plugin`
- `python`

---

# Instalación en Linux

## Instalar Python

Comprueba primero si Python ya está instalado:

```bash
python3 --version
```

Si no está instalado:

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

### Arch Linux

```bash
sudo pacman -S python python-pip
```

### Fedora

```bash
sudo dnf install -y python3 python3-pip
```

---

## Instalar uv

`uv` es el gestor de paquetes y entornos utilizado por el proyecto.

### Instalación rápida

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Después, reinicia la terminal o ejecuta:

```bash
source ~/.bashrc
```

Comprobar instalación:

```bash
uv --version
```

---

## Instalar Docker

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y docker.io
```

### Arch Linux

```bash
sudo pacman -S docker
```

### Fedora

```bash
sudo dnf install -y docker
```

Habilitar y arrancar Docker:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Comprobar instalación:

```bash
docker --version
```

---

## Instalar Docker Compose Plugin

### Ubuntu / Debian

```bash
sudo apt install -y docker-compose-plugin
```

### Arch Linux

```bash
sudo pacman -S docker-compose
```

### Fedora

```bash
sudo dnf install -y docker-compose-plugin
```

Comprobar instalación:

```bash
docker compose version
```

---

# Levantar la Documentación

Para ejecutar la documentación localmente:

## Entrar en la carpeta documentation

```bash
cd documentation
```

## Iniciar el servidor de documentación

```bash
uv run zensical serve
```

Una vez iniciado el servidor, abre el navegador y accede a:

```text
http://localhost:8000
```

---

# Notas

- Asegúrate de tener todas las dependencias instaladas antes de ejecutar los comandos.
- Docker debe estar iniciado para poder utilizar los servicios relacionados con contenedores.
- Si `uv` no funciona tras instalarlo, reinicia la terminal.
