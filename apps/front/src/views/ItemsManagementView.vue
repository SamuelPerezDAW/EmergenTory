<template>
  <section class="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
    <BaseForm
      title="Gestión de items"
      description="Crea, actualiza y elimina material vinculado al vehículo seleccionado en sesión."
      submit-label="Guardar item"
      eyebrow="Inventario"
      @submit="handleSubmit"
    >
      <label class="space-y-2 text-sm font-medium text-slate-700">
        <span>Vehículo</span>
        <select
          v-model="selectedMatricula"
          class="w-full rounded-2xl cursor-pointer border border-slate-200 px-4 py-3 outline-none focus:border-brand-500"
        >
          <option v-for="vehicle in vehiculosStore.vehiculos" :key="vehicle.matricula" :value="vehicle.matricula" class="cursor-pointer">
            {{ vehicle.matricula }} · {{ vehicle.marca }} {{ vehicle.modelo }}
          </option>
        </select>
      </label>

      <label class="space-y-2 text-sm font-medium text-slate-700">
        <span>Nombre del item</span>
        <input v-model="form.nombre" placeholder="Introduce el nombre del item..." class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500 placeholder-slate-700/50" />
      </label>

      <label class="flex items-center gap-3 cursor-pointer rounded-2xl bg-slate-50 px-4 py-3 text-sm font-medium text-slate-700">
        <input v-model="form.activo" type="checkbox" />
        Item operativo
      </label>

      <template #actions>
        <span class="w-full flex flex-col gap-2 items-center">
          <button
            type="submit"
            v-bind:disabled="disableSubmit"
            v-bind:class="{
              'cursor-pointer': !disableSubmit,
              'cursor-not-allowed': disableSubmit,
              'bg-brand-600/50': disableSubmit,
              'bg-brand-600': !disableSubmit,
              'hover:bg-brand-600/50': disableSubmit,
              'hover:bg-brand-700': !disableSubmit,
            }"
            class="w-full rounded-2xl bg-brand-600 px-4 py-3 text-sm font-semibold text-white transition "
          >
            {{ editingId ? 'Actualizar item' : 'Crear item' }}
          </button>
          <div
            @click="resetForm"
            class="w-fit rounded-2xl cursor-pointer text-slate-700 border-slate-700 hover:bg-rose-400 px-4 py-3 border-1 text-sm font-semibold hover:text-white hover:border-rose-400 transition "
          >
            Limpiar información
          </div>

        </span>
      </template>
    </BaseForm>

    <ItemList title="Items del vehículo en sesión" :items="currentItems" @edit="startEdit" @changeItemStatus="changeItemStatus" @remove="removeItem" />
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import BaseForm from '@/components/BaseForm.vue';
import ItemList from '@/components/ItemList.vue';
import { useItemsStore } from '@/stores/items';
import { useVehiculosStore } from '@/stores/vehiculos';

const vehiculosStore = useVehiculosStore();
const itemsStore = useItemsStore();

const selectedMatricula = ref(sessionStorage.getItem('selected_vehicle') || '');
const editingId = ref<number | null>(null);
const form = reactive({
  nombre: '',
  activo: false,
});

const disableSubmit = computed(() => form.nombre == '' ? true : false);

const currentVehiculo = computed(
  () => vehiculosStore.vehiculos.find((vehiculo) => vehiculo.matricula === selectedMatricula.value) ?? null,
);
const currentItems = computed(() => currentVehiculo.value?.lista[0].items ?? []);

watch(selectedMatricula, (value) => {
  if (value) {
    vehiculosStore.selectVehiculo(value);
  }
});

const resetForm = () => {
  editingId.value = null;
  form.nombre = '';
  form.activo = false;
};

const handleSubmit = async () => {
  if (!selectedMatricula.value) return;

  if (editingId.value) {
    await itemsStore.editItem(selectedMatricula.value, {
      id: editingId.value,
      nombre: form.nombre,
      activo: form.activo,
    });
  } else {
    await itemsStore.addItem(selectedMatricula.value, {
      id: Date.now(),
      nombre: form.nombre,
      activo: form.activo,
    });
  }

  resetForm();
  fetchVehiculos();
};

const startEdit = (item: { id: number; nombre: string; activo: boolean }) => {
  editingId.value = item.id;
  form.nombre = item.nombre;
  form.activo = item.activo;
};

const changeItemStatus = async (item: { id: number; nombre: string; activo: boolean }) => {
    await itemsStore.editItem(selectedMatricula.value, {
      id: item.id,
      nombre: item.nombre,
      activo: !item.activo,
    });
    fetchVehiculos();
};

const removeItem = async (itemId: number) => {
  if (!selectedMatricula.value) return;
  await itemsStore.removeItem(selectedMatricula.value, itemId)
  if (editingId.value === itemId) {
    resetForm();
  }
  fetchVehiculos();
};

const fetchVehiculos = async () => {
  await vehiculosStore.fetchVehiculos();
};

onMounted(async () => {
  if (!vehiculosStore.vehiculos.length) {
    await fetchVehiculos();
  }

  if (!selectedMatricula.value && vehiculosStore.vehiculos.length) {
    selectedMatricula.value = vehiculosStore.vehiculos[0].matricula;
  }
});
</script>
