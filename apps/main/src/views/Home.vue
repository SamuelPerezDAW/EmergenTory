<template>
  <section class="dashboard">
    <header class="dashboard__header">
      <h1 class="dashboard__title">
        {{ title || 'Panel de vehículos' }}
      </h1>

      <div class="dashboard__summary">
        <span class="summary__item">
          Total: <strong>{{ totalVehicles }}</strong>
        </span>
        <span class="summary__item">
          Activos: <strong>{{ activeVehiclesCount }}</strong>
        </span>
        <span v-if="selectedVehicle" class="summary__item summary__item--highlight">
          Seleccionado: <strong>{{ selectedVehicle.name }}</strong>
        </span>
      </div>

      <div class="dashboard__filters">
        <input
          v-model="searchTerm"
          type="text"
          class="filters__search"
          placeholder="Buscar por nombre o matrícula..."
        />

        <label class="filters__checkbox">
          <input
            v-model="filters.onlyActive"
            type="checkbox"
          />
          Mostrar solo activos
        </label>
      </div>
    </header>

    <main class="dashboard__content">
      <div v-if="isLoading" class="dashboard__state dashboard__state--loading">
        Cargando vehículos...
      </div>

      <div v-else-if="error" class="dashboard__state dashboard__state--error">
        {{ error }}
      </div>

      <div v-else class="dashboard__grid">
        <VehicleCard
          v-for="vehicle in filteredVehicles"
          :key="vehicle.id"
          :vehicle="vehicle"
          :selected="vehicle.id === selectedVehicleId"
          @view-items="handleViewItems"
        >
          <!-- Slot de cabecera extra listo para personalización -->
          <template #header-extra>
            <span
              class="badge"
              :class="vehicle.active ? 'badge--success' : 'badge--muted'"
            >
              {{ vehicle.active ? 'Activo' : 'Inactivo' }}
            </span>
          </template>

          <!-- Slot de pie de tarjeta con acción principal -->
          <template #footer>
            <button
              class="btn btn--primary"
              type="button"
              @click.stop="handleViewItems(vehicle.id)"
            >
              Ver items ({{ vehicle.itemsCount ?? 0 }})
            </button>
          </template>
        </VehicleCard>

        <p v-if="!filteredVehicles.length" class="dashboard__state dashboard__state--empty">
          No se encontraron vehículos con los filtros actuales.
        </p>
      </div>
    </main>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { storeToRefs } from 'pinia';

import { useVehicleStore } from '@/stores/vehicleStore';
import VehicleCard from '@/components/VehicleCard.vue';

interface Vehicle {
  id: string;
  name: string;
  plate: string;
  active: boolean;
  itemsCount?: number;
}

const props = defineProps<{
  title?: string;
}>();

const emit = defineEmits<{
  (e: 'open-vehicle-items', payload: { vehicleId: string }): void;
}>();

const vehicleStore = useVehicleStore();
const { vehicles, isLoading, error } = storeToRefs(vehicleStore);

const searchTerm = ref<string>('');
const selectedVehicleId = ref<string | null>(null);

const filters = reactive({
  search: '',
  onlyActive: false,
});

watch(
  searchTerm,
  (value) => {
    filters.search = value.trim();
  }
);

const filteredVehicles = computed<Vehicle[]>(() => {
  const term = filters.search.toLowerCase();

  return vehicles.value
    .filter((vehicle) =>
      filters.onlyActive ? vehicle.active : true
    )
    .filter((vehicle) => {
      if (!term) return true;
      return (
        vehicle.name.toLowerCase().includes(term) ||
        vehicle.plate.toLowerCase().includes(term)
      );
    });
});

const totalVehicles = computed(() => vehicles.value.length);

const activeVehiclesCount = computed(() =>
  vehicles.value.filter((v) => v.active).length
);

const selectedVehicle = computed<Vehicle | undefined>(() =>
  vehicles.value.find((v) => v.id === selectedVehicleId.value)
);

function handleViewItems(vehicleId: string) {
  selectedVehicleId.value = vehicleId;
  emit('open-vehicle-items', { vehicleId });
}

onMounted(() => {
  if (!vehicles.value.length) {
    vehicleStore.fetchVehicles();
  }
});
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.75rem 1.5rem;
}

.dashboard__header {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.dashboard__title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
}

.dashboard__summary {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  font-size: 0.95rem;
  color: #4b5563;
}

.summary__item--highlight {
  color: #111827;
}

.dashboard__filters {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem;
}

.filters__search {
  flex: 1 1 220px;
  min-width: 0;
  padding: 0.55rem 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid #d1d5db;
  font-size: 0.95rem;
}

.filters__search:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 1px rgba(37, 99, 235, 0.15);
}

.filters__checkbox {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.9rem;
  color: #4b5563;
}

.dashboard__content {
  min-height: 200px;
}

.dashboard__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}

.dashboard__state {
  font-size: 0.95rem;
  color: #6b7280;
}

.dashboard__state--loading {
  color: #2563eb;
}

.dashboard__state--error {
  color: #b91c1c;
}

.dashboard__state--empty {
  color: #6b7280;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.15rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge--success {
  background-color: #dcfce7;
  color: #166534;
}

.badge--muted {
  background-color: #e5e7eb;
  color: #4b5563;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  padding: 0.5rem 0.85rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background-color 0.15s ease, box-shadow 0.15s ease, transform 0.05s ease;
}

.btn--primary {
  background-color: #2563eb;
  color: #ffffff;
}

.btn--primary:hover {
  background-color: #1d4ed8;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3);
}

.btn:active {
  transform: translateY(1px);
  box-shadow: none;
}
</style>