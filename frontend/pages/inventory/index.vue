//pages/inventory/index.vue
<template>
<NuxtLayout>
  <div class="min-h-screen bg-gray-50">
    <div class="container px-4 py-8 mx-auto max-w-7xl">
      <!-- Skeleton loader -->
      <div v-if="loading" class="animate-pulse">
        <!-- Header Skeleton -->
        <div class="flex flex-col gap-4 mb-8 md:flex-row md:items-center md:justify-between">
          <div>
            <div class="w-48 h-8 bg-gray-200 rounded-lg"></div>
            <div class="w-64 h-4 mt-2 bg-gray-200 rounded-lg"></div>
          </div>
          <div class="flex flex-col gap-3 sm:flex-row">
            <div class="w-32 h-10 bg-gray-200 rounded-lg"></div>
            <div class="w-32 h-10 bg-gray-200 rounded-lg"></div>
          </div>
        </div>

        <!-- Filters Skeleton -->
        <div class="p-4 mb-6 bg-white shadow-sm rounded-xl md:p-6">
          <div class="grid grid-cols-1 gap-4 md:grid-cols-4 md:gap-6">
            <div class="space-y-2" v-for="i in 4" :key="i">
              <div class="w-20 h-4 bg-gray-200 rounded"></div>
              <div class="w-full h-10 bg-gray-200 rounded-lg"></div>
            </div>
          </div>
        </div>

        <!-- Mobile Skeleton -->
        <div class="grid grid-cols-1 gap-4 md:hidden">
          <div v-for="i in 3" :key="i" class="p-4 bg-white shadow-sm rounded-xl">
            <div class="flex justify-between mb-4">
              <div class="space-y-2">
                <div class="w-32 h-5 bg-gray-200 rounded"></div>
                <div class="w-48 h-4 bg-gray-200 rounded"></div>
              </div>
              <div class="flex space-x-2">
                <div class="w-8 h-8 bg-gray-200 rounded-lg"></div>
                <div class="w-8 h-8 bg-gray-200 rounded-lg"></div>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div v-for="j in 4" :key="j">
                <div class="w-20 h-4 mb-2 bg-gray-200 rounded"></div>
                <div class="w-24 h-6 bg-gray-200 rounded-full"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Desktop Table Skeleton -->
        <div class="hidden overflow-hidden bg-white shadow-sm rounded-xl md:block">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th v-for="i in 8" :key="i" class="px-6 py-4">
                  <div class="w-24 h-4 bg-gray-200 rounded"></div>
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="i in 5" :key="i">
                <td v-for="j in 8" :key="j" class="px-6 py-4">
                  <div class="w-24 h-4 bg-gray-200 rounded"></div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Actual content -->
      <template v-else>
        <!-- Header Section -->
        <div class="flex flex-col gap-4 mb-8 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900 md:text-3xl">Inventario</h1>
            <p class="mt-1 text-sm text-gray-500">Gestiona tus productos y categorías</p>
          </div>
          <div class="flex flex-col gap-3 sm:flex-row">
            <button
              @click="openModal('item')"
              class="flex items-center justify-center px-4 py-2 text-sm font-medium text-white transition-colors bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <Icon name="material-symbols:add" class="w-5 h-5 mr-2" />
              Nuevo Ítem
            </button>
            <button
              @click="openModal('category')"
              class="flex items-center justify-center px-4 py-2 text-sm font-medium text-white transition-colors bg-green-600 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
            >
              <Icon name="material-symbols:add" class="w-5 h-5 mr-2" />
              Nueva Categoría
            </button>
          </div>
        </div>

        <!-- Filters Section -->
        <div class="p-4 mb-6 bg-white shadow-sm rounded-xl md:p-6">
          <div class="grid grid-cols-1 gap-4 md:grid-cols-4 md:gap-6">
            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700">Categoría</label>
              <select 
                v-model="filters.categoria" 
                class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Todas las categorías</option>
                <option v-for="cat in inventory.categories" :key="cat.id" :value="cat.id">
                  {{ cat.nombre }}
                </option>
              </select>
            </div>
            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700">Estado</label>
              <select 
                v-model="filters.estado" 
                class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Todos los estados</option>
                <option value="Disponible">Disponible</option>
                <option value="Agotado">Agotado</option>
                <option value="Prestado">Prestado</option>
              </select>
            </div>
            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700">Estado Artículo</label>
              <select 
                v-model="filters.estadoArticulo" 
                class="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Todos los estados</option>
                <option value="Excelente">Excelente</option>
                <option value="Bueno">Bueno</option>
                <option value="Regular">Regular</option>
                <option value="Defectuoso">Defectuoso</option>
              </select>
            </div>
            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700">Buscar</label>
              <div class="relative">
                <Icon 
                  name="material-symbols:search" 
                  class="absolute w-5 h-5 text-gray-400 transform -translate-y-1/2 left-3 top-1/2"
                />
                <input
                  v-model="filters.search"
                  type="text"
                  placeholder="Buscar por nombre..."
                  class="w-full py-2 pl-10 pr-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Mobile Card View -->
        <div class="grid grid-cols-1 gap-4 md:hidden">
          <div 
            v-for="item in filteredItems" 
            :key="item.id"
            class="p-4 bg-white shadow-sm rounded-xl"
          >
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 class="text-lg font-medium text-gray-900">{{ item.nombre_item }}</h3>
                <p class="mt-1 text-sm text-gray-500">{{ item.descripcion }}</p>
              </div>
              <div class="flex space-x-2">
                <button
                  @click="editItem(item)"
                  class="p-2 text-blue-600 transition-colors rounded-lg hover:bg-blue-50"
                >
                  <Icon name="material-symbols:edit" class="w-5 h-5" />
                </button>
                <button
                  @click="deleteItem(item.id)"
                  class="p-2 text-red-600 transition-colors rounded-lg hover:bg-red-50"
                >
                  <Icon name="material-symbols:delete" class="w-5 h-5" />
                </button>
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-500">Categoría</p>
                <span class="inline-flex px-2 py-1 mt-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-full">
                  {{ item.categoria?.nombre }}
                </span>
              </div>
              <div>
                <p class="text-sm text-gray-500">Cantidad</p>
                <span
                  :class="[
                    'inline-flex items-center px-2.5 py-1 mt-1 rounded-full text-xs font-medium',
                    item.cantidad <= 2 
                      ? 'bg-red-50 text-red-700 ring-1 ring-inset ring-red-600/20' 
                      : 'bg-green-50 text-green-700 ring-1 ring-inset ring-green-600/20'
                  ]"
                >
                  <Icon 
                    :name="item.cantidad <= 2 ? 'material-symbols:warning' : 'material-symbols:check-circle'" 
                    class="w-4 h-4 mr-1"
                  />
                  {{ item.cantidad }}
                </span>
              </div>
              <div>
                <p class="text-sm text-gray-500">Precio</p>
                <p class="mt-1 text-sm font-medium text-gray-900">{{ formatCurrency(item.precio) }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Estado</p>
                <span
                  :class="[
                    'inline-flex items-center px-2.5 py-1 mt-1 rounded-full text-xs font-medium',
                    getEstadoClass(item.estado)
                  ]"
                >
                  <Icon 
                    :name="getEstadoIcon(item.estado)"
                    class="w-4 h-4 mr-1"
                  />
                  {{ item.estado }}
                </span>
              </div>
              <div>
                <p class="text-sm text-gray-500">Estado Artículo</p>
                <span
                  :class="[
                    'inline-flex items-center px-2.5 py-1 mt-1 rounded-full text-xs font-medium',
                    getEstadoArticuloClass(item.estado_articulo)
                  ]"
                >
                  <Icon 
                    :name="getEstadoArticuloIcon(item.estado_articulo)"
                    class="w-4 h-4 mr-1"
                  />
                  {{ item.estado_articulo }}
                </span>
              </div>
              <div class="col-span-2">
                <p class="text-sm text-gray-500">Última Actualización</p>
                <p class="mt-1 text-sm text-gray-900">{{ formatDate(item.fecha_actualizacion) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Desktop Table View -->
        <div class="hidden overflow-hidden bg-white shadow-sm rounded-xl md:block">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Item
                  </th>
                  <th class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Categoría
                  </th>
                  <th class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Cantidad
                  </th>
                  <th class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Precio
                  </th>
                  <th class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Estado
                  </th>
                  <th class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Estado Artículo
                  </th>
                  <th class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                    Última Actualización
                  </th>
                  <th class="px-6 py-3 text-xs font-medium tracking-wider text-right text-gray-500 uppercase">
                    Acciones
                  </th>
                </tr>
              </thead>
             <tbody class="divide-y divide-gray-200">
                <tr v-for="item in filteredItems" :key="item.id" class="transition-colors hover:bg-gray-50">
                  <td class="px-6 py-4">
                    <div class="text-xs font-medium text-gray-900">{{ item.nombre_item }}</div>
                    <div class="text-xs text-gray-500">{{ item.descripcion }}</div>
                  </td>
                  <td class="px-6 py-4">
                    <span class="inline-flex px-2 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-full">
                      {{ item.categoria?.nombre }}
                    </span>
                  </td>
                  <td class="px-6 py-4">
                    <span
                      :class="[
                        'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium',
                        item.cantidad <= 10 
                          ? 'bg-red-50 text-red-700 ring-1 ring-inset ring-red-600/20' 
                          : 'bg-green-50 text-green-700 ring-1 ring-inset ring-green-600/20'
                      ]"
                    >
                      <Icon 
                        :name="item.cantidad <= 10 ? 'material-symbols:warning' : 'material-symbols:check-circle'" 
                        class="w-4 h-4 mr-1"
                      />
                      {{ item.cantidad }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-900">
                    {{ formatCurrency(item.precio) }}
                  </td>
                  <td class="px-6 py-4">
                    <span
                      :class="[
                        'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium',
                        getEstadoClass(item.estado)
                      ]"
                    >
                      <Icon 
                        :name="getEstadoIcon(item.estado)"
                        class="w-4 h-4 mr-1"
                      />
                      {{ item.estado }}
                    </span>
                  </td>
                  <td class="px-6 py-4">
                    <span
                      :class="[
                        'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium',
                        getEstadoArticuloClass(item.estado_articulo)
                      ]"
                    >
                      <Icon 
                        :name="getEstadoArticuloIcon(item.estado_articulo)"
                        class="w-4 h-4 mr-1"
                      />
                      {{ item.estado_articulo }}
                    </span>
                  </td>
                  <td class="px-6 py-4">
                    <div class="text-sm text-gray-900">{{ formatDate(item.fecha_actualizacion) }}</div>
                  </td>
                  <td class="px-6 py-4">
                    <div class="flex justify-end space-x-3">
                      <button
                        @click="editItem(item)"
                        class="p-2 text-blue-600 transition-colors rounded-lg hover:bg-blue-50"
                        title="Editar"
                      >
                        <Icon name="material-symbols:edit" class="w-5 h-5" />
                      </button>
                      <button
                        @click="deleteItem(item.id)"
                        class="p-2 text-red-600 transition-colors rounded-lg hover:bg-red-50"
                        title="Eliminar"
                      >
                        <Icon name="material-symbols:delete" class="w-5 h-5" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Pagination -->
        <Pagination
          v-model="currentPage"
          :total="filteredTotal"
          :per-page="itemsPerPage"
        />
      </template>
    </div>

    <!-- Modals -->
    <ItemModal
      v-if="showItemModal"
      :item="editingItem"
      @close="closeModal('item')"
      @save="saveItem"
    />

    <CategoryModal
      v-if="showCategoryModal"
      @close="closeModal('category')"
      @save="saveCategory"
    />
  </div>
