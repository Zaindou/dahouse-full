<template>
    <aside id="desktop-sidebar"
        class="relative flex flex-col h-full transition-all duration-500 ease-in-out border-r bg-gradient-to-b from-gray-900 to-gray-800 backdrop-blur-xl border-gray-700/30"
        :class="[isSidebarOpen ? 'w-72' : 'w-20', 'group']">

        <!-- Efecto de resplandor en el borde -->
        <div class="absolute inset-y-0 right-0 w-px bg-gradient-to-b from-gray-700/50 via-purple-500/20 to-gray-700/50">
        </div>

        <!-- Header con logo adaptativo -->
        <div class="flex items-center justify-between p-6 border-b border-gray-700/30">
            <div class="flex items-center overflow-hidden transition-all duration-500"
                :class="isSidebarOpen ? 'w-full space-x-3' : 'w-8'">
                <!-- Logo que cambia entre texto completo y solo inicial -->
                <span v-if="isSidebarOpen"
                    class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-300">
                    DAHOUSE
                </span>
                <span v-else class="text-2xl font-bold text-white">D</span>
            </div>
        </div>

        <!-- Navegación con iconos centrados cuando está cerrado -->
        <nav
            class="flex-1 px-4 py-6 space-y-2 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-transparent">
            <SidebarNavigation :is-sidebar-open="isSidebarOpen" />
        </nav>

        <!-- Footer con avatar centrado cuando está cerrado -->
        <div class="p-6 border-t border-gray-700/30 bg-gray-900/50">
            <div class="flex items-center" :class="isSidebarOpen ? 'space-x-4' : 'justify-center'">
                <div class="relative group">
                    <img class="w-10 h-10 transition-transform duration-300 rounded-lg ring-2 ring-purple-500/20 group-hover:scale-105"
                        :src="`https://ui-avatars.com/api/?name=${userName}&background=random`" alt="Avatar" />
                    <div class="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-gray-900 rounded-full">
                    </div>

                    <!-- Tooltip que aparece solo cuando está cerrado -->
                    <div v-if="!isSidebarOpen"
                        class="absolute z-50 px-3 py-2 ml-4 transition-opacity duration-300 bg-gray-800 rounded-lg shadow-lg opacity-0 left-full group-hover:opacity-100 whitespace-nowrap">
                        <p class="text-sm font-medium text-white">{{ userName }}</p>
                        <p class="text-xs text-gray-400">{{ mail }}</p>
                        <!-- Versión en tooltip -->
                        <p v-if="isLoading" class="mt-1 text-xs text-gray-400">Cargando versiones...</p>
                        <p v-else-if="error" class="mt-1 text-xs text-red-400">Error al cargar versiones</p>
                        <p v-else class="mt-1 text-xs text-gray-400">
                            API {{ version.apiVersion }} - Frontend {{ version.frontVersion }}
                        </p>
                    </div>
                </div>
                <!-- Información del usuario visible solo cuando está abierto -->
                <div v-if="isSidebarOpen" class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-white truncate">{{ userName }}</p>
                    <p class="text-xs text-gray-400 truncate">{{ mail }}</p>
                </div>
            </div>

            <!-- Versión con diseño adaptativo cuando está abierto -->
            <div v-if="isSidebarOpen" class="mt-4 text-xs text-center">
                <div v-if="isLoading" class="px-3 py-1 text-gray-400 border rounded-full bg-gray-800/50 border-gray-700/30">
                    Cargando versiones...
                </div>
                <div v-else-if="error" class="px-3 py-1 text-red-400 border rounded-full bg-gray-800/50 border-gray-700/30">
                    Error al cargar versiones
                </div>
                <span v-else class="px-3 py-1 text-gray-400 border rounded-full bg-gray-800/50 border-gray-700/30">
                    API {{ apiVersion }} - Frontend {{ frontVersion }}
                </span>
            </div>
        </div>
    </aside>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useVersionStore } from '~/stores/version';
import { storeToRefs } from 'pinia';

const props = defineProps({
    isSidebarOpen: {
        type: Boolean,
        required: true
    },
    userName: {
        type: String,
        required: true
    },
    mail: {
        type: String,
        required: true
    }
});

// Usar storeToRefs para mantener la reactividad
const versionStore = useVersionStore();
const { apiVersion, frontVersion, isLoading, error } = storeToRefs(versionStore);

// Cargar versiones al montar el componente
onMounted(async () => {
    await versionStore.fetchVersion();
});

// Recargar versiones cuando la página vuelve a estar activa
if (process.client) {
    const handleVisibilityChange = async () => {
        if (!document.hidden) {
            await versionStore.fetchVersion();
        }
    };
    
    onMounted(() => {
        document.addEventListener('visibilitychange', handleVisibilityChange);
    });
    
    onUnmounted(() => {
        document.removeEventListener('visibilitychange', handleVisibilityChange);
    });
}

// Recargar versiones periódicamente
const interval = ref(null);

onMounted(() => {
    interval.value = setInterval(async () => {
        await versionStore.fetchVersion();
    }, 5 * 60 * 1000);
});

onUnmounted(() => {
    if (interval.value) {
        clearInterval(interval.value);
    }
});
</script>