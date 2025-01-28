//components/inventory/ItemModal.vue
<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
    <Modal :closeOnClickOutside="false" @close="$emit('close')" class="w-full max-w-2xl mx-auto">
      <template #header>
        <div class="flex items-center space-x-2">
          <Icon 
            :name="props.item ? 'material-symbols:edit-outline' : 'material-symbols:add-circle-outline'" 
            class="w-5 h-5 text-blue-600 sm:w-6 sm:h-6"
          />
          <h3 class="text-lg font-semibold text-gray-900 sm:text-xl">
            {{ props.item ? 'Editar' : 'Nuevo' }} Ítem
          </h3>
        </div>
      </template>

      <template #body>
        <form @submit.prevent="handleSubmit" class="space-y-4 sm:space-y-6">
          <div class="grid grid-cols-1 gap-4 sm:gap-6 md:grid-cols-2">
            <!-- Nombre -->
            <div class="col-span-2">
              <label class="block mb-1 text-sm font-medium text-gray-700">
                <div class="flex items-center space-x-1">
                  <Icon name="material-symbols:inventory-2" class="w-4 h-4 text-gray-600 sm:w-5 sm:h-5" />
                  <span>Nombre</span>
                </div>
              </label>
              <input
                v-model="formData.nombre_item"
                type="text"
                required
                class="block w-full p-2 sm:p-2.5 mt-1 text-sm sm:text-base border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              />
            </div>

            <!-- Descripción -->
            <div class="col-span-2">
              <label class="block mb-1 text-sm font-medium text-gray-700">
                <div class="flex items-center space-x-1">
                  <Icon name="material-symbols:description-outline" class="w-4 h-4 text-gray-600 sm:w-5 sm:h-5" />
                  <span>Descripción</span>
                </div>
              </label>
              <textarea
                v-model="formData.descripcion"
                required
                rows="3"
                class="block w-full p-2 sm:p-2.5 mt-1 text-sm sm:text-base border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              ></textarea>
            </div>

            <!-- Categoría -->
            <div class="col-span-2 md:col-span-1">
              <label class="block mb-1 text-sm font-medium text-gray-700">
                <div class="flex items-center space-x-1">
                  <Icon name="material-symbols:category" class="w-4 h-4 text-gray-600 sm:w-5 sm:h-5" />
                  <span>Categoría</span>
                </div>
              </label>
              <select
                v-model="formData.categoria_id"
                required
                class="block w-full p-2 sm:p-2.5 mt-1 text-sm sm:text-base border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              >
                <option value="" disabled selected>Seleccionar categoría</option>
                <option v-for="cat in inventory.categories" :key="cat.id" :value="cat.id">
                  {{ cat.nombre }}
                </option>
              </select>
            </div>

            <!-- Cantidad -->
            <div class="col-span-2 md:col-span-1">
              <label class="block mb-1 text-sm font-medium text-gray-700">
                <div class="flex items-center space-x-1">
                  <Icon name="material-symbols:inventory" class="w-4 h-4 text-gray-600 sm:w-5 sm:h-5" />
                  <span>Cantidad</span>
                </div>
              </label>
              <input
                v-model.number="formData.cantidad"
                type="number"
                min="0"
                required
                class="block w-full p-2 sm:p-2.5 mt-1 text-sm sm:text-base border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              />
            </div>

            <!-- Precio -->
            <div class="col-span-2 md:col-span-1">
              <label class="block mb-1 text-sm font-medium text-gray-700">
                <div class="flex items-center space-x-1">
                  <Icon name="material-symbols:payments-outline" class="w-4 h-4 text-gray-600 sm:w-5 sm:h-5" />
                  <span>Precio</span>
                </div>
              </label>
              <div class="relative">
                <span class="absolute text-gray-500 -translate-y-1/2 left-3 top-1/2">$</span>
                <input
                  :value="formatPrice(formData.precio)"
                  @input="handlePriceInput"
                  type="text"
                  inputmode="numeric"
                  required
                  class="block w-full pl-5 sm:pl-6 p-2 sm:p-2.5 mt-1 text-sm sm:text-base border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  placeholder="0"
                />
              </div>
            </div>

            <!-- Estado -->
            <div class="col-span-2 md:col-span-1">
              <label class="block mb-1 text-sm font-medium text-gray-700">
                <div class="flex items-center space-x-1">
                  <Icon name="material-symbols:circle-outline" class="w-4 h-4 text-gray-600 sm:w-5 sm:h-5" />
                  <span>Estado</span>
                </div>
              </label>
              <select
                v-model="formData.estado"
                required
                class="block w-full p-2 sm:p-2.5 mt-1 text-sm sm:text-base border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              >
                <option value="Disponible">Disponible</option>
                <option value="Prestado">Prestado</option>
                <option value="Agotado">Agotado</option>
              </select>
            </div>

            <!-- Estado Artículo -->
            <div class="col-span-2 md:col-span-1">
              <label class="block mb-1 text-sm font-medium text-gray-700">
                <div class="flex items-center space-x-1">
                  <Icon name="material-symbols:check-circle-outline" class="w-4 h-4 text-gray-600 sm:w-5 sm:h-5" />
                  <span>Estado Artículo</span>
                </div>
              </label>
              <select
                v-model="formData.estado_articulo"
                required
                class="block w-full p-2 sm:p-2.5 mt-1 text-sm sm:text-base border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              >
                <option value="Excelente">Excelente</option>
                <option value="Regular">Regular</option>
                <option value="Defectuoso">Defectuoso</option>
              </select>
            </div>
          </div>
        </form>
      </template>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="$emit('close')"
            class="flex items-center justify-center px-4 py-2 space-x-1 text-gray-700 transition-all bg-gray-100 rounded-lg hover:bg-gray-200"
          >
            <Icon name="material-symbols:close" class="w-4 h-4 sm:w-5 sm:h-5" />
            <span>Cancelar</span>
          </button>
          <button
            type="button"
            @click="handleSubmit"
            class="flex items-center justify-center w-full px-4 py-2 space-x-1 text-white transition-all bg-blue-600 rounded-lg sm:w-auto hover:bg-blue-700"
          >
            <Icon 
              :name="props.item ? 'material-symbols:save' : 'material-symbols:add'" 
              class="w-4 h-4 sm:w-5 sm:h-5"
            />
            <span>{{ props.item ? 'Actualizar' : 'Crear' }}</span>
          </button>
        </div>
      </template>
    </Modal>
  </div>
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

watchEffect(() => {
  if (props.item) {
    formData.value = { ...props.item }
  }
})

function formatPrice(value) {
  if (!value) return ''
  return new Intl.NumberFormat('es-CO', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

function handlePriceInput(event) {
  // Eliminar todo excepto números
  const numericValue = event.target.value.replace(/[^0-9]/g, '')
  // Convertir a número
  const numberValue = numericValue ? parseInt(numericValue) : 0
  // Actualizar el valor en el formulario
  formData.value.precio = numberValue
}

function handleSubmit() {
  emit('save', { ...formData.value })
}
</script>