//components/inventory/CategoryModal.vue
<template>
  <Modal @close="$emit('close')">
    <template #header>
      <h3 class="text-lg font-medium text-gray-900">Nueva Categoría</h3>
    </template>

    <template #body>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Nombre</label>
          <input
            v-model="formData.nombre"
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
      </form>
    </template>

    <template #footer>
      <button
        type="button"
        @click="handleSubmit"
        class="px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700"
      >
        Crear
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
import Modal from '~/components/inventory/Modal.vue'

const emit = defineEmits(['close', 'save'])

const formData = ref({
  nombre: '',
  descripcion: ''
})

function handleSubmit() {
  emit('save', { ...formData.value })
}
</script>