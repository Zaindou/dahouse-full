// components/DailyStats/DistributionChart.vue
<template>
  <div class="p-6 bg-white rounded-lg shadow">
    <div class="flex items-center justify-between mb-4">
      <div>
        <h3 class="text-lg font-semibold">Distribución por Página</h3>
        <div class="mt-1 text-sm text-gray-500">
          <template v-if="data.filtered_nickname !== 'All Models'">
            <span class="font-medium">Modelo:</span> {{ data.filtered_nickname }}
          </template>
          <template v-if="data.filtered_date !== 'Full Period'">
            <span class="ml-2 font-medium">Fecha:</span> {{ formatDate(data.filtered_date) }}
          </template>
        </div>
      </div>
      <div class="text-sm text-gray-500">
        Total: {{ totalTokens.toLocaleString() }} tokens
      </div>
    </div>
    
    <div class="grid grid-cols-1 gap-6">
      <!-- Gráfica de Pie -->
      <div class="h-[300px]">
        <apexchart
          type="pie"
          height="100%"
          :options="chartOptions"
          :series="chartSeries"
        />
      </div>
      
      <!-- Detalles por página -->
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div 
          v-for="(data, page) in distribution" 
          :key="page"
          class="flex items-center justify-between p-3 border border-gray-100 rounded bg-gray-50"
        >
          <div class="flex items-center space-x-2">
            <div 
              class="w-3 h-3 rounded-full"
              :style="{ backgroundColor: getPageColor(page) }"
            ></div>
            <span class="font-medium">{{ page }}</span>
          </div>
          <div class="text-right">
            <div class="font-semibold">{{ data.tokens.toLocaleString() }}</div>
            <div class="text-sm text-gray-500">{{ data.percentage }}%</div>
          </div>
        </div>
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

// Colores para cada página
const pageColors = {
  'Chaturbate': '#f5a142',
  'Stripchat': '#b83737',
  'Streamate': '#2b20bd',
  'Camsoda': '#11d5f7'
}

// Función para obtener el color de cada página
const getPageColor = (page) => pageColors[page] || '#808080'

// Función para formatear la fecha
const formatDate = (dateString) => {
  if (!dateString || dateString === 'Full Period') return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Datos computados
const distribution = computed(() => props.data.earnings_distribution || {})
const totalTokens = computed(() => props.data.total_tokens || 0)

// Configuración del gráfico
const chartOptions = computed(() => ({
  chart: {
    type: 'pie',
    animations: {
      enabled: true,
      speed: 500,
      animateGradually: {
        enabled: true,
        delay: 150
      },
      dynamicAnimation: {
        enabled: true,
        speed: 350
      }
    }
  },
  colors: Object.values(pageColors),
  labels: Object.keys(distribution.value),
  legend: {
    position: 'bottom',
    horizontalAlign: 'center',
    floating: false,
    fontSize: '14px',
    formatter: function(seriesName, opts) {
      const value = opts.w.globals.series[opts.seriesIndex]
      const percentage = ((value / totalTokens.value) * 100).toFixed(1)
      return `${seriesName}: ${percentage}%`
    }
  },
  tooltip: {
    y: {
      formatter: (value) => {
        const percentage = ((value / totalTokens.value) * 100).toFixed(1)
        return `${value.toLocaleString()} tokens (${percentage}%)`
      }
    }
  },
  plotOptions: {
    pie: {
      dataLabels: {
        enabled: true,
        formatter: function(val, opts) {
          return `${val.toFixed(1)}%`
        }
      },
      donut: {
        size: '65%'
      }
    }
  },
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        height: 300
      },
      legend: {
        position: 'bottom'
      }
    }
  }],
  states: {
    hover: {
      filter: {
        type: 'none'
      }
    },
    active: {
      filter: {
        type: 'none'
      }
    }
  }
}))

const chartSeries = computed(() => {
  if (!distribution.value) return []
  return Object.values(distribution.value).map(item => item.tokens)
})
</script>