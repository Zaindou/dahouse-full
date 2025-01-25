<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header Section -->
        <div class="bg-white shadow">
            <div class="px-4 py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
                <div class="flex flex-col items-start justify-between gap-4 md:flex-row md:items-center">
                    <div>
                        <h1 class="text-2xl font-bold tracking-tight text-gray-900">Gestión de Deducciones</h1>
                        <p class="mt-1 text-sm text-gray-500">Administra las deducciones de tus empleados de forma
                            eficiente</p>
                    </div>
                    <div class="relative w-full md:w-64">
                        <div class="absolute inset-y-0 left-0 flex items-center pl-3">
                            <Icon name="uil:search" class="w-5 h-5 text-gray-400" />
                        </div>
                        <input v-model="filtro" type="text" placeholder="Buscar empleados..."
                            class="w-full py-2 pl-10 pr-4 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="px-4 py-8 mx-auto max-w-7xl sm:px-6 lg:px-8">
            <!-- Loading Skeleton -->
            <div v-if="initialSkeleton" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                <div v-for="n in 6" :key="n" class="p-4 bg-white rounded-lg shadow animate-pulse">
                    <div class="h-24"></div>
                </div>
            </div>

            <!-- Employee Cards Grid -->
            <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                <div v-for="modelo in modelosFiltrados" :key="modelo.id"
                    class="overflow-hidden transition-shadow duration-200 bg-white rounded-lg shadow-sm hover:shadow-lg">
                    <div class="p-6">
                        <!-- Employee Header -->
                        <div class="flex items-center justify-between pb-4">
                            <div class="flex items-center space-x-4">
                                <div class="flex-shrink-0">
                                    <img class="w-12 h-12 rounded-full"
                                        :src="`https://ui-avatars.com/api/?name=${modelo.nombres}+${modelo.apellidos}&background=random`"
                                        :alt="modelo.nombres" />
                                </div>
                                <div>
                                    <h2 class="text-lg font-medium text-gray-900">
                                        {{ modelo.nombres }} {{ modelo.apellidos }}
                                    </h2>
                                    <p class="text-sm text-gray-500">{{ modelo.nombre_usuario }}</p>
                                </div>
                            </div>
                        </div>

                        <!-- Action Buttons -->
                        <div class="grid grid-cols-3 gap-4 mt-4">
                            <button @click="abrirFormularioDeduccion(modelo)"
                                class="flex flex-col items-center p-3 text-sm text-blue-600 transition-colors rounded-lg hover:bg-blue-50">
                                <Icon name="uil:plus" class="w-6 h-6 mb-1" />
                                <span>Nueva</span>
                            </button>
                            <button @click="abrirModalDeduciblesActivos(modelo)"
                                class="flex flex-col items-center p-3 text-sm text-green-600 transition-colors rounded-lg hover:bg-green-50">
                                <Icon name="uil:credit-card" class="w-6 h-6 mb-1" />
                                <span>Activas</span>
                            </button>
                            <button @click="abrirModalHistorico(modelo)"
                                class="flex flex-col items-center p-3 text-sm text-purple-600 transition-colors rounded-lg hover:bg-purple-50">
                                <Icon name="uil:history" class="w-6 h-6 mb-1" />
                                <span>Histórico</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Pagination -->
            <div class="flex items-center justify-between mt-6">
                <div>
                    <p class="text-sm text-gray-700">
                        Mostrando
                        <span class="font-medium">{{ paginationStart + 1 }}</span> a
                        <span class="font-medium">{{ paginationEnd }}</span> de
                        <span class="font-medium">{{ modelosFiltrados.length }}</span> resultados
                    </p>
                </div>
                <div class="flex space-x-2">
                    <button @click="prevPage" :disabled="currentPage === 1"
                        class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                        Anterior
                    </button>
                    <button @click="nextPage" :disabled="currentPage === totalPages"
                        class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                        Siguiente
                    </button>
                </div>
            </div>
        </div>

        <!-- Modales -->
        <Teleport to="body">
            <div v-if="openModal" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50"
                @click="closeAllModals">
                <div class="min-h-screen px-4 text-center">
                    <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
                    <div class="inline-block w-full max-w-2xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
                        @click.stop>
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-semibold text-gray-900">
                                Nueva Deducción - {{ modeloSeleccionado?.nombres }} {{ modeloSeleccionado?.apellidos }}
                            </h3>
                            <button @click="closeAllModals" class="text-gray-500 hover:text-gray-700">
                                <Icon name="uil:times" class="w-6 h-6" />
                            </button>
                        </div>

                        <form @submit.prevent="guardarDeduccion" class="space-y-6"
                            :class="{ 'opacity-50 pointer-events-none': isSubmitting }">
                            <div>
                                <label for="concepto" class="block text-sm font-medium text-gray-700">Concepto</label>
                                <input id="concepto" v-model="deduccion.concepto" type="text" required
                                    class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                    placeholder="Ingrese el concepto" />
                            </div>

                            <div>
                                <label for="valor-total" class="block text-sm font-medium text-gray-700">Valor
                                    Total</label>
                                <div class="relative mt-1">
                                    <input id="valor-total" v-model="formattedValorTotal" type="text" required
                                        class="block w-full pr-12 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                                        placeholder="0.00" />
                                    <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                                        <span class="text-gray-500 sm:text-sm">COP</span>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <label for="plazo" class="block text-sm font-medium text-gray-700">
                                    Plazo (máx 6 periodos)
                                </label>
                                <input id="plazo" v-model.number="deduccion.plazo" type="number" required max="6"
                                    min="1"
                                    class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                            </div>

                            <div>
                                <label for="tasa" class="block text-sm font-medium text-gray-700">
                                    Tasa de Interés (%)
                                </label>
                                <input id="tasa" v-model.number="deduccion.tasa" type="number" required step="0.01"
                                    min="0"
                                    class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
                            </div>

                            <div class="flex justify-end pt-4 space-x-4">
                                <button v-if="!removeSimulationButton" type="button" @click="simularDeduccion"
                                    class="px-4 py-2 text-white bg-purple-500 rounded-md hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2">
                                    <Icon name="uil:calculator" class="inline-block w-5 h-5 mr-2" />
                                    Simular
                                </button>
                                <button v-if="removeSimulationButton" type="submit" :disabled="isSubmitting"
                                    class="inline-flex items-center px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed">
                                    <!-- Spinner cuando está cargando -->
                                    <Icon v-if="isSubmitting" name="uil:spinner" class="w-5 h-5 mr-2 animate-spin" />
                                    <!-- Icono normal cuando no está cargando -->
                                    <Icon v-else name="uil:save" class="w-5 h-5 mr-2" />
                                    {{ isSubmitting ? 'Creando...' : 'Crear' }}
                                </button>
                                <button type="button" @click="closeAllModals"
                                    class="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                                    <Icon name="uil:times" class="inline-block w-5 h-5 mr-2" />
                                    Cancelar
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Modal Simulación -->
            <div v-if="openSimulationModal" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50"
                @click="closeAllModals">
                <div class="min-h-screen px-4 text-center">
                    <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
                    <div class="inline-block w-full max-w-4xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
                        @click.stop>
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-semibold text-gray-900">
                                Simulación de Deducción
                            </h3>
                            <button @click="closeAllModals" class="text-gray-500 hover:text-gray-700">
                                <Icon name="uil:times" class="w-6 h-6" />
                            </button>
                        </div>

                        <div class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th scope="col"
                                            class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                                            Periodo
                                        </th>
                                        <th scope="col"
                                            class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                                            Cuota Quincenal
                                        </th>
                                        <th scope="col"
                                            class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                                            Capital
                                        </th>
                                        <th scope="col"
                                            class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                                            Interés
                                        </th>
                                        <th scope="col"
                                            class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                                            Balance
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
                                    <tr v-for="pago in pagosDetalle" :key="pago.periodo">
                                        <td class="px-6 py-4 whitespace-nowrap">{{ pago.periodo }}</td>
                                        <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.cuotaQuincenal)
                                            }}</td>
                                        <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.principal) }}
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.interes) }}</td>
                                        <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.balanceRestante)
                                            }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div class="p-4 mt-4 rounded-lg bg-gray-50">
                            <h4 class="mb-3 text-lg font-semibold">Resumen del Préstamo</h4>
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <p class="text-sm font-medium text-gray-500">Número de periodos</p>
                                    <p class="mt-1">{{ resumenPrestamo.numeroPeriodos }}</p>
                                </div>
                                <div>
                                    <p class="text-sm font-medium text-gray-500">Valor a adeudar</p>
                                    <p class="mt-1">{{ formatCurrency(resumenPrestamo.valorAdeudar) }}</p>
                                </div>
                                <div>
                                    <p class="text-sm font-medium text-gray-500">Valor total con intereses</p>
                                    <p class="mt-1">{{ formatCurrency(resumenPrestamo.valorConIntereses) }}</p>
                                </div>
                                <div>
                                    <p class="text-sm font-medium text-gray-500">Cuota quincenal</p>
                                    <p class="mt-1">{{ formatCurrency(resumenPrestamo.cuotaQuincenal) }}</p>
                                </div>
                            </div>
                        </div>

                        <div class="flex justify-end mt-6 space-x-4">
                            <button @click="acceptSimulation"
                                class="px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                                <Icon name="uil:check" class="inline-block w-5 h-5 mr-2" />
                                Aceptar
                            </button>
                            <button @click="closeAllModals"
                                class="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
                                <Icon name="uil:times" class="inline-block w-5 h-5 mr-2" />
                                Cerrar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Modal Deducibles Activos -->
            <div v-if="openActiveDebtModal" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50"
                @click="closeAllModals">
                <div class="min-h-screen px-4 text-center">
                    <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
                    <div class="inline-block w-full max-w-3xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
                        @click.stop>
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-semibold text-gray-900">
                                Deducciones Activas - {{ modeloSeleccionado?.nombres }} {{ modeloSeleccionado?.apellidos
                                }}
                            </h3>
                            <button @click="closeAllModals" class="text-gray-500 hover:text-gray-700">
                                <Icon name="uil:times" class="w-6 h-6" />
                            </button>
                        </div>

                        <div class="mt-4">
                            <div v-if="modeloSeleccionado?.deducibles?.filter(d => d.estado === 'Activo').length > 0"
                                class="space-y-4">
                                <div v-for="deducible in modeloSeleccionado.deducibles.filter(d => d.estado === 'Activo')"
                                    :key="deducible.id" class="p-4 bg-white border rounded-lg">
                                    <div class="grid grid-cols-2 gap-4">
                                        <div>
                                            <p class="text-sm font-medium text-gray-500">Concepto</p>
                                            <p class="mt-1">{{ deducible.concepto }}</p>
                                        </div>
                                        <div>
                                            <p class="text-sm font-medium text-gray-500">Valor Total</p>
                                            <p class="mt-1">{{ formatCurrency(deducible.valor_total) }}</p>
                                        </div>
                                        <div>
                                            <p class="text-sm font-medium text-gray-500">Plazo</p>
                                            <p class="mt-1">{{ deducible.plazo }} períodos</p>
                                        </div>
                                        <div>
                                            <p class="text-sm font-medium text-gray-500">Estado</p>
                                            <span
                                                class="inline-flex px-2 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full">
                                                {{ deducible.estado }}
                                            </span>
                                        </div>
                                        <div>
                                            <p class="text-sm font-medium text-gray-500">Fecha inicio</p>
                                            <p class="mt-1">{{ formatDate(deducible.fecha_inicio) }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-else class="p-4 text-center text-gray-500">
                                No hay deducciones activas
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Modal Histórico -->
            <div v-if="openRecordModal" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50"
                @click="closeAllModals">
                <div class="min-h-screen px-4 text-center">
                    <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
                    <div class="inline-block w-full max-w-3xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
                        @click.stop>
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-semibold text-gray-900">
                                Histórico de Deducciones - {{ modeloSeleccionado?.nombres }} {{
                                    modeloSeleccionado?.apellidos }}
                            </h3>
                            <button @click="closeAllModals" class="text-gray-500 hover:text-gray-700">
                                <Icon name="uil:times" class="w-6 h-6" />
                            </button>
                        </div>

                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700">Seleccionar mes:</label>
                            <select v-model="selectedMonth" @change="filterDeduciblesByMonth"
                                class="block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                                <option v-for="month in availableMonths" :key="month" :value="month">
                                    {{ formatMonth(month) }}
                                </option>
                            </select>
                        </div>

                        <div class="mt-4">
                            <div v-if="paginatedDeducibles.length > 0" class="space-y-4">
                                <div v-for="deducible in paginatedDeducibles" :key="deducible.id"
                                    class="p-4 bg-white border rounded-lg">
                                    <div class="grid grid-cols-2 gap-4">
                                        <div>
                                            <p class="text-sm font-medium text-gray-500">Concepto</p>
                                            <p class="mt-1">{{ deducible.concepto }}</p>
                                        </div>
                                        <div>
                                            <p class="text-sm font-medium text-gray-500">Valor Total</p>
                                            <p class="mt-1">{{ formatCurrency(deducible.valor_total) }}</p>
                                        </div>
                                        <div>
                                            <p class="text-sm font-medium text-gray-500">Plazo</p>
                                            <p class="mt-1">{{ deducible.plazo }} períodos</p>
                                        </div>
                                        <div>
                                            <p class="text-sm font-medium text-gray-500">Estado</p>
                                            <span :class="{
                                                'inline-flex px-2 py-1 text-xs font-semibold rounded-full': true,
                                                'bg-green-100 text-green-800': deducible.estado === 'Activo',
                                                'bg-red-100 text-red-800': deducible.estado === 'Inactivo'
                                            }">
                                                {{ deducible.estado }}
                                            </span>
                                        </div>
                                        <div>
                                            <p class="text-sm font-medium text-gray-500">Fecha inicio</p>
                                            <p class="mt-1">{{ formatDate(deducible.fecha_inicio) }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-else class="p-4 text-center text-gray-500">
                                No hay deducciones para este mes
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Teleport>
    </div>
</template>
<script setup>


useHead({
    titleTemplate: '%s - Deducciones',
})


import { ref, computed } from 'vue';
import { useModelosStore } from '~/stores/modelo';

const modelosStore = useModelosStore();
const isLoading = ref(false);
const initialSkeleton = ref(false);
const openModal = ref(false);
const openActiveDebtModal = ref(false);
const openRecordModal = ref(false);
const modelos = ref([]);
const filtro = ref('');
const modeloSeleccionado = ref(null);
const openSimulationModal = ref(false);
const pagosDetalle = ref([]);
const resumenPrestamo = ref({});
const removeSimulationButton = ref(false);
const isSubmitting = ref(false);

const deduccion = ref({
    concepto: '',
    valor_total: 0,  // Asegúrate de que estos no son undefined o strings vacíos
    plazo: 0,
    tasa: 0
});

const selectedMonth = ref('');
const currentPage = ref(1);
const itemsPerPage = 5;

const fetchInitialData = async () => {
    initialSkeleton.value = true;
    try {
        modelos.value = await modelosStore.fetchModelos();
    } catch (error) {
        Swal.fire('Error', 'No se pudo cargar la lista de usuarios', 'error');
    } finally {
        initialSkeleton.value = false;
    }
};

fetchInitialData();

const availableMonths = computed(() => {
    if (!modeloSeleccionado.value || !modeloSeleccionado.value.deducibles) return [];
    const months = modeloSeleccionado.value.deducibles.map(d => {
        const date = new Date(d.fecha_inicio);
        return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    });
    return [...new Set(months)].sort();
});

const filteredDeducibles = computed(() => {
    if (!modeloSeleccionado.value || !modeloSeleccionado.value.deducibles) return [];
    if (!selectedMonth.value) return modeloSeleccionado.value.deducibles;
    return modeloSeleccionado.value.deducibles.filter(d => {
        const date = new Date(d.fecha_inicio);
        const deducibleMonth = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        return deducibleMonth === selectedMonth.value;
    });
});

const totalPages = computed(() => Math.ceil(filteredDeducibles.value.length / itemsPerPage));

const paginatedDeducibles = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return filteredDeducibles.value.slice(start, end);
});

