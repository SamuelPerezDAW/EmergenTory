<script setup lang="ts">
import type { Habilidad } from '../interfaces/Habilidad'

defineProps<Habilidad>()
const logos: Record<string, string> = {
  vue: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 261.76 226.69" class="w-6 h-6"><path fill="#41B883" d="M130.88 0L0 226.69h261.76L130.88 0z"/><path fill="#35495E" d="M130.88 0l130.88 226.69H130.88L0 226.69z"/></svg>`,
  tailwind: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" class="w-6 h-6"><path fill="#38B2AC" d="M24 0c-13.254 0-24 10.746-24 24s10.746 24 24 24 24-10.746 24-24S37.254 0 24 0zm0 44C12.954 44 4 35.046 4 24S12.954 4 24 4s20 8.954 20 20-8.954 20-20 20z"/><path fill="#38B2AC" d="M24 10c-7.732 0-14 6.268-14 14 0 7.732 6.268 14 14 14 7.732 0 14-6.268 14-14 0-7.732-6.268-14-14-14zm0 24c-5.523 0-10-4.477-10-10s4.477-10 10-10 10 4.477 10 10-4.477 10-10 10z"/></svg>`
}
</script>

<template>
  <article class="rounded-xl border border-white/10 bg-white/5 p-5">
    <div class="flex items-center gap-3">
      <span v-html="logos[logo.toLowerCase()] || ''" class="w-6 h-6"></span>
      <h3 class="font-semibold">{{ name }}</h3>
    </div>

    <p class="mt-2 text-sm text-white/70">
      {{ description }}
    </p>

    <!-- Nivel gráfico -->
    <div class="mt-3 flex gap-1">
      <span
        v-for="n in 5"
        :key="n"
        class="h-2 w-6 rounded"
        :class="n <= level ? 'bg-green-400' : 'bg-white/20'"
      />
    </div>
  </article>
</template>
