<template>
    <div class="container mx-auto p-4">
        <loading :is-loading="isLoading"></loading>
        <button @click="nuevoModelo" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-2">
            Crear usuario
        </button>
        <div v-if="mostrarFormulario" class="mb-2">
            <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-2">
                <div class="grid gap-6 mb-6 md:grid-cols-2">
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="tipo_documento">
                            Tipo de documento
                        </label>
                        <select class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="tipo_documento" v-model="modeloForm.tipo_documento" v-bind:disabled="modeloForm.id">
                            <option value="CC">Cédula de ciudadanía</option>
                            <option value="CE">Cédula de extranjería</option>
                        </select>
                    </div>
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2 " for="numero_documento">
                            Número de documento
                        </label>
                        <input
                            class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker disabled-input"
                            id="numero_documento" type="text" v-model="modeloForm.numero_documento"
                            v-bind:disabled="modeloForm.id">
                    </div>
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="nombres">
                            Nombres
                        </label>
                        <input class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="nombres" type="text" v-model="modeloForm.nombres">
                    </div>
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="apellidos">
                            Apellidos
                        </label>
                        <input class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="apellidos" type="text" v-model="modeloForm.apellidos">
                    </div>
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="fecha_nacimiento">
                            Fecha de nacimiento
                        </label>
                        <input class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="fecha_nacimiento" type="date" v-model="modeloForm.fecha_nacimiento" :max="fechaMaxima">
                    </div>
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="correo_electronico">
                            Correo electrónico
                        </label>
                        <input class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="correo_electronico" type="email" v-model="modeloForm.correo_electronico">
                    </div>
                    <!-- NOMBRE DE USUARIO -->
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="nombre_usuario">
                            Nombre de usuario
                        </label>
                        <input
                            class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker disabled-input"
                            id="nombre_usuario" type="text" v-model="modeloForm.nombre_usuario"
                            v-bind:disabled="modeloForm.id">
                    </div>
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="rol_id">
                            Tipo de usuario
                        </label>
                        <select class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="rol_id" v-model="modeloForm.rol_id" v-bind:disabled="modeloForm.id">
                            <option v-for="rol in rolesDisponibles" :key="rol.id" :value="rol.id">
                                {{ rol.nombre }}
                            </option>
                        </select>
                    </div>
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="banco">
                            Banco
                        </label>
                        <select class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="banco" v-model="modeloForm.banco">
                            <option v-for="banco in bancosDisponibles" :key="banco" :value="banco">
                                {{ banco }}
                            </option>
                        </select>
                    </div>
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="numero_cuenta">
                            Número de cuenta
                        </label>
                        <input class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="numero_cuenta" type="text" v-model="modeloForm.numero_cuenta">
                    </div>
                    <div class="mb-1">
                        <label for="paginas_habilitadas" class="block mb-2 text-sm font-medium text-gray-900">Páginas
                            habilitadas</label>
                        <div class="grid grid-cols-2">
                            <div v-for="pagina in paginasDisponibles" :key="pagina.id"
                                class="flex items-center p-1 rounded hover:bg-gray-100">
                                <input :id="'checkbox-item-' + pagina.id" type="checkbox" v-model="pagina.habilitada"
                                    class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2">
                                <label :for="'checkbox-item-' + pagina.id"
                                    class="ml-2 text-sm font-medium text-gray-900 rounded">
                                    {{ pagina.nombre }}
                                </label>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="flex items-center justify-between">
                    <button @click="guardarModelo"
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                        Guardar
                    </button>
                    <button @click="cancelar"
                        class="bg-gray-500 hover:bg-grey-700 text-white font-bold py-2 px-4 rounded">
                        Cancelar
                    </button>
                </div>
            </div>
        </div>
        <div class="bg-white shadow-md rounded my-6">
            <table class="text-left w-full border-collapse">
                <thead>
                    <tr>
                        <th
                            class="py-4 px-6 bg-grey-lightest font-bold uppercase text-sm text-grey-dark border-b border-grey-light">
                            Nombre
                        </th>
                        <th
                            class="py-4 px-6 bg-grey-lightest font-bold uppercase text-sm text-grey-dark border-b border-grey-light">
                            Correo electrónico
                        </th>
                        <th
                            class="py-4 px-6 bg-grey-lightest font-bold uppercase text-sm text-grey-dark border-b border-grey-light">
                            Tipo de usuario
                        </th>
                        <th
                            class="py-4 px-6 bg-grey-lightest font-bold uppercase text-sm text-grey-dark border-b border-grey-light">
                            Acciones
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="hover:bg-grey-lighter" v-for="modelo in modelos" :key="modelo.id">
                        <td class="py-4 px-6 border-b border-grey-light">{{ modelo.nombres }} {{ modelo.apellidos }}
                        </td>
                        <td class="py-4 px-6 border-b border-grey-light">{{ modelo.correo_electronico }}</td>
                        <td class="py-4 px-6 border-b border-grey-light">{{ modelo.rol }}</td>
                        <td class="py-4 px-6 border-b border-grey-light">
                            <button @click="editarModelo(modelo)"
                                class="text-sm bg-blue-500 hover:bg-blue-700 text-white py-1 px-2 rounded">
                                Editar
                            </button>
                            <!-- <button @click="eliminarModelo(modelo.id)"
                                class="text-sm bg-red-500 hover:bg-red-700 text-white py-1 px-2 rounded">
                                Eliminar
                            </button> -->
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useModelosStore } from '~/stores/modelo'

