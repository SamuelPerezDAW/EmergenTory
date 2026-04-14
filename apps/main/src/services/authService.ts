import type { AuthPayload, Usuario } from '@/types';
import { mockUser } from './mockData';
import axios from 'axios';
import CryptoJS from 'crypto-js';

export function convertPassword(password: string, hashedPassword: string) {
  const parts = hashedPassword.split('$');
  if (parts.length !== 4) return false;

  const [, iterations, salt, originalHash] = parts;

  const derivedKey = CryptoJS.PBKDF2(password, salt, {
    keySize: 256 / 32,
    iterations: parseInt(iterations, 10),
    hasher: CryptoJS.algo.SHA256
  });

  const base64Hash = CryptoJS.enc.Base64.stringify(derivedKey);
  return base64Hash;
}

const wait = (ms = 350) => new Promise((resolve) => setTimeout(resolve, ms));


export async function loginService(payload: AuthPayload): Promise<{ token: string; user: Usuario } | undefined | null> {
  await wait();

  const response = await axios.get(`http://127.0.0.1:8000/api/users/profile/${payload.username}`, {
    headers: {
      "Authorization": "Bearer f5a7f855-28d9-4c63-91ad-f2381a4a6866"
    }
  })

  const {
    status,
    data
  } = response;

  if (status == 200){  
    try {
      if (
        data.usuario.nombre_usuario === payload.username && 
        data.usuario.email === payload.email && 
        convertPassword(payload.password, data.usuario.contraseña) === data.usuario.contraseña.split("$")[3]
      ){
        return {
          token: `token-${payload.username}-emergentory`,
          user: {
            ...mockUser,
            username: payload.username,
          },
        };
      } else {
        console.log(data)
        return
      }
    } catch(error) {
      console.log("ERROR: ", error)
    }
  }
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
