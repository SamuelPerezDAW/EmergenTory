<template>
  <article class="rounded-[2rem] border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-lg">
    <div class="flex items-start justify-between gap-4">
      <div>
        <p class="text-md font-semibold tracking-[0.3em]">Categoría: <b class="text-brand-600 uppercase text-base">{{ categorias.find((cat) => cat.clave === vehicle.categoria)?.valor ?? 'NaN' }}</b></p>
        <p class="mt-1 text-sm text-slate-500">Matrícula: {{ vehicle.matricula }}</p>
        <h3 class="mt-2 text-md font-semibold text-slate-900">
          Marca: 
          <b class="rounded-full bg-brand-50 px-3 py-1 text-base font-semibold text-brand-700">{{ vehicle.marca }}</b> 
          Modelo: 
          <b class="rounded-full bg-brand-50 px-3 py-1 text-base font-semibold text-brand-700">{{ vehicle.modelo }}</b>
        </h3>
      </div>
      <span class="rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700">
        {{ activeCount }}/{{ totalCount }} items activos
      </span>
    </div>

    <div class="mt-5 grid grid-cols-3 gap-3 text-center">
      <div class="rounded-2xl bg-slate-50 px-3 py-3">
        <p class="text-xs uppercase tracking-[0.2em] text-slate-500">Última Lista</p>
        <p class="mt-2 text-lg font-semibold text-slate-900">#{{ vehicle.lista[0].id }}</p>
      </div>
      <div class="rounded-2xl bg-slate-50 px-3 py-3">
        <p class="text-xs uppercase tracking-[0.2em] text-slate-500">Items Totales</p>
        <p class="mt-2 text-lg font-semibold text-slate-900">{{ totalCount }}</p>
      </div>
      <div class="rounded-2xl bg-slate-50 px-3 py-3">
        <p class="text-xs uppercase tracking-[0.2em] text-slate-500">Items Inactivos Totales</p>
        <p class="mt-2 text-lg font-semibold text-amber-600">{{ inactiveCount }}</p>
      </div>
    </div>

    <div class="mt-5 flex flex-wrap items-center gap-3">
      <button
        type="button"
        class="cursor-pointer rounded-2xl bg-slate-800 border border-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-950"
        @click="$emit('select', vehicle.matricula)"
      >
        Ver detalle
      </button>
      <button
        type="button"
        class="cursor-pointer rounded-2xl border border-slate-200 px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-brand-200 hover:bg-brand-50"
        @click="$emit('manage-items', vehicle.matricula)"
      >
        Gestionar items
      </button>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { Vehiculo } from '@/types';
import { useVehiculos } from '@/composables/useVehiculos';

const { categorias } = useVehiculos();

const props = defineProps<{
  vehicle: Vehiculo;
}>();

defineEmits<{
  (event: 'select', matricula: string): void;
  (event: 'manage-items', matricula: string): void;
}>();

const totalCount = computed(() => {
  let count = 0
  props.vehicle.lista.forEach((checklist) => {
    count += checklist.items.length
  })
  return count
});

const activeCount = computed(() => {
  let count = 0
  props.vehicle.lista.forEach((checklist) => {
    count += checklist.items.filter((item) => item.activo).length
  })
  return count
});

const inactiveCount = computed(() => totalCount.value - activeCount.value);
</script>
