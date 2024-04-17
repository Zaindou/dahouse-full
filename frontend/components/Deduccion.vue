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
                            <button @click="openModal = true"
                                class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded ml-1">Deducibles
                                activos</button>
                            <button @click="openModal = true"
                                class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded ml-1">Historico</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <!-- Modal para Crear Deducción -->
        <div v-if="openModal && modeloSeleccionado"
            class="fixed inset-0 bg-gray-900 bg-opacity-75 z-50 flex justify-center items-center transition-opacity duration-300">
            <div class="bg-white p-8 rounded-xl shadow-2xl max-w-lg w-full m-4">
                <h3 class="text-lg font-bold text-center text-gray-800 font-bold py-2 px-4 rounded">
                    Crear Deducción para {{
            modeloSeleccionado.nombres }} {{ modeloSeleccionado.apellidos }}</h3>
                <form @submit.prevent="guardarDeduccion">
                    <input v-model="deduccion.concepto" placeholder="Concepto"
                        class="block w-full mb-4 p-2 border rounded" required>
                    <input type="number" v-model="deduccion.valor_total" placeholder="Valor Total"
                        class="[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none block w-full mb-4 p-2 border rounded"
                        required>
                    <input type="number" v-model="deduccion.plazo" placeholder="Plazo"
                        class="[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none block w-full mb-4 p-2 border rounded"
                        required>
                    <input type="number" v-model="deduccion.tasa" placeholder="Tasa de Interés"
                        class="[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none block w-full mb-4 p-2 border rounded"
                        required>
                    <div class="flex justify-between">
                        <button type="submit"
                            class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-6 rounded">Guardar</button>
                        <button @click="openModal = false"
                            class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded">Cancelar</button>
                    </div>
                </form>
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
const modelos = ref([]);
const filtro = ref('');
const modeloSeleccionado = ref(null);

const deduccion = ref({
    concepto: '',
    valor_total: 0,
    plazo: 0,
    tasa: 0
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

const abrirFormularioDeduccion = (modelo) => {
    modeloSeleccionado.value = modelo;
    openModal.value = true;
    // Restablecer la deduccion
    deduccion.value = { concepto: '', valor_total: '', plazo: '', tasa: '' };
};

const guardarDeduccion = async () => {
    try {
        isLoading.value = true;
        const response = await modelosStore.crearDeduccion(modeloSeleccionado.value.nombre_usuario, deduccion.value);
        modelos.value = await modelosStore.fetchModelos(); // Recargar lista de modelos
        openModal.value = false;
        isLoading.value = false;
        Swal.fire('Éxito', response.mensaje, 'success');
    } catch (error) {
        Swal.fire('Error', error.response?.data?.error || 'Ha ocurrido un error', 'error');
    }
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