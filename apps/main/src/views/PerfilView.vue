<template>
  <section v-if="user" class="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
    <article class="rounded-[2rem] bg-slate-900 p-6 text-white shadow-sm">
      <img :src="user.perfil.avatar" :alt="user.username" class="h-28 w-28 rounded-[2rem] object-cover" />
      <p class="mt-5 text-xs uppercase tracking-[0.35em] text-brand-100">Perfil</p>
      <h2 class="mt-2 text-3xl font-semibold">{{ user.first_name }} {{ user.last_name }}</h2>
      <p class="mt-2 text-slate-300">{{ user.email }}</p>
      <p class="mt-6 rounded-2xl bg-white/10 p-4 text-sm leading-6 text-slate-200">{{ user.perfil.bio }}</p>
    </article>

    <article class="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
      <p class="text-xs uppercase tracking-[0.35em] text-brand-600">Datos de usuario</p>
      <h2 class="mt-2 text-2xl font-semibold text-slate-900">Información operativa</h2>

      <form action="">
        <dl class="mt-6 grid gap-4 sm:grid-cols-2">
          <div class="rounded-2xl bg-slate-50 p-4">
            <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Usuario</dt>
            <input v-model="nombre_usuario" class="mt-2 text-lg font-semibold text-slate-900"/>
          </div>
          
          <div class="rounded-2xl bg-slate-50 p-4">
            <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Email</dt>
            <input type="email" v-model="email" class="mt-2 text-lg font-semibold text-slate-900"/>
          </div>

          <div class="rounded-2xl bg-slate-50 p-4">
            <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Teléfono</dt>
            <input type="tel" @input="validatePhoneNumber()" v-model="telefono" class="mt-2 text-lg font-semibold text-slate-900"></input>
            <dd v-if="error != ''" class="rounded border border-2 border-red/50 p-2 my-2">{{ error }}</dd>
          </div>

          <div class="rounded-2xl bg-slate-50 p-4">
            <dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Rol</dt>
            <dd class="mt-2 text-lg font-semibold text-slate-900">{{ user.perfil.admin ? 'Administrador' : 'Operador' }}</dd>
          </div>
        </dl>    
        <button v-bind:disabled="disableSubmit">Guardar</button>  
      </form>
    </article>
  </section>
</template>

<script setup lang="ts">
  import { storeToRefs } from 'pinia';
  import { useAuthStore } from '@/stores/auth';
  import { ref } from 'vue';

  function validatePhoneNumber(): void {
    if (telefono.value.length !== 9) {
        error.value = 'El teléfono solo debe de tener 9 números';
        disableSubmit.value = true;
        return;
    }

    for (const letter of telefono.value) {
      if ("abcdefghijklmnñopqrstuvwxyzáéíóú".includes(letter)) {
        error.value = 'El teléfono solo debe de tener 9 números';
        disableSubmit.value = true;
        return;
      }
    }
    error.value = '';
    disableSubmit.value = false;
  } 

  const authStore = useAuthStore();
  const { user } = storeToRefs(authStore);

  let nombre_usuario = ref<string>(user.value?.username ?? '');
  let email = ref<string>(user.value?.email ?? '');
  let telefono = ref<string>(user.value?.perfil.telefono ?? '');

  let error = ref<string>('');
  let disableSubmit = ref<boolean>(false);

</script>
