import { computed, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import type { AuthPayload } from '@/types';

const isSubmitting = ref(false);

export const isAdmin = computed<boolean>(() => JSON.parse(sessionStorage.getItem('emergentory_user') ?? '')['perfil']['admin'])

export function useAuth() {
  const authStore = useAuthStore();
  const isAuthenticated = computed(() => authStore.isAuthenticated);

  const submitLogin = async (payload: AuthPayload) => {
    isSubmitting.value = true;
    try {
      if ( await authStore.login(payload)) {
        isSubmitting.value = false;
        return true;

      } else {
        isSubmitting.value = false;
        return null;
      }

    } catch (error) {
      console.error('ERROR: ', error)
      return null;
    }
  };

  return {
    isAuthenticated,
    isSubmitting,
    submitLogin,
    logout: authStore.logout,
  };
}
