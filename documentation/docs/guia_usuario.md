---
icon: lucide/book-open
---

# Guía de Usuario

Esta guía explica cómo utilizar el frontend de EmergenTory para gestionar vehículos de emergencia, listas de material, perfiles y usuarios.

## Acceso a la Aplicación

Al abrir la aplicación se muestra la pantalla de autenticación.

Para iniciar sesión:

1. Introduce el nombre de usuario.
2. Introduce la contraseña.
3. Pulsa `Entrar`.

Si las credenciales son correctas, la aplicación abre el dashboard principal. Si no son válidas, se muestra un mensaje de error.

## Recuperar Contraseña

Desde la pantalla de login se puede solicitar un enlace para restablecer la contraseña.

1. Pulsa `Olvidé mi contraseña`.
2. Introduce el email asociado al usuario.
3. Pulsa `Enviar enlace`.
4. Abre el enlace de recuperación.
5. Escribe la nueva contraseña dos veces.
6. Pulsa `Actualizar contraseña`.

En desarrollo local, el enlace se imprime en la consola del `rqworker` con el formato:

```text
RESET_PASSWORD_URL=http://localhost:5173/reset-password/...
```

## Navegación Principal

Después de iniciar sesión, la aplicación muestra una barra lateral con las secciones disponibles.

| Sección     | Uso                                                     |
| ----------- | ------------------------------------------------------- |
| `Dashboard` | Vista resumen de la actividad.                          |
| `Perfil`    | Consulta y edición de los datos personales.             |
| `Vehículos` | Consulta, búsqueda y gestión de vehículos.              |
| `Items`     | Gestión del material asociado a los vehículos.          |
| `Usuarios`  | Gestión de usuarios. Solo aparece para administradores. |

En pantallas pequeñas, la barra lateral se abre como menú desplegable.

## Dashboard

El dashboard muestra un resumen operativo de la aplicación:

- Total de vehículos registrados.
- Número de items activos.
- Última matrícula seleccionada.
- Última ruta visitada.
- Vehículos destacados.
- Resumen de items activos por vehículo.

Desde los vehículos destacados se puede:

- Entrar al detalle del vehículo.
- Ir directamente a la gestión de items.

## Perfil de Usuario

La sección `Perfil` permite consultar la información del usuario conectado.

Muestra:

- Imagen de perfil.
- Nombre y apellido.
- Email.
- Usuario.
- Teléfono.
- Biografía.
- Rol: administrador u operador.

Para modificar el perfil:

1. Pulsa `Editar perfil`.
2. Actualiza los campos necesarios.
3. Opcionalmente selecciona una nueva foto de perfil.
4. Pulsa `Guardar cambios`.

La aplicación valida el formato del email y la longitud del teléfono antes de guardar.

## Vehículos

La sección `Vehículos` permite consultar la flota registrada.

Cada tarjeta de vehículo muestra:

- Categoría.
- Matrícula.
- Marca.
- Modelo.
- Número de items activos.
- Total de items.
- Items inactivos.
- Identificador de la checklist.

### Buscar y Filtrar

En la parte superior se puede:

- Buscar por matrícula, marca o modelo.
- Filtrar por categoría: todas, bombero, policía o ambulancia.

### Ver Detalle

Para consultar un vehículo:

1. Busca el vehículo.
2. Pulsa `Ver detalle`.

La vista de detalle muestra:

- Categoría.
- Marca y modelo.
- Matrícula.
- Identificador de checklist.
- Fecha de creación.
- Fecha de última actualización.
- Lista de items del vehículo.

Desde esta vista también se puede acceder a `Gestionar inventario`.

### Crear Vehículo

Los usuarios administradores pueden crear vehículos.

1. Pulsa `Añadir Vehículo`.
2. Introduce matrícula, marca y modelo.
3. Selecciona la categoría.
4. Pulsa `Guardar cambios`.

Al crear un vehículo, el sistema genera automáticamente su checklist.

### Eliminar Vehículo

Los administradores pueden eliminar vehículos desde la tarjeta del vehículo pulsando `Eliminar`.

Al eliminar un vehículo también se elimina su checklist asociada.

## Items

La sección `Items` permite gestionar el material de un vehículo.

Para trabajar con items:

1. Selecciona un vehículo en el desplegable.
2. Revisa la lista de items actuales.
3. Crea, edita, activa, desactiva o elimina items.

### Crear Item

1. Selecciona el vehículo.
2. Escribe el nombre del item.
3. Marca `Item operativo` si está disponible.
4. Pulsa `Crear item`.

### Editar Item

1. Pulsa la acción de edición sobre un item.
2. Modifica el nombre o el estado operativo.
3. Pulsa `Actualizar item`.

### Cambiar Estado

Los items pueden marcarse como activos o inactivos. Este estado se usa para calcular el material operativo del vehículo.

### Eliminar Item

Pulsa la acción de eliminar del item correspondiente. El item se borra de la checklist del vehículo.

## Gestión de Usuarios

La sección `Usuarios` solo está disponible para perfiles administradores.

Permite:

- Listar usuarios.
- Crear nuevos usuarios.
- Editar usuarios existentes.
- Cambiar el rol entre operador y administrador.
- Eliminar usuarios.

### Crear Usuario

1. Pulsa `Nuevo usuario`.
2. Rellena usuario y contraseña inicial.
3. Añade nombre, apellido, email, teléfono y biografía si corresponde.
4. Marca `Administrador` si el usuario debe tener permisos de gestión.
5. Pulsa `Guardar`.

Al crear un usuario se genera automáticamente su perfil y token de acceso.

### Editar Usuario

1. Pulsa `Editar` en la fila del usuario.
2. Modifica los datos necesarios.
3. Pulsa `Guardar`.

### Eliminar Usuario

Pulsa `Eliminar` en la fila del usuario. La aplicación impide que un usuario se elimine a sí mismo desde la tabla.

## Cierre de Sesión

Para cerrar sesión:

1. Ve a la barra lateral.
2. Pulsa `Cerrar sesión`.

La aplicación elimina los datos de sesión del navegador y vuelve a la pantalla de login.

## Roles y Permisos

| Rol           | Permisos                                                                    |
| ------------- | --------------------------------------------------------------------------- |
| Operador      | Acceso a dashboard, perfil, vehículos e items.                              |
| Administrador | Incluye permisos de operador y además puede gestionar usuarios y vehículos. |

## Recomendaciones de Uso

- Mantén actualizado el email del perfil para poder recuperar la contraseña.
- Revisa los items inactivos antes de marcarlo como operativo.
- Usa filtros de vehículos cuando la flota sea grande.
- Cierra sesión al terminar si usas un equipo compartido.
