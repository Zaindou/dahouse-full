<template>
    <div class="min-h-screen bg-gray-50 p-6">
        <div class="max-w-4xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="p-8">
                <form :key="formKey" @submit.prevent="handleSubmit">
                    <!-- Encabezado -->
                    <div class="mb-8 border-b pb-6">
                        <h2 class="text-3xl font-semibold text-gray-900">
                            {{ isEditing ? 'Editar' : 'Crear' }} Usuario
                        </h2>
                        <p class="mt-2 text-gray-600">Complete la información del usuario</p>
                    </div>

                    <!-- Grid de campos -->
                    <div class="grid gap-6 mb-8 grid-cols-1 md:grid-cols-2">
                        <div v-for="field in formFields" :key="field.id" class="form-group space-y-2">
                            <label :for="field.id" class="block text-sm font-medium text-gray-700">
                                {{ field.label }}
                            </label>

                            <!-- Input estilizado -->
                            <input v-if="field.component === 'input'" :id="field.id" :type="field.props?.type || 'text'"
                                v-model="localModeloForm[field.id]" :required="field.required"
                                class="block w-full px-4 py-3 rounded-lg border-gray-300 bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out" />

                            <!-- Select estilizado -->
                            <select v-else-if="field.component === 'select'" :id="field.id"
                                v-model="localModeloForm[field.id]" :required="field.required"
                                class="block w-full px-4 py-3 rounded-lg border-gray-300 bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out">
                                <option value="" disabled selected>Seleccione una opción</option>
                                <option v-for="option in field.options" :key="option.value" :value="option.value">
                                    {{ option.label }}
                                </option>
                            </select>
                        </div>
                    </div>

                    <!-- Sección de páginas habilitadas -->
                    <div class="mb-8">
                        <h3 class="text-lg font-medium text-gray-900 mb-4">Páginas habilitadas</h3>
                        <div class="bg-gray-50 rounded-lg p-4">
                            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                                <div v-for="pagina in localPaginasDisponibles" :key="pagina.id"
                                    class="relative flex items-center p-4 rounded-lg hover:bg-white transition duration-150 ease-in-out">
                                    <div class="flex items-center h-5">
                                        <input :id="'checkbox-item-' + pagina.id" type="checkbox"
                                            v-model="pagina.habilitada"
                                            class="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                                    </div>
                                    <label :for="'checkbox-item-' + pagina.id"
                                        class="ml-3 text-sm font-medium text-gray-700 cursor-pointer">
                                        {{ pagina.nombre }}
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Botones de acción -->
                    <div class="flex justify-end space-x-4 pt-6 border-t">
                        <button type="button" @click="emit('cancelar')"
                            class="px-6 py-3 rounded-lg text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition duration-150 ease-in-out">
                            Cancelar
                        </button>
                        <button type="submit"
                            class="px-6 py-3 rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150 ease-in-out">
                            {{ isEditing ? 'Guardar cambios' : 'Crear usuario' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { is } from 'date-fns/locale';

// Props y emits (mantienen la misma lógica)
const props = defineProps({
    modeloForm: {
        type: Object,
        required: true
    },
    rolesDisponibles: Array,
    paginasDisponibles: Array,
    bancosDisponibles: Array,
    fechaMaxima: String
})

const isEditing = computed(() => props.modeloForm.id !== null)

const emit = defineEmits(['guardar', 'cancelar'])

// Estado local reactivo
const localModeloForm = ref({})
const localPaginasDisponibles = ref([])
const formKey = ref(0)

// Watch y form fields (mantienen la misma lógica)
watch(
    () => props.modeloForm,
    async (newModeloForm) => {
        await nextTick()
        localModeloForm.value = { ...newModeloForm }
        localPaginasDisponibles.value = props.paginasDisponibles.map(pagina => ({
            ...pagina,
            habilitada: newModeloForm.paginas_habilitadas?.includes(pagina.nombre) || false
        }))
        formKey.value++
    },
    { immediate: true }
)

const formFields = [
    {
        id: 'nombres',
        label: 'Nombres',
        component: 'input',
        props: { type: 'text' },
        required: true
    },
    {
        id: 'apellidos',
        label: 'Apellidos',
        component: 'input',
        props: { type: 'text' },
        required: true
    },
    {
        id: 'tipo_documento',
        label: 'Tipo de documento',
        component: 'select',
        required: true,
        options: [
            { value: 'CC', label: 'Cédula de ciudadanía' },
            { value: 'CE', label: 'Cédula de extranjería' }
        ]
    },
    {
        id: 'numero_documento',
        label: 'Número de documento',
        component: 'input',
        props: { type: 'text' },
        required: true
    },
    {
        id: 'fecha_nacimiento',
        label: 'Fecha de nacimiento',
        component: 'input',
        props: { type: 'date', max: props.fechaMaxima },
        required: true
    },
    {
        id: 'correo_electronico',
        label: 'Correo electrónico',
        component: 'input',
        props: { type: 'email' },
        required: true
    },
    {
        id: 'numero_celular',
        label: 'Celular',
        component: 'input',
        props: { type: 'number' },
        required: true
    },
    {
        id: 'nombre_usuario',
        label: 'Nombre de usuario',
        component: 'input',
        props: { type: 'text' },
        required: true
    },
    {
        id: 'rol_id',
        label: 'Rol',
        component: 'select',
        required: true,
        options: props.rolesDisponibles.map(rol => ({
            value: rol.id,
            label: rol.nombre
        }))
    },
    {
        id: 'password',
        label: 'Contraseña',
        component: 'input',
        props: { type: 'password' },
        required: true
    },
    {
        id: 'banco',
        label: 'Banco',
        component: 'select',
        required: true,
        options: props.bancosDisponibles.map(banco => ({
            value: banco,
            label: banco
        }))
    },
    {
        id: 'numero_cuenta',
        label: 'Número de cuenta',
        component: 'input',
        props: { type: 'text' },
        required: true
    },
]

const handleSubmit = () => {
    const formData = {
        ...localModeloForm.value,
        paginas_habilitadas: localPaginasDisponibles.value
            .filter(pagina => pagina.habilitada)
            .map(pagina => pagina.nombre)
    }
    emit('guardar', formData)
}
</script>