</NuxtLayout>
</template>

<script setup>
import { useInventoryStore } from '~/stores/inventory'
import ItemModal from '~/components/inventory/AddItemModal.vue'
import CategoryModal from '~/components/inventory/AddCategoryModal.vue'
import Pagination from '~/components/inventory/Pagination.vue'
import { toast } from 'vue-sonner'

const inventory = useInventoryStore()
const loading = ref(true)
const currentPage = ref(1)
const itemsPerPage = 7

const filters = ref({
  categoria: '',
  estado: '',
  estadoArticulo: '',
  search: ''
})

// Reset page when filters change
watch(filters, () => {
  currentPage.value = 1
}, { deep: true })

const showItemModal = ref(false)
const showCategoryModal = ref(false)
const editingItem = ref(null)

onMounted(async () => {
  try {
    await Promise.all([
      inventory.fetchCategories(),
      inventory.fetchItems()
    ])
  } catch (error) {
    toast.error('Error al cargar los datos: ' + error.message)
    console.error('Error al cargar datos:', error)
  } finally {
    loading.value = false
  }
})

// Computed para el total de items filtrados
const filteredTotal = computed(() => {
  return inventory.items.filter(item => {
    const matchesCategory = !filters.value.categoria || item.categoria?.id === parseInt(filters.value.categoria)
    const matchesStatus = (!filters.value.estado || item.estado === filters.value.estado) &&
      (!filters.value.estadoArticulo || item.estado_articulo === filters.value.estadoArticulo)
    const matchesSearch = !filters.value.search || 
      item.nombre_item.toLowerCase().includes(filters.value.search.toLowerCase()) ||
      item.descripcion?.toLowerCase().includes(filters.value.search.toLowerCase())
    
    return matchesCategory && matchesStatus && matchesSearch
  }).length
})

