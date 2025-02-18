<!-- components/DailyStats/DistributionChart.vue -->
<template>
  <div class="p-6 transition-all duration-300 bg-white shadow-lg rounded-xl">
    <!-- Header Section -->
    <div class="flex flex-col justify-between gap-4 mb-4 md:flex-row md:items-center">
      <div class="space-y-2">
        <div class="flex items-center gap-2">
          <Icon name="ph:chart-pie-slice-bold" class="w-6 h-6 text-blue-600" />
          <h3 class="text-xl font-bold text-gray-900">Distribución por Página</h3>
        </div>
        <div class="flex flex-wrap gap-3 text-sm text-gray-600">
          <template v-if="data.filtered_nickname !== 'All Models'">
            <div class="flex items-center gap-1">
              <Icon name="ph:user-circle" class="w-4 h-4" />
              <span class="font-medium">{{ data.filtered_nickname }}</span>
            </div>
          </template>
          <template v-if="data.filtered_date !== 'Full Period'">
            <div class="flex items-center gap-1">
              <Icon name="ph:calendar" class="w-4 h-4" />
              <span>{{ formatDate(data.filtered_date) }}</span>
            </div>
          </template>
        </div>
      </div>
      <div class="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-50">
        <Icon name="ph:coins" class="w-5 h-5 text-blue-500" />
        <div class="text-sm">
          <span class="text-gray-500">Total:</span>
          <span class="ml-1 font-bold text-gray-900">
            {{ totalTokens.toLocaleString() }} tokens
          </span>
        </div>
      </div>
    </div>
    
    <div class="grid gap-6 md:grid-cols-5">
      <!-- Chart Section -->
      <div class="md:col-span-3">
        <div class="h-[400px] bg-gray-50 rounded-lg p-4">
          <apexchart
            type="pie"
            height="100%"
            :options="chartOptions"
            :series="chartSeries"
          />
        </div>
      </div>
      
      <!-- Details Section -->
      <div class="space-y-4 md:col-span-2">
<!-- "        <div class="mb-2 text-sm font-medium text-gray-600">
          Desglose Detallado
        </div>" -->
        <div class="space-y-3">
          <div 
            v-for="item in sortedDistribution" 
            :key="item.page"
            class="flex items-center justify-between p-4 transition-all duration-200 rounded-lg bg-gray-50 hover:shadow-md"
          >
            <div class="flex items-center gap-3">
              <div 
                class="w-4 h-4 rounded-full"
                :style="{ backgroundColor: getPageColor(item.page) }"
              ></div>
              <div class="space-y-1">
                <span class="font-medium text-gray-900">{{ item.page }}</span>
                <div class="text-xs text-gray-500">
                  {{ item.percentage }}% del total
                </div>
              </div>
            </div>
            <div class="text-right">
              <div class="font-bold text-gray-900">
                {{ item.tokens.toLocaleString() }}
              </div>
              <div class="text-xs text-gray-500">tokens</div>
            </div>
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
  'Chaturbate': '#f09711',  // Blue
  'Stripchat': '#c9240a',   // Red
  'Streamate': '#0356fc',   // Green
  'Camsoda': '#22f2eb',     // Yellow
  'Bongacams': '#de3159',   // Purple
}

const getPageColor = (page) => pageColors[page] || '#CBD5E1'

const formatDate = (dateString) => {
  if (!dateString || dateString === 'Full Period') return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const distribution = computed(() => props.data.earnings_distribution || {})
const totalTokens = computed(() => props.data.total_tokens || 0)

// Ordenar la distribución por tokens (de mayor a menor)
const sortedDistribution = computed(() => {
  const distributionArray = Object.entries(distribution.value).map(([page, data]) => ({
    page,
    tokens: data.tokens,
    percentage: data.percentage
  }))
  
  return distributionArray.sort((a, b) => b.tokens - a.tokens)
})

// Obtener las etiquetas y series ordenadas para el gráfico
const sortedLabels = computed(() => sortedDistribution.value.map(item => item.page))
const sortedSeries = computed(() => sortedDistribution.value.map(item => item.tokens))

const chartOptions = computed(() => ({
  chart: {
    type: 'pie',
    fontFamily: 'Inter, sans-serif',
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
    },
    background: 'transparent'
  },
  colors: sortedLabels.value.map(page => getPageColor(page)),
  labels: sortedLabels.value,
  legend: {
    position: 'bottom',
    horizontalAlign: 'center',
    floating: false,
    fontSize: '14px',
    labels: {
      colors: '#64748b'
    },
    markers: {
      width: 12,
      height: 12,
      radius: 6
    },
    formatter: function(seriesName, opts) {
      const value = opts.w.globals.series[opts.seriesIndex]
      const percentage = ((value / totalTokens.value) * 100).toFixed(1)
      return `${seriesName}: ${percentage}%`
    }
  },
  tooltip: {
    enabled: true,
    theme: 'light',
    y: {
      formatter: (value) => {
        const percentage = ((value / totalTokens.value) * 100).toFixed(1)
        return `${value.toLocaleString()} tokens (${percentage}%)`
      }
    }
  },
  plotOptions: {
    pie: {
      expandOnClick: false,
      dataLabels: {
        enabled: true,
        formatter: function(val, opts) {
          return `${val.toFixed(1)}%`
        },
        style: {
          fontSize: '14px',
          fontFamily: 'Inter, sans-serif',
          fontWeight: 600
        }
      },
      donut: {
        size: '65%',
        labels: {
          show: false
        }
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
        position: 'bottom',
        fontSize: '12px'
      }
    }
  }],
  states: {
    hover: {
      filter: {
        type: 'darken',
        value: 0.1
      }
    },
    active: {
      filter: {
        type: 'darken',
        value: 0.1
      }
    }
  },
  stroke: {
    width: 2,
    colors: ['#fff']
  }
}))

const chartSeries = computed(() => sortedSeries.value)
</script>