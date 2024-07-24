<template>
    <div>
        <!-- Botón para mostrar/ocultar el sidebar en móviles -->
        <button @click="toggleSidebar" class="md:hidden fixed top-4 left-4 z-20 bg-gray-800 text-white p-2 rounded">
            <Icon name="ic:sharp-menu" class="w-6 h-6" />
        </button>

        <!-- Overlay para cerrar el sidebar en móviles -->
        <div v-if="isSidebarOpen" @click="closeSidebar" class="fixed inset-0 bg-black bg-opacity-50 z-30 md:hidden">
        </div>

        <!-- Sidebar -->
        <div :class="[
            'fixed md:static inset-y-0 left-0 z-40 transition-all duration-300 ease-in-out',
            'flex flex-col h-full py-4 px-3 bg-gray-800',
            isSidebarOpen ? 'w-64' : 'w-0 md:w-16',
            'md:transform md:translate-x-0',
            isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        ]">
            <div class="flex items-center justify-between mb-6">
                <h1
                    :class="['text-white font-bold transition-all duration-300 ease-in-out', isSidebarOpen ? 'text-2xl' : 'text-xs md:text-2xl']">
                    {{ isSidebarOpen ? 'DAHOUSE' : 'DH' }}
                </h1>
                <button @click="toggleSidebar" class="text-white hidden md:block">
                    <Icon :name="isSidebarOpen ? 'ic:baseline-chevron-left' : 'ic:baseline-chevron-right'"
                        class="w-6 h-6" />
                </button>
            </div>

            <nuxt-link to="/" :class="linkClasses" @click="handleLinkClick">
                <Icon name="ic:sharp-menu" :class="iconClasses" />
                <span :class="{ 'hidden': !isSidebarOpen }">Inicio</span>
            </nuxt-link>
            <nuxt-link to="/admcreadoras" :class="linkClasses" @click="handleLinkClick">
                <Icon name="ic:sharp-people" :class="iconClasses" />
                <span :class="{ 'hidden': !isSidebarOpen }">Usuarios</span>
            </nuxt-link>
            <nuxt-link to="/prestamos" :class="linkClasses" @click="handleLinkClick">
                <Icon name="material-symbols:account-balance" :class="iconClasses" />
                <span :class="{ 'hidden': !isSidebarOpen }">Deducción</span>
            </nuxt-link>
            <nuxt-link to="/liquidacion" :class="linkClasses" @click="handleLinkClick">
                <Icon name="ic:sharp-attach-money" :class="iconClasses" />
                <span :class="{ 'hidden': !isSidebarOpen }">Liquidación</span>
            </nuxt-link>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const isSidebarOpen = ref(true);

const toggleSidebar = () => {
    isSidebarOpen.value = !isSidebarOpen.value;
};

const closeSidebar = () => {
    if (window.innerWidth < 768) {  // 768px es el breakpoint para 'md' en Tailwind por defecto
        isSidebarOpen.value = false;
    }
};

const handleLinkClick = () => {
    closeSidebar();
};

const linkClasses = computed(() => [
    'flex items-center text-white p-2 mb-2 rounded hover:bg-gray-700',
    { 'justify-center': !isSidebarOpen.value }
]);

const iconClasses = computed(() => [
    'menu-icon transition-all duration-300 ease-in-out',
    isSidebarOpen.value ? 'mr-2' : 'mr-0 w-6 h-6'
]);
</script>

<style scoped>
.menu-icon {
    width: 25px;
    height: 25px;
}
</style>