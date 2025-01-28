<!-- components/Loans/ActiveLoansModal.vue -->
<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50" @click="onClose">
    <div class="min-h-screen px-4 text-center">
      <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
      <div class="inline-block w-full max-w-3xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
        @click.stop>
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">
            Deducciones Activas - {{ selectedUser?.nombres }} {{ selectedUser?.apellidos }}
          </h3>
          <button @click="onClose" class="text-gray-500 hover:text-gray-700">
            <Icon name="uil:times" class="w-6 h-6" />
          </button>
        </div>

        <div class="mt-4">
          <div v-if="activeDeductions.length > 0" class="space-y-4">
            <div v-for="deducible in activeDeductions" :key="deducible.id" class="p-4 bg-white border rounded-lg">
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
                  <span class="inline-flex px-2 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full">
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
            No hay deducciones activas
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

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

const activeDeductions = computed(() => {
  return props.selectedUser?.deducibles?.filter(d => d.estado === 'Activo') || [];
});

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

const onClose = () => {
  emit('close');
};
</script>