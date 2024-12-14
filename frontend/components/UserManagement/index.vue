<template>
    <loading :is-loading="isLoading" />
    <SkeletonLoader v-if="initialSkeleton" />
    <div v-else class="p-4">

        <user-actions @nuevo-modelo="nuevoModelo" v-model:search-query="searchQuery" />

        <Transition name="fade" mode="out-in">
            <user-form v-if="mostrarFormulario" :key="formKey" :modelo-form="modeloForm"
                :roles-disponibles="rolesDisponibles" :paginas-disponibles="paginasDisponibles"
                :bancos-disponibles="bancosDisponibles" :fecha-maxima="fechaMaxima" @guardar="guardarModelo"
                @cancelar="confirmarCancelar" />
        </Transition>

        <user-list v-if="!mostrarFormulario" :modelos="paginatedModelos" @editar="editarModelo"
            @toggle-estado="toggleEstado" />

        <pagination-controls v-if="!mostrarFormulario" v-model:current-page="currentPage" v-model:per-page="perPage"
            :total-pages="totalPages" />
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue'
import { useModelosStore } from '~/stores/modelo'
import Swal from 'sweetalert2'

// Importaciones de componentes
import UserActions from './UserActions.vue'
import UserForm from './UserForm.vue'
import UserList from './UserList.vue'
import PaginationControls from './PaginationControls.vue'

const modelosStore = useModelosStore()

const modelos = ref([])
const rolesDisponibles = ref([])
const paginasDisponibles = ref([])
const isLoading = ref(false)
const initialSkeleton = ref(false)
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
const formKey = ref(0)
const modeloForm = ref({
    id: null,
    nombres: '',
    apellidos: '',
    tipo_documento: '',
    numero_documento: '',
    nombre_usuario: '',
    correo_electronico: '',
    fecha_nacimiento: '',
    rol_id: null,
    banco: '',
    numero_cuenta: '',
    paginas_habilitadas: []
})

const searchQuery = ref('')
const currentPage = ref(1)
const perPage = ref(8)

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
    return filtered.sort((a, b) => {
        if (a.habilitado !== b.habilitado) {
            return a.habilitado ? -1 : 1
        }
        const nombreCompletoA = `${a.nombres} ${a.apellidos}`.toLowerCase()
        const nombreCompletoB = `${b.nombres} ${b.apellidos}`.toLowerCase()
        return nombreCompletoA.localeCompare(nombreCompletoB)
    })
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
    initialSkeleton.value = true
    await fetchInitialData()
    initialSkeleton.value = false
})

const fetchInitialData = async () => {
    try {
        const [paginas, modelosData, roles] = await Promise.all([
            modelosStore.fetchPaginasDisponibles(),
            modelosStore.fetchModelos(),
            modelosStore.fetchRolesDisponibles()
        ])
        paginasDisponibles.value = paginas.map(pagina => ({ ...pagina, habilitada: false }))
        modelos.value = modelosData
        rolesDisponibles.value = roles
    } catch (error) {
        console.error('Error al cargar datos:', error)
        Swal.fire('Error', 'No se pudieron cargar los datos. Por favor, intente de nuevo.', 'error')
    }
}

const nuevoModelo = () => {
    modeloForm.value = {
        id: null,
        nombres: '',
        apellidos: '',
        tipo_documento: '',
        numero_documento: '',
        nombre_usuario: '',
        correo_electronico: '',
        numero_celular: '',
        fecha_nacimiento: '',
        rol_id: null,
        banco: '',
        numero_cuenta: '',
        paginas_habilitadas: []
    }
    paginasDisponibles.value.forEach(pagina => {
        pagina.habilitada = false
    })
    formKey.value++
    mostrarFormulario.value = true
}

