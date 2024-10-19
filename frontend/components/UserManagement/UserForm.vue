<template>
    <div class="p-4 bg-white shadow-md rounded">
        <form @submit.prevent="handleSubmit">
            <h2 class="text-2xl font-bold mb-6 text-center">{{ isEditing ? 'Editar' : 'Crear' }} Usuario</h2>

            <!-- Campos del formulario -->
            <div class="grid gap-4 mb-6 grid-cols-1 md:grid-cols-2">
                <div v-for="field in formFields" :key="field.id" class="form-group">
                    <label :for="field.id" class="block text-gray-700 text-sm font-bold mb-2">{{ field.label }}</label>
                    <component :is="field.component" :id="field.id" v-model="localModeloForm[field.id]"
                        :required="field.required"
                        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring focus:border-blue-300"
                        v-bind="field.props || {}">
                        <template v-if="field.options">
                            <option v-for="option in field.options" :key="option.value" :value="option.value">
                                {{ option.label }}
                            </option>
                        </template>
                    </component>
                </div>
            </div>

            <!-- Páginas habilitadas -->
            <div class="mb-6">
                <label class="block mb-2 text-sm font-medium text-gray-700">Páginas habilitadas</label>
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                    <div v-for="pagina in localPaginasDisponibles" :key="pagina.id"
                        class="flex items-center p-2 rounded hover:bg-gray-100">
                        <input :id="'checkbox-item-' + pagina.id" type="checkbox" v-model="pagina.habilitada"
                            class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2">
                        <label :for="'checkbox-item-' + pagina.id" class="ml-2 text-sm font-medium text-gray-900">{{
                            pagina.nombre
                            }}</label>
                    </div>
                </div>
            </div>

            <!-- Botones de acción -->
            <div class="flex justify-end space-x-4 mt-4">
                <button type="button" @click="emit('cancelar')"
                    class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">Cancelar</button>
                <button type="submit"
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Guardar</button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, nextTick, watchEffect } from 'vue'

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

const emit = defineEmits(['guardar', 'cancelar'])

// Inicializamos los refs locales
const localModeloForm = ref({})
const localPaginasDisponibles = ref([])

// Usamos watchEffect para sincronizar los valores de forma inmediata
watchEffect(async () => {
    await nextTick() // Espera a que Vue termine de renderizar
    console.log('Actualizando localModeloForm con modeloForm:', props.modeloForm)
    localModeloForm.value = { ...props.modeloForm }

    // Sincronizar las páginas disponibles
    localPaginasDisponibles.value = props.paginasDisponibles.map(pagina => ({
        ...pagina,
        habilitada: localModeloForm.value.paginas_habilitadas?.includes(pagina.nombre) || false
    }))
    console.log('localPaginasDisponibles actualizado:', localPaginasDisponibles.value)
})

// Manejo del envío del formulario
const handleSubmit = () => {
    const formData = {
        ...localModeloForm.value,
        paginas_habilitadas: localPaginasDisponibles.value
            .filter(pagina => pagina.habilitada)
            .map(pagina => pagina.nombre)
    }
    console.log('Datos del formulario enviados:', formData)
    emit('guardar', formData)
}

// Definir los campos del formulario
const formFields = [
    {
        id: 'tipo_documento', label: 'Tipo de documento', component: 'select', required: true, options: [
            { value: 'CC', label: 'Cédula de ciudadanía' },
            { value: 'CE', label: 'Cédula de extranjería' }
        ]
    },
    { id: 'numero_documento', label: 'Número de documento', component: 'input', required: true, props: { type: 'text' } },
    { id: 'nombres', label: 'Nombres', component: 'input', required: true, props: { type: 'text' } },
    { id: 'apellidos', label: 'Apellidos', component: 'input', required: true, props: { type: 'text' } },
    { id: 'fecha_nacimiento', label: 'Fecha de nacimiento', component: 'input', required: true, props: { type: 'date', max: props.fechaMaxima } },
    { id: 'correo_electronico', label: 'Correo electrónico', component: 'input', required: true, props: { type: 'email' } },
    { id: 'nombre_usuario', label: 'Nombre de usuario', component: 'input', required: true, props: { type: 'text' } },
    { id: 'rol_id', label: 'Tipo de usuario', component: 'select', required: true, options: props.rolesDisponibles.map(rol => ({ value: rol.id, label: rol.nombre })) },
    { id: 'banco', label: 'Banco', component: 'select', required: true, options: props.bancosDisponibles.map(banco => ({ value: banco, label: banco })) },
    { id: 'numero_cuenta', label: 'Número de cuenta', component: 'input', required: true, props: { type: 'text' } },
    { id: 'password', label: 'Contraseña', component: 'input', required: false, props: { type: 'password' } }
]
</script>
