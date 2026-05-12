import { computed, ref } from 'vue';
import { defineStore } from 'pinia';
import { createItemService, deleteItemService, updateItemService } from '@/services/itemService';
import { useVehiculosStore } from './vehiculos';
import type { Item } from '@/types';

export const useItemsStore = defineStore('items', () => {
  const saving = ref(false);
  const vehiculosStore = useVehiculosStore();

  const totalItems = computed(() =>
    vehiculosStore.vehiculos.reduce((total, vehiculo) => total + vehiculo.lista[0].items.length, 0),
  );

  const addItem = async (matricula: string, item: Item) => {
    saving.value = true;
    try {
      const created = await createItemService(item, matricula);
      const vehiculo = vehiculosStore.vehiculos.find((entry) => entry.matricula === matricula);
      if (!vehiculo || !created) return;
      vehiculo.lista[0].items.push(created);
      vehiculosStore.updateVehiculo({ ...vehiculo });
    } finally {
      saving.value = false;
    }
  };

  const editItem = async (matricula: string, item: Item) => {
    saving.value = true;
    try {
      const updated = await updateItemService(item);
      const vehiculo = vehiculosStore.vehiculos.find((entry) => entry.matricula === matricula);
      if (!vehiculo) return;
      vehiculo.lista[0].items = vehiculo.lista[0].items.map((entry) => (entry.id === updated.id ? updated : entry));
      vehiculosStore.updateVehiculo({ ...vehiculo });
    } finally {
      saving.value = false;
    }
  };

  const removeItem = async (matricula: string, itemId: number) => {
    saving.value = true;
    try {
      const deletedId = await deleteItemService(itemId);
      const vehiculo = vehiculosStore.vehiculos.find((entry) => entry.matricula === matricula);
      if (!vehiculo) return;
      vehiculo.lista[0].items = vehiculo.lista[0].items.filter((entry) => entry.id !== deletedId);
      vehiculosStore.updateVehiculo({ ...vehiculo });
    } finally {
      saving.value = false;
    }
  };

  return { saving, totalItems, addItem, editItem, removeItem };
});
