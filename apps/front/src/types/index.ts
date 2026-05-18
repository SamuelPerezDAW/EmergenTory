export interface Perfil {
  admin: boolean;
  avatar: string;
  bio: string;
  telefono: string;
}

export interface Usuario {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  perfil: Perfil;
}

export interface Item {
  id: number;
  nombre: string;
  activo: boolean;
}

export interface Lista {
  id: number;
  creado: string;
  actualizado: string;
  items: Item[];
}

export interface Vehiculo {
  matricula: string;
  marca: string;
  modelo: string;
  categoria: string;
  lista: Lista[];
}

export interface AuthPayload {
  username: string;
  password: string;
  email?: string;
  first_name?: string;
  last_name?: string;
}

export interface SessionSummary {
  lastVehicleMatricula: string | null;
  lastVisitedRoute: string | null;
}
