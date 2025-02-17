<!-- components/DailyStats/GoalProgress.vue -->
<template>
  <div class="p-6 transition-shadow duration-300 bg-white shadow-sm rounded-xl hover:shadow-md">
    <!-- Header con información de meta -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h3 class="text-lg font-semibold text-gray-900">Progreso de Meta Mensual</h3>
        <p class="mt-1 text-sm text-gray-500">
          Periodo actual: {{ getCurrentPeriod() }}
        </p>
      </div>
      <div class="flex flex-col items-end">
        <div class="text-sm font-medium text-gray-900">
          Meta: {{ formatNumber(data.meta_mensual) }} tokens
        </div>
        <div class="mt-1 text-sm text-gray-500">
          Restantes: {{ formatNumber(data.meta_mensual - data.tokens_totales_generados) }}
        </div>
      </div>
    </div>

    <!-- Progreso general con animación y gradiente -->
    <div class="mb-8">
      <div class="flex justify-between mb-2">
        <span class="text-sm font-medium text-gray-700">
          {{ formatNumber(data.tokens_totales_generados) }} tokens generados
        </span>
        <div class="flex items-center gap-2">
          <span :class="getProgressColor(data.porcentaje_cumplimiento_mensual)"
                class="text-sm font-semibold">
            {{ data.porcentaje_cumplimiento_mensual }}%
          </span>
          <TrendIndicator :value="getProgressTrend()" />
        </div>
      </div>
      <div class="w-full h-3 bg-gray-100 rounded-full">
        <div class="h-3 transition-all duration-700 ease-out rounded-full"
             :class="getProgressBarColor(data.porcentaje_cumplimiento_mensual)"
             :style="{ 
               width: `${Math.min(data.porcentaje_cumplimiento_mensual, 100)}%`,
               backgroundImage: 'linear-gradient(45deg, rgba(255,255,255,.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,.15) 50%, rgba(255,255,255,.15) 75%, transparent 75%, transparent)',
               backgroundSize: '1rem 1rem',
               animation: 'progress-stripes 1s linear infinite'
             }"
        />
      </div>
    </div>

    <!-- Progreso por periodo con cards mejoradas -->
    <div class="grid grid-cols-2 gap-4 mb-8">
      <div v-for="(periodo, index) in ['primer_periodo', 'segundo_periodo']" 
           :key="periodo"
           class="p-4 transition-colors duration-300 rounded-xl bg-gray-50 hover:bg-gray-100"
      >
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full"
                 :class="getPeriodStatusColor(data.porcentaje_por_periodo[periodo])" />
            <span class="text-sm font-medium text-gray-800">
              {{ index + 1 }}° Periodo
            </span>
          </div>
          <span class="text-sm font-semibold"
                :class="getProgressColor(data.porcentaje_por_periodo[periodo])">
            {{ data.porcentaje_por_periodo[periodo] }}%
          </span>
        </div>
        <div class="w-full h-2 overflow-hidden bg-gray-200 rounded-full">
          <div class="h-2 transition-all duration-500 rounded-full"
               :class="getProgressBarColor(data.porcentaje_por_periodo[periodo])"
               :style="{ width: `${Math.min(data.porcentaje_por_periodo[periodo], 100)}%` }"
          />
        </div>
        <div class="flex items-center justify-between mt-2">
          <div class="text-sm text-gray-600">
            {{ formatNumber(data.tokens_por_periodo[periodo]) }} / 
            {{ formatNumber(data.meta_por_periodo) }}
          </div>
          <GoalBadge 
            :completed="data.tokens_por_periodo[periodo] >= data.meta_por_periodo"
          />
        </div>
      </div>
    </div>

    <!-- Progreso semanal con mini gráficos -->
    <div>
      <div class="flex items-center justify-between mb-4">
        <h4 class="text-sm font-semibold text-gray-800">Progreso Semanal</h4>
        <button @click="toggleWeeklyView"
                class="text-sm font-medium text-blue-600 hover:text-blue-700">
          {{ showDetailed ? 'Ver Simple' : 'Ver Detallado' }}
        </button>
      </div>
      
      <div :class="{'grid-cols-2': !showDetailed, 'grid-cols-4': showDetailed}"
           class="grid gap-4">
        <div v-for="(tokens, week) in data.tokens_por_semana" 
             :key="week"
             class="p-3 transition-colors duration-300 rounded-xl bg-gray-50 hover:bg-gray-100"
        >
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-700">
              Semana {{ week.slice(-1) }}
            </span>
            <span :class="getProgressColor((tokens / data.meta_por_semana) * 100)"
                  class="text-sm font-semibold">
              {{ ((tokens / data.meta_por_semana) * 100).toFixed(1) }}%
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-1.5 overflow-hidden">
            <div class="h-1.5 rounded-full transition-all duration-500"
                 :class="getProgressBarColor((tokens / data.meta_por_semana) * 100)"
                 :style="{ width: `${Math.min((tokens / data.meta_por_semana) * 100, 100)}%` }"
            />
          </div>
          <div class="flex items-center justify-between mt-2">
            <div class="text-xs text-gray-600">
              {{ formatNumber(tokens) }} / {{ formatNumber(data.meta_por_semana) }}
            </div>
            <GoalBadge 
              :completed="tokens >= data.meta_por_semana"
              size="small"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { toast } from 'vue-sonner'
import TrendIndicator from './TrendIndicator.vue'
import GoalBadge from './GoalBadge.vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const showDetailed = ref(false)

const formatNumber = (number) => {
  return new Intl.NumberFormat('es-MX').format(number)
}

const getCurrentPeriod = () => {
  const now = new Date()
  return now.getDate() <= 15 ? 'Primer periodo' : 'Segundo periodo'
}

const getProgressTrend = () => {
  // Implementar lógica para calcular tendencia
  return 'up' // 'up' | 'down' | 'neutral'
}

const getProgressColor = (percentage) => {
  if (percentage >= 100) return 'text-green-600'
  if (percentage >= 75) return 'text-blue-600'
  if (percentage >= 50) return 'text-yellow-600'
  return 'text-red-600'
}

const getProgressBarColor = (percentage) => {
  if (percentage >= 100) return 'bg-green-500'
  if (percentage >= 75) return 'bg-blue-500'
  if (percentage >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
}

const getPeriodStatusColor = (percentage) => {
  if (percentage >= 100) return 'bg-green-500'
  if (percentage >= 75) return 'bg-blue-500'
  if (percentage >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
}

const toggleWeeklyView = () => {
  showDetailed.value = !showDetailed.value
  toast.success(`Vista ${showDetailed.value ? 'detallada' : 'simple'} activada`)
}
</script>

<style scoped>
@keyframes progress-stripes {
  from { background-position: 1rem 0; }
  to { background-position: 0 0; }
}
</style>