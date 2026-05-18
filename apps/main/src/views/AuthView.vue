<template>
  <section class="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(22,124,104,0.22),_transparent_35%),linear-gradient(135deg,#f8fafc_0%,#ecfeff_45%,#f4efe8_100%)]">
    <div class="mx-auto grid min-h-screen max-w-7xl items-center gap-10 px-4 py-10 lg:grid-cols-[1.05fr_0.95fr] lg:px-8">
      <div class="space-y-6">
        <p class="text-xs font-semibold uppercase tracking-[0.45em] text-brand-700">Inventario de emergencia</p>
        <h1 class="max-w-xl text-5xl font-semibold leading-tight text-slate-900">
          Controla la flota, el material y la trazabilidad desde un único panel.
        </h1>
        <p class="max-w-lg text-base text-slate-600">
          Gestión de ambulancias, autobombas y unidades policiales con listas dinámicas, sesión persistente y seguimiento por vehículo.
        </p>

        <div class="grid gap-4 sm:grid-cols-3">
          <div class="rounded-[1.75rem] border border-white/70 bg-white/70 p-4 shadow-sm">
            <p class="text-2xl font-semibold text-slate-900">{{ auditedVehicles }}</p>
            <p class="text-sm text-slate-500">vehículos auditados</p>
          </div>
          <div class="rounded-[1.75rem] border border-white/70 bg-white/70 p-4 shadow-sm">
            <p class="text-2xl font-semibold text-slate-900">{{ operationalMaterial }}</p>
            <p class="text-sm text-slate-500">material operativo</p>
          </div>
          <div class="rounded-[1.75rem] border border-white/70 bg-white/70 p-4 shadow-sm">
            <p class="text-2xl font-semibold text-slate-900">24/7</p>
            <p class="text-sm text-slate-500">seguimiento continuo</p>
          </div>
        </div>
      </div>

      <div class="mx-auto w-full max-w-xl">
        <BaseForm
          :title="formTitle"
          :description="formDescription"
          :submit-label="submitLabel"
          eyebrow="Autenticación"
          @submit="handleSubmit"
        >
          <div v-if="mode === 'login'" class="grid gap-4">
            <label class="space-y-2 text-sm font-medium text-slate-700">
              <span>Usuario</span>
              <input v-model="form.username" type="text" class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 focus:border-brand-500" />
            </label>
            <label class="space-y-2 text-sm font-medium text-slate-700">
              <span>Contraseña</span>
              <input v-model="form.password" type="password" class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 focus:border-brand-500" />
            </label>
          </div>
          <div v-else-if="mode === 'forgot'" class="grid gap-4">
            <label class="space-y-2 text-sm font-medium text-slate-700">
              <span>Email</span>
              <input v-model.trim="resetEmail" type="email" class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 focus:border-brand-500" />
            </label>
          </div>
          <div v-else class="grid gap-4">
            <label class="space-y-2 text-sm font-medium text-slate-700">
              <span>Nueva contraseña</span>
              <input v-model="newPassword" type="password" class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 focus:border-brand-500" />
            </label>
            <label class="space-y-2 text-sm font-medium text-slate-700">
              <span>Repite la contraseña</span>
              <input v-model="repeatPassword" type="password" class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 focus:border-brand-500" />
            </label>
          </div>

          <p v-if="message" class="rounded-2xl bg-brand-50 px-4 py-3 text-sm font-medium text-brand-700">{{ message }}</p>
          <p v-if="error" class="rounded-2xl bg-red-50 px-4 py-3 text-sm font-medium text-red-700">{{ error }}</p>

          <template #actions>
            <div class="flex w-full flex-col gap-3 sm:flex-row">
              <button
                type="submit"
                class="flex-1 rounded-2xl bg-brand-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-brand-700"
              >
                {{ isSubmitting ? 'Procesando...' : submitLabel }}
              </button>
              <button
                v-if="mode === 'login'"
                type="button"
                class="rounded-2xl border border-slate-200 px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-brand-500 hover:text-brand-700"
                @click="setMode('forgot')"
              >
                Olvidé mi contraseña
              </button>
              <button
                v-else
                type="button"
                class="rounded-2xl border border-slate-200 px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-brand-500 hover:text-brand-700"
                @click="setMode('login')"
              >
                Volver al login
              </button>
            </div>
          </template>
        </BaseForm>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import BaseForm from '@/components/BaseForm.vue';
import { useAuth } from '@/composables/useAuth';
import { confirmPasswordResetService, requestPasswordResetService } from '@/services/authService';
import { getVehiculos } from '@/services/vehiculoService';
import type { Vehiculo } from '@/types';

const router = useRouter();
const route = useRoute();
const { submitLogin, isSubmitting } = useAuth();

type AuthMode = 'login' | 'forgot' | 'reset';

const mode = ref<AuthMode>(route.name === 'reset-password' ? 'reset' : 'login');
const form = reactive({
  username: '',
  password: '',
});
const resetEmail = ref('');
const newPassword = ref('');
const repeatPassword = ref('');
const message = ref('');
const error = ref('');
const statsVehicles = ref<Vehiculo[]>([]);

const auditedVehicles = computed(() => statsVehicles.value.length);
const operationalMaterial = computed(() => {
  const totalItems = statsVehicles.value.reduce(
    (total, vehicle) => total + vehicle.lista.reduce((items, lista) => items + lista.items.length, 0),
    0,
  );
  const activeItems = statsVehicles.value.reduce(
    (total, vehicle) =>
      total + vehicle.lista.reduce((items, lista) => items + lista.items.filter((item) => item.activo).length, 0),
    0,
  );

  if (!totalItems) return '0%';
  return `${Math.round((activeItems / totalItems) * 100)}%`;
});

const formTitle = computed(() => {
  if (mode.value === 'forgot') return 'Recuperar contraseña';
  if (mode.value === 'reset') return 'Nueva contraseña';
  return 'Acceso seguro';
});

const formDescription = computed(() => {
  if (mode.value === 'forgot') return 'Introduce tu correo y enviaremos un enlace de restablecimiento.';
  if (mode.value === 'reset') return 'Define una nueva contraseña para tu cuenta.';
  return 'Inicia sesión para gestionar inventarios y listas de verificación.';
});

const submitLabel = computed(() => {
  if (mode.value === 'forgot') return 'Enviar enlace';
  if (mode.value === 'reset') return 'Actualizar contraseña';
  return 'Entrar';
});

const setMode = (nextMode: AuthMode) => {
  mode.value = nextMode;
  message.value = '';
  error.value = '';
};

const handleSubmit = async () => {
  message.value = '';
  error.value = '';

  try {
    if (mode.value === 'login') {
      if (await submitLogin(form)) {
        await router.push('/dashboard');
      } else {
        error.value = 'Credenciales inválidas.';
      }
      return;
    }

    if (mode.value === 'forgot') {
      message.value = await requestPasswordResetService(resetEmail.value);
      return;
    }

    if (newPassword.value !== repeatPassword.value) {
      error.value = 'Las contraseñas no coinciden.';
      return;
    }

    message.value = await confirmPasswordResetService(
      String(route.params.uid),
      String(route.params.token),
      newPassword.value,
    );
    newPassword.value = '';
    repeatPassword.value = '';
  } catch (requestError: any) {
    const responseError = requestError?.response?.data?.error;
    error.value = Array.isArray(responseError)
      ? responseError.join(' ')
      : responseError || 'No se pudo completar la operación.';
  }
};

onMounted(async () => {
  try {
    statsVehicles.value = await getVehiculos();
  } catch {
    statsVehicles.value = [];
  }
});
</script>
