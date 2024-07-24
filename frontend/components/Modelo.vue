<template>
    <div class="container mx-auto p-4">
        <loading :is-loading="isLoading"></loading>

        <div class="mb-4 flex flex-col sm:flex-row justify-between items-center">
            <button @click="nuevoModelo"
                class="w-full sm:w-auto bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-105 mb-4 sm:mb-0">
                <i class="fas fa-user-plus mr-2"></i>
                <span class="hidden sm:inline">Crear usuario</span>
                <span class="sm:hidden">Crear usuario</span>
            </button>
            <div class="relative w-full sm:w-auto">
                <input type="text" v-model="searchQuery" placeholder="Buscar usuarios..."
                    class="w-full sm:w-64 pl-10 pr-4 py-2 border rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-300 focus:border-blue-300 transition duration-150 ease-in-out"
                    aria-label="Buscar usuarios">
                <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
            </div>
        </div>

        <transition name="fade">
            <div v-if="mostrarFormulario" class="mb-4">
                <form @submit.prevent="guardarModelo" class="bg-white shadow-md rounded px-4 md:px-8 pt-6 pb-8 mb-4">
                    <h2 class="text-2xl font-bold mb-6 text-center">{{ modeloForm.id ? 'Editar' : 'Crear' }} Usuario
                    </h2>

                    <div class="grid gap-4 mb-6 grid-cols-1 md:grid-cols-2">
                        <div class="form-group">
                            <label for="tipo_documento" class="block text-gray-700 text-sm font-bold mb-2">Tipo de
                                documento</label>
                            <select id="tipo_documento" v-model="modeloForm.tipo_documento" required
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring focus:border-blue-300">
                                <option value="CC">Cédula de ciudadanía</option>
                                <option value="CE">Cédula de extranjería</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="numero_documento" class="block text-gray-700 text-sm font-bold mb-2">Número de
                                documento</label>
                            <input id="numero_documento" type="text" v-model="modeloForm.numero_documento" required
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring focus:border-blue-300">
                        </div>
                        <div class="form-group">
                            <label for="nombres" class="block text-gray-700 text-sm font-bold mb-2">Nombres</label>
                            <input id="nombres" type="text" v-model="modeloForm.nombres" required
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring focus:border-blue-300">
                        </div>
                        <div class="form-group">
                            <label for="apellidos" class="block text-gray-700 text-sm font-bold mb-2">Apellidos</label>
                            <input id="apellidos" type="text" v-model="modeloForm.apellidos" required
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring focus:border-blue-300">
                        </div>
                        <div class="form-group">
                            <label for="fecha_nacimiento" class="block text-gray-700 text-sm font-bold mb-2">Fecha de
                                nacimiento</label>
                            <input id="fecha_nacimiento" type="date" v-model="modeloForm.fecha_nacimiento"
                                :max="fechaMaxima" required
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring focus:border-blue-300">
                        </div>
                        <div class="form-group">
                            <label for="correo_electronico" class="block text-gray-700 text-sm font-bold mb-2">Correo
                                electrónico</label>
                            <input id="correo_electronico" type="email" v-model="modeloForm.correo_electronico" required
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring focus:border-blue-300">
                        </div>
                        <div class="form-group">
                            <label for="nombre_usuario" class="block text-gray-700 text-sm font-bold mb-2">Nombre de
                                usuario</label>
                            <input id="nombre_usuario" type="text" v-model="modeloForm.nombre_usuario" required
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring focus:border-blue-300">
                        </div>
                        <div class="form-group">
                            <label for="rol_id" class="block text-gray-700 text-sm font-bold mb-2">Tipo de
                                usuario</label>
                            <select id="rol_id" v-model="modeloForm.rol_id" required
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring focus:border-blue-300">
                                <option v-for="rol in rolesDisponibles" :key="rol.id" :value="rol.id">
                                    {{ rol.nombre }}
                                </option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="banco" class="block text-gray-700 text-sm font-bold mb-2">Banco</label>
                            <select id="banco" v-model="modeloForm.banco" required
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring focus:border-blue-300">
                                <option v-for="banco in bancosDisponibles" :key="banco" :value="banco">
                                    {{ banco }}
                                </option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="numero_cuenta" class="block text-gray-700 text-sm font-bold mb-2">Número de
                                cuenta</label>
                            <input id="numero_cuenta" type="text" v-model="modeloForm.numero_cuenta" required
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring focus:border-blue-300">
                        </div>
                    </div>

                    <div class="mb-6">
                        <label class="block mb-2 text-sm font-medium text-gray-700">Páginas habilitadas</label>
                        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                            <div v-for="pagina in paginasDisponibles" :key="pagina.id"
                                class="flex items-center p-2 rounded hover:bg-gray-100">
                                <input :id="'checkbox-item-' + pagina.id" type="checkbox" v-model="pagina.habilitada"
                                    class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2">
                                <label :for="'checkbox-item-' + pagina.id"
                                    class="ml-2 text-sm font-medium text-gray-900">
                                    {{ pagina.nombre }}
                                </label>
                            </div>
                        </div>
                    </div>

                    <div class="flex flex-col md:flex-row items-center justify-between">
                        <button type="submit"
                            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring focus:border-blue-300 mb-2 md:mb-0">
                            <i class="fas fa-save mr-2"></i> Guardar
                        </button>
                        <button type="button" @click="confirmarCancelar"
                            class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring focus:border-gray-300">
                            <i class="fas fa-times mr-2"></i> Cancelar
                        </button>
                    </div>
                </form>
            </div>
        </transition>

        <div class="bg-white shadow-md rounded-lg overflow-hidden">
            <!-- Vista de tabla para pantallas medianas y grandes -->
            <div class="hidden md:block overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Usuario
                            </th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Correo
                            </th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Tipo
                            </th>
                            <th scope="col"
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Estado
                            </th>
                            <th scope="col"
                                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Acciones
                            </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="modelo in filteredModelos" :key="modelo.id">
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
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-gray-900">{{ modelo.correo_electronico }}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-gray-900">{{ modelo.rol }}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span
                                    :class="modelo.habilitado ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                                    class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full">
                                    {{ modelo.habilitado ? 'Activo' : 'Inactivo' }}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                <button @click="editarModelo(modelo)"
                                    class="text-indigo-600 hover:text-indigo-900 mr-3">
                                    Editar
                                </button>
                                <button @click="toggleEstado(modelo)"
                                    :class="modelo.habilitado ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'">
                                    {{ modelo.habilitado ? 'Desactivar' : 'Activar' }}
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Vista de tarjetas para móviles -->
            <div class="md:hidden">
                <div v-for="modelo in filteredModelos" :key="modelo.id"
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
                                    {{ modelo.correo_electronico }}
                                </p>
                            </div>
                        </div>
                        <span :class="modelo.habilitado ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                            class="px-2 py-1 text-xs leading-5 font-semibold rounded-full">
                            {{ modelo.habilitado ? 'Activo' : 'Inactivo' }}
                        </span>
                    </div>
                    <div class="border-t border-gray-200">
                        <dl>
                            <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    Tipo de usuario
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                    {{ modelo.rol }}
                                </dd>
                            </div>
                        </dl>
                    </div>
                    <div class="px-4 py-3 bg-gray-50 text-right sm:px-6">
                        <button @click="editarModelo(modelo)"
                            class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 mr-2">
                            Editar
                        </button>
                        <button @click="toggleEstado(modelo)"
                            :class="modelo.habilitado ? 'bg-red-600 hover:bg-red-700 focus:ring-red-500' : 'bg-green-600 hover:bg-green-700 focus:ring-green-500'"
                            class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2">
                            {{ modelo.habilitado ? 'Desactivar' : 'Activar' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>




        <div class="mt-4 flex flex-col sm:flex-row justify-between items-center">
            <div class="mb-4 sm:mb-0">
                <span class="mr-2">Filas por página:</span>
                <select v-model="perPage" @change="changePage(1)" class="border rounded p-1">
                    <option :value="10">10</option>
                    <option :value="20">20</option>
                    <option :value="50">50</option>
                </select>
            </div>
            <div class="flex items-center">
                <button @click="prevPage" :disabled="currentPage === 1"
                    class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-l focus:outline-none focus:ring focus:border-gray-300">
                    <i class="fas fa-chevron-left"></i>
                </button>
                <span class="px-4">Página {{ currentPage }} de {{ totalPages }}</span>
                <button @click="nextPage" :disabled="currentPage === totalPages"
                    class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-r focus:outline-none focus:ring focus:border-gray-300">
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useModelosStore } from '~/stores/modelo'
import Swal from 'sweetalert2'

const modelosStore = useModelosStore()
const modelos = ref([])
const rolesDisponibles = ref([])
const paginasDisponibles = ref([])
const isLoading = ref(false)
const bancosDisponibles = ref([
    'Banco de Bogotá', 'Banco Popular', 'Banco Itaú', 'Bancolombia', 'Citibank',
    'BBVA Colombia', 'Banco GNB Sudameris', 'Banco GNB Colombia', 'Banco de Occidente',
    'Banco Caja Social', 'Banco Pichincha', 'Bancoomeva', 'Banco Falabella',
    'Banco Davivienda', 'Banco AV Villas', 'Nequi', 'DaviPlata'
])

const fechaMaxima = computed(() => {
    const hoy = new Date()
    const maximo = new Date(hoy.getFullYear() - 18, hoy.getMonth(), hoy.getDate())
    return maximo.toISOString().split('T')[0]
})

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

const searchQuery = ref('')
const currentPage = ref(1)
const perPage = ref(10)

const filteredModelos = computed(() => {
    let filtered = modelos.value
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(modelo =>
            modelo.nombres.toLowerCase().includes(query) ||
            modelo.apellidos.toLowerCase().includes(query) ||
            modelo.correo_electronico.toLowerCase().includes(query)
        )
    }
    // Ordenar usuarios: activos primero, luego por orden alfabético
    return filtered.sort((a, b) => {
        if (a.habilitado !== b.habilitado) {
            return a.habilitado ? -1 : 1; // activos primero
        }
        // Si tienen el mismo estado, ordenar alfabéticamente por nombre completo
        const nombreCompletoA = `${a.nombres} ${a.apellidos}`.toLowerCase();
        const nombreCompletoB = `${b.nombres} ${b.apellidos}`.toLowerCase();
        return nombreCompletoA.localeCompare(nombreCompletoB);
    });
})

