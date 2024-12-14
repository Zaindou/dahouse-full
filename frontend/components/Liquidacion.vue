<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header Section -->
        <div class="bg-white shadow">
            <div class="px-4 py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
                <div class="flex flex-col items-start justify-between gap-4 md:flex-row md:items-center">
                    <div>
                        <h1 class="text-2xl font-bold tracking-tight text-gray-900">Liquidar Ganancias</h1>
                        <p class="mt-1 text-sm text-gray-500">Gestiona y procesa los pagos de tus modelos</p>
                    </div>
                    <div class="relative w-full md:w-64">
                        <div class="absolute inset-y-0 left-0 flex items-center pl-3">
                            <Icon name="uil:search" class="w-5 h-5 text-gray-400" />
                        </div>
                        <input v-model="filtro" type="text" placeholder="Buscar modelos..."
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
                    <div class="flex items-center space-x-4">
                        <div class="w-12 h-12 bg-gray-200 rounded-full"></div>
                        <div class="flex-1">
                            <div class="w-3/4 h-4 bg-gray-200 rounded"></div>
                            <div class="w-1/2 h-3 mt-2 bg-gray-200 rounded"></div>
                        </div>
                    </div>
                    <div class="h-4 mt-4 bg-gray-200 rounded"></div>
                    <div class="flex justify-end mt-4 space-x-2">
                        <div class="w-20 h-8 bg-gray-200 rounded"></div>
                        <div class="w-20 h-8 bg-gray-200 rounded"></div>
                    </div>
                </div>
            </div>

            <!-- Users Grid -->
            <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                <div v-for="modelo in paginatedModelos" :key="modelo.id"
                    class="overflow-hidden transition-shadow duration-200 bg-white rounded-lg shadow-sm hover:shadow-lg">
                    <div class="p-6">
                        <!-- User Header -->
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

                        <!-- Status Badge -->
                        <div class="flex items-center justify-center py-3">
                            <span :class="[
                                'inline-flex items-center px-3 py-1 rounded-full text-sm font-medium',
                                estadoGanancia(modelo).bgColor,
                                estadoGanancia(modelo).textColor
                            ]">
                                <Icon :name="estadoGanancia(modelo).icono" class="w-4 h-4 mr-2" />
                                {{ estadoGanancia(modelo).texto }}
                            </span>
                        </div>

                        <!-- Action Buttons -->
                        <div class="grid grid-cols-2 gap-4 mt-4">
                            <button @click="seleccionarModelo(modelo)"
                                :disabled="modelo.periodo_actual === modelo.ganancia_info.ultimo_periodo"
                                class="flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed">
                                <Icon name="uil:money-withdrawal" class="w-5 h-5 mr-2" />
                                Liquidar
                            </button>
                            <button @click="verGanancia(modelo)"
                                :disabled="modelo.estado_ganancia === 'Pendiente' || modelo.periodo_actual !== modelo.ganancia_info.ultimo_periodo"
                                class="flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed">
                                <Icon name="uil:eye" class="w-5 h-5 mr-2" />
                                Ver ganancia
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
                        class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                        <Icon name="uil:angle-left" class="w-4 h-4 mr-1" />
                        Anterior
                    </button>
                    <button @click="nextPage" :disabled="currentPage === totalPages"
                        class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                        Siguiente
                        <Icon name="uil:angle-right" class="w-4 h-4 ml-1" />
                    </button>
                </div>
            </div>

            <!-- Modales -->
            <Teleport to="body">
                <!-- Modal Liquidar Ganancias -->
                <div v-if="modeloSeleccionado" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50"
                    @click="cerrarLiquidacion">
                    <div class="min-h-screen px-4 text-center">
                        <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
                        <div class="inline-block w-full max-w-2xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
                            @click.stop>
                            <div class="flex items-center justify-between mb-4">
                                <h3 class="text-lg font-semibold text-gray-900">
                                    Liquidar a {{ modeloSeleccionado.nombre_usuario }}
                                </h3>
                                <button @click="cerrarLiquidacion" class="text-gray-500 hover:text-gray-700">
                                    <Icon name="uil:times" class="w-6 h-6" />
                                </button>
                            </div>

                            <div class="grid gap-6 mt-4">
                                <div v-for="pagina in modeloSeleccionado.paginas_habilitadas" :key="pagina"
                                    class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
                                    <label :for="`pagina-${pagina}`"
                                        class="block mb-2 text-sm font-medium text-gray-700">
                                        {{ pagina }}
                                        <span v-if="pagina === 'Streamate'" class="text-xs text-blue-500">
                                            (en dólares)
                                        </span>
                                    </label>
                                    <div class="relative">
                                        <div class="absolute inset-y-0 left-0 flex items-center pl-3">
                                            <span class="text-gray-500">
                                                {{ pagina === 'Streamate' ? '$' : '#' }}
                                            </span>
                                        </div>
                                        <input type="number" v-model="gananciaForm.paginas[pagina]"
                                            :id="`pagina-${pagina}`"
                                            class="block w-full pl-8 pr-4 border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                                            :placeholder="pagina === 'Streamate' ? 'Valor en dólares' : 'Cantidad de tokens'" />
                                    </div>
                                </div>
                            </div>

                            <div class="flex justify-end mt-6 space-x-4">
                                <button @click="liquidarGanancias" :disabled="isLoadingLiquidacion"
                                    class="inline-flex items-center px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed">
                                    <Icon v-if="isLoadingLiquidacion" name="uil:spinner"
                                        class="w-5 h-5 mr-2 animate-spin" />
                                    <Icon v-else name="uil:check" class="w-5 h-5 mr-2" />
                                    {{ isLoadingLiquidacion ? 'Procesando...' : 'Confirmar' }}
                                </button>
                                <button @click="cerrarLiquidacion" :disabled="isLoadingLiquidacion"
                                    class="inline-flex items-center px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">
                                    <Icon name="uil:times" class="w-5 h-5 mr-2" />
                                    Cancelar
                                </button>
                            </div>
                        </div>
                    </div>
                </div>


                <!-- Modal Ver Ganancia -->
                <div v-if="gananciaSeleccionada" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50"
                    @click="cerrarGananciaSeleccionada">
                    <div class="min-h-screen px-4 text-center">
                        <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
                        <div class="inline-block w-full max-w-3xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
                            @click.stop>
                            <div class="flex items-center justify-between mb-6">
                                <h3 class="text-xl font-semibold text-gray-900">Detalles de Ganancia</h3>
                                <button @click="cerrarGananciaSeleccionada" class="text-gray-500 hover:text-gray-700">
                                    <Icon name="uil:times" class="w-6 h-6" />
                                </button>
                            </div>

                            <!-- Información General -->
                            <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
                                <div class="p-4 rounded-lg bg-gray-50">
                                    <p class="text-sm font-medium text-gray-500">Id liquidación</p>
                                    <p class="mt-1 text-lg font-semibold">{{ gananciaSeleccionada.id }}</p>
                                </div>
                                <div class="p-4 rounded-lg bg-gray-50">
                                    <p class="text-sm font-medium text-gray-500">Periodo</p>
                                    <p class="mt-1 text-lg font-semibold">{{ gananciaSeleccionada.nombre_periodo }}
                                    </p>
                                </div>
                                <div class="p-4 rounded-lg bg-gray-50">
                                    <p class="text-sm font-medium text-gray-500">TRM</p>
                                    <p class="mt-1 text-lg font-semibold">{{
                                        formatCurrency(gananciaSeleccionada.trm) }}
                                    </p>
                                </div>
                                <div class="p-4 rounded-lg bg-gray-50">
                                    <p class="text-sm font-medium text-gray-500">Deducción</p>
                                    <p class="mt-1 text-lg font-semibold text-red-600">
                                        {{ formatCurrency(gananciaSeleccionada.total_deducibles) }}
                                    </p>
                                </div>
                                <div class="p-4 rounded-lg bg-gray-50">
                                    <p class="text-sm font-medium text-gray-500">Total COP</p>
                                    <p class="mt-1 text-lg font-semibold text-green-600">
                                        {{ formatCurrency(gananciaSeleccionada.gran_total_cop) }}
                                    </p>
                                </div>
                                <div class="p-4 rounded-lg bg-gray-50">
                                    <p class="text-sm font-medium text-gray-500">Porcentaje</p>
                                    <p class="mt-1 text-lg font-semibold text-blue-600">
                                        {{ (gananciaSeleccionada.porcentaje * 100).toFixed(2) }}%
                                    </p>
                                </div>
                            </div>

                            <!-- Detalle por Página -->
                            <h4 class="mt-8 mb-4 text-lg font-semibold text-gray-900">Detalle por Página</h4>
                            <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
                                <div v-for="detalle in gananciaSeleccionada.detalles_paginas"
                                    :key="detalle.nombre_pagina" class="p-4 rounded-lg bg-gray-50">
                                    <div class="flex items-center justify-between mb-2">
                                        <h5 class="text-lg font-medium text-gray-900">
                                            {{ detalle.nombre_pagina }}
                                        </h5>
                                        <span
                                            class="px-3 py-1 text-sm font-medium text-green-800 bg-green-100 rounded-full">
                                            {{ formatCurrency(detalle.total_cop) }}
                                        </span>
                                    </div>
                                    <div class="mt-2 space-y-1">
                                        <div class="flex items-center justify-between text-sm">
                                            <span class="text-gray-500">Tokens/Dólares:</span>
                                            <span class="font-medium">{{ detalle.tokens }}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Botones de Acción -->
                            <div class="flex flex-wrap justify-end gap-3 mt-8">
                                <button @click="cerrarGananciaSeleccionada"
                                    class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                                    <Icon name="uil:times" class="w-5 h-5 mr-2" />
                                    Cerrar
                                </button>

                                <button v-if="gananciaSeleccionada.estado === 'Pagado'" @click="pagarGanancia"
                                    :disabled="isLoadingPago"
                                    class="inline-flex items-center px-4 py-2 text-sm font-medium text-yellow-700 bg-yellow-100 border border-transparent rounded-lg hover:bg-yellow-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 disabled:opacity-50 disabled:cursor-not-allowed">
                                    <Icon v-if="isLoadingPago" name="uil:spinner" class="w-5 h-5 mr-2 animate-spin" />
                                    <Icon v-else name="uil:redo" class="w-5 h-5 mr-2" />
                                    {{ isLoadingPago ? 'Procesando...' : 'Re-enviar pago' }}
                                </button>

                                <button v-else @click="pagarGanancia" :disabled="isLoadingPago"
                                    class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed">
                                    <Icon v-if="isLoadingPago" name="uil:spinner" class="w-5 h-5 mr-2 animate-spin" />
                                    <Icon v-else name="uil:money-withdraw" class="w-5 h-5 mr-2" />
                                    {{ isLoadingPago ? 'Procesando...' : 'Realizar pago' }}
                                </button>

                                <button @click="eliminarLiquidacion" :disabled="isLoadingEliminar"
                                    class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed">
                                    <Icon v-if="isLoadingEliminar" name="uil:spinner"
                                        class="w-5 h-5 mr-2 animate-spin" />
                                    <Icon v-else name="uil:trash-alt" class="w-5 h-5 mr-2" />
                                    {{ isLoadingEliminar ? 'Eliminando...' : 'Deshacer pago' }}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </Teleport>
        </div>
    </div>
