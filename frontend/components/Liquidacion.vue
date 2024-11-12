<template>
    <div class="container mx-auto p-4">
        <loading :is-loading="isLoading"></loading>

        <div class="mb-4 flex flex-col sm:flex-row justify-between items-center">
            <h2 class="text-2xl font-bold mb-4 sm:mb-0">Liquidar Ganancias</h2>
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
                            class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Estado</th>
                        <th scope="col"
                            class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Acciones</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="modelo in paginatedModelos" :key="modelo.id" class="hover:bg-gray-50">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex items-center">
                                <div class="flex-shrink-0 h-10 w-10">
                                    <img class="h-10 w-10 rounded-full"
                                        :src="`https://ui-avatars.com/api/?name=${modelo.nombres}+${modelo.apellidos}&background=random`"
                                        alt="">
                                </div>
                                <div class="ml-4">
                                    <div class="text-sm font-medium text-gray-900">{{ modelo.nombres }} {{
                                        modelo.apellidos }}</div>
                                    <div class="text-sm text-gray-500">{{ modelo.nombre_usuario }}</div>
                                </div>
                            </div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-center">
                            <span :class="estadoGanancia(modelo).color"
                                class="flex items-center justify-center text-xs">
                                <Icon class="mr-1" :name="estadoGanancia(modelo).icono" />
                                {{ estadoGanancia(modelo).texto }}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                            <button @click="seleccionarModelo(modelo)"
                                :disabled="modelo.periodo_actual === modelo.ganancia_info.ultimo_periodo"
                                :class="{ 'opacity-50 cursor-not-allowed': modelo.periodo_actual === modelo.ganancia_info.ultimo_periodo }"
                                class="text-indigo-600 hover:text-indigo-900 mr-2">
                                Liquidar
                            </button>
                            <button @click="verGanancia(modelo)"
                                :disabled="modelo.estado_ganancia === 'Pendiente' || modelo.periodo_actual !== modelo.ganancia_info.ultimo_periodo"
                                :class="{ 'opacity-50 cursor-not-allowed': modelo.estado_ganancia === 'Pendiente' || modelo.periodo_actual !== modelo.ganancia_info.ultimo_periodo }"
                                class="text-green-600 hover:text-green-900">
                                Ver ganancia
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Vista de tarjetas para móviles -->
        <div class="md:hidden space-y-4">
            <div v-for="modelo in paginatedModelos" :key="modelo.id"
                class="bg-white shadow overflow-hidden sm:rounded-lg">
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
                    <span :class="estadoGanancia(modelo).color" class="flex items-center text-xs">
                        <Icon class="mr-1" :name="estadoGanancia(modelo).icono" />
                        {{ estadoGanancia(modelo).texto }}
                    </span>
                </div>
                <div class="border-t border-gray-200 px-4 py-4">
                    <div class="flex justify-between">
                        <button @click="seleccionarModelo(modelo)"
                            :disabled="modelo.periodo_actual === modelo.ganancia_info.ultimo_periodo"
                            :class="{ 'opacity-50 cursor-not-allowed': modelo.periodo_actual === modelo.ganancia_info.ultimo_periodo }"
                            class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">
                            Liquidar
                        </button>
                        <button @click="verGanancia(modelo)"
                            :disabled="modelo.estado_ganancia === 'Pendiente' || modelo.periodo_actual !== modelo.ganancia_info.ultimo_periodo"
                            :class="{ 'opacity-50 cursor-not-allowed': modelo.estado_ganancia === 'Pendiente' || modelo.periodo_actual !== modelo.ganancia_info.ultimo_periodo }"
                            class="text-green-600 hover:text-green-900 text-sm font-medium">
                            Ver ganancia
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Paginación -->
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

        <!-- Modal para ver ganancias -->
        <div v-if="gananciaSeleccionada"
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
            @click="cerrarGananciaSeleccionada">
            <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-4/5 lg:w-3/5 shadow-lg rounded-md bg-white"
                @click.stop>
                <h3 class="text-xl font-semibold mb-4">Detalles de Ganancia</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-gray-100 p-3 rounded">
                        <p class="font-semibold">Id liquidación:</p>
                        <p>{{ gananciaSeleccionada.id }}</p>
                    </div>
                    <div class="bg-gray-100 p-3 rounded">
                        <p class="font-semibold">Periodo:</p>
                        <p>{{ gananciaSeleccionada.nombre_periodo }}</p>
                    </div>
                    <div class="bg-gray-100 p-3 rounded">
                        <p class="font-semibold">Deducción:</p>
                        <p>{{ formatCurrency(gananciaSeleccionada.total_deducibles) }}</p>
                    </div>
                    <div class="bg-gray-100 p-3 rounded">
                        <p class="font-semibold">Total COP:</p>
                        <p>{{ formatCurrency(gananciaSeleccionada.gran_total_cop) }}</p>
                    </div>
                    <div class="bg-gray-100 p-3 rounded">
                        <p class="font-semibold">Porcentaje de ganancia:</p>
                        <p>{{ (gananciaSeleccionada.porcentaje * 100).toFixed(2) }}%</p>
                    </div>
                    <div class="bg-gray-100 p-3 rounded">
                        <p class="font-semibold">TRM:</p>
                        <p>{{ formatCurrency(gananciaSeleccionada.trm) }}</p>
                    </div>
                </div>

                <h4 class="text-lg font-semibold mt-6 mb-3">Detallado por página</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div v-for="(detalle, index) in gananciaSeleccionada.detalles_paginas" :key="index"
                        class="bg-gray-100 p-3 rounded flex flex-col items-center justify-center">
                        <p class="font-semibold">{{ detalle.nombre_pagina }}</p>
                        <p>Tokens: {{ detalle.tokens }}</p>
                        <p>Total COP: {{ formatCurrency(detalle.total_cop) }}</p>
                    </div>
                </div>

                <div class="mt-6 flex justify-end">
                    <button @click="cerrarGananciaSeleccionada"
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mr-1 rounded">
                        Cerrar
                    </button>
                    <button v-if="gananciaSeleccionada.estado === 'Pagado'" @click="pagarGanancia"
                        class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 mr-1 rounded">
                        Re-enviar pago
                    </button>
                    <button v-else @click="pagarGanancia"
                        class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 mr-1 rounded">
                        Realizar pago
                    </button>
                    <button @click="eliminarLiquidacion"
                        class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                        Deshacer pago
                    </button>
                </div>
            </div>
        </div>
        <!-- Modal para liquidar ganancias -->
        <div v-if="modeloSeleccionado"
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
            @click="cerrarLiquidacion">
            <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-4/5 lg:w-3/5 shadow-lg rounded-md bg-white"
                @click.stop>
                <h3 class="text-xl font-semibold mb-6">Liquidar a {{ modeloSeleccionado.nombre_usuario }}</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div v-for="pagina in modeloSeleccionado.paginas_habilitadas" :key="pagina"
                        class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                        <label :for="`pagina-${pagina}`" class="block text-sm font-medium text-gray-700 mb-2">
                            {{ pagina }}:
                            <span v-if="pagina === 'Streamate'" class="text-xs text-blue-500">(en dólares)</span>
                        </label>
                        <input type="number" v-model="gananciaForm.paginas[pagina]" :id="`pagina-${pagina}`"
                            class="w-full bg-white border border-gray-300 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            :placeholder="pagina === 'Streamate' ? 'Ingresar valor en dólares' : 'Ingresar tokens'">
                    </div>
                </div>
                <div class="mt-6 flex justify-end space-x-4">
                    <button @click="liquidarGanancias"
                        class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-6 rounded-lg">
                        Confirmar
                    </button>
                    <button @click="cerrarLiquidacion"
                        class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-6 rounded-lg">
                        Cancelar
                    </button>
                </div>
            </div>
        </div>

    </div>
