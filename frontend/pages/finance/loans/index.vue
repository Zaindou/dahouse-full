<template>
  <NuxtLayout>
    <div class="min-h-screen bg-gray-50">
      <!-- Header Section -->
      <div class="bg-white shadow">
        <div class="px-4 py-6 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div class="flex flex-col items-start justify-between gap-4 md:flex-row md:items-center">
            <div>
              <h1 class="text-2xl font-bold tracking-tight text-gray-900">Gestión de Deducciones</h1>
              <p class="mt-1 text-sm text-gray-500">Administra las deducciones de tus empleados de forma eficiente</p>
            </div>
            <div class="relative w-full md:w-64">
              <div class="absolute inset-y-0 left-0 flex items-center pl-3">
                <Icon name="uil:search" class="w-5 h-5 text-gray-400" />
              </div>
              <input v-model="filtro" type="text" placeholder="Buscar empleados..."
                class="w-full py-2 pl-10 pr-4 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="px-4 py-8 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <!-- Loading Skeleton -->
        <div v-if="initialSkeleton" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <div v-for="n in 6" :key="n" class="p-4 bg-white rounded-lg shadow animate-pulse">
            <div class="h-24"></div>
          </div>
        </div>

        <!-- Employee Cards Grid -->
        <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <div v-for="modelo in modelosFiltrados" :key="modelo.id"
            class="overflow-hidden transition-shadow duration-200 bg-white rounded-lg shadow-sm hover:shadow-lg">
            <div class="p-6">
              <!-- Employee Header -->
              <div class="flex items-center justify-between pb-4">
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
                    <img class="w-12 h-12 rounded-full"
                      :src="`https://ui-avatars.com/api/?name=${modelo.nombres}+${modelo.apellidos}&background=random`"
                      :alt="modelo.nombres" />
                  </div>
                  <div>
                    <h2 class="text-lg font-medium text-gray-900">
                      {{ modelo.nombres }} {{ modelo.apellidos }}
                    </h2>
                    <p class="text-sm text-gray-500">{{ modelo.nombre_usuario }}</p>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="grid grid-cols-3 gap-4 mt-4">
                <button @click="abrirFormularioDeduccion(modelo)"
                  class="flex flex-col items-center p-3 text-sm text-blue-600 transition-colors rounded-lg hover:bg-blue-50">
                  <Icon name="uil:plus" class="w-6 h-6 mb-1" />
                  <span>Nueva</span>
                </button>
                <button @click="abrirModalDeduciblesActivos(modelo)"
                  class="flex flex-col items-center p-3 text-sm text-green-600 transition-colors rounded-lg hover:bg-green-50">
                  <Icon name="uil:credit-card" class="w-6 h-6 mb-1" />
                  <span>Activas</span>
                </button>
                <button @click="abrirModalHistorico(modelo)"
                  class="flex flex-col items-center p-3 text-sm text-purple-600 transition-colors rounded-lg hover:bg-purple-50">
                  <Icon name="uil:history" class="w-6 h-6 mb-1" />
                  <span>Histórico</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Modales -->
      <NewLoanModal 
        :show="openModal" 
        :selected-user="modeloSeleccionado"
        :remove-simulation-button="removeSimulationButton"
        :is-submitting="isSubmitting"
        @close="closeAllModals"
        @submit="guardarDeduccion"
        @simulate="simularDeduccion"
      />

      <SimulationModal 
        :show="openSimulationModal"
        :pagos-detalle="pagosDetalle"
        :resumen-prestamo="resumenPrestamo"
        @close="closeAllModals"
        @accept="acceptSimulation"
      />

      <ActiveLoansModal 
        :show="openActiveDebtModal"
        :selected-user="modeloSeleccionado"
        @close="closeAllModals"
      />

      <LoanHistoryModal 
        :show="openRecordModal"
        :selected-user="modeloSeleccionado"
        @close="closeAllModals"
      />
    </div>
  </NuxtLayout>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useModelosStore } from '~/stores/modelo';
import NewLoanModal from '~/components/Loans/NewLoanModal.vue';
import SimulationModal from '~/components/Loans/SimulationModal.vue';
import ActiveLoansModal from '~/components/Loans/ActiveLoansModal.vue';
import LoanHistoryModal from '~/components/Loans/LoanHistoryModal.vue';

useHead({
  titleTemplate: '%s - Deducciones',
});

const modelosStore = useModelosStore();
const isLoading = ref(false);
const initialSkeleton = ref(false);
const openModal = ref(false);
const openActiveDebtModal = ref(false);
const openRecordModal = ref(false);
const modelos = ref([]);
const filtro = ref('');
const modeloSeleccionado = ref(null);
const openSimulationModal = ref(false);
const pagosDetalle = ref([]);
const resumenPrestamo = ref({});
const removeSimulationButton = ref(false);
const isSubmitting = ref(false);

