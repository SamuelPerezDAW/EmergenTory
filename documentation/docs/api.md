---
icon: lucide/cable
---

La API está hecha en el Framework Django, en el cual está desarrollado en el lenguaje de programación Python.

## Objetivo

La implementación de esa API tiene como objetivo agilizar la gestión de la base de datos desde el frontend, ejecutando estos métodos en el backend.

## Peticiones

Las siguientes peticiones se realizarán desde el frontend a la API en el backend utilizando los métodos a travez de las URI

??? info "Uso de peticiones"

    Algunas peticiones están restringidas a ciertos permisos de administrador o requiere de ser el usuario propietario

### Usuario

Permite añadir un usuario a la base de datos, este crea un perfil y un token de manera automática para el usuario recien añadido

```
  POST: /api/users/add/
```

- [x] Admin necesario

### Perfil

Obtiene el perfil del usuario

```
  GET: /api/users/profile/nombre_usuario/
```

- [x] Admin necesario
- [x] Token propietario necesario

Modifica la información del perfil de un usuario

```
  POST: /api/users/profile/nombre_usuario/mod/
```

- [x] Admin necesario
- [x] Token propietario necesario

Elimina el usuario junto a su perfil y token de la base de datos

```
  POST: /api/users/profile/nombre_usuario/del/
```

- [x] Admin necesario
- [x] Token propietario necesario

Reinicia la contraseña en caso de perderla mediante un correo electrónico

```
  POST: /api/users/profile/nombre_usuario/reset-password/
```

- [x] Admin necesario
- [x] Token propietario necesario

### Vehiculo

Lista los vehiculos guardados en la base de datos

```
  GET: /api/users/vehicles/
```

Añade un nuevo vehiculo a la base de datos que a su vez genera una checklist para este vehículo

```
  POST: /api/users/vehicles/add/
```

- [x] Admin necesario

Elimina el vehiculo seleccionado junto a su checklist con todos los respectivos items asignados

```
  POST: /api/users/vehicles/del/
```

- [x] Admin necesario

### Checklist

Permite revisar las listas de la base de datos

```
  POST: /api/checklists/
```

### Checkitem

Permite revisar los items de cada lista

```
  POST: /api/checklists/checkitems/
```

Añade un item a una lista en concreto

```
  POST: /api/checklists/checkitems/add/
```

- [x] Admin necesario
- [x] Token propietario necesario

Modifica el item de la lista seleccionada

```
  POST: /api/checklists/matricula/nombre_item/mod/
```

- [x] Admin necesario

Elimina el item de la lista seleccionada

```
  POST: /api/checklists/matricula/nombre_item/del/
```

- [x] Admin necesario
