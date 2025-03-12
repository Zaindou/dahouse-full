<template>
    <div class="flex items-center justify-center min-h-screen p-4 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        <!-- Efecto de fondo con blur -->
        <div class="absolute inset-0 bg-grid-white/[0.02] bg-grid" aria-hidden="true"></div>
        <div class="absolute inset-0 bg-gradient-to-b from-gray-900/30 via-gray-900/80 to-gray-900/30 backdrop-blur-sm"></div>

        <!-- Card principal -->
        <div class="relative w-full max-w-md">
            <!-- Efectos de resplandor -->
            <div class="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl opacity-20 blur"></div>
            <div class="relative overflow-hidden bg-gray-900 border border-gray-800 shadow-2xl rounded-xl">
                <!-- Logo Section con animación -->
                <div class="px-6 pt-8">
                    <div class="flex justify-center transition-transform duration-300 transform hover:scale-105">
                        <img src="assets/dh-white.png" alt="Logo" class="w-auto h-12 drop-shadow-2xl" />
                    </div>
                </div>

                <!-- Header con mejor tipografía -->
                <div class="p-6 space-y-2">
                    <h2 class="text-3xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
                        Restablecer Contraseña
                    </h2>
                    <p class="text-sm font-medium text-center text-gray-400">
                        Ingresa tu nombre de usuario y te enviaremos un correo con las instrucciones
                    </p>
                </div>

                <!-- Form con mejor interactividad -->
                <div class="p-6 pt-2">
                    <form @submit.prevent="handleResetPassword" class="space-y-5">
                        <!-- Campo Usuario -->
                        <div class="space-y-2">
                            <label for="username" class="block text-sm font-medium text-gray-300">
                                Usuario
                            </label>
                            <div class="relative group">
                                <div class="absolute inset-0 transition-opacity duration-300 rounded-lg opacity-50 bg-gradient-to-r from-blue-500 to-purple-600 blur-sm group-hover:opacity-100 -z-10"></div>
                                <input 
                                    id="username" 
                                    v-model="username" 
                                    type="text" 
                                    required
                                    :disabled="isLoading" 
                                    placeholder="Nombre de usuario"
                                    class="w-full px-4 py-2.5 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 transition-all duration-200" 
                                />
                            </div>
                        </div>

                        <!-- Mensajes de Estado -->
                        <TransitionRoot appear :show="!!errorMessage" as="div"
                            enter="transform transition-all duration-300"
                            enter-from="opacity-0 translate-y-4"
                            enter-to="opacity-100 translate-y-0"
                            leave="transform transition-all duration-300"
                            leave-from="opacity-100 translate-y-0"
                            leave-to="opacity-0 translate-y-4">
                            <div v-if="errorMessage"
                                class="px-4 py-3 text-sm text-red-200 border rounded-lg bg-red-500/10 border-red-500/50">
                                {{ errorMessage }}
                            </div>
                        </TransitionRoot>

                        <TransitionRoot appear :show="!!successMessage" as="div"
                            enter="transform transition-all duration-300"
                            enter-from="opacity-0 translate-y-4"
                            enter-to="opacity-100 translate-y-0"
                            leave="transform transition-all duration-300"
                            leave-from="opacity-100 translate-y-0"
                            leave-to="opacity-0 translate-y-4">
                            <div v-if="successMessage"
                                class="px-4 py-3 text-sm text-green-200 border rounded-lg bg-green-500/10 border-green-500/50">
                                {{ successMessage }}
                            </div>
                        </TransitionRoot>

                        <!-- Botón de Enviar -->
                        <button type="submit" :disabled="isLoading"
                            class="relative w-full overflow-hidden rounded-lg group">
                            <!-- Fondo animado -->
                            <div class="absolute inset-0 transition-transform duration-300 bg-gradient-to-r from-blue-600 to-purple-600 group-hover:scale-105"></div>
                            <!-- Contenido del botón -->
                            <div class="relative flex items-center justify-center px-4 py-3 space-x-2 transition-all duration-300 bg-gradient-to-r from-blue-500 to-purple-600 group-hover:bg-opacity-90">
                                <!-- Loading Spinner -->
                                <span v-if="isLoading" 
                                    class="w-5 h-5 animate-spin">
                                    <svg class="text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                </span>
                                <!-- Email Icon -->
                                <span v-else class="text-white">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                                        <polyline points="22,6 12,13 2,6"></polyline>
                                    </svg>
                                </span>
                                <span class="font-medium text-white">
                                    {{ isLoading ? 'Enviando...' : 'Enviar Instrucciones' }}
                                </span>
                            </div>
                        </button>

                        <!-- Footer con mejor diseño -->
                        <div class="mt-6 text-center">
                            <NuxtLink to="/login"
                                class="relative inline-block group">
                                <span class="relative z-10 text-sm font-medium text-blue-400 transition-colors duration-200 group-hover:text-blue-300">
                                    Volver al inicio de sesión
                                </span>
                                <div class="absolute inset-x-0 bottom-0 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300"></div>
                            </NuxtLink>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { TransitionRoot } from '@headlessui/vue'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const username = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)

const handleResetPassword = async () => {
    if (isLoading.value) return

    try {
        isLoading.value = true
        errorMessage.value = ''
        successMessage.value = ''

        // Aquí deberías llamar a tu función de reset password del store
        const success = await authStore.resetPassword(username.value)

        if (success) {
            successMessage.value = 'Se han enviado las instrucciones a tu correo electrónico.'
            username.value = '' // Limpiar el campo
        } else {
            errorMessage.value = 'No se encontró ninguna cuenta con ese nombre de usuario.'
        }
    } catch (error) {
        console.error('Error al restablecer contraseña:', error)
        errorMessage.value = 'Ocurrió un error al intentar procesar tu solicitud. Por favor, inténtalo de nuevo.'
    } finally {
        isLoading.value = false
    }
}
</script>

<style>
/* Patrón de fondo */
.bg-grid {
    background-size: 40px 40px;
    background-image: 
        linear-gradient(to right, rgb(255 255 255 / 0.05) 1px, transparent 1px),
        linear-gradient(to bottom, rgb(255 255 255 / 0.05) 1px, transparent 1px);
}
</style>