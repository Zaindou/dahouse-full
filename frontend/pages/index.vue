<template>
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 to-gray-800 p-4">
        <div class="w-full max-w-md bg-gray-800 rounded-xl shadow-xl overflow-hidden">
            <!-- Logo Section -->
            <div class="pt-8 px-6">
                <div class="flex justify-center">
                    <!-- Puedes reemplazar la URL con la de tu logo -->
                    <img src="assets/dh-white.png" alt="Logo" class="h-11 w-auto" />
                </div>
            </div>

            <!-- Header -->
            <div class="p-6 space-y-1">
                <h2 class="text-2xl font-bold text-center text-white">Bienvenido</h2>
                <p class="text-gray-400 text-center text-sm">
                    Ingresa tus credenciales para acceder
                </p>
            </div>

            <!-- Form -->
            <div class="p-6 pt-2">
                <form @submit.prevent="handleLogin" class="space-y-4">
                    <div class="space-y-2">
                        <label for="username" class="block text-sm font-medium text-gray-200">
                            Usuario
                        </label>
                        <input id="username" v-model="credentials.nombre_usuario" type="text" required
                            :disabled="isLoading" placeholder="Nombre de usuario"
                            class="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 transition-colors duration-200" />
                    </div>

                    <div class="space-y-2">
                        <label for="password" class="block text-sm font-medium text-gray-200">
                            Contraseña
                        </label>
                        <input id="password" v-model="credentials.password" type="password" required
                            :disabled="isLoading" placeholder="••••••••"
                            class="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 transition-colors duration-200" />
                    </div>

                    <!-- Error Message -->
                    <TransitionRoot appear :show="!!errorMessage">
                        <div v-if="errorMessage"
                            class="bg-red-900/50 border border-red-500 text-red-200 px-4 py-2 rounded-md text-sm">
                            {{ errorMessage }}
                        </div>
                    </TransitionRoot>

                    <!-- Login Button -->
                    <button type="submit" :disabled="isLoading"
                        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-800 disabled:opacity-50 transition-all duration-200 relative">
                        <!-- Loading Spinner -->
                        <span v-if="isLoading" class="absolute left-4 top-1/2 -translate-y-1/2">
                            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                                viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                </path>
                            </svg>
                        </span>
                        <!-- Lock Icon -->
                        <span v-else class="absolute left-4 top-1/2 -translate-y-1/2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" stroke-width="2">
                                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                                <path d="M7 11V7a5 5 0 0110 0v4"></path>
                            </svg>
                        </span>
                        <span class="ml-6">
                            {{ isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
                        </span>
                    </button>

                    <!-- Footer -->
                    <div class="mt-6 text-center">
                        <NuxtLink to="/recuperar-password"
                            class="text-blue-400 hover:text-blue-300 transition-colors duration-200 text-sm font-medium">
                            ¿Olvidaste tu contraseña?
                        </NuxtLink>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { TransitionRoot } from '@headlessui/vue'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const credentials = ref({
    nombre_usuario: '',
    password: ''
})
const errorMessage = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
    if (isLoading.value) return

    try {
        isLoading.value = true
        errorMessage.value = ''

        const success = await authStore.login(credentials.value)

        if (success) {
            await navigateTo('/dashboard')
        } else {
            errorMessage.value = 'Nombre de usuario o contraseña incorrectos.'
        }
    } catch (error) {
        console.error('Error de inicio de sesión:', error)
        errorMessage.value = 'Ocurrió un error al intentar iniciar sesión. Por favor, inténtalo de nuevo.'
    } finally {
        isLoading.value = false
    }
}
</script>

<style scoped>
/* Animación para el mensaje de error */
.v-enter-active,
.v-leave-active {
    transition: all 0.3s ease;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}
</style>