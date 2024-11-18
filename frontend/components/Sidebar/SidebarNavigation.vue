<template>
    <nav class="flex-grow">
        <SidebarLink v-for="link in links" :key="link.to" v-bind="link" :isSidebarOpen="isSidebarOpen"
            @click="$emit('linkClick')" />
        <NuxtLink v-for="item in navigationItems" :key="item.path" :to="item.path"
            class="relative flex items-center px-3 py-2 rounded-lg transition-colors duration-200 hover:bg-gray-700/50">
            <Icon :name="item.icon" class="w-5 h-5 text-gray-400" />
            <span v-if="isSidebarOpen" class="ml-3 text-sm text-gray-300">
                {{ item.name }}
            </span>
            <!-- Badge de notificación -->
            <span v-if="item.notifications"
                class="absolute right-2 top-2 h-5 min-w-[20px] flex items-center justify-center rounded-full bg-red-500 text-white text-xs px-1">
                {{ item.notifications }}
            </span>
        </NuxtLink>
    </nav>
</template>

<script setup>
import SidebarLink from '~/components/Sidebar/SidebarLink.vue'

defineProps({
    isSidebarOpen: Boolean
})

defineEmits(['linkClick'])

const links = [
    { to: '/dashboard', icon: 'ic:sharp-dashboard', text: 'Inicio' },
    { to: '/users', icon: 'ic:sharp-people', text: 'Usuarios' },
    { to: '/prestamos', icon: 'material-symbols:account-balance', text: 'Deducción' },
    { to: '/liquidacion', icon: 'ic:sharp-attach-money', text: 'Liquidación' },
    { to: '/ganancias', icon: 'carbon:align-vertical-bottom', text: 'Ganancias' },
    { to: '/mantenimiento', icon: 'mdi:tools', text: 'Mantenimiento' }
]
</script>