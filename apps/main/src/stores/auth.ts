import { computed, ref } from 'vue';
import { defineStore } from 'pinia';
import { loginService } from '@/services/authService';
import type { AuthPayload, Usuario } from '@/types';

const TOKEN_KEY = 'emergentory_token';
const USER_KEY = 'emergentory_user';

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(sessionStorage.getItem(TOKEN_KEY));
  const user = ref<Usuario | null>(JSON.parse(sessionStorage.getItem(USER_KEY) ?? 'null'));
  const loading = ref(false);

  const isAuthenticated = computed(() => Boolean(token.value));
  const fullName = computed(() => (user.value ? `${user.value.first_name} ${user.value.last_name}` : 'Invitado'));

  const persistSession = (nextToken: string, nextUser: Usuario) => {
    token.value = nextToken;
    user.value = nextUser;
    sessionStorage.setItem(TOKEN_KEY, nextToken);
    sessionStorage.setItem(USER_KEY, JSON.stringify(nextUser));
  };

  const login = async (payload: AuthPayload) => {
    loading.value = true;
    try {
      const response = await loginService(payload);
      if (!response) return null;
      persistSession(response.token, response.user);
      
    } finally {
      loading.value = false;
      return true;
    }
  };

  const logout = () => {
    token.value = null;
    user.value = null;
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(USER_KEY);
    sessionStorage.removeItem('emergentory_session_summary');
  };

  return { token, user, loading, isAuthenticated, fullName, login, logout };
});
