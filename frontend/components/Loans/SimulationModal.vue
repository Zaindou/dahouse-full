<!-- components/Loans/SimulationModal.vue -->
<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50" @click="onClose">
    <div class="min-h-screen px-4 text-center">
      <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
      <div class="inline-block w-full max-w-4xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
        @click.stop>
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">
            Simulación de Deducción
          </h3>
          <button @click="onClose" class="text-gray-500 hover:text-gray-700">
            <Icon name="uil:times" class="w-6 h-6" />
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col"
                  class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                  Periodo
                </th>
                <th scope="col"
                  class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                  Cuota Quincenal
                </th>
                <th scope="col"
                  class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                  Capital
                </th>
                <th scope="col"
                  class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                  Interés
                </th>
                <th scope="col"
                  class="px-6 py-3 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                  Balance
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="pago in pagosDetalle" :key="pago.periodo">
                <td class="px-6 py-4 whitespace-nowrap">{{ pago.periodo }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.cuotaQuincenal) }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.principal) }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.interes) }}</td>
                <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.balanceRestante) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="p-4 mt-4 rounded-lg bg-gray-50">
          <h4 class="mb-3 text-lg font-semibold">Resumen del Préstamo</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm font-medium text-gray-500">Número de periodos</p>
              <p class="mt-1">{{ resumenPrestamo.numeroPeriodos }}</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-500">Valor a adeudar</p>
              <p class="mt-1">{{ formatCurrency(resumenPrestamo.valorAdeudar) }}</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-500">Valor total con intereses</p>
              <p class="mt-1">{{ formatCurrency(resumenPrestamo.valorConIntereses) }}</p>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-500">Cuota quincenal</p>
              <p class="mt-1">{{ formatCurrency(resumenPrestamo.cuotaQuincenal) }}</p>
            </div>
          </div>
        </div>

        <div class="flex justify-end mt-6 space-x-4">
          <button @click="onAccept"
            class="px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
            <Icon name="uil:check" class="inline-block w-5 h-5 mr-2" />
            Aceptar
          </button>
          <button @click="onClose"
            class="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
            <Icon name="uil:times" class="inline-block w-5 h-5 mr-2" />
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  pagosDetalle: {
    type: Array,
    required: true
  },
  resumenPrestamo: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close', 'accept']);

const formatCurrency = (value) => {
  const formatted = new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0,
  }).format(value);

  return formatted.replace(/\s+/g, '');
};

const onClose = () => {
  emit('close');
};

const onAccept = () => {
  emit('accept');
};
</script>