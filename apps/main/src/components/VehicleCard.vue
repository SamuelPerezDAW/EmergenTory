<template>
  <article class="vehicle-card">
    <header class="vehicle-card__header">
      <h2 class="vehicle-card__title">
        {{ vehicle.name }}
      </h2>

      <div class="vehicle-card__counters">
        <span class="badge badge--pending">
          Pendientes: {{ pendingItemsCount }}
        </span>
        <span class="badge badge--completed">
          Completados: {{ completedItemsCount }}
        </span>
        <span class="badge badge--total">
          Total: {{ totalItems }}
        </span>
      </div>
    </header>

    <section class="vehicle-card__body">
      <!-- Lista simple para mostrar la reactividad de ref + computed -->
      <ul class="vehicle-card__items">
        <li
          v-for="item in itemsState"
          :key="item.id"
          class="vehicle-card__item"
        >
          <label class="vehicle-card__item-label">
            <input
              type="checkbox"
              v-model="item.completed"
            />
            <span :class="{ 'vehicle-card__item--done': item.completed }">
              {{ item.label }}
            </span>
          </label>
        </li>
      </ul>

      <!-- Slot por defecto para contenido adicional -->
      <slot />
    </section>

    <footer class="vehicle-card__footer">
      <!-- Slot de acciones adicionales -->
      <slot name="actions" />

      <button
        type="button"
        class="btn btn--primary"
        @click="handleSelect"
      >
        Seleccionar vehículo
      </button>
    </footer>
  </article>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';

interface VehicleItem {
  id: string | number;
  label: string;
  completed: boolean;
}

interface Vehicle {
  id: string | number;
  name: string;
  items: VehicleItem[];
}

const props = defineProps<{
  vehicle: Vehicle;
}>();

const emit = defineEmits<{
  (e: 'selectVehicle', vehicleId: string | number): void;
}>();

// ref + reactividad local de items para mostrar cambios en tiempo real
const itemsState = ref<VehicleItem[]>([...props.vehicle.items]);

// Sincronizar si el vehículo cambia desde el padre
watch(
  () => props.vehicle.items,
  (newItems) => {
    itemsState.value = [...newItems];
  },
  { deep: true }
);

// computed para contar items
const totalItems = computed(() => itemsState.value.length);

const completedItemsCount = computed(() =>
  itemsState.value.filter((item) => item.completed).length
);

const pendingItemsCount = computed(() =>
  Math.max(totalItems.value - completedItemsCount.value, 0)
);

function handleSelect() {
  emit('selectVehicle', props.vehicle.id);
}
</script>

<style scoped>
.vehicle-card {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
  background-color: #ffffff;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
}

.vehicle-card__header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.vehicle-card__title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  color: #111827;
}

.vehicle-card__counters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  font-size: 0.8rem;
}

.vehicle-card__body {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.vehicle-card__items {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.vehicle-card__item {
  font-size: 0.9rem;
}

.vehicle-card__item-label {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
}

.vehicle-card__item--done {
  text-decoration: line-through;
  color: #6b7280;
}

.vehicle-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.25rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  font-weight: 500;
}

.badge--pending {
  background-color: #fef3c7;
  color: #92400e;
}

.badge--completed {
  background-color: #dcfce7;
  color: #166534;
}

.badge--total {
  background-color: #e5e7eb;
  color: #374151;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.45rem 0.9rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: background-color 0.15s ease, box-shadow 0.15s ease,
    transform 0.05s ease;
}

.btn--primary {
  background-color: #2563eb;
  color: #ffffff;
}

.btn--primary:hover {
  background-color: #1d4ed8;
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
}

.btn--primary:active {
  transform: translateY(1px);
  box-shadow: none;
}
</style>