const fetchInitialData = async () => {
  initialSkeleton.value = true;
  try {
    modelos.value = await modelosStore.fetchModelos();
  } catch (error) {
    Swal.fire('Error', 'No se pudo cargar la lista de usuarios', 'error');
  } finally {
    initialSkeleton.value = false;
  }
};

fetchInitialData();

const modelosFiltrados = computed(() => {
  if (!modelos.value) {
    return [];
  }
  let filtered = modelos.value.filter(modelo => {
    const filtroEnMinusculas = filtro.value.toLowerCase();
    return (modelo.nombre_usuario.toLowerCase().includes(filtroEnMinusculas) ||
      modelo.nombres.toLowerCase().includes(filtroEnMinusculas) ||
      modelo.apellidos.toLowerCase().includes(filtroEnMinusculas)) &&
      modelo.habilitado === true && modelo.rol === 'Modelo';
  });

  return filtered.sort((a, b) => {
    const nombreCompletoA = `${a.nombres} ${a.apellidos}`.toLowerCase();
    const nombreCompletoB = `${b.nombres} ${b.apellidos}`.toLowerCase();
    return nombreCompletoA.localeCompare(nombreCompletoB);
  });
});

const abrirFormularioDeduccion = (modelo) => {
  modeloSeleccionado.value = modelo;
  openModal.value = true;
};

const abrirModalDeduciblesActivos = (modelo) => {
  modeloSeleccionado.value = modelo;
  openActiveDebtModal.value = true;
};

const abrirModalHistorico = (modelo) => {
  modeloSeleccionado.value = modelo;
  openRecordModal.value = true;
};

const closeAllModals = () => {
  openModal.value = false;
  openActiveDebtModal.value = false;
  openRecordModal.value = false;
  openSimulationModal.value = false;
  removeSimulationButton.value = false;
  modeloSeleccionado.value = null;
  isSubmitting.value = false;
};

const acceptSimulation = () => {
  openSimulationModal.value = false;
  removeSimulationButton.value = true;
};

const simularDeduccion = (deduccionData) => {
  const valorTotal = parseFloat(deduccionData.valor_total) || 0;
  const plazo = parseInt(deduccionData.plazo, 10) || 0;
  let tasa = parseFloat(deduccionData.tasa) || 0;

  if (tasa > 1) {
    tasa = tasa / 100;
  }

  if (valorTotal <= 0 || plazo <= 0 || tasa < 0) {
    alert('Por favor, introduzca valores válidos. Todos los campos deben ser números y mayores que cero.');
    return;
  }

  const tasaQuincenal = tasa / 2;
  const cuotaQuincenal = valorTotal * ((tasaQuincenal * Math.pow(1 + tasaQuincenal, plazo)) / (Math.pow(1 + tasaQuincenal, plazo) - 1));
  let saldoCapital = valorTotal;
  pagosDetalle.value = [];

  for (let i = 1; i <= plazo; i++) {
    const interes = saldoCapital * tasaQuincenal;
    const principal = cuotaQuincenal - interes;
    saldoCapital -= principal;

    if (saldoCapital < 0) saldoCapital = 0;

    pagosDetalle.value.push({
      periodo: i,
      cuotaQuincenal: cuotaQuincenal.toFixed(2),
      principal: principal.toFixed(2),
      interes: interes.toFixed(2),
      saldoCapital: saldoCapital.toFixed(2),
      balanceRestante: (saldoCapital > 0 ? saldoCapital : 0).toFixed(2)
    });
  }

  resumenPrestamo.value = {
    numeroPeriodos: plazo,
    valorAdeudar: valorTotal.toFixed(2),
    valorConIntereses: (cuotaQuincenal * plazo).toFixed(2),
    cuotaQuincenal: cuotaQuincenal.toFixed(2)
  };

  openSimulationModal.value = true;
};

const guardarDeduccion = async (deduccionData) => {
  if (isSubmitting.value) return;

  try {
    isSubmitting.value = true;
    const response = await modelosStore.crearDeduccion(
      modeloSeleccionado.value.nombre_usuario,
      deduccionData
    );
    modelos.value = await modelosStore.fetchModelos();
    closeAllModals();
    Swal.fire('Éxito', response.mensaje, 'success');
  } catch (error) {
    Swal.fire('Error', 'Ha ocurrido un error', 'error');
  } finally {
    isSubmitting.value = false;
  }
};
</script>