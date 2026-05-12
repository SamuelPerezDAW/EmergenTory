import { computed, onMounted, reactive, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useVehiculosStore } from '@/stores/vehiculos';

export function useVehiculos() {
  const vehiculosStore = useVehiculosStore();
  const { vehiculos, loading, selectedMatricula } = storeToRefs(vehiculosStore);

  const filters = reactive({
    search: '',
    categoria: 'Todas',
  });

  const categorias: {'clave': string, 'valor': string}[] = [
    {
      "clave": 'BOM',
      "valor": 'Bomberos'
    },
    {
      "clave": 'POL',
      "valor": 'Policias'
    },
    {
      "clave": 'AMB',
      "valor": 'Ambulancias'
    },
  ];  
  const selectedVehicleCount = ref(0);

  const filteredVehiculos = computed(() =>
    vehiculos.value.filter((vehiculo) => {
      const matchesSearch =
        vehiculo.matricula.toLowerCase().includes(filters.search.toLowerCase()) ||
        vehiculo.marca.toLowerCase().includes(filters.search.toLowerCase()) ||
        vehiculo.modelo.toLowerCase().includes(filters.search.toLowerCase());
      const matchesCategory = filters.categoria === 'Todas' || vehiculo.categoria === filters.categoria;
      return matchesSearch && matchesCategory;
    }),
  );

  const activeItems = computed(() =>
    vehiculos.value.reduce((totalActive, vehiculo) => 
      totalActive += vehiculo.lista.reduce((totalLista, lis) =>
        totalLista += lis.items.filter((item) => item.activo).length
      , 0)
    , 0)
  );

  onMounted(async () => {
    if (!vehiculos.value.length) {
      await vehiculosStore.fetchVehiculos();
    }
  });

  return {
    vehiculos,
    loading,
    selectedMatricula,
    filters,
    categorias,
    filteredVehiculos,
    activeItems,
    selectedVehicleCount,
    selectVehiculo: vehiculosStore.selectVehiculo,
  };
}
