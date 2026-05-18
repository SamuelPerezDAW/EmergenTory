---
icon: lucide/palette
---

# Diseño Web

La interfaz de EmergenTory está diseñada como una herramienta operativa para gestionar vehículos de emergencia, usuarios y listas de revisión. El diseño prioriza claridad, lectura rápida y acciones directas.

## Diseño Responsive

La aplicación se adapta a distintos tamaños de pantalla mediante utilidades responsive de Tailwind CSS.

El layout principal usa una estructura flexible:

- En escritorio muestra navegación lateral, barra superior y contenido principal.
- En móvil mantiene el contenido en una sola columna.
- El menú lateral se oculta y puede abrirse sobre el contenido.
- Las rejillas de tarjetas cambian de una columna a varias columnas según el ancho disponible.
- Los formularios mantienen campos apilados en móvil para facilitar la interacción táctil.

Ejemplos aplicados:

```html
<div class="grid gap-4 md:grid-cols-3">
```

```html
<div class="mx-auto grid min-h-screen max-w-7xl items-center gap-10 px-4 py-10 lg:grid-cols-[1.05fr_0.95fr] lg:px-8">
```

Con esto, la aplicación puede usarse tanto en equipos de escritorio como en tablets o móviles.

## Accesibilidad WCAG

La interfaz sigue criterios básicos de accesibilidad alineados con WCAG:

| Criterio | Aplicación en EmergenTory |
| --- | --- |
| Contraste | Se usan textos oscuros sobre fondos claros y textos claros sobre fondos oscuros. |
| Jerarquía visual | Los títulos, etiquetas y acciones principales tienen tamaños y pesos diferenciados. |
| Formularios etiquetados | Los campos de login, perfil, usuarios e items usan etiquetas visibles. |
| Estados de foco | Los inputs tienen estilos `focus` para indicar el campo activo. |
| Navegación consistente | La barra lateral mantiene rutas estables para las secciones principales. |
| Mensajes de error | Las operaciones muestran errores en texto visible, no solo mediante color. |

Ejemplo de campo accesible:

```html
<label class="space-y-2 text-sm font-medium text-slate-700">
  <span>Contraseña</span>
  <input type="password" class="focus:border-brand-500" />
</label>
```

!!! note "Mejora futura"

    Para una auditoría WCAG completa conviene añadir pruebas con herramientas como Lighthouse, axe DevTools o Playwright con comprobaciones de accesibilidad. También sería recomendable revisar navegación completa por teclado y atributos `aria-*` en modales y menús.

## Framework CSS

El frontend usa Tailwind CSS 4 integrado con Vite mediante `@tailwindcss/vite`.

Dependencias principales:

```json
{
  "@tailwindcss/vite": "^4.1.18",
  "tailwindcss": "^4.1.18"
}
```

El archivo global de estilos es:

```text
apps/main/src/style.css
```

En él se importa Tailwind y se definen variables de color del tema:

```css
@import "tailwindcss";

@theme {
  --color-brand-50: #eef8f5;
  --color-brand-100: #d4eee6;
  --color-brand-500: #167c68;
  --color-brand-600: #0e6655;
  --color-brand-700: #0c5144;
  --color-ink-900: #102127;
  --color-sand-100: #f4efe8;
}
```

Tailwind permite mantener estilos consistentes sin crear CSS específico para cada componente.

## Gama de Color

La gama de color está pensada para una aplicación de emergencias e inventario operativo:

| Color | Uso |
| --- | --- |
| Verde `brand` | Identidad principal, botones y estados activos. |
| Gris pizarra `slate` | Fondos, texto principal y estructura de panel. |
| Blanco | Tarjetas, formularios y superficies de lectura. |
| Arena suave `sand` | Apoyo visual en fondos y zonas secundarias. |
| Rojo | Errores y avisos de validación. |

El verde principal transmite control, disponibilidad y estado operativo sin saturar la interfaz. Los grises y blancos mantienen una lectura limpia para tareas repetitivas de gestión.

## Usabilidad

La aplicación cumple criterios de usabilidad orientados a un entorno de trabajo:

- La navegación principal está agrupada en secciones claras: dashboard, perfil, vehículos, items y usuarios.
- Las acciones frecuentes están visibles en cada pantalla.
- Los formularios usan campos reconocibles y mensajes de error directos.
- El dashboard resume vehículos, items activos y última sesión.
- Los vehículos se representan mediante tarjetas para facilitar identificación rápida.
- Las rutas protegidas redirigen automáticamente según el estado de sesión.
- Los usuarios administradores tienen acceso a gestión de usuarios, mientras que el resto conserva una navegación más limitada.

## Componentes de Interfaz

La interfaz se organiza con componentes reutilizables:

| Componente | Función de diseño |
| --- | --- |
| `NavBar.vue` | Muestra contexto de página y usuario activo. |
| `Sidebar.vue` | Centraliza la navegación principal. |
| `BaseForm.vue` | Homogeneiza formularios. |
| `BaseModal.vue` | Mantiene diálogos consistentes. |
| `VehicleCard.vue` | Resume información de vehículos. |
| `ItemList.vue` | Presenta items de checklist de forma escaneable. |

Esta organización reduce duplicación visual y mantiene coherencia entre pantallas.

## Conclusión

EmergenTory usa una interfaz responsive, apoyada en Tailwind CSS, con una paleta sobria y apropiada para una aplicación operativa. La estructura de navegación, los componentes reutilizables y los flujos de sesión ayudan a que la aplicación sea usable y fácil de mantener.
