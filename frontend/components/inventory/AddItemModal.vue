//components/inventory/ItemModal.vue
<template>
  <Modal @close="$emit('close')">
    <template #header>
      <h3 class="text-lg font-medium text-gray-900">
        {{ props.item ? 'Editar' : 'Nuevo' }} Ítem
      </h3>
    </template>

    <template #body>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Nombre</label>
          <input
            v-model="formData.nombre_item"
            type="text"
            required
            class="block w-full p-2 mt-1 border rounded-md shadow-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Descripción</label>
          <textarea
            v-model="formData.descripcion"
            required
            rows="3"
            class="block w-full p-2 mt-1 border rounded-md shadow-sm"
          ></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700" >Categoría</label>
          <select
            v-model="formData.categoria_id"
            required
            class="block w-full p-2 mt-1 border rounded-md shadow-sm"

          >
           <option value="" disabled selected>Seleccionar categoría</option>
            <option v-for="cat in inventory.categories" :key="cat.id" :value="cat.id">
              {{ cat.nombre }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Cantidad</label>
          <input
            v-model.number="formData.cantidad"
            type="number"
            min="0"
            required
            class="block w-full p-2 mt-1 border rounded-md shadow-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Precio</label>
          <input
            v-model.number="formData.precio"
            type="number"
            min="0"
            step="100"
            required
            class="block w-full p-2 mt-1 border rounded-md shadow-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Estado</label>
          <select
            v-model="formData.estado"
            required
            class="block w-full p-2 mt-1 border rounded-md shadow-sm"
          >
            <option value="Disponible">Disponible</option>
            <option value="Prestado">Prestado</option>
            <option value="Agotado">Agotado</option>
          </select>
        </div>

          <div>
          <label class="block text-sm font-medium text-gray-700">Estado Articulo</label>
          <select
            v-model="formData.estado_articulo"
            required
            class="block w-full p-2 mt-1 border rounded-md shadow-sm"
          >
            <option value="Excelente">Excelente</option>
            <option value="Regular">Regular</option>
            <option value="Defectuoso">Defectuoso</option>
          </select>
        </div>
        
      </form>
    </template>

    <template #footer>
      <button
        type="button"
        @click="handleSubmit"
        class="px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700"
      >
        {{ props.item ? 'Actualizar' : 'Crear' }}
      </button>
      <button
        type="button"
        @click="$emit('close')"
        class="ml-3 text-gray-600 hover:text-gray-800"
      >
        Cancelar
      </button>
    </template>
  </Modal>
</template>

<script setup>
import { useInventoryStore } from '~/stores/inventory'
import Modal from '~/components/inventory/Modal.vue'


const props = defineProps({
  item: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'save'])
const inventory = useInventoryStore()

const formData = ref({
  nombre_item: '',
  descripcion: '',
  categoria_id: '',
  cantidad: 0,
  precio: 0,
  estado: 'Disponible',
  estado_articulo: 'Excelente'
})

// Si hay un item, llenar el formulario
watchEffect(() => {
  if (props.item) {
    formData.value = { ...props.item }
  }
})

function handleSubmit() {
  emit('save', { ...formData.value })
}
</script>