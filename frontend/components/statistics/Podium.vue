<template>
    <div class="p-6 bg-white border border-gray-100 shadow-lg rounded-xl">
        <!-- Mensaje sin datos -->
        <div v-if="data.length === 0" class="flex items-center justify-center h-32 text-gray-500 rounded-lg bg-gray-50">
            <Icon name="ph:warning-circle" class="w-5 h-5 mr-2" />
            No hay datos disponibles para los filtros seleccionados.
        </div>

        <div v-else class="flex flex-col">
            <!-- Lista de modelos paginada -->
            <div class="relative flex flex-col items-center space-y-4 min-h-[480px]">
                <div v-for="(modelo, index) in paginatedData" :key="modelo.modelo"
                    class="w-full max-w-sm p-5 transition-all duration-300 shadow-sm rounded-xl hover:shadow-md" :class="[
                        index === 0 && currentPage === 1 ? 'bg-gradient-to-br from-yellow-50 to-yellow-100 border-2 border-yellow-200' :
                            index === 1 && currentPage === 1 ? 'bg-gradient-to-br from-gray-50 to-gray-100 border-2 border-gray-200' :
                                index === 2 && currentPage === 1 ? 'bg-gradient-to-br from-amber-50 to-amber-100 border-2 border-amber-200' :
                                    'bg-white border-2 border-gray-100'
                    ]">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <!-- Iconos para los tres primeros lugares -->
                            <div class="flex items-center justify-center rounded-full w-9 h-9" :class="[
                                getRealIndex(index) === 0 ? 'bg-yellow-200' :
                                    getRealIndex(index) === 1 ? 'bg-gray-200' :
                                        getRealIndex(index) === 2 ? 'bg-amber-200' :
                                            'bg-gray-100'
                            ]">
                                <template v-if="getRealIndex(index) < 3 && currentPage === 1">
                                    <Icon v-if="getRealIndex(index) === 0" name="ph:trophy"
                                        class="w-5 h-5 text-yellow-600" />
                                    <Icon v-else name="ph:medal" :class="[
                                        'w-5 h-5',
                                        getRealIndex(index) === 1 ? 'text-gray-600' : 'text-amber-600'
                                    ]" />
                                </template>
                                <span v-else class="text-sm font-semibold text-gray-600">
                                    {{ getRealIndex(index) + 1 }}
                                </span>
                            </div>

                            <div>
                                <span class="text-xs font-semibold uppercase" :class="[
                                    getRealIndex(index) === 0 ? 'text-yellow-600' :
                                        getRealIndex(index) === 1 ? 'text-gray-600' :
                                            getRealIndex(index) === 2 ? 'text-amber-600' :
                                                'text-gray-400'
                                ]">
                                    {{
                                        getRealIndex(index) === 0 ? 'Primer Lugar' :
                                            getRealIndex(index) === 1 ? 'Segundo Lugar' :
                                                getRealIndex(index) === 2 ? 'Tercer Lugar' :
                                                    `Puesto ${getRealIndex(index) + 1}`
                                    }}
                                </span>
                                <h3 class="text-base font-bold text-gray-800">{{ modelo.modelo }}</h3>
                            </div>
                        </div>
                        <div class="text-right">
                            <p class="text-lg font-bold text-gray-800">
                                {{ formatNumber(modelo.tokens) }}
                            </p>
                            <span class="text-xs text-gray-500">tokens</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Nueva Paginación -->
            <div v-if="totalPages > 1"
                class="flex items-center justify-between px-4 py-3 mt-4 border-t border-gray-200 sm:px-6">
                <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
                    <div>
                        <p class="text-sm text-gray-700">
                            Mostrando
                            <span class="font-medium">{{ startItem }}</span>
                            a
                            <span class="font-medium">{{ endItem }}</span>
                            de
                            <span class="font-medium">{{ totalItems }}</span>
                            resultados
                        </p>
                    </div>
                    <div class="flex items-center gap-2">
                        <button @click="prevPage" :disabled="currentPage === 1"
                            class="relative inline-flex items-center px-3 py-2 text-sm font-medium transition-colors rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:hover:bg-white"
                            :class="currentPage === 1 ? 'text-gray-300' : 'text-gray-700'">
                            <Icon name="ph:caret-left" class="w-5 h-5" />
                        </button>

                        <div class="flex items-center">
                            <template v-for="page in displayedPages" :key="page">
                                <button v-if="page !== '...'" @click="currentPage = page"
                                    class="relative inline-flex items-center px-4 py-2 text-sm font-medium transition-colors rounded-md"
                                    :class="[
                                        currentPage === page
                                            ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                                            : 'text-gray-700 hover:bg-gray-50'
                                    ]">
                                    {{ page }}
                                </button>
                                <span v-else
                                    class="relative inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700">
                                    ...
                                </span>
                            </template>
                        </div>

                        <button @click="nextPage" :disabled="currentPage === totalPages"
                            class="relative inline-flex items-center px-3 py-2 text-sm font-medium transition-colors rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:hover:bg-white"
                            :class="currentPage === totalPages ? 'text-gray-300' : 'text-gray-700'">
                            <Icon name="ph:caret-right" class="w-5 h-5" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
    data: {
        type: Array,
        default: () => []
    }
});

const itemsPerPage = 4;
const currentPage = ref(1);

// Computed properties para la paginación
const totalPages = computed(() => Math.ceil(props.data.length / itemsPerPage));
const totalItems = computed(() => props.data.length);
const startItem = computed(() => ((currentPage.value - 1) * itemsPerPage) + 1);
const endItem = computed(() => Math.min(currentPage.value * itemsPerPage, totalItems.value));

const paginatedData = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return props.data.slice(start, end);
});

const displayedPages = computed(() => {
    const pages = [];
    const maxDisplayed = 5;

    if (totalPages.value <= maxDisplayed) {
        return Array.from({ length: totalPages.value }, (_, i) => i + 1);
    }

    // Siempre mostrar primera página
    pages.push(1);

    // Calcular páginas alrededor de la página actual
    let start = Math.max(2, currentPage.value - 1);
    let end = Math.min(totalPages.value - 1, currentPage.value + 1);

    if (start > 2) pages.push('...');
    for (let i = start; i <= end; i++) {
        pages.push(i);
    }
    if (end < totalPages.value - 1) pages.push('...');

    // Siempre mostrar última página
    pages.push(totalPages.value);

    return pages;
});

// Métodos
const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++;
    }
};

const prevPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--;
    }
};

const getRealIndex = (index) => {
    return (currentPage.value - 1) * itemsPerPage + index;
};

const formatNumber = (value) => {
    return new Intl.NumberFormat('es-CO').format(value);
};
</script>