const paginationStart = computed(() => (currentPage.value - 1) * itemsPerPage);
const paginationEnd = computed(() => Math.min(currentPage.value * itemsPerPage, filteredDeducibles.value.length));

const filterDeduciblesByMonth = () => {
    currentPage.value = 1;
};

const prevPage = () => {
    if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
    if (currentPage.value < totalPages.value) currentPage.value++;
};

const formatMonth = (dateString) => {
    const [year, month] = dateString.split('-');
    const date = new Date(year, month - 1);
    return date.toLocaleString('default', { month: 'long', year: 'numeric' });
};

const formatDate = (dateString) => {
    console.log(dateString)
    if (!dateString) return '-';

    try {
        // Si la fecha viene como string, la convertimos a objeto Date
        const date = new Date(dateString);

        // Verificamos si la fecha es válida
        if (isNaN(date.getTime())) {
            // Si no es válida, intentamos parsear formatos comunes
            const parts = dateString.split(/[-/]/);
            if (parts.length === 3) {
                // Asumimos que puede venir como DD-MM-YYYY o YYYY-MM-DD
                if (parts[0].length === 4) {
                    // Formato YYYY-MM-DD
                    date = new Date(parts[0], parts[1] - 1, parts[2]);
                } else {
                    // Formato DD-MM-YYYY
                    date = new Date(parts[2], parts[1] - 1, parts[0]);
                }
            }
        }

        // Verificamos una última vez si la fecha es válida
        if (isNaN(date.getTime())) {
            return '-';
        }

        // Formateamos la fecha usando el API de Intl
        return new Intl.DateTimeFormat('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(date);
    } catch (error) {
        console.error('Error formateando fecha:', error);
        return '-';
    }
};

const closeAllModals = () => {
    openModal.value = false;
    openActiveDebtModal.value = false;
    openRecordModal.value = false;
    openSimulationModal.value = false;
    removeSimulationButton.value = false;
    modeloSeleccionado.value = null;
    isSubmitting.value = false;
    deduccion.value = {
        concepto: '',
        valor_total: 0,
        plazo: 0,
        tasa: 0
    };
};

const acceptSimulation = () => {
    openSimulationModal.value = false;
    removeSimulationButton.value = true;
};

const simularDeduccion = () => {
    const valorTotal = parseFloat(deduccion.value.valor_total) || 0;
    const plazo = parseInt(deduccion.value.plazo, 10) || 0;
    let tasa = parseFloat(deduccion.value.tasa) || 0;

    // Convertir tasa a decimal si está en porcentaje
    if (tasa > 1) {
        tasa = tasa / 100;
    }

    if (valorTotal <= 0 || plazo <= 0 || tasa < 0) {
        alert('Por favor, introduzca valores válidos. Todos los campos deben ser números y mayores que cero.');
        return;
    }

    // Calcular cuota fija (sistema francés o cuota fija)
    const tasaQuincenal = tasa / 2; // Dividir tasa para calcular interés por periodo
    const cuotaQuincenal = valorTotal * ((tasaQuincenal * Math.pow(1 + tasaQuincenal, plazo)) / (Math.pow(1 + tasaQuincenal, plazo) - 1));
    let saldoCapital = valorTotal;
    let balanceRestante = valorTotal;
    pagosDetalle.value = [];

    for (let i = 1; i <= plazo; i++) {
        const interes = saldoCapital * tasaQuincenal;
        const principal = cuotaQuincenal - interes;
        saldoCapital -= principal;

        // Asegurar que no haya errores por redondeo
        if (saldoCapital < 0) saldoCapital = 0;

        pagosDetalle.value.push({
            periodo: i,
            cuotaQuincenal: cuotaQuincenal.toFixed(2),
            principal: principal.toFixed(2),
            interes: interes.toFixed(2),
            saldoCapital: saldoCapital.toFixed(2),
            balanceRestante: (saldoCapital > 0 ? saldoCapital : 0).toFixed(2)
        });
    }

    resumenPrestamo.value = {
        numeroPeriodos: plazo,
        valorAdeudar: valorTotal.toFixed(2),
        valorConIntereses: (cuotaQuincenal * plazo).toFixed(2),
        cuotaQuincenal: cuotaQuincenal.toFixed(2)
    };

    openSimulationModal.value = true;
    removeSimulationButton.value = true;
};


const modelosFiltrados = computed(() => {
    if (!modelos.value) {
        return [];
    }
    let filtered = modelos.value.filter(modelo => {
        const filtroEnMinusculas = filtro.value.toLowerCase();
        return (modelo.nombre_usuario.toLowerCase().includes(filtroEnMinusculas) ||
            modelo.nombres.toLowerCase().includes(filtroEnMinusculas) ||
            modelo.apellidos.toLowerCase().includes(filtroEnMinusculas)) &&
            modelo.habilitado === true && modelo.rol === 'Modelo';

    });

    // Ordenar alfabéticamente por nombre completo
    return filtered.sort((a, b) => {
        const nombreCompletoA = `${a.nombres} ${a.apellidos}`.toLowerCase();
        const nombreCompletoB = `${b.nombres} ${b.apellidos}`.toLowerCase();
        return nombreCompletoA.localeCompare(nombreCompletoB);
    });
});


const abrirFormularioDeduccion = (modelo) => {
    modeloSeleccionado.value = modelo;
    openModal.value = true;
    // Restablecer la deduccion
    deduccion.value = { concepto: '', valor_total: '', plazo: '', tasa: '' };
};

const abrirModalDeduciblesActivos = (modelo) => {
    modeloSeleccionado.value = modelo;
    openActiveDebtModal.value = true;
    // Restablecer la deduccion
    deduccion.value = { concepto: '', valor_total: '', plazo: '', tasa: '' };
};

const abrirModalHistorico = (modelo) => {
    modeloSeleccionado.value = modelo;
    openRecordModal.value = true;
    // Restablecer la deduccion
    deduccion.value = { concepto: '', valor_total: '', plazo: '', tasa: '' };
};

const formattedValorTotal = computed({
    get() {
        if (document.activeElement.id !== "valor-total-input") {
            return new Intl.NumberFormat('es-CO', {
                style: 'currency',
                currency: 'COP',
                minimumFractionDigits: 0,
            }).format(deduccion.value.valor_total);
        }
        return deduccion.value.valor_total.toString();
    },
    set(newValue) {
        let parsedValue = newValue.replace(/\D/g, '');
        deduccion.value.valor_total = parseFloat(parsedValue);
    }
});

const guardarDeduccion = async () => {
    if (isSubmitting.value) return;

    try {
        isSubmitting.value = true;
        const response = await modelosStore.crearDeduccion(
            modeloSeleccionado.value.nombre_usuario,
            deduccion.value
        );
        modelos.value = await modelosStore.fetchModelos();
        closeAllModals();
        Swal.fire('Éxito', response.mensaje, 'success');
    } catch (error) {
        Swal.fire('Error', 'Ha ocurrido un error', 'error');
    } finally {
        isSubmitting.value = false;
    }
};

const formatCurrency = (value) => {
    // Primero formateamos con Intl.NumberFormat
    const formatted = new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
    }).format(value);

    // Removemos el espacio entre el símbolo y el número
    return formatted.replace(/\s+/g, '');
};

</script>