</template>


<script setup>
import { is } from 'date-fns/locale';
import { ref, computed } from 'vue';
import { useModelosStore } from '~/stores/modelo';

const modelosStore = useModelosStore();
const isLoading = ref(false);
const openModal = ref(false);
const modelos = ref([]);
const filtro = ref('');
const modeloSeleccionado = ref(null);
const gananciaSeleccionada = ref(null);
const gananciaForm = ref({
    nombre_usuario: '',
    paginas: {}
});

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
            modelo.habilitado === true;
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
        return { texto: 'Pendiente', color: 'text-gray-500', icono: 'material-symbols:pending-actions' };
    } else if (modelo.estado_ganancia === 'Liquidado') {
        return { texto: 'Liquidado', color: 'text-yellow-500', icono: 'material-symbols:playlist-add-check-circle-outline' };
    } else if (modelo.estado_ganancia === 'Pagado') {
        return { texto: 'Pagado', color: 'text-green-500', icono: 'material-symbols:payments' };
    } else {
        return { texto: 'Desconocido', color: 'text-gray-500', icono: 'mdi-help-circle' };
    }
};

const liquidarGanancias = async () => {
    try {
        isLoading.value = true;
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
        isLoading.value = false;
        Swal.fire('Éxito', response.mensaje, 'success');
    } catch (error) {
        Swal.fire('Error', error.response.data.error, 'error');
        console.error(error);
    }
};

const pagarGanancia = async () => {
    try {
        isLoading.value = true;
        const response = await modelosStore.fetchPagarGanancia(gananciaSeleccionada.value.id);
        console.log(response);
        Swal.fire('Éxito', 'Ganancia pagada correctamente', 'success');
        cerrarGananciaSeleccionada();
        isLoading.value = false;
        modelos.value = await modelosStore.fetchModelos();
    } catch (error) {
        console.error("Error al pagar ganancia:", error);
        Swal.fire('Error', 'Hubo un problema al pagar la ganancia', 'error');
    }
};

const eliminarLiquidacion = async () => {
    try {
        isLoading.value = true;
        const response = await modelosStore.eliminarLiquidacion(gananciaSeleccionada.value.id);
        console.log(response);
        Swal.fire('Éxito', 'Liquidación eliminada correctamente', 'success');
        isLoading.value = false;
        cerrarGananciaSeleccionada();
        modelos.value = await modelosStore.fetchModelos();
    } catch (error) {
        console.error("Error al eliminar liquidación:", error);
        Swal.fire('Error', 'Hubo un problema al eliminar la liquidación', 'error');
    }
};


const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
    }).format(value);
};

const formatDate = (date) => {
    // Formato de fecha en español, nombre del mes y día de la semana
    return new Intl.DateTimeFormat('es-CO', {
        dateStyle: 'full',
    }).format(new Date(date));

};

modelos.value = await modelosStore.fetchModelos();
</script>

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
    opacity: 0.5 !important;
}
</style>
