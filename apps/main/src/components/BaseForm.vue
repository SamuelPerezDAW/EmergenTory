<template>
  <form class="space-y-5 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm" @submit.prevent="$emit('submit')">
    <div class="space-y-1">
      <p v-if="eyebrow" class="text-xs font-semibold uppercase tracking-[0.35em] text-brand-600">{{ eyebrow }}</p>
      <h3 class="text-2xl font-semibold text-slate-900">{{ title }}</h3>
      <p v-if="description" class="text-sm text-slate-500">{{ description }}</p>
    </div>

    <slot />

    <div class="flex items-center justify-between gap-3">
      <slot name="actions">
        <button
          type="submit"
          class="w-full rounded-2xl bg-brand-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-brand-700"
        >
          {{ submitLabel }}
        </button>
      </slot>
    </div>
  </form>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    title: string;
    submitLabel?: string;
    description?: string;
    eyebrow?: string;
  }>(),
  {
    submitLabel: 'Guardar',
    description: '',
    eyebrow: '',
  },
);

defineEmits<{
  (event: 'submit'): void;
}>();
</script>
