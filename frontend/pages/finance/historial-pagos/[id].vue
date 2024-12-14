<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header Section con búsqueda -->
        <div class="bg-white shadow">
            <div class="px-4 py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
                <div class="md:flex md:items-center md:justify-between">
                    <div class="flex-1 min-w-0">
                        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl">
                            Historial de Pagos
                        </h2>
                    </div>
                    <!-- Barra de búsqueda -->
                    <div class="mt-4 md:mt-0 md:ml-4">
                        <div class="relative">
                            <input v-model="searchQuery" type="text"
                                class="w-full py-2 pl-10 pr-4 border border-gray-300 rounded-lg md:w-64 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder="Buscar modelo..." @input="searchModelos">
                            <Icon name="uil:search"
                                class="absolute w-5 h-5 text-gray-400 transform -translate-y-1/2 left-3 top-1/2" />
                        </div>
                        <!-- Resultados de búsqueda -->
                        <div v-if="showResults && filteredModelos.length > 0"
                            class="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg md:w-64">
                            <ul class="py-1">
                                <li v-for="modelo in filteredModelos" :key="modelo.id"
                                    class="px-4 py-2 cursor-pointer hover:bg-gray-100" @click="selectModelo(modelo)">
                                    <div class="flex items-center">
                                        <img :src="`https://ui-avatars.com/api/?name=${modelo.nombres}+${modelo.apellidos}&background=random`"
                                            class="w-8 h-8 mr-3 rounded-full" :alt="modelo.nombres">
                                        <div>
                                            <div class="text-sm font-medium text-gray-900">
                                                {{ modelo.nombres }} {{ modelo.apellidos }}
                                            </div>
                                            <div class="text-xs text-gray-500">
                                                {{ modelo.nombre_usuario }}
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="px-4 py-8 mx-auto max-w-7xl sm:px-6 lg:px-8">
            <!-- Loading State -->
            <div v-if="isLoading" class="space-y-4">
                <div v-for="n in 3" :key="n" class="animate-pulse">
                    <div class="w-3/4 h-4 bg-gray-200 rounded"></div>
                    <div class="h-4 mt-4 bg-gray-200 rounded"></div>
                    <div class="w-5/6 h-4 mt-4 bg-gray-200 rounded"></div>
                </div>
            </div>

            <!-- No Data State -->
            <div v-else-if="!modelData" class="py-12 text-center">
                <Icon name="uil:info-circle" class="w-12 h-12 mx-auto text-gray-400" />
                <h3 class="mt-2 text-sm font-medium text-gray-900">No hay datos disponibles</h3>
                <p class="mt-1 text-sm text-gray-500">Selecciona una modelo para ver su historial.</p>
            </div>

            <!-- Data State -->
            <div v-else>
                <!-- Info Cards -->
                <div class="grid gap-6 mb-8 md:grid-cols-3">
                    <div class="p-6 bg-white rounded-lg shadow">
                        <div class="text-sm font-medium text-gray-500">Banco</div>
                        <div class="mt-1 text-xl font-semibold">{{ modelData.banco }}</div>
                        <div class="mt-1 text-sm text-gray-500">Cuenta: {{ modelData.numero_cuenta }}</div>
                    </div>

                    <div class="p-6 bg-white rounded-lg shadow">
                        <div class="text-sm font-medium text-gray-500">Documento</div>
                        <div class="mt-1 text-xl font-semibold">{{ modelData.numero_documento }}</div>
                        <div class="mt-1 text-sm text-gray-500">{{ modelData.tipo_documento }}</div>
                    </div>

                    <div class="p-6 bg-white rounded-lg shadow">
                        <div class="text-sm font-medium text-gray-500">Contacto</div>
                        <div class="mt-1 text-xl font-semibold">{{ modelData.numero_celular }}</div>
                        <div class="mt-1 text-sm text-gray-500">{{ modelData.correo_electronico }}</div>
                    </div>
                </div>

                <!-- Timeline de Pagos -->
                <div v-if="pagosFiltrados.length > 0" class="flow-root">
                    <ul role="list" class="-mb-8">
                        <li v-for="(pago, index) in pagosFiltrados" :key="pago.ganancia_id">
                            <div class="relative pb-8">
                                <span v-if="index !== pagosFiltrados.length - 1"
                                    class="absolute left-4 top-4 -ml-px h-full w-0.5 bg-gray-200"
                                    aria-hidden="true"></span>
                                <div class="relative flex space-x-3">
                                    <div>
                                        <span
                                            class="flex items-center justify-center w-8 h-8 bg-blue-500 rounded-full ring-8 ring-white">
                                            <Icon name="uil:usd-circle" class="w-5 h-5 text-white" />
                                        </span>
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <div class="p-4 bg-white rounded-lg shadow">
                                            <!-- Encabezado del pago -->
                                            <div class="flex justify-between mb-4">
                                                <div>
                                                    <h3 class="text-lg font-medium text-gray-900">
                                                        Periodo: {{ pago.periodo.nombre }}
                                                    </h3>
                                                    <p class="text-sm text-gray-500">
                                                        {{ formatDate(pago.periodo.fecha_inicio) }} - {{
                                                            formatDate(pago.periodo.fecha_fin) }}
                                                    </p>
                                                </div>
                                                <div class="text-right">
                                                    <p class="text-lg font-semibold text-green-600">
                                                        {{ formatCurrency(pago.total_cop) }}
                                                    </p>
                                                    <p class="text-sm text-gray-500">
                                                        TRM: {{ formatCurrency(pago.trm) }}
                                                    </p>
                                                </div>
                                            </div>

                                            <!-- Detalles por página -->
                                            <div class="mb-4">
                                                <h4 class="mb-2 text-sm font-medium text-gray-700">Detalles por página
                                                </h4>
                                                <div class="grid gap-4 md:grid-cols-3">
                                                    <div v-for="detalle in pago.detalles_paginas"
                                                        :key="detalle.nombre_pagina" class="p-3 rounded-lg bg-gray-50">
                                                        <div class="flex items-center justify-between mb-1">
                                                            <span class="font-medium">{{ detalle.nombre_pagina }}</span>
                                                            <span class="text-sm text-gray-500">{{ detalle.tokens }}
                                                                tokens</span>
                                                        </div>
                                                        <div class="flex items-center justify-between text-sm">
                                                            <span class="text-gray-500">Total:</span>
                                                            <span class="font-medium text-green-600">
                                                                {{ formatCurrency(detalle.total_cop) }}
                                                            </span>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Deducciones -->
                                            <div v-if="pago.deducciones_asociadas.length > 0">
                                                <h4 class="mb-2 text-sm font-medium text-gray-700">Deducciones aplicadas
                                                </h4>
                                                <div class="space-y-2">
                                                    <div v-for="deduccion in pago.deducciones_asociadas"
                                                        :key="deduccion.deduccion_id"
                                                        class="flex items-center justify-between p-2 rounded-lg bg-red-50">
                                                        <div>
                                                            <p class="font-medium text-red-700">{{ deduccion.concepto }}
                                                            </p>
                                                            <p class="text-sm text-red-600">
                                                                Cuota {{ deduccion.plazo - deduccion.cuotas_restantes
                                                                }}/{{ deduccion.plazo }}
                                                            </p>
                                                        </div>
                                                        <div class="text-right">
                                                            <p class="font-medium text-red-700">
                                                                {{ formatCurrency(deduccion.monto_pagado) }}
                                                            </p>
                                                            <div class="text-sm">
                                                                <span :class="{
                                                                    'px-2 py-1 rounded-full text-xs font-medium': true,
                                                                    'bg-green-100 text-green-800': deduccion.estado === 'Pagado',
                                                                    'bg-yellow-100 text-yellow-800': deduccion.estado === 'Pendiente'
                                                                }">
                                                                    {{ deduccion.estado }}
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>

                                            <!-- Resumen -->
                                            <div class="pt-4 mt-4 border-t border-gray-200">
                                                <div class="flex items-center justify-between">
                                                    <div class="text-sm text-gray-500">
                                                        Porcentaje: {{ (pago.porcentaje * 100).toFixed(2) }}%
                                                    </div>
                                                    <div class="text-right">
                                                        <p class="text-sm text-gray-500">Ganancia estudio:</p>
                                                        <p class="font-semibold text-gray-900">
                                                            {{ formatCurrency(pago.ganancia_estudio_general_cop) }}
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
                <div v-else class="py-12 text-center">
                    <p class="text-gray-500">No hay pagos registrados para esta modelo.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useModelosStore } from '~/stores/modelo';

