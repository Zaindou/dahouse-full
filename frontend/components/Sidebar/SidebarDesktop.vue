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
            <button @click="$emit('toggle-sidebar')"
                class="items-center justify-center hidden w-8 h-8 transition-all duration-300 rounded-lg md:flex hover:bg-gray-700/50 hover:shadow-lg hover:shadow-purple-500/10 group"
                :class="isSidebarOpen ? 'text-gray-400 hover:text-white' : 'text-purple-400 hover:text-white'">
                <Icon
                    :name="isSidebarOpen ? 'ic:round-keyboard-double-arrow-left' : 'ic:round-keyboard-double-arrow-right'"
                    class="w-5 h-5 transition-transform duration-300 group-hover:scale-110" />
            </button>
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
                    </div>
                </div>
                <!-- Información del usuario visible solo cuando está abierto -->
                <div v-if="isSidebarOpen" class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-white truncate">{{ userName }}</p>
                    <p class="text-xs text-gray-400 truncate">{{ mail }}</p>
                </div>
            </div>

            <!-- Versión con diseño adaptativo -->
            <div v-if="isSidebarOpen" class="mt-4 text-xs text-center">
                <span class="px-3 py-1 text-gray-400 border rounded-full bg-gray-800/50 border-gray-700/30">
                    API 1.5.0 - Frontend 1.5.0
                </span>
            </div>
        </div>
    </aside>
</template>

<script setup>
defineProps({
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
})
</script>