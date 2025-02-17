// components/DailyStats/StatsCards.vue
<template>
  <div class="grid grid-cols-1 gap-6 mb-6 md:grid-cols-2 lg:grid-cols-4">
    <div v-for="(card, index) in statsCards" 
         :key="index"
         class="p-6 bg-white rounded-lg shadow"
    >
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm font-medium text-gray-600">{{ card.title }}</p>
          <p class="mt-1 text-2xl font-semibold text-gray-900">
            {{ card.value }}
          </p>
        </div>
        <div class="p-3 rounded-full bg-blue-50">
          <Icon 
            :name="card.icon" 
            class="w-6 h-6 text-blue-500"
          />
        </div>
      </div>
      <div class="mt-4">
        <p class="text-sm text-gray-500">
          {{ card.description }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

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
      value: totals.total_tokens.toLocaleString(),
      icon: 'ic:baseline-token',
      description: 'Tokens generados en el periodo'
    },
    {
      title: 'Total Horas',
      value: totals.total_hours?.toFixed(2) || '0',
      icon: 'ic:baseline-schedule',
      description: 'Horas trabajadas'
    },
    {
      title: 'Días Trabajados',
      value: totals.total_dias_asistidos || '0',
      icon: 'ic:baseline-calendar-today',
      description: 'Días con actividad registrada'
    },
    {
      title: 'Promedio Tokens/Día',
      value: ((totals.total_tokens || 0) / 
              (totals.total_dias_asistidos || 1)).toFixed(2),
      icon: 'ic:baseline-trending-up',
      description: 'Promedio diario de tokens'
    }
  ]
})
</script>