const route = useRoute();
const router = useRouter();
const modelosStore = useModelosStore();

// Estados
const isLoading = ref(false);
const historialPagos = ref(null);
const searchQuery = ref('');
const showResults = ref(false);
const allModelos = ref([]);

// Computed properties
const modelData = computed(() => {
    return historialPagos.value?.[0] || null;
});

const pagosFiltrados = computed(() => {

    if (!historialPagos.value) return [];
    return historialPagos.value.slice(1);
});

const filteredModelos = computed(() => {
    if (!searchQuery.value) return [];

    const query = searchQuery.value.toLowerCase();
    return allModelos.value.filter(modelo =>
        modelo.nombres.toLowerCase().includes(query) ||
        modelo.apellidos.toLowerCase().includes(query) ||
        modelo.nombre_usuario.toLowerCase().includes(query)
    ).slice(0, 5);
});

// Métodos
const fetchHistorialPagos = async () => {
    const modelo_id = route.params.id;
    if (!modelo_id) return;

    try {
        isLoading.value = true;
        // Usar directamente el store para mantener consistencia
        const response = await modelosStore.fetchHistorialPagos(modelo_id);

        if (response && Array.isArray(response)) {
            historialPagos.value = response;
        } else {
            historialPagos.value = null;
        }
    } catch (error) {
        console.error('Error al cargar el historial:', error);
        historialPagos.value = null;
        useToast().error('No se pudo cargar el historial de pagos');
    } finally {
        isLoading.value = false;
    }
};

