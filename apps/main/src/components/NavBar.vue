<template>
  <header class="sticky top-0 z-30 border-b border-white/60 bg-white/90 backdrop-blur">
    <div class="flex items-center justify-between px-4 py-4 sm:px-6">
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.35em] text-brand-600">EmergenTory</p>
        <h1 class="text-lg font-semibold text-slate-900">{{ pageTitle }}</h1>
      </div>

      <div class="flex items-center gap-3">
        <button
          type="button"
          class="rounded-2xl bg-slate-900 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-slate-700 lg:hidden"
          @click="$emit('toggle-sidebar')"
        >
          Menú
        </button>

        <div class="hidden rounded-2xl border border-slate-200 bg-slate-50 px-3 py-2 sm:flex sm:items-center sm:gap-3">
          <img
            v-if="user?.perfil.avatar"
            :src="user.perfil.avatar"
            :alt="user.username"
            class="h-10 w-10 rounded-xl object-cover"
          />
          <div class="text-right">
            <p class="text-sm font-semibold text-slate-900">{{ fullName }}</p>
            <p class="text-xs text-slate-500">{{ user?.email }}</p>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import type { Usuario } from '@/types';

defineProps<{
  pageTitle: string;
  fullName: string;
  user: Usuario | null;
}>();

defineEmits<{
  (event: 'toggle-sidebar'): void;
}>();
</script>
