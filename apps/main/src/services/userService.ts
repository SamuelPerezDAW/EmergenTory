import axios from 'axios';
import type { Usuario } from '@/types';
import { mapProfileResponse } from '@/services/authService';

const API_URL = 'http://127.0.0.1:8000/api/users';

const authHeaders = () => ({
  Authorization: `Bearer ${sessionStorage.getItem('emergentory_token') ?? ''}`,
});

export interface UserCreatePayload {
  nombre_usuario: string;
  contraseña: string;
  nombre?: string;
  apellido?: string;
  email?: string;
  telefono?: string;
  bio?: string;
  admin?: boolean;
}

export async function listUsersService(): Promise<Usuario[]> {
  const response = await axios.get(`${API_URL}/`, {
    headers: authHeaders(),
  });

  if (response.status === 200 && Array.isArray(response.data)) {
    return response.data.map(mapProfileResponse);
  }

  return [];
}

export async function createUserService(payload: UserCreatePayload): Promise<Usuario | undefined> {
  const response = await axios.post(`${API_URL}/add/`, payload, {
    headers: authHeaders(),
  });

  if (response.status === 200) {
    return mapProfileResponse(response.data);
  }
}

export async function deleteUserService(username: string): Promise<void> {
  await axios.post(
    `${API_URL}/profile/${username}/del/`,
    {},
    {
      headers: authHeaders(),
    },
  );
}
