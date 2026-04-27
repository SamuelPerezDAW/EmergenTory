<template>
  <section v-if="user" class="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
    <article class="rounded-[2rem] bg-slate-900 p-6 text-white shadow-sm">
      <img :src="user.perfil.avatar" :alt="user.username" class="h-28 w-28 rounded-[2rem] object-cover" />
      <p class="mt-5 text-xs uppercase tracking-[0.35em] text-brand-100">Perfil</p>
      <h2 class="mt-2 text-3xl font-semibold">{{ user.first_name }} {{ user.last_name }}</h2>
      <p class="mt-2 text-slate-300">{{ user.email }}</p>
      <p class="mt-6 rounded-2xl bg-white/10 p-4 text-sm leading-6 text-slate-200">{{ user.perfil.bio }}</p>
      <p>{{ user.perfil.admin ? 'Administrador' : 'Operador' }}</p>
    </article>

    <article class="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
      <p class="text-xs uppercase tracking-[0.35em] text-brand-600">Datos de usuario</p>
      <h2 class="mt-2 text-2xl font-semibold text-slate-900">Información operativa</h2>

      <dl class="mt-6 grid gap-4 sm:grid-cols-2">
        <div class="rounded-2xl bg-slate-50 p-4 w-fit">
          <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Usuario</dt>
          <input v-model="nombre_usuario" class="mt-2 text-lg font-semibold text-slate-900"/>
        </div>

        <div>
          <div class="rounded-2xl bg-slate-50 p-4 w-fit">
            <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Email</dt>
            <input v-model="email" class="mt-2 text-lg font-semibold text-slate-900"/>
          </div>
          <dd v-if="emailError != ''" class="rounded border border-2 border-red/50 p-2 my-2">{{ emailError }}</dd>
        </div>

        <div>
          <div class="rounded-2xl bg-slate-50 p-4 w-fit">
            <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Teléfono</dt>
            <input type="tel" v-model="telefono" class="mt-2 text-lg font-semibold text-slate-900"></input>
          </div>
          <dd v-if="phoneError != ''" class="rounded border border-2 border-red/50 p-2 my-2">{{ phoneError }}</dd>
        </div>

        <div class="rounded-2xl bg-slate-50 p-4 w-fit">
          <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Rol</dt>
          <dd class="mt-2 text-lg font-semibold text-slate-900">{{ user.perfil.admin ? 'Administrador' : 'Operador' }}</dd>
        </div>
      </dl>    
      <button @click="validatePayload()">Guardar</button>
    </article>
  </section>
</template>

<script setup lang="ts">
  import { storeToRefs } from 'pinia';
  import { useAuthStore } from '@/stores/auth';
  import { ref } from 'vue';

  async function onSaveProfile(): Promise<void> {
    console.log("OnSaveProfile: He entrado")
  }

  function validatePayload(): void {
    const regexEmail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (!regexEmail.test(email.value)) {
      emailError.value = 'El formato del correo electrónico no es válido';

    } else {
      emailError.value = '';
    }    

    if (telefono.value.length !== 9) {
      phoneError.value = 'El teléfono solo debe de tener 9 números';
    }

    for (const letter of telefono.value) {
      if ("abcdefghijklmnñopqrstuvwxyzáéíóú".includes(letter)) {
        phoneError.value = 'El teléfono solo debe de tener 9 números';
      }
    }

    if (phoneError.value !== '' || emailError.value !== '') {
      return;
    }

    console.log("ValidatePayload: Todo bien")

    phoneError.value = '';
    emailError.value = '';
    console.log("hola")
    onSaveProfile()
  } 

  const authStore = useAuthStore();
  const { user } = storeToRefs(authStore);

  let nombre_usuario = ref<string>(user.value?.username ?? '');
  let email = ref<string>(user.value?.email ?? '');
  let telefono = ref<string>(user.value?.perfil.telefono ?? '');

  let emailError = ref<string>('');
  let phoneError = ref<string>('');
</script>
