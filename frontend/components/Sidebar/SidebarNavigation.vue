<template>
    <nav class="flex-grow">
        <SidebarLink v-for="link in links" :key="link.to" v-bind="link" :isSidebarOpen="isSidebarOpen"
            @click="$emit('linkClick')" />
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