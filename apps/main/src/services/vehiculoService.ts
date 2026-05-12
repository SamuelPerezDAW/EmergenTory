import type { Vehiculo } from '@/types';
import { mockVehiculos } from './mockData';
import axios from 'axios';

const wait = (ms = 300) => new Promise((resolve) => setTimeout(resolve, ms));

export async function getVehiculos(): Promise<Vehiculo[]> {
  await wait();

  const response = await axios.get(`http://127.0.0.1:8000/api/vehicles/`, {});

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

  const response = await axios.get(`http://127.0.0.1:8000/api/vehicles/?matricula=${matricula}`, {
    
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

  const response = await axios.post(`http://127.0.0.1:8000/api/vehicles/add/`, {
    vehiculo
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
