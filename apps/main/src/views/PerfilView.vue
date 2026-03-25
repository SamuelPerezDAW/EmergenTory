<template>
  <section v-if="user" class="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
    <article class="rounded-[2rem] bg-slate-900 p-6 text-white shadow-sm">
      <img :src="user.perfil.avatar" :alt="user.username" class="h-28 w-28 rounded-[2rem] object-cover" />
      <p class="mt-5 text-xs uppercase tracking-[0.35em] text-brand-100">Perfil</p>
      <h2 class="mt-2 text-3xl font-semibold">{{ user.first_name }} {{ user.last_name }}</h2>
      <p class="mt-2 text-slate-300">{{ user.email }}</p>
      <p class="mt-6 rounded-2xl bg-white/10 p-4 text-sm leading-6 text-slate-200">{{ user.perfil.bio }}</p>
    </article>

    <article class="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
      <p class="text-xs uppercase tracking-[0.35em] text-brand-600">Datos de usuario</p>
      <h2 class="mt-2 text-2xl font-semibold text-slate-900">Información operativa</h2>

      <dl class="mt-6 grid gap-4 sm:grid-cols-2">
        <div class="rounded-2xl bg-slate-50 p-4">
          <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Usuario</dt>
          <dd class="mt-2 text-lg font-semibold text-slate-900">{{ user.username }}</dd>
        </div>
        <div class="rounded-2xl bg-slate-50 p-4">
          <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Teléfono</dt>
          <dd class="mt-2 text-lg font-semibold text-slate-900">{{ user.perfil.telefono }}</dd>
        </div>
        <div class="rounded-2xl bg-slate-50 p-4">
          <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Rol</dt>
          <dd class="mt-2 text-lg font-semibold text-slate-900">{{ user.perfil.admin ? 'Administrador' : 'Operador' }}</dd>
        </div>
        <div class="rounded-2xl bg-slate-50 p-4">
          <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Última ruta</dt>
          <dd class="mt-2 text-lg font-semibold text-slate-900">{{ lastVisitedRoute }}</dd>
        </div>
      </dl>
    </article>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);

const lastVisitedRoute = computed(() => sessionStorage.getItem('emergentory_last_route') || '/dashboard');
</script>
