---
icon: lucide/rocket
---

# EmergenTory

EmergenTory es una aplicación web para gestionar el inventariado y las listas de revisión de vehículos de emergencia. La solución está dividida en una aplicación frontend con Vue y una API backend con Django.

## Estructura del Proyecto

```text
apps/
├── api/      # Backend Django
├── main/     # Frontend Vue
└── bbdd/     # Espacio reservado para base de datos
```

## Documentación

- [Guía de Usuario](guia_usuario.md)
- [Base de Datos](bbdd.md)
- [Aplicación con Vue](vue.md)
- [API](api.md)

## Tecnologías

| Área | Tecnología |
| --- | --- |
| Frontend | Vue 3, TypeScript, Vite, Pinia, Vue Router, Axios, Tailwind CSS |
| Backend | Django, Python |
| Base de datos | SQLite en desarrollo |
| Documentación | Zensical y Markdown |

## Resumen Funcional

La aplicación permite:

- Iniciar sesión con usuarios registrados.
- Consultar y editar el perfil del usuario.
- Gestionar vehículos de emergencia.
- Crear y mantener checklists por vehículo.
- Gestionar usuarios desde perfiles administradores.

## Arranque en Desarrollo

Backend:

```bash
cd apps/api
python manage.py runserver
```

Frontend:

```bash
cd apps/main
npm run dev
```

Documentación:

```bash
cd documentation
zensical serve
```
