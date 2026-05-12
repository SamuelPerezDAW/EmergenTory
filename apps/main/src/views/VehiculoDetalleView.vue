<template>
  <section v-if="vehiculo" class="space-y-6">
    <article class="rounded-[2rem] bg-slate-900 p-6 text-white shadow-sm">
      <p class="text-xs uppercase tracking-[0.35em] text-brand-100">{{ vehiculo.categoria }}</p>
      <div class="mt-3 flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <h2 class="text-3xl font-semibold">{{ vehiculo.marca }} {{ vehiculo.modelo }}</h2>
          <p class="mt-2 text-slate-300">Matrícula {{ vehiculo.matricula }}</p>
        </div>
        <RouterLink to="/items" class="rounded-2xl bg-white px-4 py-3 text-sm font-semibold text-ink-900">
          Gestionar inventario
        </RouterLink>
      </div>
    </article>

    <div class="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
      <article class="rounded-[2rem] border border-slate-200 bg-white p-5 shadow-sm">
        <p class="text-xs uppercase tracking-[0.35em] text-brand-600">Metadatos</p>
        <dl class="mt-5 space-y-4">
          <div class="rounded-2xl bg-slate-50 p-4">
            <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Lista</dt>
            <dd class="mt-2 text-lg font-semibold text-slate-900">#{{ vehiculo.lista[0].id }}</dd>
          </div>
          <div class="rounded-2xl bg-slate-50 p-4">
            <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Creado</dt>
            <dd class="mt-2 text-lg font-semibold text-slate-900">{{ formatDate(vehiculo.lista[0].creado) }}</dd>
          </div>
          <div class="rounded-2xl bg-slate-50 p-4">
            <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Actualizado</dt>
            <dd class="mt-2 text-lg font-semibold text-slate-900">{{ formatDate(vehiculo.lista[0].actualizado) }}</dd>
          </div>
        </dl>
      </article>

      <ItemList title="Items del vehículo" :items="vehiculo.lista[0].items" @edit="openEditor" @remove="removeItem" />
    </div>

    <BaseModal :open="modalOpen" title="Editar item" eyebrow="Mantenimiento" @close="closeModal">
      <div class="space-y-4">
        <label class="block space-y-2 text-sm font-medium text-slate-700">
          <span>Nombre del item</span>
          <input v-model="editableItem.nombre" class="w-full rounded-2xl border border-slate-200 px-4 py-3" />
        </label>
        <label class="flex items-center gap-3 rounded-2xl bg-slate-50 px-4 py-3 text-sm font-medium text-slate-700">
          <input v-model="editableItem.activo" type="checkbox" />
          Item activo
        </label>
        <button type="button" class="w-full rounded-2xl bg-brand-600 px-4 py-3 text-sm font-semibold text-white" @click="saveItem">
          Guardar cambios
        </button>
      </div>
    </BaseModal>
  </section>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import BaseModal from '@/components/BaseModal.vue';
import ItemList from '@/components/ItemList.vue';
import { useItemsStore } from '@/stores/items';
import { useVehiculosStore } from '@/stores/vehiculos';
import type { Item, Vehiculo } from '@/types';

const route = useRoute();
const vehiculosStore = useVehiculosStore();
const itemsStore = useItemsStore();

const vehiculo = ref<Vehiculo | null>(null);
const modalOpen = ref(false);
const editableItem = reactive<Item>({
  id: 0,
  nombre: '',
  activo: false,
});

const loadVehiculo = async () => {
  const matricula = route.params.matricula as string;
  vehiculosStore.selectVehiculo(matricula);
  vehiculo.value = (await vehiculosStore.fetchVehiculo(matricula)) ?? null;
};

const openEditor = (item: Item) => {
  editableItem.id = item.id;
  editableItem.nombre = item.nombre;
  editableItem.activo = item.activo;
  modalOpen.value = true;
};

const closeModal = () => {
  modalOpen.value = false;
};

const saveItem = async () => {
  if (!vehiculo.value) return;
  await itemsStore.editItem(vehiculo.value.matricula, { ...editableItem });
  await loadVehiculo();
  closeModal();
};

const removeItem = async (itemId: number) => {
  if (!vehiculo.value) return;
  await itemsStore.removeItem(vehiculo.value.matricula, itemId);
  await loadVehiculo();
};

const formatDate = (date: string) =>
  new Intl.DateTimeFormat('es-ES', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(date));

onMounted(loadVehiculo);
</script>
