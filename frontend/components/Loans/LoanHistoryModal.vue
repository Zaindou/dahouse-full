<!-- components/Loans/LoanHistoryModal.vue -->
<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="fixed inset-0 bg-black/30 backdrop-blur-sm" @click="onClose"></div>
    
    <div class="min-h-screen px-4 text-center">
      <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
      
      <div class="inline-block w-full max-w-3xl p-6 my-8 text-left align-middle transition-all transform bg-white shadow-2xl rounded-xl"
        @click.stop>
        <!-- Header with improved styling -->
        <div class="flex items-center justify-between mb-6">
          <div>
            <h3 class="text-xl font-bold text-gray-900">
              Histórico de Deducciones
            </h3>
            <p class="mt-1 text-sm text-gray-500">
              {{ selectedUser?.nombres }} {{ selectedUser?.apellidos }}
            </p>
          </div>
          <button @click="onClose" 
            class="p-2 text-gray-400 transition-colors rounded-full hover:bg-gray-100 hover:text-gray-600">
            <Icon name="i-uil-times" class="w-5 h-5" />
          </button>
        </div>

        <!-- Search and filters section -->
        <div class="mb-6 space-y-4">
          <!-- Search input -->
          <div class="relative">
            <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
              <Icon name="i-uil-search" class="w-5 h-5 text-gray-400"/>
            </div>
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Buscar por concepto o creador..."
              class="block w-full pl-10 pr-4 py-2.5 text-gray-700 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
            />
          </div>

          <!-- Month selector -->
          <div>
            <label class="block mb-2 text-sm font-medium text-gray-700">Seleccionar mes:</label>
            <div class="relative">
              <select v-model="selectedMonth" @change="filterDeduciblesByMonth"
                class="w-full px-4 py-2.5 text-gray-700 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500">
                <option value="">Todos los meses</option>
                <option v-for="month in availableMonths" :key="month" :value="month">
                  {{ formatMonth(month) }}
                </option>
              </select>
              <Icon name="i-uil-angle-down" class="absolute w-5 h-5 text-gray-400 -translate-y-1/2 pointer-events-none right-3 top-1/2" />
            </div>
          </div>

          <!-- Active filters -->
          <div v-if="hasActiveFilters" class="flex flex-wrap gap-2">
            <div v-if="searchQuery" 
              class="inline-flex items-center px-3 py-1 text-sm text-blue-700 rounded-full bg-blue-50">
              <span>Búsqueda: {{ searchQuery }}</span>
              <button @click="searchQuery = ''" class="ml-2 hover:text-blue-900">
                <Icon name="i-uil-times" class="w-4 h-4" />
              </button>
            </div>
            <div v-if="selectedMonth" 
              class="inline-flex items-center px-3 py-1 text-sm text-blue-700 rounded-full bg-blue-50">
              <span>Mes: {{ formatMonth(selectedMonth) }}</span>
              <button @click="selectedMonth = ''" class="ml-2 hover:text-blue-900">
                <Icon name="i-uil-times" class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- Deductions list -->
        <div class="space-y-4">
          <div v-if="paginatedDeducibles.length > 0" class="space-y-3">
            <div v-for="deducible in paginatedDeducibles" :key="deducible.id" 
              class="p-5 transition-colors border border-gray-100 bg-gray-50 rounded-xl hover:bg-gray-50/80">
              <div class="grid grid-cols-2 gap-6">
                <div>
                  <p class="text-sm font-medium text-gray-500">Concepto</p>
                  <p class="mt-1 font-medium text-gray-900">{{ deducible.concepto }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Valor Total</p>
                  <p class="mt-1 font-medium text-gray-900">{{ formatCurrency(deducible.valor_total) }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Plazo</p>
                  <p class="mt-1 font-medium text-gray-900">{{ deducible.plazo }} períodos</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Estado</p>
                  <span :class="{
                    'inline-flex px-3 py-1 text-sm font-medium rounded-full': true,
                    'bg-green-100 text-green-700 ring-1 ring-green-700/10': deducible.estado === 'Activo',
                    'bg-blue-100 text-blue-700 ring-1 ring-blue-700/10': deducible.estado === 'Pagado',
                    'bg-yellow-100 text-yellow-700 ring-1 ring-yellow-700/10': deducible.estado === 'Refinanciado',

                  }">
                    {{ deducible.estado }}
                  </span>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Fecha inicio</p>
                  <p class="mt-1 font-medium text-gray-900">{{ formatDate(deducible.fecha_inicio) }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Creado por</p>
                  <div class="flex items-center mt-1 space-x-2">
                    <div class="flex-shrink-0">
                      <div class="flex items-center justify-center w-6 h-6 bg-gray-200 rounded-full">
                        <Icon name="i-uil-user" class="w-4 h-4 text-gray-600" />
                      </div>
                    </div>
                    <p class="font-medium text-gray-900">{{ deducible.creado_por || '-' }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="py-12 text-center bg-gray-50 rounded-xl">
            <Icon name="i-uil-file-search-alt" class="w-12 h-12 mx-auto text-gray-400" />
            <p class="mt-2 text-gray-500">
              {{ hasActiveFilters ? 'No se encontraron deducciones con los filtros aplicados' : 'No hay deducciones disponibles' }}
            </p>
          </div>
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-between pt-6 mt-6 border-t border-gray-100">
          <div>
            <p class="text-sm text-gray-600">
              Mostrando
              <span class="font-medium text-gray-900">{{ paginationStart + 1 }}</span> a
              <span class="font-medium text-gray-900">{{ paginationEnd }}</span> de
              <span class="font-medium text-gray-900">{{ filteredDeducibles.length }}</span> resultados
            </p>
          </div>
          <div class="flex space-x-2">
            <button @click="prevPage" :disabled="currentPage === 1"
              class="px-4 py-2 text-sm font-medium text-gray-700 transition-colors bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              <div class="flex items-center space-x-2">
                <Icon name="i-uil-angle-left" class="w-4 h-4" />
                <span>Anterior</span>
              </div>
            </button>
            <button @click="nextPage" :disabled="currentPage === totalPages"
              class="px-4 py-2 text-sm font-medium text-gray-700 transition-colors bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              <div class="flex items-center space-x-2">
                <span>Siguiente</span>
                <Icon name="i-uil-angle-right" class="w-4 h-4" />
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  selectedUser: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close']);

const searchQuery = ref('');
const selectedMonth = ref('');
const currentPage = ref(1);
const itemsPerPage = 5;

const availableMonths = computed(() => {
  if (!props.selectedUser?.deducibles) return [];
  const months = props.selectedUser.deducibles.map(d => {
    const date = new Date(d.fecha_inicio);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
  });
  return [...new Set(months)].sort();
});

const hasActiveFilters = computed(() => {
  return searchQuery.value || selectedMonth.value;
});

const filteredDeducibles = computed(() => {
  if (!props.selectedUser?.deducibles) return [];
  
  let filtered = props.selectedUser.deducibles;

  // Filtrar por mes
  if (selectedMonth.value) {
    filtered = filtered.filter(d => {
      const date = new Date(d.fecha_inicio);
      const deducibleMonth = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
      return deducibleMonth === selectedMonth.value;
    });
  }

  // Filtrar por búsqueda (incluye búsqueda en creado_por)
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(d => 
      d.concepto.toLowerCase().includes(query) ||
      (d.creado_por && d.creado_por.toLowerCase().includes(query))
    );
  }

  return filtered;
});

const totalPages = computed(() => Math.ceil(filteredDeducibles.value.length / itemsPerPage));

const paginatedDeducibles = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredDeducibles.value.slice(start, end);
});