const searchModelos = async () => {
    if (!allModelos.value.length) {
        try {
            const response = await modelosStore.fetchModelos();
            allModelos.value = response;
        } catch (error) {
            console.error('Error al obtener modelos:', error);
        }
    }
    showResults.value = true;
};

const selectModelo = async (modelo) => {
    try {
        // Primero navegar
        await navigateTo(`${modelo.id}`);
        // Luego cargar los datos
        await fetchHistorialPagos();
        searchQuery.value = '';
        showResults.value = false;
    } catch (error) {
        console.error('Error al seleccionar modelo:', error);
    }
};

const formatCurrency = (value) => {
    if (!value) return '$0';
    const formatted = new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
    }).format(value);
    return formatted.replace(/\s+/g, '');
};

const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(date);
};

const handleClickOutside = (event) => {
    if (!event.target.closest('.search-container')) {
        showResults.value = false;
    }
};

// Lifecycle hooks
onMounted(() => {
    document.addEventListener('click', handleClickOutside);
    if (route.params.id) {
        fetchHistorialPagos();
    }
});

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
});

// Continuación del script setup...

// Watch route changes
watch(() => route.params.id, (newId) => {
    if (newId) {
        fetchHistorialPagos();
        searchQuery.value = '';
        showResults.value = false;
    } else {
        historialPagos.value = null;
    }
});

useHead({
    title: 'Historial de Pagos',
    meta: [
        {
            name: 'description',
            content: 'Historial de pagos y deducciones de modelos'
        }
    ]
});
</script>

<style scoped>
.search-container {
    position: relative;
    z-index: 50;
}

/* Animaciones para el timeline */
.timeline-enter-active,
.timeline-leave-active {
    transition: all 0.3s ease;
}

.timeline-enter-from,
.timeline-leave-to {
    opacity: 0;
    transform: translateY(30px);
}

/* Estilo para scrollbar personalizado */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #666;
}
</style>