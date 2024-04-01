<template>
    <div class="container mx-auto p-4">
        <button @click="nuevoModelo" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-2">
            Añadir Modelo
        </button>
        <div v-if="mostrarFormulario" class="mb-2">
            <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-2">
                <div class="grid gap-6 mb-6 md:grid-cols-2">
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="tipo_documento">
                            Tipo de documento
                        </label>
                        <select class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="tipo_documento" v-model="modeloForm.tipo_documento">
                            <option value="CC">Cédula de ciudadanía</option>
                            <option value="CE">Cédula de extranjería</option>
                        </select>
                    </div>
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="numero_documento">
                            Número de documento
                        </label>
                        <input class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="numero_documento" type="text" v-model="modeloForm.numero_documento">
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
                    <!-- NOMBRE DE USUARIO -->
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="nombre_usuario">
                            Nombre de usuario
                        </label>
                        <input class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="nombre_usuario" type="text" v-model="modeloForm.nombre_usuario">
                    </div>
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="rol_id">
                            Rol
                        </label>
                        <select class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker"
                            id="rol_id" v-model="modeloForm.rol_id">
                            <option v-for="rol in rolesDisponibles" :key="rol.id" :value="rol.id">
                                {{ rol.nombre }}
                            </option>
                        </select>
                    </div>

                    <!-- Input para las páginas habilitadas -->
                    <div class="mb-1">
                        <label class="block text-grey-darker text-sm font-bold mb-2" for="paginas_habilitadas">
                            Páginas habilitadas
                        </label>
                        <select id="paginas_habilitadas" v-model="modeloForm.paginas_habilitadas" multiple
                            class="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker">
                            <option v-for="pagina in paginasDisponibles" :key="pagina.id" :value="pagina.id">
                                {{ pagina.nombre }}
                            </option>
                        </select>
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
                            Nombres
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
                        <td class="py-4 px-6 border-b border-grey-light">
                            <button @click="editarModelo(modelo)"
                                class="text-sm bg-blue-500 hover:bg-blue-700 text-white py-1 px-2 rounded">
                                Editar
                            </button>
                            <button @click="eliminarModelo(modelo.id)"
                                class="text-sm bg-red-500 hover:bg-red-700 text-white py-1 px-2 rounded">
                                Eliminar
                            </button>
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
    modelos.value = await modelosStore.fetchModelos()
    rolesDisponibles.value = await modelosStore.fetchRolesDisponibles(); // Implementa esta función
    paginasDisponibles.value = await modelosStore.fetchPaginasDisponibles(); // Implementa esta función

});

function nuevoModelo() {
    mostrarFormulario.value = true
    modeloForm.value = { nombres: '', apellidos: '' } // Reinicia el formulario
}

async function guardarModelo() {
    try {
        const response = await modelosStore.addModelo(modeloForm.value);
        mostrarFormulario.value = false;
        modeloForm.value = { nombres: '', apellidos: '' }; // Reinicia el formulario
        Swal.fire('Éxito', response.mensaje, 'success'); // Usa el mensaje de la API
    } catch (error) {
        const mensaje = error.response?.data?.mensaje || 'Error desconocido';
        Swal.fire('Error', mensaje, 'error'); // Usa el mensaje de error de la API
    }
}

function editarModelo(modelo) {
    mostrarFormulario.value = true
    modeloForm.value = { ...modelo } // Rellena el formulario con datos del modelo
}

async function eliminarModelo(modeloId) {
    try {
        const response = await modelosStore.deleteModelo(modeloId);
        Swal.fire('Éxito', response.mensaje, 'success');
    } catch (error) {
        const mensaje = error.response?.data?.mensaje || 'Error desconocido';
        Swal.fire('Error', mensaje, 'error');
    }
}

function cancelar() {
    mostrarFormulario.value = false
}

</script>
