<template>
  <section class="space-y-6">
    <article class="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.35em] text-brand-600">Administracion</p>
          <h2 class="mt-2 text-2xl font-semibold text-slate-900">Usuarios de la empresa</h2>
          <p class="mt-2 text-sm text-slate-500">Alta, edicion y baja de usuarios con acceso a EmergenTory.</p>
        </div>

        <button type="button" class="w-fit rounded-2xl bg-brand-600 px-5 py-3 text-sm font-semibold text-white hover:bg-brand-700" @click="openCreateModal">
          Nuevo usuario
        </button>
      </div>
    </article>

    <article class="overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-sm">
      <div v-if="loading" class="p-6 text-sm font-medium text-slate-500">Cargando usuarios...</div>
      <div v-else-if="error" class="p-6 text-sm font-medium text-red-600">{{ error }}</div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-200">
          <thead class="bg-slate-50">
            <tr>
              <th class="px-5 py-4 text-left text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Usuario</th>
              <th class="px-5 py-4 text-left text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Contacto</th>
              <th class="px-5 py-4 text-left text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Rol</th>
              <th class="px-5 py-4 text-right text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="usuario in usuarios" :key="usuario.id" class="align-top">
              <td class="px-5 py-4">
                <div class="flex items-center gap-3">
                  <img
                    v-if="hasCustomAvatar(usuario)"
                    :src="usuario.perfil.avatar"
                    :alt="usuario.username"
                    class="h-11 w-11 rounded-2xl border border-slate-200 object-cover"
                  />
                  <div v-else class="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-900 text-sm font-semibold uppercase text-white">
                    {{ getInitials(usuario) }}
                  </div>
                  <div>
                    <p class="font-semibold text-slate-900">{{ usuario.first_name }} {{ usuario.last_name }}</p>
                    <p class="text-sm text-slate-500">{{ usuario.username }}</p>
                  </div>
                </div>
              </td>
              <td class="px-5 py-4">
                <p class="text-sm font-medium text-slate-900">{{ usuario.email || 'Sin email' }}</p>
                <p class="mt-1 text-sm text-slate-500">{{ usuario.perfil.telefono || 'Sin telefono' }}</p>
              </td>
              <td class="px-5 py-4">
                <span class="inline-flex rounded-2xl px-3 py-1 text-xs font-semibold" :class="usuario.perfil.admin ? 'bg-brand-100 text-brand-700' : 'bg-slate-100 text-slate-600'">
                  {{ usuario.perfil.admin ? 'Administrador' : 'Operador' }}
                </span>
              </td>
              <td class="px-5 py-4">
                <div class="flex justify-end gap-2">
                  <button type="button" class="rounded-2xl bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-200" @click="openEditModal(usuario)">
                    Editar
                  </button>
                  <button
                    type="button"
                    class="rounded-2xl bg-red-50 px-4 py-2 text-sm font-semibold text-red-700 hover:bg-red-100 disabled:cursor-not-allowed disabled:opacity-50"
                    :disabled="usuario.id === authStore.user?.id"
                    @click="removeUser(usuario)"
                  >
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>

    <BaseModal :open="modalOpen" :title="editingUser ? 'Editar usuario' : 'Nuevo usuario'" eyebrow="Usuarios" @close="closeModal">
      <form class="space-y-4" @submit.prevent="saveUser">
        <div class="grid gap-4 sm:grid-cols-2">
          <label class="block">
            <span class="text-sm font-medium text-slate-700">Nombre</span>
            <input v-model.trim="form.nombre" type="text" class="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
          </label>

          <label class="block">
            <span class="text-sm font-medium text-slate-700">Apellido</span>
            <input v-model.trim="form.apellido" type="text" class="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
          </label>
        </div>

        <label class="block">
          <span class="text-sm font-medium text-slate-700">Usuario</span>
          <input v-model.trim="form.nombre_usuario" type="text" class="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
        </label>

        <label v-if="!editingUser" class="block">
          <span class="text-sm font-medium text-slate-700">Contraseña inicial</span>
          <input v-model="form.contraseña" type="password" class="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-700">Email</span>
          <input v-model.trim="form.email" type="email" class="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-700">Telefono</span>
          <input v-model.trim="form.telefono" type="tel" class="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
        </label>

        <label class="block">
          <span class="text-sm font-medium text-slate-700">Biografia</span>
          <textarea v-model.trim="form.bio" rows="3" class="mt-2 w-full resize-none rounded-2xl border border-slate-200 px-4 py-3 outline-none focus:border-brand-500" />
        </label>

        <label class="flex items-center gap-3 rounded-2xl bg-slate-50 px-4 py-3 text-sm font-medium text-slate-700">
          <input v-model="form.admin" type="checkbox" />
          Administrador
        </label>

        <p v-if="formError" class="rounded-2xl bg-red-50 p-3 text-sm font-medium text-red-700">{{ formError }}</p>

        <div class="flex flex-col-reverse gap-3 pt-2 sm:flex-row sm:justify-end">
          <button type="button" class="rounded-2xl bg-slate-100 px-5 py-3 text-sm font-semibold text-slate-700 disabled:opacity-60" :disabled="saving" @click="closeModal">
            Cancelar
          </button>
          <button type="submit" class="rounded-2xl bg-brand-600 px-5 py-3 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-60" :disabled="saving || !canSubmit">
            {{ saving ? 'Guardando...' : 'Guardar' }}
          </button>
        </div>
      </form>
    </BaseModal>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import BaseModal from '@/components/BaseModal.vue';
