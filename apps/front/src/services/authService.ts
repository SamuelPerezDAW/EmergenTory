import type { AuthPayload, Usuario } from '@/types';
import axios from 'axios';

const wait = (ms = 350) => new Promise((resolve) => setTimeout(resolve, ms));
const API_URL = import.meta.env.VITE_API_URL;

export function mapProfileResponse(data: any): Usuario {
  return {
    id: data.usuario.id,
    username: data.usuario.nombre_usuario,
    email: data.usuario.email,
    first_name: data.usuario.nombre,
    last_name: data.usuario.apellido,
    perfil: {
      admin: data.admin,
      avatar: data.avatar,
      bio: data.bio,
      telefono: data.telefono ?? '',
    },
  };
}

export async function loginService(payload: AuthPayload): Promise<{ token: string; user: Usuario } | undefined | null> {
  await wait();

  const response = await axios.post(`${API_URL}/api/users/login/`, {
    nombre_usuario: payload.username,
    contraseña: payload.password,
  });

  if (response.status === 200 && response.data?.token && response.data?.user) {
    return {
      token: response.data.token,
      user: mapProfileResponse(response.data.user),
    };
  }

  return null;
}

export async function updateProfileService(username: string, payload: FormData): Promise<Usuario | undefined> {
  await wait();

  const response = await axios.post(`${API_URL}/api/users/profile/${username}/mod/`, payload, {
    headers: {
      Authorization: `Bearer ${sessionStorage.getItem('emergentory_token') ?? ''}`,
    },
  });

  if (response.status === 200 && response.data?.perfil) {
    return mapProfileResponse(response.data.perfil);
  }
}

export async function requestPasswordResetService(email: string): Promise<string> {
  const response = await axios.post(`${API_URL}/api/users/reset-password/`, { email });
  return response.data?.detail ?? 'Solicitud procesada.';
}

export async function confirmPasswordResetService(uid: string, token: string, password: string): Promise<string> {
  const response = await axios.post(`${API_URL}/api/users/reset-password/confirm/`, {
    uid,
    token,
    contraseña: password,
  });
  return response.data?.detail ?? 'Contraseña actualizada.';
}