</template>


<script setup>
import { ref, computed } from 'vue';
import { useModelosStore } from '~/stores/modelo';

const modelosStore = useModelosStore();
const isLoading = ref(false);
const initialSkeleton = ref(true);
const modelos = ref([]);
const filtro = ref('');
const modeloSeleccionado = ref(null);
const gananciaSeleccionada = ref(null);
const gananciaForm = ref({
    nombre_usuario: '',
    paginas: {}
});
const isLoadingPago = ref(false);
const isLoadingEliminar = ref(false);
const isLoadingLiquidacion = ref(false);

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


useHead({
    titleTemplate: '%s - Liquidación de ganancias',
})



const itemsPerPage = ref(10);
const currentPage = ref(1);

const paginatedModelos = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return modelosFiltrados.value.slice(start, end);
});

const totalPages = computed(() => Math.ceil(modelosFiltrados.value.length / itemsPerPage.value));
const paginationStart = computed(() => (currentPage.value - 1) * itemsPerPage.value);
const paginationEnd = computed(() => Math.min(currentPage.value * itemsPerPage.value, modelosFiltrados.value.length));

const prevPage = () => {
    if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
    if (currentPage.value < totalPages.value) currentPage.value++;
};

const cerrarGananciaSeleccionada = () => {
    gananciaSeleccionada.value = null;
};



