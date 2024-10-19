<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8 bg-gray-800 p-10 rounded-xl shadow-2xl">
            <div>
                <h2 class="mt-6 text-center text-3xl font-extrabold text-white">
                    Iniciar Sesión
                </h2>
            </div>
            <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
                <input type="hidden" name="remember" value="true" />
                <div class="rounded-md shadow-sm -space-y-px">
                    <div>
                        <label for="username" class="sr-only">Usuario</label>
                        <input v-model="credentials.nombre_usuario" id="username" name="username" type="text" required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-700 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="Nombre de usuario" />
                    </div>
                    <div>
                        <label for="password" class="sr-only">Contraseña</label>
                        <input v-model="credentials.password" id="password" name="password" type="password" required
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-600 placeholder-gray-400 text-white bg-gray-700 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                            placeholder="Contraseña" />
                    </div>
                </div>

                <div>
                    <button type="submit"
                        class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out">
                        <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                            <svg class="h-5 w-5 text-indigo-400 group-hover:text-indigo-300"
                                xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                                aria-hidden="true">
                                <path fill-rule="evenodd"
                                    d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                                    clip-rule="evenodd" />
                            </svg>
                        </span>
                        Iniciar Sesión
                    </button>
                </div>
            </form>
            <div v-if="errorMessage" class="mt-2 text-center text-sm text-red-400 bg-red-900 p-2 rounded">
                {{ errorMessage }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '~/stores/auth';

const authStore = useAuthStore();
const credentials = ref({ nombre_usuario: '', password: '' });
const errorMessage = ref('');

const handleLogin = async () => {
    try {
        const success = await authStore.login(credentials.value);
        if (success) {
            navigateTo('/dashboard'); // Redirige a la página principal o dashboard
        } else {
            errorMessage.value = 'Nombre de usuario o contraseña incorrectos.';
        }
    } catch (error) {
        errorMessage.value =
            'Ocurrió un error al intentar iniciar sesión. Por favor, inténtalo de nuevo.';
        console.error('Error de inicio de sesión:', error);
    }
};
</script>