const modelosStore = useModelosStore()
const modelos = ref([])
const rolesDisponibles = ref([]);
const paginasDisponibles = ref([]);
const isLoading = ref(false);
const bancosDisponibles = ref([
    'Banco de Bogotá',
    'Banco Popular',
    'Banco Itaú',
    'Bancolombia',
    'Citibank',
    'BBVA Colombia',
    'Banco GNB Sudameris',
    'Banco GNB Colombia',
    'Banco de Occidente',
    'Banco Caja Social',
    'Banco Pichincha',
    'Bancoomeva',
    'Banco Falabella',
    'Banco Davivienda',
    'Banco AV Villas',
    'Nequi',
    'DaviPlata'
]);

const fechaMaxima = computed(() => {
    const hoy = new Date();
    const maximo = new Date(hoy.getFullYear() - 18, hoy.getMonth(), hoy.getDate());
    return maximo.toISOString().split('T')[0];
});

const mostrarFormulario = ref(false)
const modeloForm = ref({
    nombres: '',
    apellidos: '',
    tipo_documento: '',
    numero_documento: '',
    nombre_usuario: '',
    rol_id: null,
    paginas_habilitadas: []
})

onMounted(async () => {
    const paginas = await modelosStore.fetchPaginasDisponibles();
    paginasDisponibles.value = paginas.map(pagina => ({ ...pagina, habilitada: false }));
    modelos.value = await modelosStore.fetchModelos()
    rolesDisponibles.value = await modelosStore.fetchRolesDisponibles(); // Implementa esta función

});

function nuevoModelo() {
    mostrarFormulario.value = true
    modeloForm.value = {
        nombres: '',
        apellidos: '',
        tipo_documento: '',
        numero_documento: '',
        nombre_usuario: '',
        rol_id: null,
        paginas_habilitadas: []
    }
}

async function guardarModelo() {
    isLoading.value = true;
    modeloForm.value.paginas_habilitadas = paginasDisponibles.value
        .filter(pagina => pagina.habilitada)
        .map(pagina => pagina.nombre);

    try {
        let response;
        if (modeloForm.value.id) {
            // Actualizar modelo existente
            response = await modelosStore.editModelo(modeloForm.value);
        } else {
            // Crear nuevo modelo
            response = await modelosStore.addModelo(modeloForm.value);
        }
        modelos.value = await modelosStore.fetchModelos();
        mostrarFormulario.value = false;
        modeloForm.value = {
            nombres: '',
            apellidos: '',
            tipo_documento: '',
            numero_documento: '',
            nombre_usuario: '',
            rol_id: null,
            paginas_habilitadas: []
        };
        Swal.fire('Éxito', response.mensaje, 'success');
    } catch (error) {
        const mensaje = error.response?.data?.mensaje || 'Error desconocido';
        Swal.fire('Error', mensaje, 'error');
    } finally {
        isLoading.value = false;
    }
}


function editarModelo(modelo) {
    mostrarFormulario.value = true;
    modeloForm.value = { ...modelo }; // Rellena el formulario con datos del modelo
    const rolEncontrado = rolesDisponibles.value.find(rol => rol.nombre === modelo.rol);
    modeloForm.value.rol_id = rolEncontrado ? rolEncontrado.id : null;
    paginasDisponibles.value.forEach(pagina => {
        pagina.habilitada = modelo.paginas_habilitadas.includes(pagina.nombre);
    });
}


function cancelar() {
    mostrarFormulario.value = false
}

</script>

<style>
/* Estilos para los campos deshabilitados */
.disabled-input {
    background-color: #ffffff;
    /* Color de fondo más tenue */
    color: #999999;
    /* Color de texto más tenue */
}
</style>
