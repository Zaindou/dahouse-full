<!-- components/Loans/ActiveLoansModal.vue -->
<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="fixed inset-0 bg-black/30 backdrop-blur-sm" @click="onClose"></div>
    
    <div class="min-h-screen px-4 text-center">
      <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
      
      <div class="inline-block w-full max-w-3xl p-4 my-8 text-left align-middle transition-all transform bg-white shadow-2xl sm:p-6 rounded-xl"
        @click.stop>
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <div class="pr-8">
            <h3 class="text-lg font-bold text-gray-900 sm:text-xl">
              Deducciones Activas
            </h3>
            <p class="mt-1 text-sm text-gray-500 truncate">
              {{ selectedUser?.nombres }} {{ selectedUser?.apellidos }}
            </p>
          </div>
          <button @click="onClose" 
            class="p-2 text-gray-400 transition-colors rounded-full hover:bg-gray-100 hover:text-gray-600 shrink-0">
            <Icon name="i-uil-times" class="w-5 h-5" />
          </button>
        </div>

        <!-- Summary cards -->
        <div class="grid grid-cols-1 gap-3 mb-6 sm:grid-cols-3 sm:gap-4">
          <div class="p-4 rounded-lg bg-blue-50">
            <h4 class="text-sm font-medium text-blue-700">Total Deducciones</h4>
            <p class="mt-2 text-xl font-semibold text-blue-900 sm:text-2xl">{{ activeDeductions.length }}</p>
          </div>
          <div class="p-4 rounded-lg bg-green-50">
            <h4 class="text-sm font-medium text-green-700">Total Pagado</h4>
            <p class="mt-2 text-xl font-semibold text-green-900 sm:text-2xl">
              {{ formatCurrency(totalPaidAmount) }}
            </p>
          </div>
          <div class="p-4 rounded-lg bg-amber-50">
            <h4 class="text-sm font-medium text-amber-700">Total Pendiente</h4>
            <p class="mt-2 text-xl font-semibold sm:text-2xl text-amber-900">
              {{ formatCurrency(totalRemainingAmount) }}
            </p>
          </div>
        </div>

        <!-- Deductions list -->
        <div class="space-y-4">
          <div v-if="activeDeductions.length > 0" class="space-y-3">
            <div v-for="deducible in activeDeductions" :key="deducible.id" 
              class="p-4 transition-colors border border-gray-100 sm:p-5 bg-gray-50 rounded-xl hover:bg-gray-50/80">
              <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-6">
                <div>
                  <p class="text-sm font-medium text-gray-500">Concepto</p>
                  <p class="mt-1 font-medium text-gray-900">{{ deducible.concepto }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Valor Total</p>
                  <p class="mt-1 font-medium text-gray-900">{{ formatCurrency(deducible.valor_total) }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Valor Quincenal</p>
                  <p class="mt-1 font-medium text-gray-900">{{ formatCurrency(deducible.valor_quincenal) }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Estado</p>
                  <span class="inline-flex px-3 py-1 text-sm font-medium text-green-700 bg-green-100 rounded-full ring-1 ring-green-700/10">
                    {{ deducible.estado }}
                  </span>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Fecha inicio</p>
                  <p class="mt-1 font-medium text-gray-900">{{ formatDate(deducible.fecha_inicio) }}</p>
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-500">Fecha fin</p>
                  <p class="mt-1 font-medium text-gray-900">{{ formatDate(deducible.fecha_fin) }}</p>
                </div>
                <div class="col-span-1 sm:col-span-2">
                  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-6">
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
                    <div>
                      <p class="text-sm font-medium text-gray-500">Quincenas pagadas</p>
                      <p class="mt-1 font-medium text-gray-900">{{ calculatePaidInstallments(deducible) }} de {{ deducible.plazo }}</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Progress bar -->
              <div class="mt-4">
                <div class="grid grid-cols-2 gap-4 mb-2">
                  <div>
                    <span class="text-sm font-medium text-green-600">Pagado: {{ formatCurrency(deducible.valor_pagado) }}</span>
                  </div>
                  <div class="text-right">
                    <span class="text-sm font-medium text-amber-600">Pendiente: {{ formatCurrency(deducible.valor_restante) }}</span>
                  </div>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div class="bg-green-500 h-2.5 rounded-full transition-all"
                    :style="{ width: `${calculateProgress(deducible)}%` }">
                  </div>
                </div>
                <div class="mt-1 text-right">
                  <span class="text-sm text-gray-500">{{ calculateProgress(deducible) }}% completado</span>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="py-12 text-center bg-gray-50 rounded-xl">
            <Icon name="i-uil-file-search-alt" class="w-12 h-12 mx-auto text-gray-400" />
            <p class="mt-2 text-gray-500">No hay deducciones activas</p>
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

const totalPaidAmount = computed(() => {
  return activeDeductions.value.reduce((total, deducible) => total + (deducible.valor_pagado || 0), 0);
});

const totalRemainingAmount = computed(() => {
  return activeDeductions.value.reduce((total, deducible) => total + (deducible.valor_restante || 0), 0);
});

const calculatePaidInstallments = (deducible) => {
  // Si quincenas_restantes es 1 y plazo es 4, significa que se han pagado 3 quincenas
  return deducible.plazo - deducible.quincenas_restantes;
};

const calculateProgress = (deducible) => {
  // Calcular el progreso basado en el valor pagado vs valor total
  const progress = (deducible.valor_pagado / deducible.valor_total) * 100;
  return Math.round(progress);
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

const onClose = () => {
  emit('close');
};
</script>