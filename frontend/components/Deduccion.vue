<template>
    <div class="container mx-auto p-4">
        <loading :is-loading="isLoading"></loading>

        <div class="mb-4 flex flex-col sm:flex-row justify-between items-center">
            <h2 class="text-2xl font-bold mb-4 sm:mb-0">Gestionar Deducciones</h2>
            <div class="relative w-full sm:w-64">
                <input v-model="filtro" type="text" placeholder="Buscar usuarios..."
                    class="w-full pl-10 pr-4 py-2 border rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-blue-300 transition duration-150 ease-in-out">
                <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
            </div>
        </div>

        <!-- Vista de tabla para pantallas medianas y grandes -->
        <div class="hidden md:block overflow-x-auto bg-white shadow-md rounded-lg">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th scope="col"
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Usuario</th>
                        <th scope="col"
                            class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Acciones</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="modelo in modelosFiltrados" :key="modelo.id">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex items-center">
                                <div class="flex-shrink-0 h-10 w-10">
                                    <img class="h-10 w-10 rounded-full"
                                        :src="`https://ui-avatars.com/api/?name=${modelo.nombres}+${modelo.apellidos}&background=random`"
                                        alt="">
                                </div>
                                <div class="ml-4">
                                    <div class="text-sm font-medium text-gray-900">
                                        {{ modelo.nombres }} {{ modelo.apellidos }}
                                    </div>
                                    <div class="text-sm text-gray-500">
                                        {{ modelo.nombre_usuario }}
                                    </div>
                                </div>
                            </div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                            <button @click="abrirFormularioDeduccion(modelo)"
                                class="text-indigo-600 hover:text-indigo-900 mr-3">Crear deducción</button>
                            <button @click="abrirModalDeduciblesActivos(modelo)"
                                class="text-green-600 hover:text-green-900 mr-3">Deducibles activos</button>
                            <button @click="abrirModalHistorico(modelo)"
                                class="text-yellow-600 hover:text-yellow-900">Histórico</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Vista de tarjetas para móviles -->
        <div class="md:hidden">
            <div v-for="modelo in modelosFiltrados" :key="modelo.id"
                class="bg-white shadow overflow-hidden sm:rounded-lg mb-4">
                <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
                    <div class="flex items-center">
                        <div class="flex-shrink-0 h-10 w-10">
                            <img class="h-10 w-10 rounded-full"
                                :src="`https://ui-avatars.com/api/?name=${modelo.nombres}+${modelo.apellidos}&background=random`"
                                alt="">
                        </div>
                        <div class="ml-4">
                            <h3 class="text-lg leading-6 font-medium text-gray-900">
                                {{ modelo.nombres }} {{ modelo.apellidos }}
                            </h3>
                            <p class="text-sm text-gray-500">
                                {{ modelo.nombre_usuario }}
                            </p>
                        </div>
                    </div>
                </div>
                <div class="border-t border-gray-200 px-4 py-5 sm:p-0">
                    <dl class="sm:divide-y sm:divide-gray-200">
                        <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt class="text-sm font-medium text-gray-500">Acciones</dt>
                            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                <button @click="abrirFormularioDeduccion(modelo)"
                                    class="text-indigo-600 hover:text-indigo-900 mr-3">Crear deducción</button>
                                <button @click="abrirModalDeduciblesActivos(modelo)"
                                    class="text-green-600 hover:text-green-900 mr-3">Deducibles activos</button>
                                <button @click="abrirModalHistorico(modelo)"
                                    class="text-yellow-600 hover:text-yellow-900">Histórico</button>
                            </dd>
                        </div>
                    </dl>
                </div>
            </div>
        </div>

        <div class="mt-4 flex items-center justify-between">
            <div>
                <p class="text-sm text-gray-700">
                    Mostrando <span class="font-medium">{{ paginationStart + 1 }}</span> a <span class="font-medium">{{
                        paginationEnd }}</span> de <span class="font-medium">{{ modelosFiltrados.length }}</span>
                    resultados
                </p>
            </div>
            <div>
                <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                    <button @click="prevPage" :disabled="currentPage === 1"
                        class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                        Anterior
                    </button>
                    <button @click="nextPage" :disabled="currentPage === totalPages"
                        class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                        Siguiente
                    </button>
                </nav>
            </div>
        </div>

        <!-- Modal Base Component -->
        <div v-if="openModal || openActiveDebtModal || openRecordModal || openSimulationModal"
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="closeAllModals">
            <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-4/5 lg:w-3/5 shadow-lg rounded-md bg-white"
                @click.stop>
                <!-- Modal content goes here -->

                <!-- Modal para Crear Deducción -->
                <div v-if="openModal && modeloSeleccionado" class="modal-content">
                    <h3 class="text-lg font-semibold text-center text-gray-700 mb-4">
                        Crear Deducción para {{ modeloSeleccionado.nombres }} {{ modeloSeleccionado.apellidos }}
                    </h3>
                    <form @submit.prevent="guardarDeduccion" class="space-y-4">
                        <div>
                            <label for="concepto" class="block text-sm font-medium text-gray-700">Concepto</label>
                            <input id="concepto" type="text" v-model="deduccion.concepto"
                                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                        </div>
                        <div>
                            <label for="valor-total" class="block text-sm font-medium text-gray-700">Valor Total</label>
                            <input id="valor-total" type="text" v-model="formattedValorTotal"
                                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                        </div>
                        <div>
                            <label for="plazo" class="block text-sm font-medium text-gray-700">Plazo (máx 6
                                periodos)</label>
                            <input id="plazo" type="number" v-model.number="deduccion.plazo" max="6"
                                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                        </div>
                        <div>
                            <label for="tasa" class="block text-sm font-medium text-gray-700">Tasa de Interés</label>
                            <input id="tasa" type="number" v-model.number="deduccion.tasa" step="0.01" min="0"
                                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                        </div>
                        <div class="flex justify-between">
                            <button v-if="!removeSimulationButton" type="button" @click="simularDeduccion"
                                class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded">Simular</button>
                            <button v-if="removeSimulationButton" type="submit"
                                class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-6 rounded">Crear</button>
                            <button @click="closeAllModals"
                                class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded">Cancelar</button>
                        </div>
                    </form>
                </div>

                <!-- Modal para ver deducibles activos -->
                <div v-if="openActiveDebtModal && modeloSeleccionado" class="modal-content">
                    <h3 class="text-2xl font-semibold text-center text-gray-800 mb-6">
                        Deducciones activas para {{ modeloSeleccionado.nombres }} {{ modeloSeleccionado.apellidos }}
                    </h3>
                    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div v-if="modeloSeleccionado.deducibles.filter(d => d.estado === 'Activo').length > 0">
                            <div v-for="(deducible, index) in modeloSeleccionado.deducibles.filter(d => d.estado === 'Activo')"
                                :key="index" class="border-t border-gray-200">
                                <dl>
                                    <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                        <dt class="text-sm font-medium text-gray-500">Concepto</dt>
                                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{
                                            deducible.concepto }}</dd>
                                    </div>
                                    <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                        <dt class="text-sm font-medium text-gray-500">Valor Total</dt>
                                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{
                                            formatCurrency(deducible.valor_total) }}</dd>
                                    </div>
                                    <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                        <dt class="text-sm font-medium text-gray-500">Plazo</dt>
                                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ deducible.plazo
                                            }} períodos</dd>
                                    </div>
                                    <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                        <dt class="text-sm font-medium text-gray-500">Estado</dt>
                                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                            <span
                                                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                                {{ deducible.estado }}
                                            </span>
                                        </dd>
                                    </div>
                                    <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                        <dt class="text-sm font-medium text-gray-500">Fecha de inicio</dt>
                                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{
                                            formatDate(deducible.fecha_inicio) }}</dd>
                                    </div>
                                </dl>
                            </div>
                        </div>
                        <div v-else class="px-4 py-5 sm:px-6">
                            <p class="text-center text-gray-500">No cuenta con deducciones activas.</p>
                        </div>
                    </div>
                    <div class="mt-4 flex justify-end">
                        <button @click="closeAllModals"
                            class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded">Cerrar</button>
                    </div>
                </div>

                <!-- Modal para ver el historial de deducibles -->
                <div v-if="openRecordModal && modeloSeleccionado" class="modal-content">
                    <h3 class="text-2xl font-semibold text-center text-gray-800 mb-6">
                        Historial de deducciones para {{ modeloSeleccionado.nombres }} {{ modeloSeleccionado.apellidos
                        }}
                    </h3>
                    <div class="mb-4">
                        <label for="month-select" class="block text-sm font-medium text-gray-700">Seleccionar
                            mes:</label>
                        <select id="month-select" v-model="selectedMonth" @change="filterDeduciblesByMonth"
                            class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
                            <option v-for="month in availableMonths" :key="month" :value="month">
                                {{ formatMonth(month) }}
                            </option>
                        </select>
                    </div>
                    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div v-if="paginatedDeducibles.length > 0">
                            <div v-for="(deducible, index) in paginatedDeducibles" :key="index"
                                class="border-t border-gray-200">
                                <dl>
                                    <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                        <dt class="text-sm font-medium text-gray-500">Concepto</dt>
                                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{
                                            deducible.concepto }}</dd>
                                    </div>
                                    <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                        <dt class="text-sm font-medium text-gray-500">Valor Total</dt>
                                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{
                                            formatCurrency(deducible.valor_total) }}</dd>
                                    </div>
                                    <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                        <dt class="text-sm font-medium text-gray-500">Plazo</dt>
                                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ deducible.plazo
                                            }} períodos</dd>
                                    </div>
                                    <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                        <dt class="text-sm font-medium text-gray-500">Estado</dt>
                                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                            <span
                                                :class="deducible.estado === 'Activo' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                                                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                                                {{ deducible.estado }}
                                            </span>
                                        </dd>
                                    </div>
                                    <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                        <dt class="text-sm font-medium text-gray-500">Fecha de inicio</dt>
                                        <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{
                                            formatDate(deducible.fecha_inicio) }}</dd>
                                    </div>
                                </dl>
                            </div>
                        </div>
                        <div v-else class="px-4 py-5 sm:px-6">
                            <p class="text-center text-gray-500">No hay deducciones para este mes.</p>
                        </div>
                    </div>
                    <div class="mt-4 flex items-center justify-between">
                        <div>
                            <p class="text-sm text-gray-700">
                                Mostrando <span class="font-medium">{{ paginationStart + 1 }}</span> a <span
                                    class="font-medium">{{ paginationEnd }}</span> de <span class="font-medium">{{
                                        filteredDeducibles.length }}</span> resultados
                            </p>
                        </div>
                        <div>
                            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
                                aria-label="Pagination">
                                <button @click="prevPage" :disabled="currentPage === 1"
                                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                                    Anterior
                                </button>
                                <button @click="nextPage" :disabled="currentPage === totalPages"
                                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                                    Siguiente
                                </button>
                            </nav>
                        </div>
                    </div>
                    <div class="mt-4 flex justify-end">
                        <button @click="closeAllModals"
                            class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded">Cerrar</button>
                    </div>
                </div>
                <!-- Modal de Simulación -->
                <div v-if="openSimulationModal" class="modal-content">
                    <h3 class="text-lg font-semibold mb-4">Detalle de la Simulación</h3>
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Periodo</th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Cuota Mensual</th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Principal</th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Interés</th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Balance Restante</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                <tr v-for="pago in pagosDetalle" :key="pago.mes">
                                    <td class="px-6 py-4 whitespace-nowrap">{{ pago.mes }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.cuotaMensual) }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.principal) }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.interes) }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.balanceRestante) }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="mt-4 p-4 bg-gray-100 rounded-lg">
                        <h4 class="text-lg font-semibold mb-2">Resumen del Préstamo</h4>
                        <p>Número de periodos: {{ resumenPrestamo.numeroPeriodos }}</p>
                        <p>Valor a adeudar: {{ formatCurrency(resumenPrestamo.valorAdeudar) }}</p>
                        <p>Valor total con intereses: {{ formatCurrency(resumenPrestamo.valorConIntereses) }}</p>
                        <p>Cuota mensual: {{ formatCurrency(resumenPrestamo.cuotaMensual) }}</p>
                    </div>
                    <div class="mt-4 flex justify-end space-x-4">
                        <button @click="acceptSimulation"
                            class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">Aceptar</button>
                        <button @click="closeAllModals"
                            class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded">Cerrar</button>
                    </div>
                </div>

            </div>
        </div>
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




