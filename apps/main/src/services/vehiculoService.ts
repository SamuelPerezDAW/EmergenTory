import type { Vehiculo } from '@/types';
import { mockVehiculos } from './mockData';

const wait = (ms = 300) => new Promise((resolve) => setTimeout(resolve, ms));

export async function getVehiculos(): Promise<Vehiculo[]> {
  await wait();
  return structuredClone(mockVehiculos);
}

export async function getVehiculoByMatricula(matricula: string): Promise<Vehiculo | undefined> {
  await wait(200);
  return structuredClone(mockVehiculos.find((vehiculo) => vehiculo.matricula === matricula));
}