const paginatedModelos = computed(() => {
    const start = (currentPage.value - 1) * perPage.value
    const end = start + perPage.value
    return filteredModelos.value.slice(start, end)
})

const totalPages = computed(() =>
    Math.ceil(filteredModelos.value.length / perPage.value)
)

watch(searchQuery, () => {
    currentPage.value = 1
})

onMounted(async () => {
    isLoading.value = true
    try {
        const paginas = await modelosStore.fetchPaginasDisponibles()
        paginasDisponibles.value = paginas.map(pagina => ({ ...pagina, habilitada: false }))
        modelos.value = await modelosStore.fetchModelos()
        rolesDisponibles.value = await modelosStore.fetchRolesDisponibles()
    } catch (error) {
        console.error('Error al cargar datos:', error)
        Swal.fire('Error', 'No se pudieron cargar los datos. Por favor, intente de nuevo.', 'error')
    } finally {
        isLoading.value = false
    }
})

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
    paginasDisponibles.value.forEach(pagina => {
        pagina.habilitada = false
    })
}

async function guardarModelo() {
    if (!validarFormulario()) return

    isLoading.value = true
    modeloForm.value.paginas_habilitadas = paginasDisponibles.value
        .filter(pagina => pagina.habilitada)
        .map(pagina => pagina.nombre)

    try {
        let response
        if (modeloForm.value.id) {
            response = await modelosStore.editModelo(modeloForm.value)
        } else {
            response = await modelosStore.addModelo(modeloForm.value)
        }
        modelos.value = await modelosStore.fetchModelos()
        mostrarFormulario.value = false
        Swal.fire('Éxito', response.mensaje, 'success')
    } catch (error) {
        const mensaje = error.response?.data?.mensaje || 'Error desconocido'
        Swal.fire('Error', mensaje, 'error')
    } finally {
        isLoading.value = false
    }
}

