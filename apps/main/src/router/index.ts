import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import AuthView from '@/views/AuthView.vue';
import DashboardView from '@/views/DashboardView.vue';
import PerfilView from '@/views/PerfilView.vue';
import VehiculosView from '@/views/VehiculosView.vue';
import VehiculoDetalleView from '@/views/VehiculoDetalleView.vue';
import ItemsManagementView from '@/views/ItemsManagementView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/auth', name: 'auth', component: AuthView, meta: { guestOnly: true } },
    { path: '/dashboard', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true } },
    { path: '/perfil', name: 'perfil', component: PerfilView, meta: { requiresAuth: true } },
    { path: '/vehiculos', name: 'vehiculos', component: VehiculosView, meta: { requiresAuth: true } },
    { path: '/vehiculos/:matricula', name: 'vehiculo-detalle', component: VehiculoDetalleView, meta: { requiresAuth: true } },
    { path: '/items', name: 'items', component: ItemsManagementView, meta: { requiresAuth: true } },
  ],
  scrollBehavior() {
    return { top: 0 };
  },
});

router.beforeEach((to) => {
  const authStore = useAuthStore();
  sessionStorage.setItem('emergentory_last_route', to.fullPath);

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'auth' };
  }

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: 'dashboard' };
  }

  return true;
});

export default router;
