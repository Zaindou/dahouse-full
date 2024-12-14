<template>
    <nav class="flex-grow">
        <SidebarLink v-for="link in links" :key="link.to || link.text" v-bind="link" :isSidebarOpen="isSidebarOpen"
            :hasSubmenu="!!link.submenu" @click="handleClick" />
    </nav>
</template>

<script setup>
import SidebarLink from '~/components/Sidebar/SidebarLink.vue'

defineProps({
    isSidebarOpen: Boolean
})

const emit = defineEmits(['linkClick'])

const handleClick = () => {
    emit('linkClick')
}

const links = [
    {
        to: '/dashboard',
        icon: 'ic:sharp-dashboard',
        text: 'Inicio'
    },
    {
        text: 'Administración',
        icon: 'mdi:cog',
        hasSubmenu: true,
        submenu: [
            { to: '/admin/users', iconSubmenu: 'ic:sharp-people', text: 'Gestión Usuarios' },
        ]
    },
    {
        text: 'Financiero',
        icon: 'material-symbols:account-balance',
        hasSubmenu: true,
        submenu: [
            { to: '/finance/prestamos', iconSubmenu: 'iconoir:piggy-bank', text: 'Préstamos' },
            { to: '/finance/liquidacion', iconSubmenu: 'streamline:money-atm-card-3-deposit-money-payment-finance-atm-withdraw', text: 'Pagos' },
            { to: '/finance/historial-pagos', iconSubmenu: 'mingcute:bill-line', text: 'Historial de pagos' },
            { to: '/finance/simulador', iconSubmenu: 'heroicons:banknotes', text: 'Simulador' },
            // { to: '/ganancias', iconSubmenu: 'carbon:align-vertical-bottom', text: 'Ganancias' },
        ]
    },
    {
        to: '/mantenimiento',
        icon: 'mingcute:hotel-fill',
        text: 'Rooms'
    }
]
</script>