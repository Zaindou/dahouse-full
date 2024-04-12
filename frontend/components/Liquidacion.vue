<template>
    <div class="container mx-auto p-4">
        <loading :is-loading="isLoading"></loading>
        <h2 class="text-xl font-bold mb-4">Liquidar Ganancias</h2>
        <div class="mb-4">
            <input v-model="filtro" type="text" placeholder="Buscar por nombre de usuario..."
                class="block w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 rounded shadow leading-tight focus:outline-none focus:shadow-outline" />
        </div>
        <div class="bg-white shadow-md rounded my-6 overflow-hidden">
            <table class="text-left w-full border-collapse">
                <thead>
                    <tr class="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
                        <th class="py-3 px-6 text-left">Nombres</th>
                        <th class="py-3 px-6 text-center">Estado</th>
                        <th class="py-3 px-6 text-center">Acciones</th>
                    </tr>
                </thead>
                <tbody class="text-gray-600 text-sm font-light">
                    <tr v-for="modelo in modelosFiltrados.slice(0, 5)" :key="modelo.id"
                        class="border-b border-gray-200 hover:bg-gray-100">
                        <td class="py-3 px-6 text-left whitespace-nowrap">{{ modelo.nombres }} {{ modelo.apellidos }}
                        </td>
                        <td class="py-3 px-6 text-center">
                            <span :class="estadoGanancia(modelo).color" class="flex items-center justify-center">
                                <Icon class="mr-1" :name="estadoGanancia(modelo).icono" />
                                {{ estadoGanancia(modelo).texto }}
                            </span>
                        </td>
                        <td class="py-3 px-6 text-center">
                            <button @click="seleccionarModelo(modelo)"
                                :class="{ 'button-disabled': modelo.periodo_actual === modelo.ganancia_info.ultimo_periodo }"
                                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Liquidar</button>
                            <button @click="verGanancia(modelo)"
                                :disabled="modelo.estado_ganancia === 'Pendiente' || modelo.periodo_actual !== modelo.ganancia_info.ultimo_periodo"
                                :class="{ 'button-disabled': modelo.estado_ganancia === 'Pendiente' || modelo.periodo_actual !== modelo.ganancia_info.ultimo_periodo }"
                                class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded ml-2">Ver
                                Ganancia</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="gananciaSeleccionada" class="bg-white p-4 rounded-lg shadow-md mb-6">
            <div class="grid grid-cols-2 gap-4">
                <div class="bg-gray-100 p-2 rounded">
                    <p class="font-semibold">Id liquidación:</p>
                    <p>{{ gananciaSeleccionada.id }}</p>
                </div>
                <div class="bg-gray-100 p-2 rounded">
                    <p class="font-semibold">Periodo:</p>
                    <p>{{ gananciaSeleccionada.nombre_periodo }}</p>
                </div>
                <div>
                    <div class="bg-gray-100 p-2 rounded" @click="openModal = true">
                        <p class="font-semibold">Deducción:</p>
                        <p>{{ formatCurrency(gananciaSeleccionada.total_deducibles) }}</p>
                    </div>

                    <!-- Modal -->
                    <div v-if="openModal"
                        class="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center items-center">
                        <div class="bg-white p-4 rounded-lg max-w-md w-full">
                            <h3 class="font-bold text-lg">Detalles de deducibles</h3>
                            <div v-for="deducible in gananciaSeleccionada.detalles_deducibles.filter(d => d.estado === 'Activo' || d.estado === 'Pendiente')"
                                :key="deducible.concepto" class="py-2">
                                <p>Concepto: {{ deducible.concepto }}</p>
                                <p>Estado: {{ deducible.estado }}</p>
                                <p>Valor total: {{ formatCurrency(deducible.valor_total) }}</p>
                                <p>Valor quincenal: {{ formatCurrency(deducible.valor_quincenal) }}</p>
                                <p>Fecha de inicio: {{ deducible.fecha_inicio }}</p>
                                <p>Fecha de fin: {{ deducible.fecha_fin }}</p>
                                <!-- Agrega más detalles según necesites -->
                            </div>
                            <div class="flex justify-end mt-4">
                                <button @click="openModal = false"
                                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Cerrar</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="bg-gray-100 p-2 rounded">
                    <p class="font-semibold">Total COP:</p>
                    <p>{{ formatCurrency(gananciaSeleccionada.gran_total_cop) }}</p>
                </div>
                <div class="bg-gray-100 p-2 rounded">
                    <p class="font-semibold">Porcentaje de ganancia:</p>
                    <p>{{ gananciaSeleccionada.porcentaje * 100 }}%</p>
                </div>
                <div class="bg-gray-100 p-2 rounded">
                    <p class="font-semibold">TRM:</p>
                    <p>{{ formatCurrency(gananciaSeleccionada.trm) }}</p>
                </div>

            </div>
            <h3 class="text-base font-bold mb-4 mt-4">Detallado por página</h3>
            <div class="grid grid-cols-2 gap-4">
                <div v-for="(detalle, index) in gananciaSeleccionada.detalles_paginas" :key="index"
                    class="bg-gray-200 p-2 rounded flex flex-col items-center justify-center">
                    <p class="font-semibold">{{ detalle.nombre_pagina }}</p>
                    <p>Tokens: {{ detalle.tokens }}</p>
                    <p>Total COP: {{ formatCurrency(detalle.total_cop) }}</p>
                </div>
            </div>

        </div>
        <div v-if="modeloSeleccionado" class="mt-8">
            <div class="bg-white p-5 rounded-lg shadow-lg">
                <h3 class="text-lg font-semibold mb-4 text-gray-800">Liquidar a {{ modeloSeleccionado.nombre_usuario }}
                </h3>
                <div class="grid grid-cols-2 gap-6">
                    <div v-for="pagina in modeloSeleccionado.paginas_habilitadas" :key="pagina"
                        class="bg-gray-50 p-3 rounded-lg border border-gray-200">
                        <label :for="`pagina-${pagina}`" class="block text-sm font-medium text-gray-700 mb-2">
                            {{ pagina }}:
                            <span v-if="pagina === 'Streamate'" class="text-xs text-blue-500">(en dólares)</span>
                        </label>
                        <input type="number" v-model="gananciaForm.paginas[pagina]" :id="`pagina-${pagina}`"
                            class="w-full bg-white border border-gray-300 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            :placeholder="pagina === 'Streamate' ? 'Ingresar valor en dólares' : 'Ingresar tokens'">
                    </div>
                </div>
                <div class="flex justify-end mt-3">
                    <button @click="liquidarGanancias"
                        class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg mr-2">Confirmar</button>
                    <button @click="cerrarLiquidacion"
                        class="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg">Cerrar</button>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
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

