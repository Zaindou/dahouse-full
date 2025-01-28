<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto bg-black/50 backdrop-blur-sm" @click="onClose">
    <div class="min-h-screen px-4 text-center">
      <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
      <div class="inline-block w-full max-w-2xl p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl"
        @click.stop>
        <!-- Header -->
        <div class="flex items-center justify-between pb-4 mb-4 border-b border-gray-200">
          <div class="space-y-1">
            <h3 class="text-xl font-semibold text-gray-900">
              Nueva Deducción
            </h3>
            <p class="text-sm text-gray-500">
              {{ selectedUser?.nombres }} {{ selectedUser?.apellidos }}
            </p>
          </div>
          <button @click="onClose" 
            class="p-2 text-gray-400 transition-colors rounded-full hover:bg-gray-100 hover:text-gray-600">
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6" :class="{ 'opacity-50 pointer-events-none': isSubmitting }">
          <!-- Switches Container -->
          <div class="flex items-center space-x-6">
            <!-- Falta Switch -->
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="isFalta" :disabled="isCustomConcept" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              <span class="ml-3 text-sm font-medium text-gray-700">Falta</span>
            </label>
            <!-- Custom Concept Switch -->
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="isCustomConcept" :disabled="isFalta" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              <span class="ml-3 text-sm font-medium text-gray-700">Concepto</span>
            </label>
          </div>

          <!-- Falta Date Section -->
          <div v-if="isFalta" class="space-y-1">
            <label for="falta-date" class="text-sm font-medium text-gray-700">Fecha de la Falta</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                <Icon name="heroicons:calendar" class="w-5 h-5 text-gray-400" />
              </div>
              <input 
                id="falta-date" 
                v-model="faltaDate" 
                type="date"
                required
                class="block w-full py-2 pl-10 pr-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>
          </div>

          <!-- Original Sections -->
          <template v-if="!isFalta">
            <!-- Concepto Section -->
            <div v-if="isCustomConcept">
              <div class="space-y-1">
                <label for="concepto" class="text-sm font-medium text-gray-700">Concepto</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <Icon name="heroicons:document-text" class="w-5 h-5 text-gray-400" />
                  </div>
                  <input 
                    id="concepto" 
                    v-model="loanData.concepto" 
                    type="text" 
                    required
                    class="block w-full py-2 pl-10 pr-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    placeholder="Ingrese el concepto de la deducción" 
                  />
                </div>
              </div>
            </div>
            <div v-else>
              <!-- Item Selection -->
              <div class="space-y-1">
                <label for="item" class="text-sm font-medium text-gray-700">Seleccionar Artículo</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <Icon name="heroicons:shopping-bag" class="w-5 h-5 text-gray-400" />
                  </div>
                  <select
                    id="item"
                    v-model="selectedItem"
                    required
                    class="block w-full py-2 pl-10 pr-10 border border-gray-300 rounded-lg shadow-sm appearance-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  >
                    <option value="" disabled selected>Seleccione un artículo</option>
                    <option v-for="item in sexShopItems" :key="item.id" :value="item">
                      {{ item.nombre_item }} - Disponible: {{ item.cantidad }}
                    </option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                  </div>
                </div>
              </div>

              <!-- Quantity Selection -->
              <div class="space-y-1" v-if="selectedItem">
                <label for="quantity" class="text-sm font-medium text-gray-700">Cantidad</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <Icon name="heroicons:calculator" class="w-5 h-5 text-gray-400" />
                  </div>
                  <select
                    id="quantity"
                    v-model="selectedQuantity"
                    required
                    class="block w-full py-2 pl-10 pr-10 border border-gray-300 rounded-lg shadow-sm appearance-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  >
                    <option value="" disabled selected>Seleccione cantidad</option>
                    <option v-for="n in selectedItem.cantidad" :key="n" :value="n">{{ n }}</option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                  </div>
                </div>
              </div>
            </div>
          </template>

