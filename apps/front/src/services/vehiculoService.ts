import type { Vehiculo } from '@/types';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const wait = (ms = 300) => new Promise((resolve) => setTimeout(resolve, ms));

export async function getVehiculos(): Promise<Vehiculo[]> {
  await wait();

  const response = await axios.get(`${API_URL}/api/vehicles/`, {});

  const status: number = response.status;
  const data: any[] = response.data;

  if (status == 200) {
    if (typeof data === 'object') {
      return structuredClone(data);

    } else {
      return [] as Vehiculo[];
    }
    
  } else {
    console.error("ERROR: Error ", status, " al hacer la petición");
    return [] as Vehiculo[];
  }
}

export async function getVehiculoByMatricula(matricula: string): Promise<Vehiculo[] | undefined> {
  await wait(200);

  const response = await axios.get(`${API_URL}/api/vehicles/?matricula=${matricula}`, {
    
  });

  const status: number = response.status;
  const data: any[] = response.data;

  if (status == 200) {
    if (typeof data === 'object' && data[0].matricula === matricula) {
      return structuredClone(data);

    } else {
      return [] as Vehiculo[];
    }
    
  } else {
    console.error("ERROR: Error ", status, " al hacer la petición");
    return [] as Vehiculo[];
  }
}

export async function createVehiculo(vehiculo: Vehiculo): Promise<Vehiculo[] | undefined> {
  await wait(200);

  const response = await axios.post(`${API_URL}/api/vehicles/add/`, {
    'matricula': vehiculo.matricula,
    'marca': vehiculo.marca,
    'modelo': vehiculo.modelo,
    'categoria': vehiculo.categoria,
  }, {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('emergentory_token') ?? ''}`,
    },
  });

  const status: number = response.status;
  const data: any[] = response.data;

  if (status == 200) {
    if (typeof data === 'object') {
      return structuredClone(data);

    } else {
      return [] as Vehiculo[];
    }
    
  } else {
    console.error("ERROR: Error ", status, " al hacer la petición");
    return [] as Vehiculo[];
  }
}

export async function removeVehiculo(matricula: string): Promise<void> {
  await wait(200);

  const response = await axios.post(`${API_URL}/api/vehicles/${matricula}/del/`, { }, {
    headers: {
      "Authorization": `Bearer ${sessionStorage.getItem('emergentory_token') ?? ''}`,
    },
  });

  const status: number = response.status;
  const data: any[] = response.data;

  if (status == 200) {
    
    
  } else {
    console.error("ERROR: Error ", status, " al hacer la petición");
  }
}
