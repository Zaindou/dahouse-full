<template>
    <div class="flex h-screen">
        <!-- Botón móvil con animación -->
        <button @click="toggleSidebar"
            class="fixed z-20 p-2 text-white transition-colors duration-200 rounded-lg md:hidden top-4 left-4 bg-gray-800/90 backdrop-blur-sm hover:bg-gray-700"
            :aria-expanded="isSidebarOpen" aria-controls="sidebar">
            <Icon :name="isSidebarOpen ? 'ic:round-close' : 'ic:sharp-menu'"
                class="w-6 h-6 transition-transform duration-200" :class="{ 'rotate-90': isSidebarOpen }" />
        </button>

        <!-- Overlay mejorado con transición -->
        <div v-if="isSidebarOpen && !isLargeScreen.value" @click="closeSidebar"
            class="fixed inset-0 z-30 bg-gray-900/60 backdrop-blur-sm md:hidden" aria-hidden="true">
        </div>

        <!-- Sidebar con transiciones mejoradas -->
        <aside :class="[
            'fixed md:relative inset-y-0 left-0 z-40',
            'flex flex-col h-full bg-gray-800/95 backdrop-blur-sm',
            'border-r border-gray-700/50',
            'transition-all duration-300 ease-in-out',
            isSidebarOpen ? 'w-72' : 'w-0 md:w-20',
            'md:transform md:translate-x-0',
            isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        ]">
            <!-- Contenido del Sidebar -->
            <div
                class="flex flex-col flex-grow overflow-y-auto scrollbar-thin scrollbar-track-gray-800 scrollbar-thumb-gray-700">
                <!-- Header del Sidebar -->
                <div class="flex items-center justify-between p-4 border-b border-gray-700/50">
                    <div :class="[
                        'transition-opacity duration-200',
                        isSidebarOpen ? 'opacity-100' : 'opacity-0 md:hidden'
                    ]">
                        <!-- Logo y Nombre -->
                        <div class="flex items-center space-x-3">
                            <span class="text-xl font-semibold text-white">DAHOUSE</span>
                        </div>
                    </div>

                    <!-- Botón toggle para desktop -->
                    <button @click="toggleSidebar"
                        class="items-center justify-center hidden w-8 h-8 text-gray-400 transition-colors duration-200 rounded-md md:flex hover:bg-gray-700 hover:text-white">
                        <Icon
                            :name="isSidebarOpen ? 'ic:round-keyboard-double-arrow-left' : 'ic:round-keyboard-double-arrow-right'"
                            class="w-5 h-5" />
                    </button>
                </div>

                <!-- Navegación -->
                <nav class="flex-1 px-2 py-4 space-y-1">
                    <SidebarNavigation :is-sidebar-open="isSidebarOpen" @link-click="handleLinkClick" />
                </nav>

                <!-- Footer del Sidebar -->
                <div class="p-4 border-t border-gray-700/50">
                    <div v-if="isSidebarOpen" class="flex items-center space-x-3">
                        <img class="w-8 h-8 rounded-full"
                            :src="`https://ui-avatars.com/api/?name=${userName}&background=random`" alt="Avatar">
                        <div class="flex-1 min-w-0">
                            <p class="text-sm font-medium text-white truncate">
                                {{ userName }}
                            </p>
                            <p class="text-xs text-gray-400 truncate">
                                {{ mail }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </aside>

        <!-- Contenido principal -->
        <main class="flex-1 overflow-auto">
            <slot />
        </main>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useMediaQuery } from '@vueuse/core'
import { useRoute } from 'vue-router'
import { useAuthStore } from '~/stores/auth'
import { computed } from "vue"

const route = useRoute()
const authStore = useAuthStore()

const userName = computed(() => authStore.userName)
const mail = computed(() => authStore.mail)

const isSidebarOpen = ref(false) // Cambiado a false por defecto
const isLargeScreen = useMediaQuery('(min-width: 768px)')

// Inicializar el estado del sidebar basado en el tamaño de pantalla
if (isLargeScreen.value) {
    isSidebarOpen.value = true
}

// Observar cambios en la ruta
watch(
    () => route.path,
    () => {
        if (!isLargeScreen.value) {
            isSidebarOpen.value = false
        }
    }
)

// Observar cambios en el tamaño de pantalla
watch(isLargeScreen, (isLarge) => {
    if (isLarge) {
        isSidebarOpen.value = true
    } else {
        isSidebarOpen.value = false
    }
}, { immediate: false }) // Agregado immediate: false para evitar que se ejecute al inicio

const toggleSidebar = () => {
    isSidebarOpen.value = !isSidebarOpen.value
}

const closeSidebar = () => {
    if (!isLargeScreen.value) {
        isSidebarOpen.value = false
    }
}

const handleLinkClick = () => {
    closeSidebar()
}
</script>

<style scoped>
.scrollbar-thin::-webkit-scrollbar {
    width: 6px;
}

.scrollbar-track-gray-800::-webkit-scrollbar-track {
    background: #1f2937;
}

.scrollbar-thumb-gray-700::-webkit-scrollbar-thumb {
    background: #374151;
    border-radius: 3px;
}

.scrollbar-thumb-gray-700::-webkit-scrollbar-thumb:hover {
    background: #4b5563;
}
</style>