<template>
    <div class="container mx-auto p-4">
        <loading :is-loading="isLoading"></loading>
        <h2 class="text-xl font-bold mb-4">Gestionar Deducciones</h2>
        <!-- Búsqueda -->
        <div class="mb-4">
            <input v-model="filtro" type="text" placeholder="Buscar por nombre de usuario..."
                class="block w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 rounded shadow leading-tight focus:outline-none focus:shadow-outline">
        </div>
        <!-- Tabla de Modelos -->
        <div class="bg-white shadow-md rounded my-6 overflow-hidden">
            <table class="text-left w-full border-collapse">
                <thead>
                    <tr class="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
                        <th class="py-3 px-6 text-left">Nombre</th>
                        <th class="py-3 px-6 text-center">Acciones</th>
                    </tr>
                </thead>
                <tbody class="text-gray-600 text-sm font-light">
                    <tr v-for="modelo in modelosFiltrados" :key="modelo.id"
                        class="border-b border-gray-200 hover:bg-gray-100">
                        <td class="py-3 px-6 text-left whitespace-nowrap">{{ modelo.nombres }} {{ modelo.apellidos }}
                        </td>
                        <td class="py-3 px-6 text-center">
                            <button @click="abrirFormularioDeduccion(modelo)"
                                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Crear
                                deducción</button>
                            <button @click="abrirModalDeduciblesActivos(modelo)"
                                class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded ml-1">Deducibles
                                activos</button>
                            <button @click="abrirModalHistorico(modelo)"
                                class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded ml-1">Historico</button>
                            <!-- Botón para simular la deducción -->
                            <!-- <button @click="simularDeduccion(modelo)"
                                class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded ml-1">Simular
                                Deducción</button>-->

                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-if="openSimulationModal"
            class="fixed inset-0 bg-gray-900 bg-opacity-50 flex justify-center items-center z-50">
            <div class="bg-white p-4 rounded-lg shadow-lg max-w-4xl w-full mx-2">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-semibold">Detalle de la Simulación</h3>
                    <button @click="openSimulationModal = false, removeSimulationButton = true"
                        class="text-blue-500">Aceptar</button>
                    <button @click="openSimulationModal = false, removeSimulationButton = false"
                        class="text-red-500">Cerrar</button>

                </div>
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
                                <td class="px-6 py-4 whitespace-nowrap">{{ pago.principal }}</td>
                                <td class="px-6 py-4 whitespace-nowrap">{{ pago.interes }}</td>
                                <td class="px-6 py-4 whitespace-nowrap">{{ pago.balanceRestante }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="mt-4 p-4 bg-gray-100 rounded-lg">
                        <h3 class="text-lg font-semibold">Resumen del Préstamo</h3>
                        <p>Numero de periodos: {{ resumenPrestamo.numeroPeriodos }}</p>
                        <p>Valor a adeudar: {{ resumenPrestamo.valorAdeudar }}</p>
                        <p>Valor total con intereses: {{ resumenPrestamo.valorConIntereses }}</p>
                        <p>Cuota mensual: {{ resumenPrestamo.cuotaMensual }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal para Crear Deducción -->
        <div v-if="openModal && modeloSeleccionado"
            class="fixed inset-0 bg-black bg-opacity-60 z-40 flex justify-center items-center transition-opacity duration-300">
            <div class="bg-white p-6 rounded-lg shadow-xl max-w-lg w-full m-4">
                <h3 class="text-lg font-semibold text-center text-gray-700 mb-4">
                    Crear Deducción para {{ modeloSeleccionado.nombres }} {{
                        modeloSeleccionado.apellidos }}</h3>
                <form @submit.prevent="guardarDeduccion">
                    <input type="text" v-model="deduccion.concepto" placeholder="Concepto"
                        class="block w-full mb-4 p-3 border-gray-300 rounded-md focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50">
                    <input type="text" v-model="formattedValorTotal" placeholder="Valor Total"
                        class="block w-full mb-4 p-3 border-gray-300 rounded-md focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50">
                    <input type="number" v-model.number="deduccion.plazo" placeholder="Plazo (máx 6 periodos)" max="6"
                        class="block w-full mb-4 p-3 border-gray-300 rounded-md focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50">
                    <input type="number" v-model.number="deduccion.tasa" placeholder="Tasa de Interés" step="0.01"
                        min="0"
                        class="block w-full mb-4 p-3 border-gray-300 rounded-md focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50">
                    <div class="flex justify-between">
                        <button v-if="!removeSimulationButton" type="button" @click="simularDeduccion"
                            class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded">Simular</button>
                        <button v-if="removeSimulationButton" type="submit"
                            class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-6 rounded-lg">Crear</button>
                        <button @click="openModal = false, removeSimulationButton = false"
                            class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg">Cancelar</button>
                    </div>
                </form>
            </div>
        </div>



        <!-- Modal para ver deducibles activos. -->
        <div v-if="openActiveDebtModal && modeloSeleccionado"
            class="fixed inset-0 bg-gray-900 bg-opacity-75 z-50 flex justify-center items-center transition-opacity duration-300">
            <div class="bg-white p-8 rounded-xl shadow-2xl max-w-lg w-full m-4">
                <h3 class="text-base font-bold text-center text-gray-800 font-bold py-2 px-4 rounded">
                    Deducciones activas para {{ modeloSeleccionado.nombres }} {{
                        modeloSeleccionado.apellidos }}</h3>
                <table class="table-auto">
                    <thead>
                        <tr>
                            <th>Concepto</th>
                            <th>Valor Total</th>
                            <th>Plazo</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for=" deduccion in
                            modeloSeleccionado.deducibles " :key="deduccion.id">
                            <td v-if="deduccion.estado === 'Activo'">{{ deduccion.concepto }}</td>
                            <td v-if="deduccion.estado === 'Activo'">{{ deduccion.valor_total }}
                            </td>
                            <td v-if="deduccion.estado === 'Activo'">{{ deduccion.plazo }}</td>
                            <td v-if="deduccion.estado === 'Activo'">{{ deduccion.estado }}</td>
                        </tr>
                        <!-- Si ninguno de los deducibles activo mostrar -->
                        <tr v-if="modeloSeleccionado.deducibles.length === 0">
                            <td colspan="4" class="text-center">No cuenta con deducciones activas.
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div class="flex justify-end mt-4">
                    <button @click="openActiveDebtModal = false"
                        class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded">Cerrar</button>
                </div>
            </div>
        </div>

        <!-- Modal para ver el historial de deducibles. -->
        <div v-if="openRecordModal && modeloSeleccionado"
            class="fixed inset-0 bg-gray-900 bg-opacity-75 z-50 flex justify-center items-center transition-opacity duration-300">
            <div class="bg-white p-8 rounded-xl shadow-2xl max-w-lg w-full m-4">
                <h3 class="text-base font-bold text-center text-gray-800 font-bold py-2 px-4 rounded">
                    Historial de deducciones para {{ modeloSeleccionado.nombres }} {{
                        modeloSeleccionado.apellidos }}
                </h3>
                <table class="table-auto">
                    <thead>
                        <tr>
                            <th>Concepto</th>
                            <th>Valor Total</th>
                            <th>Plazo</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="deduccion in modeloSeleccionado.deducibles" :key="deduccion.id">
                            <td>{{ deduccion.concepto }}</td>
                            <td>{{ deduccion.valor_total }}</td>
                            <td>{{ deduccion.plazo }}</td>
                            <td>{{ deduccion.estado }}</td>
                        </tr>
                        <tr v-if="modeloSeleccionado.deducibles.length === 0">
                            <td colspan="4" class="text-center">No tienes un historico de
                                deducciones.</td>
                        </tr>

                    </tbody>
                </table>
                <div class="flex justify-end mt-4">
                    <button @click="openRecordModal = false"
                        class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded">Cerrar</button>
                </div>
            </div>
        </div>
        <!-- Modal de Simulación -->


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
    return modelos.value.filter(modelo => {
        const filtroEnMinusculas = filtro.value.toLowerCase();
        return modelo.nombre_usuario.toLowerCase().includes(filtroEnMinusculas) ||
            modelo.nombres.toLowerCase().includes(filtroEnMinusculas) ||
            modelo.apellidos.toLowerCase().includes(filtroEnMinusculas);
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