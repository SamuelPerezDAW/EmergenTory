<template>
  <section class="space-y-6">
    <div class="flex flex-col gap-4 rounded-4xl border border-slate-200 bg-white p-5 shadow-sm lg:flex-row lg:items-end lg:justify-between">
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
          <option v-for="categoria in categorias" :key="categoria.clave" :value="categoria.clave">{{ categoria.valor }}</option>
        </select>
      </div>
    </div>

    <div
      @click="modalOpen = true"
      v-if="isAdmin"
      class="flex flex-row items-center gap-2 w-fit cursor-pointer hover:text-white hover:border-brand-600 transitioncursor-pointer rounded-2xl bg-slate-800 border border-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-950"
    >
      <span class="leading-none text-2xl">＋</span>
      <span class="leading-none">Añadir Vehículo</span>
    </div>

    <div v-if="loading" class="rounded-4xl bg-white p-8 text-center text-slate-500 shadow-sm">Cargando vehículos...</div>

    <div v-else class="grid gap-5 xl:grid-cols-2">
      <VehicleCard
        v-for="vehicle in filteredVehiculos"
        :key="vehicle.matricula"
        :vehicle="vehicle"
        @select="handleSelect"
        @manage-items="handleManageItems"
      />
    </div>
    <BaseModal :open="modalOpen" title="Crear Vehiculo" eyebrow="Gestión" @close="closeModal">
      <div class="space-y-4">
        <label title="Matrícula" class="block space-y-2 text-sm font-medium text-slate-700">
          <span>Matrícula</span>
          <input v-model="vehicleToCreate.matricula" class="w-full rounded-2xl border border-slate-200 px-4 py-3" />
        </label>
        <label title="Marca" class="block space-y-2 text-sm font-medium text-slate-700">
          <span>Marca</span>
          <input v-model="vehicleToCreate.marca" class="w-full rounded-2xl border border-slate-200 px-4 py-3" />
        </label>
        <label title="Modelo" class="block space-y-2 text-sm font-medium text-slate-700">
          <span>Modelo</span>
          <input v-model="vehicleToCreate.modelo" class="w-full rounded-2xl border border-slate-200 px-4 py-3" />
        </label>
        <label title="Categoría" class="block space-y-2 text-sm font-medium text-slate-700">
          <span>Categoría</span>
          <input v-model="vehicleToCreate.categoria" class="w-full rounded-2xl border border-slate-200 px-4 py-3" />
        </label>
        <select
          v-model="filters.categoria"
          title="Categoría"
          class="rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-brand-500"
        >
          <option v-for="categoria in categorias" :title="categoria.valor" :key="categoria.clave" :value="categoria.clave">{{ categoria.valor }}</option>
        </select>
        <button type="button" class="w-full cursor-pointer rounded-2xl bg-brand-600 px-4 py-3 text-sm font-semibold text-white" @click="saveVehicle">
          Guardar cambios
        </button>
      </div>
    </BaseModal>
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import VehicleCard from '@/components/VehicleCard.vue';
import { useVehiculos } from '@/composables/useVehiculos';
import { isAdmin } from '@/composables/useAuth';
import BaseModal from '@/components/BaseModal.vue';
import { reactive, ref } from 'vue';
import { Vehiculo } from '@/types';

const router = useRouter();
const { loading, filters, categorias, filteredVehiculos, selectVehiculo } = useVehiculos();
const modalOpen = ref<boolean>(false);

let vehicleToCreate = reactive<Vehiculo>({
  matricula: '',
  marca: '',
  modelo: '',
  categoria: '',
  lista: [],
});

const closeModal = async () => {
  modalOpen.value = false;
  vehicleToCreate = {
    matricula: '',
    marca: '',
    modelo: '',
    categoria: '',
    lista: [],
  }
};

const saveVehicle = () => {

}

const handleSelect = async (matricula: string) => {
  selectVehiculo(matricula);
  await router.push(`/vehiculos/${matricula}`);
};

const handleManageItems = async (matricula: string) => {
  selectVehiculo(matricula);
  await router.push('/items');
};
</script>
