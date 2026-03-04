<template>
  <header class="sticky top-0 z-50 bg-black/80 backdrop-blur border-b border-white/10">
    <div class="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">

      <!-- IZQUIERDA -->
      <RouterLink to="/" class="font-semibold">
        Besay González-Benavides García
      </RouterLink>

      <!-- DERECHA (ESCRITORIO) -->
      <nav class="hidden sm:flex gap-6 text-sm text-white/70">
        <RouterLink to="/#sobre-mi" class="hover:text-white">Sobre mí</RouterLink>
        <RouterLink to="/#proyectos" class="hover:text-white">Proyectos</RouterLink>
        <RouterLink to="/#contacto" class="hover:text-white">Contacto</RouterLink>
        <RouterLink to="/#habilidades" class="hover:text-white">Habilidades</RouterLink>
        <RouterLink to="/#experiencia" class="hover:text-white">Experiencia</RouterLink>
      </nav>

      <!-- BOTÓN MÓVIL -->
      <button
        class="sm:hidden rounded-lg border border-white/15 px-3 py-2 text-sm text-white/80"
        @click="isOpen = !isOpen"
      >
        ☰
      </button>
    </div>

    <!-- MENÚ MÓVIL -->
    <div v-if="isOpen" class="sm:hidden border-t border-white/10">
      <nav class="max-w-4xl mx-auto px-6 py-4 flex flex-col gap-3 text-sm text-white/70">
        <RouterLink to="/#sobre-mi" @click="closeMenu">Sobre mí</RouterLink>
        <RouterLink to="/#proyectos" @click="closeMenu">Proyectos</RouterLink>
        <RouterLink to="/#contacto" @click="closeMenu">Contacto</RouterLink>
        <RouterLink to="/#habilidades" @click="closeMenu">Habilidades</RouterLink>
        <RouterLink to="/#experiencia" @click="closeMenu">Experiencia</RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const isOpen = ref(false)
const closeMenu = () => (isOpen.value = false)
</script>
