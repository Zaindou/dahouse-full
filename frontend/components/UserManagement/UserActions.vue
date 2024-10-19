<template>
    <div class="mb-4 flex flex-col sm:flex-row justify-between items-center">
        <button @click="$emit('nuevo-modelo')"
            class="w-full sm:w-auto bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-105 mb-4 sm:mb-0">
            <i class="fas fa-user-plus mr-2"></i>
            <span class="hidden sm:inline">Crear usuario</span>
            <span class="sm:hidden">Crear usuario</span>
        </button>
        <div class="relative w-full sm:w-auto">
            <input type="text" :value="searchQuery" @input="$emit('update:searchQuery', $event.target.value)"
                placeholder="Buscar usuarios..."
                class="w-full sm:w-64 pl-10 pr-4 py-2 border rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-blue-300 transition duration-150 ease-in-out"
                aria-label="Buscar usuarios">
            <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
        </div>
    </div>
</template>

<script setup>
defineProps({
    searchQuery: String
})

defineEmits(['nuevo-modelo', 'update:searchQuery'])
</script>