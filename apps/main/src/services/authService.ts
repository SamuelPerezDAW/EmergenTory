import type { AuthPayload, Usuario } from '@/types';
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

function mapProfileResponse(data: any): Usuario {
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

  const response = await axios.get(`http://127.0.0.1:8000/api/users/profile/${payload.username}`)

  const {
    status,
    data
  } = response;

  if (status == 200){  
    try {
      if (
        data.usuario.nombre_usuario === payload.username &&
        convertPassword(payload.password, data.usuario.contraseña) === data.usuario.contraseña.split("$")[3]
      ){
        return {
          token: data.token.key,
          user: mapProfileResponse(data),
        };
      }
    } catch(error) {
      console.log("ERROR: ", error);
    }
    
  } else {
    console.error("ERROR: Error ", status, " al hacer la petición");
  }
}

export async function updateProfileService(username: string, payload: FormData): Promise<Usuario | undefined> {
  await wait();

  const response = await axios.post(`http://127.0.0.1:8000/api/users/profile/${username}/mod/`, payload, {
    headers: {
      Authorization: `Bearer ${sessionStorage.getItem('emergentory_token') ?? ''}`,
    },
  });

  if (response.status === 200 && response.data?.perfil) {
    return mapProfileResponse(response.data.perfil);
  }
}
