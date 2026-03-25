import type { AuthPayload, Usuario } from '@/types';
import { mockUser } from './mockData';

const wait = (ms = 350) => new Promise((resolve) => setTimeout(resolve, ms));

export async function loginService(payload: AuthPayload): Promise<{ token: string; user: Usuario }> {
  await wait();

  return {
    token: `token-${payload.username}-emergentory`,
    user: {
      ...mockUser,
      username: payload.username,
    },
  };
}

export async function signupService(payload: AuthPayload): Promise<{ token: string; user: Usuario }> {
  await wait();

  return {
    token: `token-${payload.username}-new`,
    user: {
      ...mockUser,
      id: 2,
      username: payload.username,
      email: payload.email ?? mockUser.email,
      first_name: payload.first_name ?? 'Nuevo',
      last_name: payload.last_name ?? 'Usuario',
    },
  };
}