const editarModelo = async (modelo) => {
    isLoading.value = true
    try {
        // Ocultar la lista y la paginación
        mostrarFormulario.value = false
        await nextTick()

        // Copia profunda del modelo
        const modeloCopy = JSON.parse(JSON.stringify(modelo))
        console.log('Modelo a editar (copia):', modeloCopy) // Para depuración

        // Actualiza modeloForm
        modeloForm.value = {
            id: modeloCopy.id,
            nombres: modeloCopy.nombres || '',
            apellidos: modeloCopy.apellidos || '',
            tipo_documento: modeloCopy.tipo_documento || '',
            numero_documento: modeloCopy.numero_documento || '',
            nombre_usuario: modeloCopy.nombre_usuario || '',
            correo_electronico: modeloCopy.correo_electronico || '',
            numero_celular: modeloCopy.numero_celular || '',
            fecha_nacimiento: modeloCopy.fecha_nacimiento || '',
            banco: modeloCopy.banco || '',
            numero_cuenta: modeloCopy.numero_cuenta || '',
            rol_id: modeloCopy.rol_id || null,
            password: 'PasswordpORDefecto123', // Contraseña temporal
            paginas_habilitadas: modeloCopy.paginas_habilitadas || []

        }

        // Encontrar y asignar el rol_id correcto
        const rolEncontrado = rolesDisponibles.value.find(rol => rol.id === modeloCopy.rol_id || rol.nombre === modeloCopy.rol)
        modeloForm.value.rol_id = rolEncontrado ? rolEncontrado.id : null

        // Actualizar las páginas habilitadas
        paginasDisponibles.value.forEach(pagina => {
            pagina.habilitada = modeloForm.value.paginas_habilitadas.includes(pagina.nombre)
        })

        // Incrementa la key para forzar la re-renderización
        formKey.value++

        // Muestra el formulario
        await nextTick()
        mostrarFormulario.value = true

    } catch (error) {
        console.error('Error al editar modelo:', error)
        Swal.fire('Error', 'No se pudo cargar el usuario para editar', 'error')
    } finally {
        isLoading.value = false
    }
}

const guardarModelo = async (formData) => {
    if (!validarFormulario(formData)) return

    isLoading.value = true
    try {
        let response
        if (formData.id) {
            response = await modelosStore.editModelo(formData)
        } else {
            response = await modelosStore.addModelo(formData)
        }
        await fetchInitialData() // Recargar datos después de guardar
        mostrarFormulario.value = false
        Swal.fire('Éxito', response.mensaje, 'success')
    } catch (error) {
        const mensaje = error.response?.data?.mensaje || 'Error desconocido'
        Swal.fire('Error', mensaje, 'error')
    } finally {
        isLoading.value = false
    }
}

const validarFormulario = (formData) => {
    const camposRequeridos = ['nombres', 'apellidos', 'tipo_documento', 'numero_documento', 'nombre_usuario', 'correo_electronico', 'numero_celular', 'fecha_nacimiento', 'rol_id', 'banco', 'numero_cuenta']

    for (const campo of camposRequeridos) {
        if (!formData[campo]) {
            Swal.fire('Error', `El campo ${campo.replace('_', ' ')} es requerido`, 'error')
            return false
        }
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.correo_electronico)) {
        Swal.fire('Error', 'El correo electrónico no es válido', 'error')
        return false
    }

    return true
}

const confirmarCancelar = () => {
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
            mostrarFormulario.value = false
        }
    })
}

const toggleEstado = async (modelo) => {
    const result = await Swal.fire({
        title: `¿${modelo.habilitado ? 'Desactivar' : 'Activar'} usuario?`,
        text: `¿Estás seguro de que quieres ${modelo.habilitado ? 'desactivar' : 'activar'} a ${modelo.nombres} ${modelo.apellidos}?`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, continuar',
        cancelButtonText: 'Cancelar'
    })

    if (result.isConfirmed) {
        try {
            isLoading.value = true
            await modelosStore.toggleEstadoModelo(modelo.id)
            await fetchInitialData() // Recargar datos después de cambiar el estado
            Swal.fire('Éxito', `Usuario ${modelo.habilitado ? 'desactivado' : 'activado'} correctamente`, 'success')
        } catch (error) {
            Swal.fire('Error', 'No se pudo cambiar el estado del usuario', 'error')
        } finally {
            isLoading.value = false
        }
    }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>