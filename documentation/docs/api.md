---
icon: lucide/cable
---

# API

La API de EmergenTory está desarrollada con Django y expone endpoints HTTP en formato JSON para que la aplicación Vue pueda consultar y modificar usuarios, vehículos y checklists.

La URL base en desarrollo es:

```text
http://127.0.0.1:8000
```

## Autenticación

La autenticación se realiza con un token propio guardado en el modelo `Token`. Las peticiones protegidas deben enviar la cabecera:

```http
Authorization: Bearer <uuid-del-token>
```

El token se crea automáticamente al crear un usuario. En el frontend se guarda en `sessionStorage` con la clave `emergentory_token`.

!!! warning "Inicio de sesión actual"

    El login del frontend consulta el perfil del usuario y compara la contraseña en cliente con el hash devuelto por la API. Esto funciona con la implementación actual, pero no es el flujo recomendado para producción porque expone el hash de contraseña en la respuesta del perfil.

## Usuarios

### Listar usuarios

```http
GET /api/users/
```

Devuelve los perfiles de usuario ordenados por nombre de usuario.

- Requiere token.
- Requiere perfil administrador.

### Crear usuario

```http
POST /api/users/add/
```

Crea un usuario de Django y, mediante señales, también crea su `Profile` y su `Token`.

Campos aceptados:

| Campo | Obligatorio | Descripción |
| --- | --- | --- |
| `nombre_usuario` | Sí | Nombre de usuario. No puede contener espacios. |
| `contraseña` | Sí | Contraseña inicial. Se guarda hasheada. |
| `nombre` | No | Nombre. |
| `apellido` | No | Apellido. |
| `email` | No | Correo electrónico. |
| `bio` | No | Biografía del perfil. |
| `telefono` | No | Teléfono validado por expresión regular. |
| `admin` | No | Marca el perfil como administrador. |

- Requiere token.
- Requiere perfil administrador.

### Obtener perfil

```http
GET /api/users/profile/<nombre_usuario>/
```

Devuelve el perfil, los datos del usuario y el token asociado.

### Modificar perfil

```http
POST /api/users/profile/<nombre_usuario>/mod/
```

Permite actualizar datos del usuario y del perfil. Acepta JSON o `multipart/form-data` cuando se actualiza el avatar.

Campos aceptados:

| Campo | Descripción |
| --- | --- |
| `nombre_usuario` | Nuevo nombre de usuario. |
| `nombre` | Nombre. |
| `apellidos` | Apellidos. |
| `email` | Correo electrónico. |
| `contraseña` | Nueva contraseña. |
| `bio` | Biografía. |
| `telefono` | Teléfono. |
| `admin` | Solo puede cambiarlo un administrador. |
| `avatar` | Archivo de imagen en `multipart/form-data`. |

- Requiere token.
- Puede modificarlo un administrador o el usuario propietario.

### Eliminar usuario

```http
POST /api/users/profile/<nombre_usuario>/del/
```

Elimina el usuario. Al estar relacionados por `CASCADE`, también se eliminan su perfil y token.

- Requiere token.
- Puede eliminarlo un administrador o el usuario propietario.

### Reiniciar contraseña

```http
POST /api/users/profile/<nombre_usuario>/reset-password/
```

Actualiza la contraseña del usuario.

```json
{
  "contraseña": "nueva-contraseña"
}
```

- Requiere token.
- Puede usarlo un administrador o el usuario propietario.

## Vehículos

### Listar vehículos

```http
GET /api/vehicles/
```

Devuelve los vehículos con su checklist asociada. Permite filtros por query string:

| Parámetro | Ejemplo |
| --- | --- |
| `matricula` | `/api/vehicles/?matricula=1234BCD` |
| `marca` | `/api/vehicles/?marca=Mercedes` |
| `modelo` | `/api/vehicles/?modelo=Sprinter` |
| `categoria` | `/api/vehicles/?categoria=AMB` |

### Crear vehículo

```http
POST /api/vehicles/add/
```

Crea un vehículo. Una señal crea automáticamente su checklist.

```json
{
  "matricula": "1234BCD",
  "marca": "Mercedes",
  "modelo": "Sprinter",
  "categoria": "AMB"
}
```

Categorías permitidas:

| Código | Categoría |
| --- | --- |
| `POL` | Policía |
| `AMB` | Ambulancia |
| `BOM` | Bombero |

- Requiere token.
- Requiere perfil administrador.

### Cambiar imagen

```http
POST /api/vehicles/<matricula>/change_vehicle_image/
```

Actualiza el campo `imagen` del vehículo.

- Requiere token.
- Requiere perfil administrador.

### Eliminar vehículo

```http
POST /api/vehicles/<matricula>/del/
```

Elimina el vehículo. Su checklist asociada se elimina por la relación `CASCADE`.

- Requiere token.
- Requiere perfil administrador.

## Checklists

### Listar checklists

```http
GET /api/checklists/
```

Devuelve las checklists con usuario, vehículo e items. Permite filtros:

| Parámetro | Descripción |
| --- | --- |
| `usuario` | Filtra por nombre de usuario. |
| `vehiculo` | Filtra por matrícula. |
| `creado` | Filtra por fecha de creación exacta. |
| `actualizado` | Filtra por fecha de actualización exacta. |

### Listar items

```http
GET /api/checklists/checkitems/
```

Devuelve los items de checklist. Permite filtros:

| Parámetro | Descripción |
| --- | --- |
| `nombre` | Filtra por nombre exacto. |
| `activo` | Filtra por estado. |
| `checklist` | Filtra por matrícula del vehículo. |

### Crear item

```http
POST /api/checklists/checkitems/add/
```

```json
{
  "nombre": "Botiquín",
  "activo": true,
  "checklist": "1234BCD"
}
```

- Requiere token.

### Modificar item

```http
POST /api/checklists/checkitems/mod/
```

```json
{
  "id": 1,
  "nombre": "Botiquín revisado",
  "activo": false,
  "checklist": "1234BCD"
}
```

- Requiere token.

### Eliminar item

```http
POST /api/checklists/checkitems/del/
```

```json
{
  "id": 1
}
```

- Requiere token.
