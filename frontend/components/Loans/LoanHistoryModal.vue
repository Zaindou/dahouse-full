<!-- components/Loans/LoanHistoryModal.vue -->
<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50" @click="onClose">
    <div class="min-h-screen px-4 text-center">
      <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
      <div class="inline-block w-full max-w-3xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
        @click.stop>
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">
            Histórico de Deducciones - {{ selectedUser?.nombres }} {{ selectedUser?.apellidos }}
          </h3>
          <button @click="onClose" class="text-gray-500 hover:text-gray-700">
            <Icon name="uil:times" class="w-6 h-6" />
          </button>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Seleccionar mes:</label>
          <select v-model="selectedMonth" @change="filterDeduciblesByMonth"
            class="block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
            <option v-for="month in availableMonths" :key="month" :value="month">
              {{ formatMonth(month) }}
            </option>
          </select>
        </div>

        <div class="mt-4">
          <div v-if="paginatedDeducibles.length > 0" class="space-y-4">
            <div v-for="deducible in paginatedDeducibles" :key="deducible.id" class="p-4 bg-white border rounded-lg">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <p class="text-sm font-medium text-gray-500">Concepto</p>
                  <p class="mt-1">{{ deducible.concepto }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Valor Total</p>
                  <p class="mt-1">{{ formatCurrency(deducible.valor_total) }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Plazo</p>
                  <p class="mt-1">{{ deducible.plazo }} períodos</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Estado</p>
                  <span :class="{
                    'inline-flex px-2 py-1 text-xs font-semibold rounded-full': true,
                    'bg-green-100 text-green-800': deducible.estado === 'Activo',
                    'bg-red-100 text-red-800': deducible.estado === 'Inactivo'
                  }">
                    {{ deducible.estado }}
                  </span>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Fecha inicio</p>
                  <p class="mt-1">{{ formatDate(deducible.fecha_inicio) }}</p>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="p-4 text-center text-gray-500">
            No hay deducciones para este mes
          </div>
        </div>

        <div class="flex items-center justify-between mt-6">
          <div>
            <p class="text-sm text-gray-700">
              Mostrando
              <span class="font-medium">{{ paginationStart + 1 }}</span> a
              <span class="font-medium">{{ paginationEnd }}</span> de
              <span class="font-medium">{{ filteredDeducibles.length }}</span> resultados
            </p>
          </div>
          <div class="flex space-x-2">
            <button @click="prevPage" :disabled="currentPage === 1"
              class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              Anterior
            </button>
            <button @click="nextPage" :disabled="currentPage === totalPages"
              class="px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
              Siguiente
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

const filteredDeducibles = computed(() => {
  if (!props.selectedUser?.deducibles) return [];
  if (!selectedMonth.value) return props.selectedUser.deducibles;
  return props.selectedUser.deducibles.filter(d => {
    const date = new Date(d.fecha_inicio);
    const deducibleMonth = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    return deducibleMonth === selectedMonth.value;
  });
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
  return date.toLocaleString('default', { month: 'long', year: 'numeric' });
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
  selectedMonth.value = '';
  currentPage.value = 1;
};
</script>