const cerrarLiquidacion = () => {
    modeloSeleccionado.value = null;
    gananciaForm.value = { nombre_usuario: '', paginas: {} };
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



const seleccionarModelo = (modelo) => {
    modeloSeleccionado.value = modelo;
    gananciaForm.value.nombre_usuario = modelo.nombre_usuario;
    gananciaForm.value.paginas = {};
    gananciaSeleccionada.value = null;
};

const verGanancia = async (modelo) => {
    try {
        isLoading.value = true;
        const response = await modelosStore.fetchGananciaInfo(modelo.nombre_usuario, modelo.periodo_actual);
        gananciaSeleccionada.value = response;  // Asumiendo que la respuesta contiene directamente la información de ganancia
        isLoading.value = false;
    } catch (error) {
        console.error('Error al obtener la información de ganancia:', error);
        Swal.fire('Error', 'No se pudo obtener la información de ganancia', 'error');
        isLoading.value = false;
    }
};


const estadoGanancia = (modelo) => {
    if (modelo.periodo_actual !== modelo.ganancia_info.ultimo_periodo) {
        return {
            texto: 'Pendiente',
            textColor: 'text-gray-800',
            bgColor: 'bg-gray-100',
            icono: 'material-symbols:pending-actions'
        };
    } else if (modelo.estado_ganancia === 'Liquidado') {
        return {
            texto: 'Liquidado',
            textColor: 'text-yellow-800',
            bgColor: 'bg-yellow-100',
            icono: 'material-symbols:playlist-add-check-circle-outline'
        };
    } else if (modelo.estado_ganancia === 'Pagado') {
        return {
            texto: 'Pagado',
            textColor: 'text-green-800',
            bgColor: 'bg-green-100',
            icono: 'material-symbols:payments'
        };
    } else {
        return {
            texto: 'Desconocido',
            textColor: 'text-gray-800',
            bgColor: 'bg-gray-100',
            icono: 'mdi-help-circle'
        };
    }
};

const liquidarGanancias = async () => {
    if (isLoadingLiquidacion.value) return;

    try {
        isLoadingLiquidacion.value = true;
        const paginasArray = Object.entries(gananciaForm.value.paginas).map(([nombre, valor]) => ({
            nombre,
            valor
        }));

        const datosParaEnviar = {
            nombre_usuario: gananciaForm.value.nombre_usuario,
            paginas: paginasArray
        };

        const response = await modelosStore.liquidarGanancias(datosParaEnviar);
        cerrarLiquidacion();
        modelos.value = await modelosStore.fetchModelos();
        Swal.fire('Éxito', response.mensaje, 'success');
    } catch (error) {
        Swal.fire('Error', error.response?.data?.error || 'Error al liquidar ganancias', 'error');
        console.error(error);
    } finally {
        isLoadingLiquidacion.value = false;
    }
};

const pagarGanancia = async () => {
    if (isLoadingPago.value) return;

    try {
        isLoadingPago.value = true;
        const response = await modelosStore.fetchPagarGanancia(gananciaSeleccionada.value.id);
        Swal.fire('Éxito', 'Ganancia pagada correctamente', 'success');
        cerrarGananciaSeleccionada();
        modelos.value = await modelosStore.fetchModelos();
    } catch (error) {
        console.error("Error al pagar ganancia:", error);
        Swal.fire('Error', 'Hubo un problema al pagar la ganancia', 'error');
    } finally {
        isLoadingPago.value = false;
    }
};

const eliminarLiquidacion = async () => {
    if (isLoadingEliminar.value) return;

    try {
        isLoadingEliminar.value = true;
        await modelosStore.eliminarLiquidacion(gananciaSeleccionada.value.id);
        Swal.fire('Éxito', 'Liquidación eliminada correctamente', 'success');
        cerrarGananciaSeleccionada();
        modelos.value = await modelosStore.fetchModelos();
    } catch (error) {
        console.error("Error al eliminar liquidación:", error);
        Swal.fire('Error', 'Hubo un problema al eliminar la liquidación', 'error');
    } finally {
        isLoadingEliminar.value = false;
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

<style scoped>
.button-disabled {
    background-color: #999;
    cursor: not-allowed;
    opacity: 0.5 !important;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
