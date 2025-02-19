// pages/index.vue
<template>
  <NuxtLayout>
    <div class='container mx-auto'>
    <!-- Filtros -->
      <Filters
    :periodo="selectedPeriodo"
    :subperiodo="selectedSubPeriodo"
    :modelo="selectedModelo"
    @update:periodo="selectedPeriodo = $event"
    @update:subperiodo="selectedSubPeriodo = $event"
    @update:modelo="selectedModelo = $event"
  />


    <!-- Tabs -->
    <div class="mb-6 border-b border-gray-200">
      <nav class="flex space-x-4" aria-label="Tabs">
        <button
          v-for="tab in visibleTabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          :class="[
            activeTab === tab.key
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
            'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
          ]"
        >
          <div class="flex items-center">
            <Icon :name="tab.icon" class="w-5 h-5 mr-2" />
            {{ tab.name }}
          </div>
        </button>
      </nav>
    </div>

    <div v-if="loading" class="flex items-center justify-center py-8">
      <div class="w-12 h-12 border-b-2 border-blue-500 rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <!-- Vista de Estadísticas -->
      <div v-if="activeTab === 'stats'">
        <!-- Tarjetas de estadísticas -->
        <StatsCards
          v-if="earningsData"
          :data="earningsData"
          class="mb-6"
        />

        <div class="grid grid-cols-1 gap-6 mb-6 lg:grid-cols-2">
          <!-- Gráfica de tokens por día -->
          <TokensChart
            v-if="earningsData"
            :data="earningsData.tokens_por_dia_y_semana"
            v-model:selectedDate="selectedDate"
            @update:selectedDate="handleDateSelection"
          />

          <!-- Distribución por página -->
          <DistributionChart
            v-if="distributionData"
            :data="distributionData"
            :model-value="selectedModelo"
          />
        </div>
      </div>

      <!-- Vista de Podio -->
      <div v-else-if="activeTab === 'podium' && !selectedModelo">
        <ModelsPodium
          v-if="earningsData"
          :data="earningsData"
        />
      </div>

      <!-- Vista de Metas -->
      <div v-else-if="activeTab === 'goals' && !selectedModelo">
        <GoalProgress
          v-if="goalProgress"
          :data="goalProgress"
        />
      </div>
    </template>
  </div></NuxtLayout>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useEarningsStore } from '~/stores/earnings'
import { toast } from 'vue-sonner'

// Importar componentes
import Filters from '~/components/DailyStats/Filters.vue'
import StatsCards from '~/components/DailyStats/StatsCards.vue'
import TokensChart from '~/components/DailyStats/TokensChart.vue'
import DistributionChart from '~/components/DailyStats/DistributionChart.vue'
import GoalProgress from '~/components/DailyStats/GoalProgress.vue'
import ModelsPodium from '~/components/DailyStats/ModelsPodium.vue'

const store = useEarningsStore()

// Estado local
const selectedPeriodo = ref('')
const selectedSubPeriodo = ref('')
const selectedModelo = ref('')
const selectedDate = ref(null)
const activeTab = ref('stats')

// Configuración de tabs
const tabs = [
  { key: 'stats', name: 'Estadísticas', icon: 'ic:baseline-analytics' },
  { key: 'podium', name: 'Ranking', icon: 'ic:baseline-leaderboard' },
  { key: 'goals', name: 'Metas', icon: 'ic:baseline-flag' }
]

// Computed properties para acceder al store
const loading = computed(() => store.loading)
const earningsData = computed(() => store.earningsData)
const distributionData = computed(() => store.distributionData)
const goalProgress = computed(() => store.goalProgress)

// Computed property para controlar qué tabs se muestran
const visibleTabs = computed(() => {
  if (selectedModelo.value) {
    return tabs.filter(tab => tab.key === 'stats')
  }
  return tabs
})

// Función para manejar la selección de fecha
const handleDateSelection = async (date) => {
  try {
    await store.fetchDistribution(selectedPeriodo.value, selectedSubPeriodo.value, selectedModelo.value, date);
  } catch (error) {
    toast.error('Error al cargar distribución por fecha');
  }
};

// Watch para cambios en el tab activo
watch(activeTab, async (newTab) => {
  if (newTab === 'goals' && !selectedModelo.value && !goalProgress.value) {
    try {
      await store.fetchGoalProgress(selectedPeriodo.value)
    } catch (error) {
      toast.error('Error al cargar las metas')
    }
  }
})

// Cargar datos cuando cambien los filtros
watch([selectedPeriodo, selectedSubPeriodo, selectedModelo], async ([periodo, subperiodo, modelo], [oldPeriodo, oldsubperiodo, oldModelo]) => {
  if (!periodo) return
  
  try {
    // Resetear datos de distribución y fecha seleccionada
    store.distributionData = null
    selectedDate.value = null
    
    // Realizar las peticiones
    const requests = [
      store.fetchEarnings(periodo,subperiodo, modelo),
      store.fetchDistribution(periodo, subperiodo, modelo)
    ]

    // Si no hay modelo seleccionado y estamos en la vista de metas, cargar metas
    if (!modelo && activeTab.value === 'goals') {
      requests.push(store.fetchGoalProgress(periodo))
    }

    await Promise.all(requests)
  } catch (error) {
    toast.error('Error al cargar los datos')
  }
}, { immediate: true })

// Watch para cambiar a tab de estadísticas cuando se selecciona un modelo
watch(selectedModelo, (newValue) => {
  if (newValue) {
    activeTab.value = 'stats'
  }
})

// Cargar datos iniciales
onMounted(async () => {
  try {
    await store.fetchInitialData()
    selectedPeriodo.value = store.selectedMes
  } catch (error) {
    toast.error('Error al cargar datos iniciales')
  }
})
</script>