const modelosFiltrados = computed(() => {
    if (!modelos.value) {
        return [];
    }
    return modelos.value.filter(modelo => {
        const filtroEnMinusculas = filtro.value.toLowerCase();
        return modelo.nombre_usuario.toLowerCase().includes(filtroEnMinusculas) ||
            modelo.nombres.toLowerCase().includes(filtroEnMinusculas) ||
            modelo.apellidos.toLowerCase().includes(filtroEnMinusculas);
    });
});

const seleccionarModelo = (modelo) => {
    modeloSeleccionado.value = modelo;
    gananciaForm.value.nombre_usuario = modelo.nombre_usuario;
    gananciaForm.value.paginas = {};
    gananciaSeleccionada.value = null;
};

const verGanancia = async (modelo) => {
    isLoading.value = true;
    await modelosStore.fetchGananciaInfo(modelo.nombre_usuario, modelo.periodo_actual);
    gananciaSeleccionada.value = modelosStore.gananciaInfo;
    cerrarLiquidacion();
    isLoading.value = false;
};

const cerrarLiquidacion = () => {
    modeloSeleccionado.value = null;
    gananciaForm.value = { nombre_usuario: '', paginas: {} };
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
        isLoading.value = false;
        modelos.value = await modelosStore.fetchModelos();
        Swal.fire('Éxito', response.mensaje, 'success');
    } catch (error) {
        Swal.fire('Error', error.response.data.error, 'error');
        console.error(error);
    }
};

const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
    }).format(value);
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
    opacity: 0.5;
}
</style>
