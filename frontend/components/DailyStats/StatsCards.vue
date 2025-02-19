<!-- components/DailyStats/StatsCards.vue -->
<template>
  <div class="grid grid-cols-1 gap-6 mb-6 md:grid-cols-2 lg:grid-cols-4">
    <div 
      v-for="(card, index) in statsCards" 
      :key="index"
      class="relative p-6 transition-all duration-300 transform bg-white rounded-lg shadow-md group hover:shadow-lg hover:-translate-y-1"
      :class="{'bg-gray-50': loading}"
      role="article"
      :aria-label="card.title"
      tabindex="0"
    >
      <div class="flex items-center justify-between">
        <div class="flex-1">
          <div class="flex items-center">
            <h3 class="text-sm font-medium text-gray-600 transition-colors group-hover:text-gray-800">
              {{ card.title }}
            </h3>
            <button 
              class="ml-2 text-gray-400 transition-colors hover:text-blue-500"
              @click="showInfo(card)"
            >
              <Icon name="ri:information-line" class="w-4 h-4" />
            </button>
          </div>
          <p class="mt-1 text-2xl font-semibold text-gray-900">
            <span class="sr-only">Valor:</span>
            {{ formatValue(card.value, card.type) }}
          </p>
        </div>
        <div 
          :class="[
            'p-3 transition-colors rounded-full',
            card.bgColor,
            card.hoverBgColor
          ]"
          aria-hidden="true"
        >
          <Icon 
            :name="card.icon" 
            :class="['w-6 h-6 transition-colors', card.iconColor, card.hoverIconColor]"
          />
        </div>
      </div>

      <div class="mt-4">
        <p class="text-sm text-gray-500 transition-colors group-hover:text-gray-600">
          {{ card.description }}
        </p>
        <div v-if="card.trend" class="mt-2 text-xs">
          <span 
            :class="[
              card.trend > 0 ? 'text-green-600' : 'text-red-600',
              'font-medium'
            ]"
          >
            {{ card.trend > 0 ? '↑' : '↓' }} {{ Math.abs(card.trend) }}%
          </span>
          <span class="ml-1 text-gray-500">vs periodo anterior</span>
        </div>
      </div>

      <!-- Loading overlay -->
      <div v-if="loading" 
           class="absolute inset-0 flex items-center justify-center rounded-lg bg-white/50 backdrop-blur-sm">
        <Icon name="ri:loader-4-line" class="w-6 h-6 text-blue-500 animate-spin" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { toast } from 'vue-sonner'

const loading = ref(false)

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const statsCards = computed(() => {
  if (!props.data) return []

  const { totals } = props.data
  
  return [
    {
      title: 'Total Tokens',
      value: totals.total_tokens || 0,
      type: 'number',
      icon: 'ph:coins',
      description: 'Tokens generados en el periodo',
      trend: calculateTrend(totals.total_tokens, totals.previous_total_tokens),
      info: 'Total de tokens generados durante el período actual, incluyendo todos los tipos de solicitudes y respuestas.',
      bgColor: 'bg-purple-50',
      hoverBgColor: 'group-hover:bg-purple-100',
      iconColor: 'text-purple-500',
      hoverIconColor: 'group-hover:text-purple-600'
    },
    {
      title: 'Total Horas',
      value: totals.total_hours || 0,
      type: 'hours',
      icon: 'ic:baseline-schedule',
      description: 'Horas trabajadas',
      trend: calculateTrend(totals.total_hours, totals.previous_total_hours),
      info: 'Suma total de horas registradas en el período actual. Incluye todo el tiempo con actividad registrada.',
      bgColor: 'bg-blue-50',
      hoverBgColor: 'group-hover:bg-blue-100',
      iconColor: 'text-blue-500',
      hoverIconColor: 'group-hover:text-blue-600'
    },
    {
      title: 'Días Trabajados',
      value: totals.total_days_worked || 0,
      type: 'number',
      icon: 'ic:baseline-calendar-today',
      description: 'Días con actividad registrada',
      trend: calculateTrend(totals.total_days_worked, totals.previous_total_dias),
      info: 'Número total de días únicos en los que se registró al menos una actividad durante el período.',
      bgColor: 'bg-emerald-50',
      hoverBgColor: 'group-hover:bg-emerald-100',
      iconColor: 'text-emerald-500',
      hoverIconColor: 'group-hover:text-emerald-600'
    },
    {
      title: 'Promedio Tokens/Día',
      value: calculateAverage(totals.total_tokens, totals.total_days_worked),
      type: 'number',
      icon: 'ic:baseline-trending-up',
      description: 'Promedio diario de tokens',
      info: 'Promedio diario de tokens calculado como el total de tokens dividido entre el número de días con actividad.',
      bgColor: 'bg-amber-50',
      hoverBgColor: 'group-hover:bg-amber-100',
      iconColor: 'text-amber-500',
      hoverIconColor: 'group-hover:text-amber-600'
    }
  ]
})

function calculateTrend(currentValue, previousValue) {
  if (!previousValue || !currentValue) return null
  const difference = ((currentValue - previousValue) / previousValue) * 100
  return Math.round(difference)
}

function calculateAverage(total, days) {
  if (!days || days === 0) return 0
  return (total / days).toFixed(2)
}

function formatValue(value, type) {
  if (typeof value !== 'number') return value

  if (type === 'hours') {
    return Math.round(value).toString()
  }

  if (value >= 1000) {
    return value.toLocaleString('es-ES')
  }
  
  return value.toString()
}

function showInfo(card) {
  toast.info(card.info, {
    duration: 4000,
    position: 'bottom-center',
    className: 'bg-white shadow-lg rounded-lg',
    style: {
      padding: '1rem'
    }
  })
}

async function refreshData() {
  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    toast.success('Datos actualizados correctamente')
  } catch (error) {
    toast.error('Error al actualizar los datos')
  } finally {
    loading.value = false
  }
}

defineExpose({
  refresh: refreshData
})
</script>