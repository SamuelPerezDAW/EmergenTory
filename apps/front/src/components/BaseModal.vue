<template>
  <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/55 px-4">
    <div class="w-full max-w-lg rounded-[2rem] bg-white p-6 shadow-2xl">
      <div class="flex items-start justify-between gap-4">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.35em] text-brand-600">{{ eyebrow }}</p>
          <h3 class="mt-2 text-2xl font-semibold text-slate-900">{{ title }}</h3>
        </div>
        <button type="button" class="rounded-2xl cursor-pointer bg-slate-100 px-3 py-2 text-sm font-medium text-slate-600" @click="$emit('close')">
          Cerrar
        </button>
      </div>

      <div class="mt-5">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    open: boolean;
    title: string;
    eyebrow?: string;
  }>(),
  {
    eyebrow: 'Editor',
  },
);

defineEmits<{
  (event: 'close'): void;
}>();
</script>
