<!-- components/Loans/NewLoanModal.vue -->
<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50" @click="onClose">
    <div class="min-h-screen px-4 text-center">
      <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
      <div class="inline-block w-full max-w-2xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
        @click.stop>
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900">
            Nueva Deducción - {{ selectedUser?.nombres }} {{ selectedUser?.apellidos }}
          </h3>
          <button @click="onClose" class="text-gray-500 hover:text-gray-700">
            <Icon name="uil:times" class="w-6 h-6" />
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6" :class="{ 'opacity-50 pointer-events-none': isSubmitting }">
          <div>
            <label for="concepto" class="block text-sm font-medium text-gray-700">Concepto</label>
            <input id="concepto" v-model="loanData.concepto" type="text" required
              class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="Ingrese el concepto" />
          </div>

          <div>
            <label for="valor-total" class="block text-sm font-medium text-gray-700">Valor Total</label>
            <div class="relative mt-1">
              <input id="valor-total" v-model="formattedValorTotal" type="text" required
                class="block w-full pr-12 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="0.00" />
              <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                <span class="text-gray-500 sm:text-sm">COP</span>
              </div>
            </div>
          </div>

          <div>
            <label for="plazo" class="block text-sm font-medium text-gray-700">
              Plazo (máx 6 periodos)
            </label>
            <input id="plazo" v-model.number="loanData.plazo" type="number" required max="6" min="1"
              class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
          </div>

          <div>
            <label for="tasa" class="block text-sm font-medium text-gray-700">
              Tasa de Interés (%)
            </label>
            <input id="tasa" v-model.number="loanData.tasa" type="number" required step="0.01" min="0"
              class="block w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
          </div>

          <div class="flex justify-end pt-4 space-x-4">
            <button v-if="!removeSimulationButton" type="button" @click="onSimulate"
              class="px-4 py-2 text-white bg-purple-500 rounded-md hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2">
              <Icon name="uil:calculator" class="inline-block w-5 h-5 mr-2" />
              Simular
            </button>
            <button v-if="removeSimulationButton" type="submit" :disabled="isSubmitting"
              class="inline-flex items-center px-4 py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed">
              <Icon v-if="isSubmitting" name="uil:spinner" class="w-5 h-5 mr-2 animate-spin" />
              <Icon v-else name="uil:save" class="w-5 h-5 mr-2" />
              {{ isSubmitting ? 'Creando...' : 'Crear' }}
            </button>
            <button type="button" @click="onClose"
              class="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
              <Icon name="uil:times" class="inline-block w-5 h-5 mr-2" />
              Cancelar
            </button>
          </div>
        </form>
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
  },
  removeSimulationButton: {
    type: Boolean,
    default: false
  },
  isSubmitting: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'submit', 'simulate']);

const loanData = ref({
  concepto: '',
  valor_total: 0,
  plazo: 0,
  tasa: 0
});

const formattedValorTotal = computed({
  get() {
    if (document.activeElement.id !== "valor-total-input") {
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
      }).format(loanData.value.valor_total);
    }
    return loanData.value.valor_total.toString();
  },
  set(newValue) {
    let parsedValue = newValue.replace(/\D/g, '');
    loanData.value.valor_total = parseFloat(parsedValue);
  }
});

const onClose = () => {
  emit('close');
  // Reset form
  loanData.value = {
    concepto: '',
    valor_total: 0,
    plazo: 0,
    tasa: 0
  };
};

const handleSubmit = () => {
  emit('submit', loanData.value);
};

const onSimulate = () => {
  emit('simulate', loanData.value);
};
</script>