<template>
  <aside
    :class="[
      'fixed inset-y-0 left-0 z-40 flex w-72 flex-col bg-ink-900 p-5 text-white shadow-2xl transition-transform lg:static lg:translate-x-0',
      open ? 'translate-x-0' : '-translate-x-full',
    ]"
  >
    <div class="mb-8 flex items-center justify-between">
      <div>
        <p class="text-xs uppercase tracking-[0.35em] text-brand-100">Centro de mando</p>
        <h2 class="mt-2 text-2xl font-semibold">Flota operativa</h2>
      </div>
      <button type="button" class="rounded-xl border border-white/15 px-3 py-2 text-sm lg:hidden" @click="$emit('close')">
        Cerrar
      </button>
    </div>

    <nav class="space-y-2">
      <RouterLink
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        class="block rounded-2xl px-4 py-3 text-sm font-medium transition"
        :class="route.path === item.to ? 'bg-brand-500 text-white' : 'text-slate-300 hover:bg-white/10 hover:text-white'"
        @click="$emit('close')"
      >
        {{ item.label }}
      </RouterLink>
    </nav>

    <div class="mt-auto rounded-3xl bg-white/8 p-4">
      <p class="text-xs uppercase tracking-[0.25em] text-brand-100">Sesión</p>
      <p class="mt-2 text-sm text-slate-300">{{ sessionText }}</p>
      <button
        type="button"
        class="mt-4 w-full rounded-2xl bg-white px-4 py-3 text-sm font-semibold text-ink-900 transition hover:bg-sand-100"
        @click="$emit('logout')"
      >
        Cerrar sesión
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router';
import { computed } from 'vue';
import { useAuthStore } from '@/stores/auth';

defineProps<{
  open: boolean;
  sessionText: string | string[];
}>();

defineEmits<{
  (event: 'close'): void;
  (event: 'logout'): void;
}>();

const route = useRoute();
const authStore = useAuthStore();

const items = computed(() => [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/perfil', label: 'Perfil' },
  { to: '/vehiculos', label: 'Vehículos' },
  { to: '/items', label: 'Items' },
  ...(authStore.user?.perfil.admin ? [{ to: '/usuarios', label: 'Usuarios' }] : []),
]);
</script>
