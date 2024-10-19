<template>
    <div class="mt-4 flex flex-col sm:flex-row justify-between items-center">
        <div class="mb-4 sm:mb-0">
            <span class="mr-2">Filas por página:</span>
            <select :value="perPage" @change="$emit('update:perPage', parseInt($event.target.value))"
                class="border rounded p-1">
                <option :value="10">10</option>
                <option :value="20">20</option>
                <option :value="50">50</option>
            </select>
        </div>
        <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button @click="$emit('update:currentPage', currentPage - 1)" :disabled="currentPage === 1"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                    Anterior
                </button>
                <button @click="$emit('update:currentPage', currentPage + 1)" :disabled="currentPage === totalPages"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                    Siguiente
                </button>
            </nav>
        </div>
    </div>
</template>

<script setup>
defineProps({
    currentPage: Number,
    perPage: Number,
    totalPages: Number
})

defineEmits(['update:currentPage', 'update:perPage'])
</script>