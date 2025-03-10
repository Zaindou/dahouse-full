<template>
    <div>
        <!-- Botón toggle -->
        <button @click="$emit('toggle-sidebar')"
            class="fixed z-20 p-2 text-white transition-colors duration-200 rounded-lg md:hidden top-4 left-4 bg-gray-800/90 backdrop-blur-sm hover:bg-gray-700"
            :aria-expanded="isSidebarOpen" aria-controls="mobile-sidebar">
            <Icon :name="isSidebarOpen ? 'ic:round-close' : 'ic:sharp-menu'"
                class="w-6 h-6 transition-transform duration-200" :class="{ 'rotate-90': isSidebarOpen }" />
        </button>

        <!-- Sidebar -->
        <aside id="mobile-sidebar"
            class="fixed inset-y-0 left-0 z-40 flex flex-col transition-transform duration-300 ease-in-out border-r bg-gray-800/95 backdrop-blur-sm border-gray-700/50"
            :class="{ '-translate-x-full': !isSidebarOpen, 'translate-x-0': isSidebarOpen }">
            <div class="flex flex-col h-full">
                <!-- Header -->
                <div class="flex items-center justify-between p-4 border-b border-gray-700/50">
                    <div class="flex items-center space-x-3">
                        <span class="text-xl font-semibold text-white">DAHOUSE</span>
                    </div>
                </div>

                <!-- Navegación -->
                <nav class="flex-1 px-2 py-4 space-y-1">
                    <SidebarNavigation @link-click="$emit('link-click')" :is-sidebar-open="isSidebarOpen" />
                </nav>

                <!-- Footer con información del usuario y la versión -->
                <div class="p-4 border-t border-gray-700/50">
                    <div class="flex items-center space-x-3">
                        <img class="w-8 h-8 rounded-full"
                            :src="`https://ui-avatars.com/api/?name=${userName}&background=random`" alt="Avatar" />
                        <div class="flex-1 min-w-0">
                            <p class="text-sm font-medium text-white truncate">{{ userName }}</p>
                            <p class="text-xs text-gray-400 truncate">{{ mail }}</p>
                        </div>
                    </div>
                    <!-- Versión del frontend -->
                    <div v-if="isLoading" class="mt-2 text-xs text-center text-gray-400 opacity-70">
                        Cargando versiones...
                    </div>
                    <div v-else-if="error" class="mt-2 text-xs text-center text-red-400 opacity-70">
                        Error al cargar versiones
                    </div>
                    <div v-else class="mt-2 text-xs text-center text-gray-400 opacity-70">
                        API {{ apiVersion }} - Frontend {{ frontVersion }}
                    </div>
                </div>
            </div>
        </aside>

        <!-- Overlay -->
        <div v-if="isSidebarOpen" @click="$emit('close-sidebar')"
            class="fixed inset-0 z-30 bg-gray-900/60 backdrop-blur-sm"></div>
    </div>
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