const paginationStart = computed(() => (currentPage.value - 1) * itemsPerPage);
const paginationEnd = computed(() => Math.min(currentPage.value * itemsPerPage, filteredDeducibles.value.length));

const formatMonth = (dateString) => {
  const [year, month] = dateString.split('-');
  const date = new Date(year, month - 1);
  return date.toLocaleString('es-ES', { month: 'long', year: 'numeric' });
};

const formatCurrency = (value) => {
  const formatted = new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0,
  }).format(value);

  return formatted.replace(/\s+/g, '');
};

const formatDate = (dateString) => {
  if (!dateString) return '-';

  try {
    const date = new Date(dateString);

    if (isNaN(date.getTime())) {
      const parts = dateString.split(/[-/]/);
      if (parts.length === 3) {
        if (parts[0].length === 4) {
          date = new Date(parts[0], parts[1] - 1, parts[2]);
        } else {
          date = new Date(parts[2], parts[1] - 1, parts[0]);
        }
      }
    }

    if (isNaN(date.getTime())) {
      return '-';
    }

    return new Intl.DateTimeFormat('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date);
  } catch (error) {
    console.error('Error formateando fecha:', error);
    return '-';
  }
};

const filterDeduciblesByMonth = () => {
  currentPage.value = 1;
};

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

const onClose = () => {
  emit('close');
  searchQuery.value = '';
  selectedMonth.value = '';
  currentPage.value = 1;
};
</script>