import { useAuthStore } from '@/stores/auth';
import { updateProfileService } from '@/services/authService';
import { createUserService, deleteUserService, listUsersService } from '@/services/userService';
import type { Usuario } from '@/types';

const authStore = useAuthStore();

const usuarios = ref<Usuario[]>([]);
const loading = ref(false);
const saving = ref(false);
const modalOpen = ref(false);
const error = ref('');
const formError = ref('');
const editingUser = ref<Usuario | null>(null);

const form = reactive({
  nombre_usuario: '',
  contraseña: '',
  nombre: '',
  apellido: '',
  email: '',
  telefono: '',
  bio: '',
  admin: false,
});

const canSubmit = computed(() => {
  if (!form.nombre_usuario) return false;
  if (!editingUser.value && !form.contraseña) return false;
  return true;
});

function resetForm(): void {
  form.nombre_usuario = '';
  form.contraseña = '';
  form.nombre = '';
  form.apellido = '';
  form.email = '';
  form.telefono = '';
  form.bio = '';
  form.admin = false;
  formError.value = '';
}

function openCreateModal(): void {
  editingUser.value = null;
  resetForm();
  modalOpen.value = true;
}

function openEditModal(usuario: Usuario): void {
  editingUser.value = usuario;
  form.nombre_usuario = usuario.username;
  form.contraseña = '';
  form.nombre = usuario.first_name;
  form.apellido = usuario.last_name;
  form.email = usuario.email;
  form.telefono = usuario.perfil.telefono;
  form.bio = usuario.perfil.bio;
  form.admin = usuario.perfil.admin;
  formError.value = '';
  modalOpen.value = true;
}

function closeModal(): void {
  if (saving.value) return;
  modalOpen.value = false;
}

function hasCustomAvatar(usuario: Usuario): boolean {
  return Boolean(usuario.perfil.avatar) && !usuario.perfil.avatar.includes('noavatar.png');
}

function getInitials(usuario: Usuario): string {
  const nameParts = [usuario.first_name, usuario.last_name].filter(Boolean);
  const source = nameParts.length ? nameParts.join(' ') : usuario.username;

  return source
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join('');
}

async function fetchUsers(): Promise<void> {
  loading.value = true;
  error.value = '';
  try {
    usuarios.value = await listUsersService();
  } catch (requestError: any) {
    error.value = requestError?.response?.data?.error ?? 'No se pudieron cargar los usuarios';
  } finally {
    loading.value = false;
  }
}

async function saveUser(): Promise<void> {
  if (!canSubmit.value) return;

  saving.value = true;
  formError.value = '';

  try {
    if (editingUser.value) {
      const payload = new FormData();
      payload.append('nombre_usuario', form.nombre_usuario);
      payload.append('nombre', form.nombre);
      payload.append('apellidos', form.apellido);
      payload.append('email', form.email);
      payload.append('telefono', form.telefono);
      payload.append('bio', form.bio);
      payload.append('admin', String(form.admin));

      await updateProfileService(editingUser.value.username, payload);
    } else {
      await createUserService({
        nombre_usuario: form.nombre_usuario,
        contraseña: form.contraseña,
        nombre: form.nombre,
        apellido: form.apellido,
        email: form.email,
        telefono: form.telefono,
        bio: form.bio,
        admin: form.admin,
      });
    }

    modalOpen.value = false;
    await fetchUsers();
  } catch (requestError: any) {
    formError.value = requestError?.response?.data?.error ?? 'No se pudo guardar el usuario';
  } finally {
    saving.value = false;
  }
}

async function removeUser(usuario: Usuario): Promise<void> {
  if (usuario.id === authStore.user?.id) return;
  if (!window.confirm(`Eliminar el usuario ${usuario.username}?`)) return;

  try {
    await deleteUserService(usuario.username);
    await fetchUsers();
  } catch (requestError: any) {
    error.value = requestError?.response?.data?.error ?? 'No se pudo eliminar el usuario';
  }
}

onMounted(fetchUsers);
</script>