<!-- Valor Total -->
          <div class="space-y-1">
            <label for="valor-total" class="text-sm font-medium text-gray-700">Valor Total</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                <Icon name="heroicons:currency-dollar" class="w-5 h-5 text-gray-400" />
              </div>
              <input 
                id="valor-total" 
                v-model="formattedValorTotal" 
                type="text" 
                required
                :readonly="!isCustomConcept || isFalta"
                class="block w-full py-2 pl-10 pr-16 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="0.00" 
              />
              <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                <span class="text-sm text-gray-500">COP</span>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <!-- Plazo Select -->
            <div class="space-y-1">
              <label for="plazo" class="text-sm font-medium text-gray-700">
                Plazo en Quincenas
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <Icon name="heroicons:calendar" class="w-5 h-5 text-gray-400" />
                </div>
                <select 
                  id="plazo" 
                  v-model="loanData.plazo"
                  required
                  class="block w-full py-2 pl-10 pr-10 border border-gray-300 rounded-lg shadow-sm appearance-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
                  <option value="" disabled selected>Seleccione el plazo</option>
                  <option v-for="n in 6" :key="n" :value="n">{{ n }} quincena{{ n !== 1 ? 's' : '' }}</option>
                </select>
                <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                </div>
              </div>
            </div>

            <!-- Tasa de Interés -->
            <div class="space-y-1">
              <label for="tasa" class="text-sm font-medium text-gray-700">
                Tasa de Interés (%)
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <Icon name="heroicons:chart-bar" class="w-5 h-5 text-gray-400" />
                </div>
                <input 
                  id="tasa" 
                  v-model.number="loanData.tasa" 
                  type="number" 
                  required 
                  step="0.01" 
                  min="0"
                  class="block w-full py-2 pl-10 pr-10 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="0.00" 
                />
                <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                  <span class="text-sm text-gray-500">%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Buttons -->
          <div class="flex justify-end pt-6 space-x-4 border-t border-gray-200">
            <button 
              v-if="showSimulateButton" 
              type="button" 
              @click="onSimulate"
              class="inline-flex items-center px-4 py-2 text-white transition-colors bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
              <Icon name="heroicons:calculator" class="w-5 h-5 mr-2" />
              Simular
            </button>
            <button 
              v-if="!showSimulateButton || removeSimulationButton" 
              type="submit" 
              :disabled="isSubmitting"
              class="inline-flex items-center px-4 py-2 text-white transition-colors bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Icon v-if="isSubmitting" name="heroicons:arrow-path" class="w-5 h-5 mr-2 animate-spin" />
              <Icon v-else name="heroicons:check" class="w-5 h-5 mr-2" />
              {{ isSubmitting ? 'Creando...' : 'Crear' }}
            </button>
            <button 
              type="button" 
              @click="onClose"
              class="inline-flex items-center px-4 py-2 text-gray-700 transition-colors bg-gray-100 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              <Icon name="heroicons:x-mark" class="w-5 h-5 mr-2" />
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useInventoryStore } from '~/stores/inventory';

const inventoryStore = useInventoryStore();
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

const isCustomConcept = ref(false);
const isFalta = ref(false);
const faltaDate = ref('');
const selectedItem = ref(null);
const selectedQuantity = ref('');

const loanData = ref({
  concepto: '',
  valor_total: 0,
  plazo: 1,
  tasa: 0
});

onMounted(async () => {
  await inventoryStore.fetchItems();
});

const sexShopItems = computed(() => {
  return inventoryStore.items.filter(item => 
    item.categoria.nombre === 'SEX SHOP' && item.cantidad > 0
  );
});

const showSimulateButton = computed(() => {
  return !props.removeSimulationButton && Number(loanData.value.tasa) !== 0;
});

const formattedValorTotal = computed({
  get() {
    if (document.activeElement.id !== "valor-total") {
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
      }).format(loanData.value.valor_total);
    }
    return loanData.value.valor_total.toString();
  },
  set(newValue) {
    if (isCustomConcept.value && !isFalta.value) {
      let parsedValue = newValue.replace(/\D/g, '');
      loanData.value.valor_total = parseFloat(parsedValue);
    }
  }
});

watch([isCustomConcept, isFalta], ([newCustom, newFalta]) => {
  if (newFalta) {
    isCustomConcept.value = false;
    selectedItem.value = null;
    selectedQuantity.value = '';
    loanData.value.valor_total = 15 * 4000;
  } else if (newCustom) {
    selectedItem.value = null;
    selectedQuantity.value = '';
    loanData.value.valor_total = 0;
  } else {
    loanData.value.concepto = '';
    loanData.value.valor_total = 0;
  }
});

watch(faltaDate, (newDate) => {
  if (isFalta.value && newDate) {
    const formattedDate = new Date(newDate).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    loanData.value.concepto = `FALTA ${formattedDate}`;
  }
});

watch([selectedItem, selectedQuantity], ([item, quantity]) => {
  if (item && quantity) {
    loanData.value.concepto = `${item.nombre_item} x${quantity}`;
    loanData.value.valor_total = item.precio * quantity;
  }
});

const onClose = () => {
  emit('close');
  loanData.value = {
    concepto: '',
    valor_total: 0,
    plazo: '',
    tasa: 0
  };
  isCustomConcept.value = false;
  isFalta.value = false;
  selectedItem.value = null;
  selectedQuantity.value = '';
  faltaDate.value = '';
};

const handleSubmit = async () => {
  try {
    await emit('submit', loanData.value);
    if (!isCustomConcept.value && !isFalta.value && selectedItem.value) {
      await inventoryStore.updateItem(selectedItem.value.id, {
        ...selectedItem.value,
        cantidad: selectedItem.value.cantidad - selectedQuantity.value
      });
    }
  } catch (error) {
    console.error('Error al procesar la deducción:', error);
  }
};

const onSimulate = () => {
  emit('simulate', loanData.value);
};
</script>