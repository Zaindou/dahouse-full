<template>
    <NuxtLayout>
        <div class="min-h-screen bg-gray-50">
            <!-- Header Section -->
            <div class="bg-white shadow">
                <div class="px-4 py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
                    <!-- Título y Filtros flexibles -->
                    <div class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
                        <div class="flex-1 min-w-0">
                            <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl">
                                Historial de Pagos
                            </h2>
                        </div>
                        <!-- Filtros en columna en móvil, fila en desktop -->
                        <div class="flex flex-col w-full space-y-2 md:flex-row md:w-auto md:space-y-0 md:space-x-4">
                            <select v-model="selectedBank"
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg md:w-auto focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                                <option value="">Todos los bancos</option>
                                <option v-for="banco in bancos" :key="banco" :value="banco">
                                    {{ banco }}
                                </option>
                            </select>
                            <div class="relative w-full md:w-64">
                                <input v-model="searchQuery" type="text"
                                    class="w-full py-2 pl-10 pr-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder="Buscar modelo...">
                                <Icon name="uil:search"
                                    class="absolute w-5 h-5 text-gray-400 transform -translate-y-1/2 left-3 top-1/2" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Main Content -->
            <div class="px-4 py-8 mx-auto max-w-7xl sm:px-6 lg:px-8">
                <!-- Loading State -->
                <div v-if="isLoading" class="space-y-4">
                    <div v-for="n in itemsPerPage" :key="n" class="p-4 bg-white rounded-lg animate-pulse">
                        <div class="flex items-center space-x-4">
                            <div class="w-12 h-12 bg-gray-200 rounded-full"></div>
                            <div class="flex-1 py-1 space-y-4">
                                <div class="w-3/4 h-4 bg-gray-200 rounded"></div>
                                <div class="w-1/2 h-4 bg-gray-200 rounded"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-else-if="filteredModelos.length > 0">
                    <!-- Info de resultados -->
                    <div class="pb-4">
                        <p class="text-sm text-gray-600">
                            {{ filteredModelos.length }} resultado{{ filteredModelos.length !== 1 ? 's' : '' }}
                            encontrado{{ filteredModelos.length !== 1 ? 's' : '' }}
                        </p>
                    </div>

                    <!-- Vista de cards para móvil -->
                    <div class="space-y-4 md:hidden">
                        <div v-for="modelo in paginatedModelos" :key="modelo.id"
                            class="overflow-hidden bg-white rounded-lg shadow">
                            <div class="p-4">
                                <div class="flex items-center space-x-4">
                                    <div class="flex-shrink-0">
                                        <img class="w-12 h-12 rounded-full"
                                            :src="`https://ui-avatars.com/api/?name=${modelo.nombres}+${modelo.apellidos}&background=random`"
                                            :alt="modelo.nombres">
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <p class="text-sm font-medium text-gray-900 truncate">
                                            {{ modelo.nombres }} {{ modelo.apellidos }}
                                        </p>
                                        <p class="text-sm text-gray-500 truncate">
                                            {{ modelo.numero_documento }}
                                        </p>
                                    </div>
                                </div>
                                <div class="mt-4">
                                    <div class="text-sm text-gray-500">
                                        <div class="flex justify-between">
                                            <span>Banco:</span>
                                            <span class="font-medium text-gray-900">{{ modelo.banco }}</span>
                                        </div>
                                        <div class="flex justify-between mt-1">
                                            <span>Cuenta:</span>
                                            <span class="font-medium text-gray-900">{{ modelo.numero_cuenta }}</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="mt-4">
                                    <button @click="navigateTo(`historial-pagos/${modelo.id}`)"
                                        class="w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700">
                                        <Icon name="uil:history" class="inline-block w-4 h-4 mr-2" />
                                        Ver Historial
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Tabla para desktop -->
                    <div class="hidden overflow-hidden bg-white shadow md:block sm:rounded-lg">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th scope="col"
                                        class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                                        Modelo
                                    </th>
                                    <th scope="col"
                                        class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                                        Banco
                                    </th>
                                    <th scope="col" class="relative px-6 py-3">
                                        <span class="sr-only">Acciones</span>
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                <tr v-for="modelo in paginatedModelos" :key="modelo.id" class="hover:bg-gray-50">
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center">
                                            <div class="flex-shrink-0 w-10 h-10">
                                                <img class="w-10 h-10 rounded-full"
                                                    :src="`https://ui-avatars.com/api/?name=${modelo.nombres}+${modelo.apellidos}&background=random`"
                                                    :alt="modelo.nombres">
                                            </div>
                                            <div class="ml-4">
                                                <div class="text-sm font-medium text-gray-900">
                                                    {{ modelo.nombres }} {{ modelo.apellidos }}
                                                </div>
                                                <div class="text-sm text-gray-500">
                                                    {{ modelo.numero_documento }}
                                                </div>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm text-gray-900">{{ modelo.banco }}</div>
                                        <div class="text-sm text-gray-500">{{ modelo.numero_cuenta }}</div>
                                    </td>
                                    <td class="px-6 py-4 text-sm font-medium text-right whitespace-nowrap">
                                        <button @click="navigateTo(`historial-pagos/${modelo.id}`)"
                                            class="inline-flex items-center px-3 py-2 text-sm font-medium text-white transition-colors bg-blue-600 rounded-md hover:bg-blue-700">
                                            <Icon name="uil:history" class="w-4 h-4 mr-2" />
                                            Ver Historial
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Paginación responsive -->
                    <div
                        class="flex flex-col items-center justify-between gap-4 px-4 py-3 mt-4 bg-white border-t border-gray-200 sm:flex-row sm:px-6">
                        <!-- Selector de items por página -->
                        <div class="flex items-center justify-center w-full sm:w-auto">
                            <label for="itemsPerPage" class="mr-2 text-sm text-gray-700">Mostrar:</label>
                            <select v-model="itemsPerPage" id="itemsPerPage"
                                class="px-2 py-1 text-sm border border-gray-300 rounded-md">
                                <option :value="5">5</option>
                                <option :value="10">10</option>
                                <option :value="20">20</option>
                                <option :value="50">50</option>
                            </select>
                        </div>

                        <!-- Información de página en móvil -->
                        <div class="text-sm text-center text-gray-700 sm:text-left">
                            <p class="sm:hidden">
                                Página {{ currentPage }} de {{ totalPages }}
                            </p>
                            <p class="hidden sm:block">
                                Mostrando {{ paginationStart + 1 }} a {{ paginationEnd }} de {{ filteredModelos.length
                                }}
                            </p>
                        </div>

                        <!-- Controles de paginación -->
                        <div class="flex justify-center w-full space-x-2 sm:w-auto">
                            <button @click="prevPage" :disabled="currentPage === 1"
                                class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50">
                                <Icon name="uil:angle-left" class="w-5 h-5" />
                            </button>
                            <!-- Números de página solo en desktop -->
                            <div class="hidden sm:flex sm:space-x-2">
                                <button v-for="page in displayedPages" :key="page" @click="currentPage = page" :class="[
                                    'px-3 py-2 text-sm font-medium rounded-md',
                                    currentPage === page
                                        ? 'bg-blue-600 text-white'
                                        : 'text-gray-700 bg-white border border-gray-300 hover:bg-gray-50'
                                ]">
                                    {{ page }}
                                </button>
                            </div>
                            <button @click="nextPage" :disabled="currentPage === totalPages"
                                class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50">
                                <Icon name="uil:angle-right" class="w-5 h-5" />
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Empty State -->
                <div v-else class="p-8 text-center bg-white rounded-lg">
                    <Icon name="uil:users-alt" class="w-12 h-12 mx-auto text-gray-400" />
                    <h3 class="mt-2 text-sm font-medium text-gray-900">No hay resultados</h3>
                    <p class="mt-1 text-sm text-gray-500">
                        No se encontraron modelos que coincidan con tu búsqueda.
                    </p>
                </div>
            </div>
        </div>
    </NuxtLayout>
