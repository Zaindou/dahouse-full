<template>
    <div class="h-screen flex">
        <!-- Botón para mostrar/ocultar el sidebar en móviles -->
        <button @click="toggleSidebar" class="md:hidden fixed top-4 left-4 z-20 bg-gray-800 text-white p-2 rounded">
            <Icon name="ic:sharp-menu" class="w-6 h-6" />
        </button>

        <!-- Overlay para cerrar el sidebar en móviles -->
        <div v-if="isSidebarOpen" @click="closeSidebar" class="fixed inset-0 bg-black bg-opacity-50 z-30 md:hidden" />

        <!-- Sidebar -->
        <aside :class="[
            'fixed md:relative inset-y-0 left-0 z-40 transition-all duration-300 ease-in-out',
            'flex flex-col h-full bg-gray-800',
            isSidebarOpen ? 'w-64' : 'w-0 md:w-16',
            'md:transform md:translate-x-0',
            isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        ]">
            <div class="flex-grow flex flex-col">
                <SidebarHeader :is-sidebar-open="isSidebarOpen" @toggle="toggleSidebar" />
                <SidebarNavigation :is-sidebar-open="isSidebarOpen" @link-click="handleLinkClick" />
            </div>
        </aside>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMediaQuery } from '@vueuse/core'

const isSidebarOpen = ref(true)
const isLargeScreen = useMediaQuery('(min-width: 768px)')

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