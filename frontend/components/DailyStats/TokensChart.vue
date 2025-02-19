<template>
  <div class="p-6 transition-all duration-200 bg-white rounded-lg shadow-lg hover:shadow-xl">
    <!-- Header Section -->
    <div class="flex items-center justify-between mb-6">
      <div class="space-y-1">
        <h3 class="text-xl font-semibold text-gray-800">Total de Tokens por Día</h3>
        <p class="text-sm text-gray-500">Visualización del consumo diario de tokens</p>
      </div>
      
      <!-- Controls Section -->
      <div class="flex items-center gap-3">
        <button 
          v-if="selectedDate"
          @click="$emit('update:selectedDate', null)"
          class="flex items-center px-3 py-1.5 text-sm text-gray-600 bg-gray-100 rounded-full transition-colors hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          {{ formatDate(selectedDate) }}
          <Icon name="ic:baseline-close" class="w-4 h-4 ml-1.5 text-gray-500" />
        </button>
        
        <!-- Período Selector -->
        <select 
          v-model="selectedPeriod" 
          class="px-3 py-1.5 text-sm bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="90">Total periodo</option>
        </select>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-3 gap-4 mb-6">
      <div class="p-4 rounded-lg bg-blue-50">
        <p class="text-sm font-medium text-blue-600">Total Tokens</p>
        <p class="text-2xl font-semibold text-blue-700">{{ totalTokens.toLocaleString() }}</p>
      </div>      
      <div class="p-4 rounded-lg bg-green-50">
        <p class="text-sm font-medium text-green-600">Día Pico</p>
        <p class="text-2xl font-semibold text-green-700">{{ peakTokens.toLocaleString() }}</p>
      </div>
          <div class="p-4 rounded-lg bg-red-50">
        <p class="text-sm font-medium text-red-600">Día valle</p>
        <p class="text-2xl font-semibold text-red-700">{{ bottomTokens.toLocaleString() }}</p>
      </div>
    </div>

    <!-- Chart -->
    <div class="relative">
      <div v-if="loading" class="absolute inset-0 z-10 flex items-center justify-center bg-white bg-opacity-75">
        <div class="w-8 h-8 border-b-2 border-blue-500 rounded-full animate-spin"></div>
      </div>
      
      <apexchart
        type="bar"
        height="350"
        :options="chartOptions"
        :series="chartSeries"
        @mounted="loading = false"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { toast } from 'vue-sonner'

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  selectedDate: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['update:selectedDate'])

// Estado
const loading = ref(true)
const selectedPeriod = ref('90')

// Funciones auxiliares
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Computados para estadísticas
const processedData = computed(() => {
  if (!props.data) return []
  
  const dailyTotals = new Map()
  
  Object.values(props.data).forEach(pageData => {
    Object.values(pageData).forEach(week => {
      Object.entries(week.tokens_por_dia).forEach(([date, tokens]) => {
        const currentTotal = dailyTotals.get(date) || 0
        dailyTotals.set(date, currentTotal + tokens)
      })
    })
  })
  
  return Array.from(dailyTotals.entries())
    .map(([date, total]) => ({
      x: new Date(date).getTime(),
      y: total
    }))
    .sort((a, b) => a.x - b.x)
})

const filteredData = computed(() => {
  if (selectedPeriod.value === 'all') return processedData.value
  
  const cutoffDate = new Date()
  cutoffDate.setDate(cutoffDate.getDate() - parseInt(selectedPeriod.value))
  
  return processedData.value.filter(item => item.x >= cutoffDate.getTime())
})

const totalTokens = computed(() => 
  filteredData.value.reduce((sum, item) => sum + item.y, 0)
)

const averageTokens = computed(() => 
  Math.round(totalTokens.value / filteredData.value.length)
)

const peakTokens = computed(() => 
  Math.max(...filteredData.value.map(item => item.y))
)

const bottomTokens = computed(() => {
  const nonZeroValues = filteredData.value.map(item => item.y).filter(y => y !== 0);
  return nonZeroValues.length > 0 ? Math.min(...nonZeroValues) : 0; // o algún valor por defecto
});

// Configuración del gráfico
const chartOptions = computed(() => ({
  chart: {
    type: 'bar',
    toolbar: {
      show: true,
      tools: {
        download: true,
        selection: true,
        zoom: true,
        zoomin: true,
        zoomout: true,
        pan: true,
      }
    },
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
    events: {
      dataPointSelection: function(event, chartContext, config) {
        const timestamp = config.w.globals.seriesX[config.seriesIndex][config.dataPointIndex]
        const date = new Date(timestamp)
        const formattedDate = date.toISOString().split('T')[0]
        emit('update:selectedDate', formattedDate)
        
        // Notificación con Sonner
        toast.success(`Seleccionado: ${formatDate(formattedDate)}`, {
          description: `Total de tokens: ${config.w.globals.series[config.seriesIndex][config.dataPointIndex].toLocaleString()}`
        })
      }
    }
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '60%',
      borderRadius: 4,
      dataLabels: {
        position: 'top'
      }
    },
  },
  dataLabels: {
    enabled: true,
    formatter: (val) => val.toLocaleString(),
    offsetY: -20,
    style: {
      fontSize: '10px',
      colors: ['#304758'],
      fontWeight: '600'
    }
  },
  xaxis: {
    type: 'datetime',
    labels: {
      format: 'dd/MMM',
      style: {
        colors: '#64748b',
        fontSize: '12px'
      },
      datetimeFormatter: {
        year: 'yyyy',
        month: 'MMM',
        day: 'dd MMM',
      }
    },
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    }
  },
  yaxis: {
    title: {
      text: 'Tokens',
      style: {
        fontSize: '13px',
        fontWeight: '500',
        color: '#64748b'
      }
    },
    labels: {
      formatter: (value) => value.toLocaleString(),
      style: {
        colors: '#64748b',
        fontSize: '12px'
      }
    }
  },
  tooltip: {
    y: {
      formatter: (value) => value.toLocaleString() + ' tokens'
    },
    x: {
      format: 'dd MMM yyyy'
    },
    theme: 'light',
    style: {
      fontSize: '12px'
    }
  },
  colors: ['#3B82F6'],
  fill: {
    opacity: 0.9,
    type: 'gradient',
    gradient: {
      shade: 'light',
      type: 'vertical',
      shadeIntensity: 0.1,
      opacityFrom: 0.9,
      opacityTo: 0.6,
    }
  },
  grid: {
    borderColor: '#f1f5f9',
    strokeDashArray: 4,
    xaxis: {
      lines: {
        show: true
      }
    }
  },
  states: {
    hover: {
      filter: {
        type: 'darken',
        value: 0.1
      }
    },
    active: {
      allowMultipleDataPointsSelection: false,
      filter: {
        type: 'none'
      }
    }
  }
}))

const chartSeries = computed(() => [{
  name: 'Total Tokens',
  data: filteredData.value
}])

// Watchers
watch(selectedPeriod, () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 500)
})
</script>