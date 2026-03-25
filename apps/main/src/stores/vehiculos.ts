import { computed, ref } from 'vue';
import { defineStore } from 'pinia';
import { getVehiculoByMatricula, getVehiculos } from '@/services/vehiculoService';
import type { Vehiculo } from '@/types';

export const useVehiculosStore = defineStore('vehiculos', () => {
  const vehiculos = ref<Vehiculo[]>([]);
  const loading = ref(false);
  const selectedMatricula = ref<string | null>(sessionStorage.getItem('selected_vehicle'));

  const totalVehiculos = computed(() => vehiculos.value.length);

  const fetchVehiculos = async () => {
    loading.value = true;
    try {
      vehiculos.value = await getVehiculos();
    } finally {
      loading.value = false;
    }
  };

  const selectVehiculo = (matricula: string) => {
    selectedMatricula.value = matricula;
    sessionStorage.setItem('selected_vehicle', matricula);
  };

  const fetchVehiculo = async (matricula: string) => {
    const localVehicle = vehiculos.value.find((vehiculo) => vehiculo.matricula === matricula);
    if (localVehicle) {
      return localVehicle;
    }
    return getVehiculoByMatricula(matricula);
  };

  const updateVehiculo = (nextVehiculo: Vehiculo) => {
    vehiculos.value = vehiculos.value.map((vehiculo) =>
      vehiculo.matricula === nextVehiculo.matricula ? nextVehiculo : vehiculo,
    );
  };

  return { vehiculos, loading, selectedMatricula, totalVehiculos, fetchVehiculos, fetchVehiculo, selectVehiculo, updateVehiculo };
});
