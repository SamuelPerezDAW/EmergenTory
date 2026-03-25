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
            <p class="text-2xl font-semibold text-slate-900">48</p>
            <p class="text-sm text-slate-500">vehículos auditados</p>
          </div>
          <div class="rounded-[1.75rem] border border-white/70 bg-white/70 p-4 shadow-sm">
            <p class="text-2xl font-semibold text-slate-900">93%</p>
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
          :title="isLogin ? 'Acceso seguro' : 'Crear cuenta'"
          :description="isLogin ? 'Inicia sesión para gestionar inventarios y listas de verificación.' : 'Registra un usuario operativo para entrar en la plataforma.'"
          :submit-label="isLogin ? 'Entrar' : 'Crear cuenta'"
          eyebrow="Autenticación"
          @submit="handleSubmit"
        >
          <div v-if="!isLogin" class="grid gap-4 sm:grid-cols-2">
            <label class="space-y-2 text-sm font-medium text-slate-700">
              <span>Nombre</span>
              <input v-model="form.first_name" class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 focus:border-brand-500" />
            </label>
            <label class="space-y-2 text-sm font-medium text-slate-700">
              <span>Apellidos</span>
              <input v-model="form.last_name" class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 focus:border-brand-500" />
            </label>
          </div>

          <div class="grid gap-4">
            <label class="space-y-2 text-sm font-medium text-slate-700">
              <span>Usuario</span>
              <input v-model="form.username" class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 focus:border-brand-500" />
            </label>
            <label class="space-y-2 text-sm font-medium text-slate-700">
              <span>Email</span>
              <input v-model="form.email" type="email" class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 focus:border-brand-500" />
            </label>
            <label class="space-y-2 text-sm font-medium text-slate-700">
              <span>Contraseña</span>
              <input v-model="form.password" type="password" class="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none ring-0 focus:border-brand-500" />
            </label>
          </div>

          <template #actions>
            <div class="flex w-full flex-col gap-3 sm:flex-row">
              <button
                type="submit"
                class="flex-1 rounded-2xl bg-brand-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-brand-700"
              >
                {{ isSubmitting ? 'Procesando...' : isLogin ? 'Entrar' : 'Crear cuenta' }}
              </button>
              <button
                type="button"
                class="flex-1 rounded-2xl border border-slate-200 px-4 py-3 text-sm font-semibold text-slate-700"
                @click="isLogin = !isLogin"
              >
                {{ isLogin ? 'Ir a registro' : 'Volver al login' }}
              </button>
            </div>
          </template>
        </BaseForm>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import BaseForm from '@/components/BaseForm.vue';
import { useAuth } from '@/composables/useAuth';

const router = useRouter();
const { submitLogin, submitSignup, isSubmitting } = useAuth();

const isLogin = ref(true);
const form = reactive({
  username: 'coordinador112',
  email: 'coordinador@emergentory.app',
  password: '123456',
  first_name: 'Lucia',
  last_name: 'Medina',
});

const handleSubmit = async () => {
  if (isLogin.value) {
    await submitLogin(form);
  } else {
    await submitSignup(form);
  }

  await router.push('/dashboard');
};
</script>
