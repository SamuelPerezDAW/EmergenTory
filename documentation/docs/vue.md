---
icon: lucide/layout
---

# Aplicación con Vue

La interfaz de EmergenTory está desarrollada con Vue 3, TypeScript y Vite. Usa Pinia para el estado global, Vue Router para la navegación, Axios para comunicarse con la API y Tailwind CSS para los estilos.

La aplicación se encuentra en:

```text
apps/main
```

## Arranque

El punto de entrada es `src/main.ts`.

```ts
const app = createApp(App);

app.use(createPinia());
app.use(router);
app.mount('#app');
```

El archivo registra Pinia, el router y monta el componente raíz `App.vue` en el elemento `#app` definido por Vite.

## Organización

```text
src/
├── App.vue
├── main.ts
├── style.css
├── assets/
├── components/
├── composables/
├── locales/
├── router/
├── services/
├── stores/
├── types/
└── views/
```

### `App.vue`

Es el layout principal de la aplicación.

- Si la ruta es `/auth`, muestra solo la vista de autenticación.
- En el resto de rutas muestra la estructura privada con `Sidebar`, `Navbar` y el contenido de `RouterView`.
- Calcula el título de página según la ruta actual.
- Gestiona la apertura del menú lateral en móvil.
- Ejecuta el cierre de sesión y redirige a `/auth`.

### `router/`

Define las rutas principales:

| Ruta | Vista | Protección |
| --- | --- | --- |
| `/` | Redirige a `/dashboard` | - |
| `/auth` | `AuthView` | Solo invitados |
| `/dashboard` | `DashboardView` | Usuario autenticado |
| `/perfil` | `PerfilView` | Usuario autenticado |
| `/vehiculos` | `VehiculosView` | Usuario autenticado |
| `/vehiculos/:matricula` | `VehiculoDetalleView` | Usuario autenticado |
| `/items` | `ItemsManagementView` | Usuario autenticado |
| `/usuarios` | `UsuariosManagementView` | Usuario autenticado y administrador |

El guard global comprueba:

- Si una ruta requiere autenticación y no hay token, redirige a `/auth`.
- Si un usuario autenticado intenta entrar en `/auth`, redirige a `/dashboard`.
- Si una ruta requiere administrador y el perfil no lo es, redirige a `/dashboard`.

### `views/`

Contiene las pantallas completas que se cargan desde el router:

| Vista | Función |
| --- | --- |
| `AuthView.vue` | Formulario de inicio de sesión. |
| `DashboardView.vue` | Panel principal operativo. |
| `PerfilView.vue` | Consulta y edición del perfil del usuario. |
| `VehiculosView.vue` | Listado y creación de vehículos. |
| `VehiculoDetalleView.vue` | Detalle de un vehículo y su checklist. |
| `ItemsManagementView.vue` | Gestión de items de checklist. |
| `UsuariosManagementView.vue` | Gestión de usuarios para administradores. |

### `components/`

Agrupa componentes reutilizables:

| Componente | Uso |
| --- | --- |
| `NavBar.vue` | Barra superior con título y datos del usuario. |
| `Sidebar.vue` | Navegación lateral y acción de logout. |
| `BaseForm.vue` | Base para formularios. |
| `BaseModal.vue` | Ventanas modales. |
| `VehicleCard.vue` | Tarjeta de vehículo. |
| `ItemList.vue` | Lista visual de items de checklist. |

### `stores/`

Pinia centraliza el estado compartido.

#### `auth.ts`

Gestiona la sesión:

- Token en `sessionStorage` con la clave `emergentory_token`.
- Usuario en `sessionStorage` con la clave `emergentory_user`.
- Estado `loading`.
- Computed `isAuthenticated`.
- Computed `fullName`.
- Acciones `login`, `logout` y `updateUser`.

#### `vehiculos.ts`

Gestiona vehículos:

- Lista de vehículos.
- Vehículo seleccionado en `selected_vehicle`.
- Carga de vehículos desde API.
- Búsqueda por matrícula.
- Creación y eliminación.
- Cómputo `totalVehiculos`.

#### `items.ts`

Gestiona operaciones sobre items:

- Crea items en una checklist.
- Modifica items existentes.
- Elimina items por `id`.
- Calcula `totalItems` recorriendo las checklists de los vehículos cargados.

### `services/`

Contiene la comunicación con la API mediante Axios.

| Servicio | Responsabilidad |
| --- | --- |
| `authService.ts` | Login, mapeo de perfil y actualización del perfil. |
| `vehiculoService.ts` | Listar, filtrar, crear y eliminar vehículos. |
| `itemService.ts` | Crear, modificar y eliminar items. |
| `userService.ts` | Listar, crear y eliminar usuarios. |

Los servicios usan actualmente la API en:

```text
http://127.0.0.1:8000
```

Las peticiones protegidas añaden la cabecera `Authorization` leyendo el token desde `sessionStorage`.

### `types/`

Define las interfaces TypeScript compartidas:

- `Perfil`
- `Usuario`
- `Item`
- `Lista`
- `Vehiculo`
- `AuthPayload`
- `SessionSummary`

Estas interfaces documentan la forma esperada de los datos que llegan desde la API y ayudan a detectar errores durante el desarrollo.

### `composables/`

Contiene lógica reutilizable basada en Composition API.

`useAuth.ts` expone:

- `isAuthenticated`
- `isSubmitting`
- `submitLogin`
- `logout`
- `isAdmin`

## Flujo de Sesión

1. El usuario introduce credenciales en `AuthView`.
2. `useAuth` llama a `authStore.login`.
3. `authStore.login` usa `loginService`.
4. `loginService` consulta `/api/users/profile/<username>/`.
5. Si las credenciales coinciden, guarda token y usuario en Pinia y `sessionStorage`.
6. El router permite acceder a las rutas privadas mientras exista token.
7. Al cerrar sesión se eliminan los datos de sesión y se redirige a `/auth`.

## Flujo de Vehículos e Items

1. Las vistas solicitan datos al store `vehiculos`.
2. El store llama a `vehiculoService`.
3. La API devuelve vehículos con su checklist.
4. Las operaciones de items usan `itemService`.
5. Cada item se crea o modifica enviando la matrícula como campo `checklist`.
6. La eliminación de items se realiza por `id`.

## Estilos

El proyecto usa Tailwind CSS 4 con el plugin de Vite. Los estilos globales están en `src/style.css`.

También se definen colores de tema:

```css
--color-brand-50
--color-brand-100
--color-brand-500
--color-brand-600
--color-brand-700
--color-ink-900
--color-sand-100
```

La interfaz usa un layout privado con fondo gris claro, barra lateral, barra superior y contenido central.

## Alias de Importación

Vite define el alias `@` apuntando a `src`, por lo que se pueden importar módulos así:

```ts
import { useAuthStore } from '@/stores/auth';
import type { Vehiculo } from '@/types';
```

## Comandos

Desde `apps/main`:

```bash
npm run dev
npm run build
npm run preview
```

`npm run dev` levanta Vite para desarrollo. `npm run build` genera la versión de producción en `dist`.
