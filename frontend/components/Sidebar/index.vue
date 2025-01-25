<template>
    <div class="flex h-screen">
        <!-- Sidebar dinámico -->
        <SidebarMobile v-if="!isLargeScreen" :is-sidebar-open="isSidebarOpen" :user-name="userName" :mail="mail"
            @toggle-sidebar="toggleSidebar" @close-sidebar="closeSidebar" @link-click="handleLinkClick" />
        <SidebarDesktop v-else :is-sidebar-open="isSidebarOpen" :user-name="userName" :mail="mail"
            @toggle-sidebar="toggleSidebar" />

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
import SidebarMobile from '~/components/Sidebar/SidebarMobile.vue'
import SidebarDesktop from '~/components/Sidebar/SidebarDesktop.vue'

const route = useRoute()
const authStore = useAuthStore()

const userName = computed(() => authStore.userName)
const mail = computed(() => authStore.mail)

const isSidebarOpen = ref(false) // Sidebar cerrado por defecto
const isLargeScreen = useMediaQuery('(min-width: 768px)')

// Inicializar el estado del sidebar basado en el tamaño de pantalla
const initializeSidebarState = () => {
    isSidebarOpen.value = isLargeScreen.value
}
initializeSidebarState()

// Observar cambios en la ruta para cerrar el sidebar solo en móvil
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
    isSidebarOpen.value = isLarge
})

// Alternar el estado del sidebar
const toggleSidebar = () => {
    isSidebarOpen.value = !isSidebarOpen.value
}

// Cerrar el sidebar explícitamente
const closeSidebar = () => {
    if (!isLargeScreen.value) {
        isSidebarOpen.value = false
    }
}

// Cerrar el sidebar al hacer clic en un enlace
const handleLinkClick = () => {
    closeSidebar()
}
</script>
