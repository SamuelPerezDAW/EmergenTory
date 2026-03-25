import { computed, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import type { AuthPayload } from '@/types';

const isSubmitting = ref(false);

export function useAuth() {
  const authStore = useAuthStore();
  const isAuthenticated = computed(() => authStore.isAuthenticated);

  const submitLogin = async (payload: AuthPayload) => {
    isSubmitting.value = true;
    try {
      await authStore.login(payload);
    } finally {
      isSubmitting.value = false;
    }
  };

  const submitSignup = async (payload: AuthPayload) => {
    isSubmitting.value = true;
    try {
      await authStore.signup(payload);
    } finally {
      isSubmitting.value = false;
    }
  };

  return {
    isAuthenticated,
    isSubmitting,
    submitLogin,
    submitSignup,
    logout: authStore.logout,
  };
}