</template>

<script setup>
const searchQuery = ref('');
const selectedBank = ref('');
const isLoading = ref(true);
const modelos = ref([]);
const currentPage = ref(1);
const itemsPerPage = ref(10);
const modelosStore = useModelosStore();

// Computed para bancos únicos
const bancos = computed(() => {
    const bancosUnicos = [...new Set(modelos.value.map(modelo => modelo.banco))];
    return bancosUnicos.sort();
});

// Computed para filtrado
const filteredModelos = computed(() => {
    let filtered = modelos.value;

    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        filtered = filtered.filter(modelo =>
            modelo.nombres.toLowerCase().includes(query) ||
            modelo.apellidos.toLowerCase().includes(query) ||
            modelo.nombre_usuario.toLowerCase().includes(query) ||
            modelo.numero_documento.includes(query)
        );
    }

    if (selectedBank.value) {
        filtered = filtered.filter(modelo => modelo.banco === selectedBank.value);
    }

    return filtered;
});

// Computed para paginación
const totalPages = computed(() => Math.ceil(filteredModelos.value.length / itemsPerPage.value));

const paginatedModelos = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return filteredModelos.value.slice(start, end);
});

const paginationStart = computed(() => (currentPage.value - 1) * itemsPerPage.value);
const paginationEnd = computed(() => Math.min(currentPage.value * itemsPerPage.value, filteredModelos.value.length));

// Computed para páginas mostradas en paginación
const displayedPages = computed(() => {
    const delta = 2;
    let pages = [];

    for (let i = Math.max(1, currentPage.value - delta);
        i <= Math.min(totalPages.value, currentPage.value + delta);
        i++) {
        pages.push(i);
    }

    // Siempre mostrar primera y última página
    if (pages[0] > 1) {
        if (pages[0] > 2) {
            pages.unshift('...');
        }
        pages.unshift(1);
    }

    if (pages[pages.length - 1] < totalPages.value) {
        if (pages[pages.length - 1] < totalPages.value - 1) {
            pages.push('...');
        }
        pages.push(totalPages.value);
    }

    return pages;
});

// Métodos
const prevPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--;
    }
};

const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++;
    }
};

const fetchModelos = async () => {
    try {
        isLoading.value = true;
        const response = await modelosStore.fetchModelos();
        modelos.value = response;
    } catch (error) {
        console.error('Error al cargar modelos:', error);
        useToast().error('Error al cargar la lista de modelos');
    } finally {
        isLoading.value = false;
    }
};

// Watchers
watch([searchQuery, selectedBank, itemsPerPage], () => {
    currentPage.value = 1;
});

// Lifecycle
onMounted(() => {
    fetchModelos();
});

// Meta tags
useHead({
    title: 'Historial de Pagos',
    meta: [
        { name: 'description', content: 'Historial de pagos y deducciones de modelos' }
    ]
});
</script>