const deduccion = ref({
    concepto: '',
    valor_total: 0,  // Asegúrate de que estos no son undefined o strings vacíos
    plazo: 0,
    tasa: 0
});

const selectedMonth = ref('');
const currentPage = ref(1);
const itemsPerPage = 5;



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
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' });
};



const closeAllModals = () => {
    openModal.value = false;
    openActiveDebtModal.value = false;
    openRecordModal.value = false;
    openSimulationModal.value = false;
    removeSimulationButton.value = false;
};

const acceptSimulation = () => {
    openSimulationModal.value = false;
    removeSimulationButton.value = true;
};

const simularDeduccion = () => {
    const valorTotal = parseFloat(deduccion.value.valor_total) || 0;
    const plazo = parseInt(deduccion.value.plazo, 10) || 0;
    const tasa = parseFloat(deduccion.value.tasa) || 0;

    if (valorTotal <= 0 || plazo <= 0 || tasa < 0) {
        alert('Por favor, introduzca valores válidos. Todos los campos deben ser números y mayores que cero.');
        return;
    }

    const tasaQuincenal = tasa / 2;
    const cuotaQuincenal = valorTotal / plazo * (1 + tasaQuincenal);
    let saldoCapital = valorTotal;
    pagosDetalle.value = [];

    for (let i = 1; i <= plazo; i++) {
        const interes = saldoCapital * tasaQuincenal;
        const principal = cuotaQuincenal - interes;
        saldoCapital -= principal;
        pagosDetalle.value.push({
            periodo: i,
            cuotaQuincenal: cuotaQuincenal.toFixed(2),
            principal: principal.toFixed(2),
            interes: interes.toFixed(2),
            saldoCapital: saldoCapital.toFixed(2)
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

    // Filtrar solo usuarios habilitados
    let filtered = modelos.value.filter(modelo => modelo.habilitado);

    // Aplicar filtro de búsqueda
    if (filtro.value) {
        const filtroLowerCase = filtro.value.toLowerCase();
        filtered = filtered.filter(modelo =>
            modelo.nombre_usuario.toLowerCase().includes(filtroLowerCase) ||
            modelo.nombres.toLowerCase().includes(filtroLowerCase) ||
            modelo.apellidos.toLowerCase().includes(filtroLowerCase)
        );
    }

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

const estadoDeduccion = (deduccion) => {
    if (deduccion.estado === 'Activo') {
        return 'Activo';
    }
    return 'Pagado';
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
    try {
        isLoading.value = true;
        // Parse deduccion.valor_total to ensure it is a number
        deduccion.value.valor_total = parseFloat(deduccion.value.valor_total);
        const response = await modelosStore.crearDeduccion(modeloSeleccionado.value.nombre_usuario, deduccion.value);
        modelos.value = await modelosStore.fetchModelos(); // Reload list of models
        openModal.value = false;
        isLoading.value = false;
        Swal.fire('Éxito', response.mensaje, 'success');
    } catch (error) {
        Swal.fire('Error', error.response?.data?.error || 'Ha ocurrido un error', 'error');
    }
};

const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
    }).format(value);
};



isLoading.value = true;
modelos.value = await modelosStore.fetchModelos();
isLoading.value = false;

</script>

// Cargar modelos al inicio
modelos.val
<style scoped>
.table-auto {
    width: 100%;
    border-collapse: collapse;
}

.table-auto th,
.table-auto td {
    padding: 8px;
    border: 1px solid #ddd;
}

.table-auto th {
    background-color: #f8f8f8;
}

.button-disabled {
    background-color: #999;
    cursor: not-allowed;
    opacity: 0.5;
}


/* remove arrows input number */
</style>