function validarFormulario() {
    // Implementar validaciones aquí
    return true
}

function editarModelo(modelo) {
    mostrarFormulario.value = true
    modeloForm.value = { ...modelo }
    const rolEncontrado = rolesDisponibles.value.find(rol => rol.nombre === modelo.rol)
    modeloForm.value.rol_id = rolEncontrado ? rolEncontrado.id : null
    paginasDisponibles.value.forEach(pagina => {
        pagina.habilitada = modelo.paginas_habilitadas.includes(pagina.nombre)
    })
}

function confirmarCancelar() {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Los cambios no guardados se perderán.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cancelar',
        cancelButtonText: 'No, continuar editando'
    }).then((result) => {
        if (result.isConfirmed) {
            cancelar()
        }
    })
}

function cancelar() {
    mostrarFormulario.value = false
}

function toggleEstado(modelo) {
    Swal.fire({
        title: `¿${modelo.habilitado ? 'Desactivar' : 'Activar'} usuario?`,
        text: `¿Estás seguro de que quieres ${modelo.habilitado ? 'desactivar' : 'activar'} a
                    ${modelo.nombres} ${modelo.apellidos}?`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, continuar',
        cancelButtonText: 'Cancelar'
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                isLoading.value = true
                await modelosStore.toggleEstadoModelo(modelo.id)
                modelos.value = await modelosStore.fetchModelos()
                Swal.fire('Éxito', `Usuario ${modelo.habilitado ? 'desactivado' : 'activado'} correctamente`,
                    'success')
            } catch (error) {
                Swal.fire('Error', 'No se pudo cambiar el estado del usuario', 'error')
            } finally {
                isLoading.value = false
            }
        }
    })
}

function prevPage() {
    if (currentPage.value > 1) {
        currentPage.value--
    }
}

function nextPage() {
    if (currentPage.value < totalPages.value) { currentPage.value++ }
} function changePage(page) {
    currentPage.value = page
} </script>

<style scoped>
.form-group {
    margin-bottom: 1rem;
}

.btn-page:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
