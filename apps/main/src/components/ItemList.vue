<template>
  <section class="rounded-[2rem] border border-slate-200 bg-white p-5 shadow-sm">
    <div class="mb-5 flex items-center justify-between gap-3">
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.35em] text-brand-600">Checklist</p>
        <h3 class="mt-2 text-xl font-semibold text-slate-900">{{ title }}</h3>
      </div>
      <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">{{ items.length }} registros</span>
    </div>

    <div class="space-y-3">
      <article
        v-for="item in items"
        :key="item.id"
        class="flex flex-col gap-3 rounded-2xl border border-slate-200 p-4 sm:flex-row sm:items-center sm:justify-between"
      >
        <div class="flex items-center gap-3">
          <span
            class="inline-flex h-10 w-10 items-center justify-center rounded-2xl text-2xl font-bold"
            :class="item.activo ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'"
          >
            {{ item.activo ? '✔' : '✖' }}
          </span>
          <div>
            <p class="font-semibold text-slate-900">{{ item.nombre }}</p>
            <p class="text-sm text-slate-500">{{ item.activo ? 'Operativo' : 'Revisión pendiente' }}</p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button
            type="button"
            class="rounded-xl border border-slate-200 px-3 py-2 text-sm font-medium text-slate-700"
            @click="$emit('edit', item)"
          >
            Editar
          </button>
          <button
            type="button"
            class="rounded-xl bg-rose-50 px-3 py-2 text-sm font-medium text-rose-700"
            @click="$emit('remove', item.id)"
          >
            Eliminar
          </button>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Item } from '@/types';

defineProps<{
  title: string;
  items: Item[];
}>();

defineEmits<{
  (event: 'edit', item: Item): void;
  (event: 'remove', itemId: number): void;
}>();
</script>
