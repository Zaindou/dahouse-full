<template>
  <div class="flex items-center justify-between px-4 py-3 bg-white border-t border-gray-200 sm:px-6">
    <div class="flex justify-between flex-1 sm:hidden">
      <button
        :disabled="currentPage === 1"
        @click="$emit('update:modelValue', currentPage - 1)"
        class="relative inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Anterior
      </button>
      <button
        :disabled="currentPage === totalPages"
        @click="$emit('update:modelValue', currentPage + 1)"
        class="relative inline-flex items-center px-4 py-2 ml-3 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Siguiente
      </button>
    </div>
    <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-gray-700">
          Mostrando
          <span class="font-medium">{{ startItem }}</span>
          a
          <span class="font-medium">{{ endItem }}</span>
          de
          <span class="font-medium">{{ total }}</span>
          resultados
        </p>
      </div>
      <div>
        <nav class="inline-flex -space-x-px rounded-md shadow-sm isolate" aria-label="Pagination">
          <button
            :disabled="currentPage === 1"
            @click="$emit('update:modelValue', currentPage - 1)"
            class="relative inline-flex items-center px-2 py-2 text-gray-400 rounded-l-md ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span class="sr-only">Anterior</span>
            <Icon name="material-symbols:chevron-left" class="w-5 h-5" />
          </button>
          
          <!-- First page -->
          <button
            v-if="showFirst"
            @click="$emit('update:modelValue', 1)"
            :class="[
              currentPage === 1 ? 'z-10 bg-blue-600 text-white' : 'text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50',
              'relative inline-flex items-center px-4 py-2 text-sm font-semibold focus:z-20 focus:outline-offset-0'
            ]"
          >
            1
          </button>
          
          <!-- Ellipsis start -->
          <span
            v-if="showLeftEllipsis"
            class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-700 ring-1 ring-inset ring-gray-300"
          >
            ...
          </span>

          <!-- Page numbers -->
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="$emit('update:modelValue', page)"
            :class="[
              currentPage === page ? 'z-10 bg-blue-600 text-white' : 'text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50',
              'relative inline-flex items-center px-4 py-2 text-sm font-semibold focus:z-20 focus:outline-offset-0'
            ]"
          >
            {{ page }}
          </button>

          <!-- Ellipsis end -->
          <span
            v-if="showRightEllipsis"
            class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-700 ring-1 ring-inset ring-gray-300"
          >
            ...
          </span>

          <!-- Last page -->
          <button
            v-if="showLast"
            @click="$emit('update:modelValue', totalPages)"
            :class="[
              currentPage === totalPages ? 'z-10 bg-blue-600 text-white' : 'text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50',
              'relative inline-flex items-center px-4 py-2 text-sm font-semibold focus:z-20 focus:outline-offset-0'
            ]"
          >
            {{ totalPages }}
          </button>

          <button
            :disabled="currentPage === totalPages"
            @click="$emit('update:modelValue', currentPage + 1)"
            class="relative inline-flex items-center px-2 py-2 text-gray-400 rounded-r-md ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span class="sr-only">Siguiente</span>
            <Icon name="material-symbols:chevron-right" class="w-5 h-5" />
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  },
  total: {
    type: Number,
    required: true
  },
  perPage: {
    type: Number,
    required: true
  }
})

defineEmits(['update:modelValue'])

const currentPage = computed(() => props.modelValue)
const totalPages = computed(() => Math.ceil(props.total / props.perPage))

const startItem = computed(() => ((currentPage.value - 1) * props.perPage) + 1)
const endItem = computed(() => Math.min(currentPage.value * props.perPage, props.total))

// Lógica para mostrar máximo 7 páginas
const visiblePages = computed(() => {
  const maxVisiblePages = 5
  let start = Math.max(currentPage.value - Math.floor(maxVisiblePages / 2), 2)
  let end = Math.min(start + maxVisiblePages - 1, totalPages.value - 1)

  if (end - start < maxVisiblePages - 1) {
    start = Math.max(2, end - maxVisiblePages + 1)
  }

  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
})

const showFirst = computed(() => visiblePages.value[0] > 2)
const showLast = computed(() => visiblePages.value[visiblePages.value.length - 1] < totalPages.value - 1)
const showLeftEllipsis = computed(() => visiblePages.value[0] > 2)
const showRightEllipsis = computed(() => visiblePages.value[visiblePages.value.length - 1] < totalPages.value - 1)
</script>