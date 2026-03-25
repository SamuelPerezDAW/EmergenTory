<template>
  <section class="space-y-6">
    <div class="flex flex-col gap-4 rounded-[2rem] border border-slate-200 bg-white p-5 shadow-sm lg:flex-row lg:items-end lg:justify-between">
      <div>
        <p class="text-xs uppercase tracking-[0.35em] text-brand-600">Inventario rodante</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-900">Lista de vehículos</h2>
      </div>

      <div class="grid gap-3 sm:grid-cols-2">
        <input
          v-model="filters.search"
          placeholder="Buscar matrícula, marca o modelo"
          class="rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-brand-500"
        />
        <select
          v-model="filters.categoria"
          class="rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-brand-500"
        >
          <option v-for="categoria in categorias" :key="categoria" :value="categoria">{{ categoria }}</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="rounded-[2rem] bg-white p-8 text-center text-slate-500 shadow-sm">Cargando vehículos...</div>

    <div v-else class="grid gap-5 xl:grid-cols-2">
      <VehicleCard
        v-for="vehicle in filteredVehiculos"
        :key="vehicle.matricula"
        :vehicle="vehicle"
        @select="handleSelect"
        @manage-items="handleManageItems"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import VehicleCard from '@/components/VehicleCard.vue';
import { useVehiculos } from '@/composables/useVehiculos';

const router = useRouter();
const { loading, filters, categorias, filteredVehiculos, selectVehiculo } = useVehiculos();

const handleSelect = async (matricula: string) => {
  selectVehiculo(matricula);
  await router.push(`/vehiculos/${matricula}`);
};

const handleManageItems = async (matricula: string) => {
  selectVehiculo(matricula);
  await router.push('/items');
};
</script>