const filteredItems = computed(() => {
  const filtered = inventory.items.filter(item => {
    const matchesCategory = !filters.value.categoria || item.categoria?.id === parseInt(filters.value.categoria)
    const matchesStatus = (!filters.value.estado || item.estado === filters.value.estado) &&
      (!filters.value.estadoArticulo || item.estado_articulo === filters.value.estadoArticulo)
    const matchesSearch = !filters.value.search || 
      item.nombre_item.toLowerCase().includes(filters.value.search.toLowerCase()) ||
      item.descripcion?.toLowerCase().includes(filters.value.search.toLowerCase())
    
    return matchesCategory && matchesStatus && matchesSearch
  })

  // Notificar cuando no hay resultados
  if (filtered.length === 0 && (filters.value.categoria || filters.value.estado || filters.value.estadoArticulo || filters.value.search)) {
    toast.info('No se encontraron items con los filtros seleccionados')
  }

  // Aplicar paginación
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filtered.slice(start, end)
})

const formatCurrency = (value) => {
  const formatted = new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0,
  }).format(value);
  return formatted.replace(/\s+/g, '');
}

function formatDate(date) {
  return new Date(date).toLocaleString('es-CO', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function getEstadoClass(estado) {
  switch (estado) {
    case 'Disponible':
      return 'bg-green-50 text-green-700 ring-1 ring-inset ring-green-600/20'
    case 'Prestado':
      return 'bg-blue-50 text-blue-700 ring-1 ring-inset ring-blue-600/20'
    default:
      return 'bg-red-50 text-red-700 ring-1 ring-inset ring-red-600/20'
  }
}

function getEstadoIcon(estado) {
  switch (estado) {
    case 'Disponible':
      return 'material-symbols:check-circle'
    case 'Prestado':
      return 'material-symbols:assignment-return'
    default:
      return 'material-symbols:error'
  }
}

function getEstadoArticuloClass(estado) {
  switch (estado) {
    case 'Excelente':
      return 'bg-green-50 text-green-700 ring-1 ring-inset ring-green-600/20'
    case 'Bueno':
      return 'bg-emerald-50 text-emerald-700 ring-1 ring-inset ring-emerald-600/20'
    case 'Regular':
      return 'bg-yellow-50 text-yellow-700 ring-1 ring-inset ring-yellow-600/20'
    case 'Defectuoso':
      return 'bg-red-50 text-red-700 ring-1 ring-inset ring-red-600/20'
    default:
      return 'bg-gray-50 text-gray-700 ring-1 ring-inset ring-gray-600/20'
  }
}

function getEstadoArticuloIcon(estado) {
  switch (estado) {
    case 'Excelente':
      return 'material-symbols:star'
    case 'Bueno':
      return 'material-symbols:stars'
    case 'Regular':
      return 'material-symbols:star-half'
    case 'Defectuoso':
      return 'material-symbols:broken-image'
    default:
      return 'material-symbols:help'
  }
}

function openModal(type) {
  if (type === 'item') {
    showItemModal.value = true
  } else {
    showCategoryModal.value = true
  }
}

function closeModal(type) {
  if (type === 'item') {
    showItemModal.value = false
    editingItem.value = null
  } else {
    showCategoryModal.value = false
  }
}

function editItem(item) {
  editingItem.value = { ...item }
  showItemModal.value = true
}

async function saveItem(itemData) {
  try {
    if (editingItem.value) {
      await inventory.updateItem(editingItem.value.id, itemData)
      toast.success('Item actualizado correctamente')
    } else {
      await inventory.addItem(itemData)
      toast.success('Item agregado correctamente')
    }
    closeModal('item')
  } catch (error) {
    toast.error('Error al guardar el item: ' + error.message)
    console.error('Error al guardar item:', error)
  }
}

async function saveCategory(categoryData) {
  try {
    await inventory.addCategory(categoryData)
    toast.success('Categoría agregada correctamente')
    closeModal('category')
  } catch (error) {
    toast.error('Error al guardar la categoría: ' + error.message)
    console.error('Error al guardar categoría:', error)
  }
}

async function deleteItem(id) {
  toast('¿Estás seguro de eliminar este ítem?', {
    action: {
      label: 'Eliminar',
      onClick: () => {
        toast.promise(
          inventory.deleteItem(id),
          {
            loading: 'Eliminando item...',
            success: 'Item eliminado correctamente',
            error: (err) => `Error al eliminar: ${err.message}`
          }
        )
      }
    },
    cancel: {
      label: 'Cancelar',
      onClick: () => toast.dismiss()
    },
    duration: Infinity // Para que no desaparezca automáticamente
  })
}
</script>