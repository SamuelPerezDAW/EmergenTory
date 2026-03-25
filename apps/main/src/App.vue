<template>
  <RouterView v-if="route.path === '/auth'" />

  <div v-else class="min-h-screen bg-slate-100">
    <div class="flex min-h-screen">
      <Sidebar :open="sidebarOpen" :session-text="sessionText" @close="sidebarOpen = false" @logout="handleLogout" />

      <div v-if="sidebarOpen" class="fixed inset-0 z-30 bg-slate-950/35 lg:hidden" @click="sidebarOpen = false" />

      <main class="min-w-0 flex-1">
        <Navbar
          :page-title="pageTitle"
          :full-name="authStore.fullName"
          :user="authStore.user"
          @toggle-sidebar="sidebarOpen = !sidebarOpen"
        />
        <div class="px-4 py-6 sm:px-6">
          <RouterView />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { RouterView, useRoute, useRouter } from 'vue-router';
import Navbar from './components/NavBar.vue';
import Sidebar from '@/components/Sidebar.vue';
import { useAuthStore } from '@/stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const sidebarOpen = ref(false);

const pageTitle = computed(() => {
  const labels: Record<string, string> = {
    '/dashboard': 'Dashboard operativo',
    '/perfil': 'Perfil de usuario',
    '/vehiculos': 'Vehículos',
    '/items': 'Gestión de items',
  };

  if (route.path.startsWith('/vehiculos/')) {
    return 'Detalle de vehículo';
  }

  return labels[route.path] ?? 'EmergenTory';
});

const sessionText = computed(() => sessionStorage.getItem('selected_vehicle') || 'Sin vehículo seleccionado');

const handleLogout = async () => {
  authStore.logout();
  await router.push('/auth');
};
</script>
