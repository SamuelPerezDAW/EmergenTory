---
icon: lucide/database
---

Este es el modelo de la base de datos a implementar en el proyecto, se mostrará el modelo de datos y el diagrama de clases.

Los datos están almacenados en un sistema de gestión de base de datos SQL con Sqlite3

## Modelo de Datos

```mermaid
erDiagram
    USUARIO

    PERFIL

    TOKEN

    LISTA

    ITEM

    VEHÍCULO


    USUARIO ||--|| PERFIL : tiene
    USUARIO o|--o| LISTA : gestiona
    LISTA ||--o{ ITEM : tiene
    VEHÍCULO ||--|| LISTA : pertenece
    USUARIO ||--|| TOKEN : obtiene
```

## Diagramas

```mermaid
classDiagram
    class Usuario {
        -int id [pk]
        -string username
        -string email
        -string firts_name
        -string last_name
        -string password
        +login()
        +signup()
        +logout()
    }

    class Perfil {
        -int id [pk]
        -bool admin
        -string avatar
        -string bio
        -string teléfono
        +editar_perfil()
        +acceder_perfil()
        +eliminar_usuario()
        +reiniciar_contraseña()
    }

    class Token {
        -uuid key [pk]
        -datetime creado
    }

    class Vehiculo {
        -string matrícula [pk]
        -string marca
        -string modelo
        -string categoría
        +listar_vehiculo()
        +crear_vehiculo()
        +eliminar_vehiculo()

    }

    class Lista {
        -int id [pk]
        -datetime creado
        -datetime actualizado
        +listar_lista()
    }

    class Item {
        -int id [pk]
        -string nombre
        -bool activo
        +listar_item()
        +añadir_item()
        +modificar_item()
        +eliminar_item()
    }


    Usuario "1" -- "1" Perfil : tiene
    Usuario "1" -- "1" Token : obtiene
    Usuario "0..1" -- "0..1" Lista : gestiona
    Vehiculo "1" -- "1" Lista : pertenece
    Lista "1" -- "0..*" Item : tiene

```
