<template>
  <section v-if="user" class="mx-auto max-w-5xl">
    <article class="overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-sm">
      <div class="bg-slate-900 p-6 text-white sm:p-8">
        <div class="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
          <div class="flex items-center gap-5">
            <img :src="user.perfil.avatar" :alt="user.username" class="h-24 w-24 rounded-[1.5rem] object-cover ring-4 ring-white/10" />
            <div>
              <p class="text-xs font-semibold uppercase tracking-[0.35em] text-brand-100">Perfil</p>
              <h2 class="mt-2 text-3xl font-semibold">{{ user.first_name }} {{ user.last_name }}</h2>
              <p class="mt-2 text-slate-300">{{ user.email }}</p>
            </div>
          </div>

          <button
            type="button"
            class="w-fit rounded-2xl bg-white px-5 py-3 text-sm font-semibold text-slate-900 transition hover:bg-brand-100"
            @click="openEditor"
          >
            Editar perfil
          </button>
        </div>
      </div>

      <div class="grid gap-6 p-6 sm:p-8 lg:grid-cols-[1fr_1.2fr]">
        <div class="rounded-2xl bg-slate-50 p-5">
          <p class="text-xs font-semibold uppercase tracking-[0.25em] text-slate-500">Biografia</p>
          <p class="mt-3 text-sm leading-6 text-slate-700">{{ user.perfil.bio || 'Sin biografia registrada.' }}</p>
        </div>

        <dl class="grid gap-4 sm:grid-cols-2">
          <div v-for="item in profileData" :key="item.label" class="rounded-2xl bg-slate-50 p-5">
            <dt class="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">{{ item.label }}</dt>
            <dd class="mt-2 break-words text-lg font-semibold text-slate-900">{{ item.value }}</dd>
          </div>
        </dl>
      </div>
    </article>

    <BaseModal :open="editorOpen" title="Editar perfil" eyebrow="Usuario" @close="closeEditor">
      <form class="space-y-4" @submit.prevent="saveProfile">
        <div class="grid gap-4 sm:grid-cols-2">
          <label class="block">
            <span class="text-sm font-medium text-slate-700">Nombre</span>
            <input v-model.trim="form.first_name" type="text" class="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-700">Apellido</span>
            <input v-model.trim="form.last_name" type="text" class="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
          </label>
        </div>

        <label class="block">
          <span class="text-sm font-medium text-slate-700">Usuario</span>
          <input v-model.trim="form.username" type="text" class="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-700">Email</span>
          <input v-model.trim="form.email" type="email" class="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
          <span v-if="errors.email" class="mt-2 block text-sm font-medium text-red-600">{{ errors.email }}</span>
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-700">Telefono</span>
          <input v-model.trim="form.telefono" type="tel" class="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
          <span v-if="errors.telefono" class="mt-2 block text-sm font-medium text-red-600">{{ errors.telefono }}</span>
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-700">Foto de perfil</span>
          <div class="mt-2 flex items-center gap-4">
            <img :src="avatarPreview" :alt="form.username" class="h-16 w-16 rounded-2xl border border-slate-200 object-cover" />
            <input type="file" accept="image/*" class="block w-full text-sm text-slate-600 file:mr-4 file:rounded-2xl file:border-0 file:bg-slate-100 file:px-4 file:py-3 file:text-sm file:font-semibold file:text-slate-700" @change="onAvatarChange" />
          </div>
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-700">Biografia</span>
          <textarea v-model.trim="form.bio" rows="4" class="mt-2 w-full resize-none rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
        </label>

        <p v-if="errors.general" class="rounded-2xl bg-red-50 p-3 text-sm font-medium text-red-700">{{ errors.general }}</p>

        <div class="flex flex-col-reverse gap-3 pt-2 sm:flex-row sm:justify-end">
          <button type="button" class="rounded-2xl bg-slate-100 px-5 py-3 text-sm font-semibold text-slate-700 disabled:opacity-60" :disabled="saving" @click="closeEditor">
            Cancelar
          </button>
          <button type="submit" class="rounded-2xl bg-brand-600 px-5 py-3 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-60" :disabled="saving">
            {{ saving ? 'Guardando...' : 'Guardar cambios' }}
          </button>
        </div>
      </form>
    </BaseModal>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue';
import { storeToRefs } from 'pinia';
import BaseModal from '@/components/BaseModal.vue';
import { useAuthStore } from '@/stores/auth';
import { updateProfileService } from '@/services/authService';
import type { Usuario } from '@/types';

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);

const editorOpen = ref(false);
const saving = ref(false);
const selectedAvatar = ref<File | null>(null);
const localAvatarPreview = ref('');
const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  telefono: '',
  bio: '',
});
const errors = reactive({
  email: '',
  telefono: '',
  general: '',
});

const profileData = computed(() => {
  if (!user.value) return [];

  return [
    { label: 'Usuario', value: user.value.username },
    { label: 'Nombre', value: user.value.first_name },
    { label: 'Apellido', value: user.value.last_name },
    { label: 'Telefono', value: user.value.perfil.telefono || 'Sin telefono' },
    { label: 'Email', value: user.value.email },
    { label: 'Rol', value: user.value.perfil.admin ? 'Administrador' : 'Operador' },
  ];
});

function fillForm(currentUser: Usuario): void {
  form.username = currentUser.username;
  form.email = currentUser.email;
  form.first_name = currentUser.first_name;
  form.last_name = currentUser.last_name;
  form.telefono = currentUser.perfil.telefono;
  form.bio = currentUser.perfil.bio;
  selectedAvatar.value = null;
  localAvatarPreview.value = '';
}

function openEditor(): void {
  if (!user.value) return;
  fillForm(user.value);
  errors.email = '';
  errors.telefono = '';
  errors.general = '';
  editorOpen.value = true;
}

function closeEditor(): void {
  if (saving.value) return;
  editorOpen.value = false;
}

const avatarPreview = computed(() => localAvatarPreview.value || user.value?.perfil.avatar || '');

function onAvatarChange(event: Event): void {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0] ?? null;

  selectedAvatar.value = file;
  localAvatarPreview.value = file ? URL.createObjectURL(file) : '';
}

function validatePayload(): boolean {
  const regexEmail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  errors.email = regexEmail.test(form.email) ? '' : 'El formato del correo electronico no es valido';
  errors.telefono = form.telefono.length <= 32 ? '' : 'El telefono no puede superar los 32 caracteres';
  errors.general = '';

  return !errors.email && !errors.telefono && Boolean(user.value);
}

async function saveProfile(): Promise<void> {
  if (!validatePayload() || !user.value) return;

  const currentUsername = user.value.username;
  const payload = new FormData();
  payload.append('nombre_usuario', form.username);
  payload.append('nombre', form.first_name);
  payload.append('apellidos', form.last_name);
  payload.append('email', form.email);
  payload.append('telefono', form.telefono);
  payload.append('bio', form.bio);

  if (selectedAvatar.value) {
    payload.append('avatar', selectedAvatar.value);
  }

  saving.value = true;
  try {
    const updatedUser = await updateProfileService(currentUsername, payload);

    if (!updatedUser) {
      errors.general = 'No se pudo actualizar el perfil';
      return;
    }

    authStore.updateUser(updatedUser);
    editorOpen.value = false;
  } catch (error: any) {
    errors.general = error?.response?.data?.error ?? 'No se pudo actualizar el perfil';
  } finally {
    saving.value = false;
  }
}
</script>
