<template>
  <section class="space-y-6">
    <div class="grid gap-4 md:grid-cols-3">
      <div class="rounded-[2rem] bg-slate-900 p-6 text-white shadow-sm">
        <p class="text-xs uppercase tracking-[0.35em] text-brand-100">Vehículos</p>
        <p class="mt-4 text-4xl font-semibold">{{ totalVehiculos }}</p>
        <p class="mt-2 text-sm text-slate-300">Unidades enlazadas a listas de control.</p>
      </div>
      <div class="rounded-[2rem] bg-white p-6 shadow-sm">
        <p class="text-xs uppercase tracking-[0.35em] text-brand-600">Items activos</p>
        <p class="mt-4 text-4xl font-semibold text-slate-900">{{ activeItems }}</p>
        <p class="mt-2 text-sm text-slate-500">Material disponible para salida inmediata.</p>
      </div>
      <div class="rounded-[2rem] bg-white p-6 shadow-sm">
        <p class="text-xs uppercase tracking-[0.35em] text-brand-600">Última sesión</p>
        <p class="mt-4 text-xl font-semibold text-slate-900">{{ sessionSummary.lastVehicleMatricula || 'Sin selección' }}</p>
        <p class="mt-2 text-sm text-slate-500">{{ sessionSummary.lastVisitedRoute || 'No hay ruta registrada' }}</p>
      </div>
    </div>

    <div class="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
      <section class="rounded-[2rem] border border-slate-200 bg-white p-5 shadow-sm">
        <div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p class="text-xs uppercase tracking-[0.35em] text-brand-600">Monitoreo</p>
            <h2 class="mt-2 text-2xl font-semibold text-slate-900">Flota destacada</h2>
          </div>
          <RouterLink to="/vehiculos" class="rounded-2xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white">
            Ver todos los vehículos
          </RouterLink>
        </div>

        <div class="mt-5 grid gap-4 lg:grid-cols-2">
          <VehicleCard
            v-for="vehicle in featuredVehiculos"
            :key="vehicle.matricula"
            :vehicle="vehicle"
            @select="goToVehicle"
            @manage-items="goToItems"
          />
        </div>
      </section>

      <section class="rounded-[2rem] border border-slate-200 bg-white p-5 shadow-sm">
        <p class="text-xs uppercase tracking-[0.35em] text-brand-600">Actividad reciente</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-900">Resumen operativo</h2>

        <div class="mt-5 space-y-4">
          <div
            v-for="vehicle in vehiculos"
            :key="vehicle.matricula"
            class="rounded-2xl bg-slate-50 p-4"
          >
            <div class="flex items-center justify-between gap-3">
              <div>
                <p class="font-semibold text-slate-900">{{ vehicle.matricula }}</p>
                <p class="text-sm text-slate-500">{{ vehicle.categoria }}</p>
              </div>
              <span class="rounded-full bg-white px-3 py-1 text-xs font-semibold text-slate-600">
                {{ vehicle.lista.items.filter((item) => item.activo).length }} activos
              </span>
            </div>
          </div>
        </div>
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import VehicleCard from '@/components/VehicleCard.vue';
import { useVehiculos } from '@/composables/useVehiculos';
import type { SessionSummary } from '@/types';

const router = useRouter();
const { vehiculos, activeItems } = useVehiculos();

const featuredVehiculos = computed(() => vehiculos.value.slice(0, 2));
const totalVehiculos = computed(() => vehiculos.value.length);
const sessionSummary = reactive<SessionSummary>({
  lastVehicleMatricula: sessionStorage.getItem('selected_vehicle'),
  lastVisitedRoute: sessionStorage.getItem('emergentory_last_route'),
});

const goToVehicle = async (matricula: string) => {
  sessionSummary.lastVehicleMatricula = matricula;
  sessionStorage.setItem('selected_vehicle', matricula);
  await router.push(`/vehiculos/${matricula}`);
};

const goToItems = async (matricula: string) => {
  sessionStorage.setItem('selected_vehicle', matricula);
  await router.push('/items');
};
</script>
