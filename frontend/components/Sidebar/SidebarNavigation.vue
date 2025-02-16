<template>
    <nav class="flex-grow">
        <SidebarLink 
            v-for="link in filteredLinks" 
            :key="link.to || link.text" 
            v-bind="link" 
            :isSidebarOpen="isSidebarOpen"
            :hasSubmenu="!!link.submenu" 
            @click="handleClick" />
    </nav>
</template>

<script setup>
import SidebarLink from '~/components/Sidebar/SidebarLink.vue'
import { useAuthStore } from '~/stores/auth'
import { computed } from 'vue'

defineProps({
    isSidebarOpen: Boolean
})

const emit = defineEmits(['linkClick'])

const handleClick = () => {
    emit('linkClick')
}

// Obtenemos el store de autenticación para acceder al rol del usuario
const authStore = useAuthStore()
const userRole = computed(() => authStore.user?.rol) // Puede ser "Administrador", "Monitor", etc.

const links = [
    {
        to: '/dashboard',
        icon: 'ic:sharp-dashboard',
        text: 'Inicio',
        roles: ['Administrador', 'Monitor', 'Modelo', 'Inventario'] 
    },
    {
        text: 'Administración',
        icon: 'mdi:cog',
        hasSubmenu: true,
        roles: ['Administrador'], 
        submenu: [
            { to: '/admin/users', iconSubmenu: 'ic:sharp-people', text: 'Gestión Usuarios', roles: ['Administrador'] }
        ]
    },
    {
        text: 'Financiero',
        icon: 'material-symbols:account-balance',
        hasSubmenu: true,
        roles: ['Administrador', 'Monitor', 'Inventario'], 
        submenu: [
            { to: '/finance/loans', iconSubmenu: 'iconoir:piggy-bank', text: 'Préstamos', roles: ['Administrador', 'Monitor', 'Inventario'] },
            { to: '/finance/liquidacion', iconSubmenu: 'streamline:money-atm-card-3-deposit-money-payment-finance-atm-withdraw', text: 'Pagos', roles: ['Administrador'] },
            { to: '/finance/historial-pagos', iconSubmenu: 'mingcute:bill-line', text: 'Historial de pagos', roles: ['Administrador'] },
            { to: '/finance/simulador', iconSubmenu: 'heroicons:banknotes', text: 'Simulador', roles: ['Administrador', 'Monitor', 'Inventario'] }
        ]
    },
    {
        icon: 'bx:bx-bar-chart-alt-2',
        text: 'Estadísticas',
        roles: ['Administrador',],
        submenu: [
            {to: '/statistics/general-summary', iconSubmenu: 'mdi:clipboard-text-outline', text: 'Resumen General', roles: ['Administrador'] },
            {to: '/statistics/statistics-daily', iconSubmenu: 'mdi:calendar-clock-outline', text: 'Estadísticas Diarias ', roles: ['Administrador', 'Monitor', 'Inventario'] }

        ]

    },
    {
        to: '/inventory',
        icon: 'ic:outline-inventory-2',
        text: 'Inventario',
        roles: ['Administrador', 'Inventario']
    },
    {
        to: '/mantenimiento',
        icon: 'mingcute:hotel-fill',
        text: 'Rooms',
        roles: ['Administrador']
    },
]

// **Filtrar links y submenús según el rol del usuario**
const filteredLinks = computed(() => {
    return links
        .filter(link => link.roles.includes(userRole.value)) // Filtrar enlaces principales
        .map(link => ({
            ...link,
            submenu: link.submenu 
                ? link.submenu.filter(sub => sub.roles.includes(userRole.value)) // Filtrar submenús
                : null 
        }))
        .filter(link => link.submenu === null || link.submenu.length > 0); // No mostrar menús vacíos
})
</script>
