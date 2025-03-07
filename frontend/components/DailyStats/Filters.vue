<!-- components/DailyStats/Filters.vue -->
<template>
  <div 
    class="p-4 mb-6 transition-all duration-300 bg-white rounded-lg shadow hover:shadow-md"
    :class="{'ring-2 ring-blue-300': hasActiveFilters}"
  >
    <!-- Título y acciones rápidas -->
    <div class="flex flex-wrap items-center justify-between mb-4">
      <h3 class="text-lg font-medium text-gray-700">Filtros</h3>
      
      <div class="flex flex-wrap gap-2 mt-2 sm:mt-0">
        <button 
          @click="selectCurrentMonth"
          class="px-3 py-1.5 text-xs font-medium text-gray-600 transition-colors bg-gray-100 rounded-md hover:bg-gray-200"
          :class="{'bg-blue-100 text-blue-700': isPeriodoActual}"
          type="button"
          aria-label="Seleccionar mes actual"
        >
          <span class="flex items-center gap-1">
            <Icon name="ph:calendar-dot" class="w-3.5 h-3.5" />
            Mes actual
          </span>
        </button>
        
        <button 
          @click="selectPreviousMonth"
          class="px-3 py-1.5 text-xs font-medium text-gray-600 transition-colors bg-gray-100 rounded-md hover:bg-gray-200"
          :class="{'bg-blue-100 text-blue-700': isPeriodoAnterior}"
          type="button"
          aria-label="Seleccionar mes anterior"
        >
          <span class="flex items-center gap-1">
            <Icon name="ph:calendar-blank" class="w-3.5 h-3.5" />
            Mes anterior
          </span>
        </button>
      </div>
    </div>

    <div class="flex flex-wrap gap-4">
      
      <!-- Selección de Mes -->
      <div class="flex-1 min-w-[200px]">
        <label for="periodo" class="block mb-2 text-sm font-medium text-gray-700">
          Mes
        </label>
        <div class="relative">
          <select 
            id="periodo"
            :value="periodo"
            @change="handlePeriodChange($event.target.value)"
            class="w-full py-2 pl-4 pr-10 transition-colors border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50 hover:border-gray-400"
            aria-label="Seleccionar mes"
          >
            <option v-for="mes in mesesOrdenados" :key="mes" :value="mes">
              {{ formatearMes(mes) }}
            </option>
          </select>
          <Icon name="ph:caret-down" class="absolute w-4 h-4 text-gray-400 -translate-y-1/2 pointer-events-none right-3 top-1/2" />
        </div>
      </div>

      <!-- Selección de Periodo -->
      <div class="flex-1 min-w-[200px]">
        <label for="subperiodo" class="block mb-2 text-sm font-medium text-gray-700">
          Periodo
        </label>
        <div class="relative">
          <select 
            id="subperiodo"
            :value="subperiodo"
            @change="$emit('update:subperiodo', $event.target.value); saveFilters()"
            class="w-full py-2 pl-4 pr-10 transition-colors border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50 hover:border-gray-400"
            :class="{'border-blue-500 bg-blue-50': subperiodo}"
            aria-label="Seleccionar periodo"
          >
            <option value="">Todo el mes</option>
            <option value="periodo_1">Periodo 1 (Semanas 1 y 2)</option>
            <option value="periodo_2">Periodo 2 (Semanas 3 y 4)</option>
          </select>
          <Icon name="ph:caret-down" class="absolute w-4 h-4 text-gray-400 -translate-y-1/2 pointer-events-none right-3 top-1/2" />
          <Icon v-if="subperiodo" name="ph:check-circle-fill" class="absolute w-4 h-4 text-blue-500 -translate-y-1/2 right-8 top-1/2" />
        </div>
      </div>

      <!-- Selección de Modelo -->
      <div class="flex-1 min-w-[200px]">
        <label for="modelo" class="block mb-2 text-sm font-medium text-gray-700">
          Modelo
        </label>
        <div class="relative">
          <select 
            id="modelo"
            :value="modelo"
            @change="$emit('update:modelo', $event.target.value); saveFilters()"
            class="w-full py-2 pl-4 pr-10 transition-colors border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50 hover:border-gray-400"
            :class="{'border-blue-500 bg-blue-50': modelo}"
            aria-label="Seleccionar modelo"
          >
            <option value="">Todos los modelos</option>
            <option v-for="modeloItem in modelos" :key="modeloItem" :value="modeloItem">
              {{ modeloItem }}
            </option>
          </select>
          <Icon name="ph:caret-down" class="absolute w-4 h-4 text-gray-400 -translate-y-1/2 pointer-events-none right-3 top-1/2" />
          <Icon v-if="modelo" name="ph:check-circle-fill" class="absolute w-4 h-4 text-blue-500 -translate-y-1/2 right-8 top-1/2" />
        </div>
      </div>

      <!-- Botón Reset -->
      <div class="flex items-end">
        <transition name="fade">
          <button 
            v-if="hasActiveFilters"
            @click="resetFilters"
            class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white transition-colors bg-blue-600 rounded-lg hover:bg-blue-700"
            type="button"
            aria-label="Limpiar todos los filtros"
          >
            <Icon name="ph:eraser" class="w-4 h-4" />
            Limpiar filtros
          </button>
        </transition>
      </div>
    </div>
    
    <!-- Resumen de filtros activos -->
    <transition name="fade">
      <div v-if="hasActiveFilters" class="flex flex-wrap gap-2 pt-4 mt-4 border-t border-gray-100">
        <div class="text-sm text-gray-500">Filtros activos:</div>
        <div v-if="subperiodo" class="px-2 py-0.5 text-xs font-medium text-blue-800 bg-blue-100 rounded-full">
          {{ subperiodo === 'periodo_1' ? 'Periodo 1' : 'Periodo 2' }}
          <button @click="$emit('update:subperiodo', ''); saveFilters()" class="ml-1 text-blue-500 hover:text-blue-700">
            <Icon name="ph:x-bold" class="w-3 h-3" />
          </button>
        </div>
        <div v-if="modelo" class="px-2 py-0.5 text-xs font-medium text-blue-800 bg-blue-100 rounded-full">
          {{ modelo }}
          <button @click="$emit('update:modelo', ''); saveFilters()" class="ml-1 text-blue-500 hover:text-blue-700">
            <Icon name="ph:x-bold" class="w-3 h-3" />
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useEarningsStore } from '~/stores/earnings'

const store = useEarningsStore()
const isLoading = ref(false)

const props = defineProps({
  periodo: { type: String, required: true },
  subperiodo: { type: String, default: '' },
  modelo: { type: String, default: '' }
})

const emit = defineEmits(['update:periodo', 'update:subperiodo', 'update:modelo'])

// Definición de meses y su orden
const MONTH_CODES = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
const MONTH_NAMES = {
    'JAN': 'Enero', 'FEB': 'Febrero', 'MAR': 'Marzo', 'APR': 'Abril',
    'MAY': 'Mayo', 'JUN': 'Junio', 'JUL': 'Julio', 'AUG': 'Agosto',
    'SEP': 'Septiembre', 'OCT': 'Octubre', 'NOV': 'Noviembre', 'DEC': 'Diciembre'
}

// Meses disponibles del store
const meses = computed(() => store.meses)
const modelos = computed(() => store.modelos)

// Verificar si hay filtros activos
const hasActiveFilters = computed(() => props.modelo || props.subperiodo)

// Ordenar meses de más reciente a más antiguo
const mesesOrdenados = computed(() => {
  return [...meses.value].sort((a, b) => {
    // Separar año y mes
    const [yearA, monthA] = a.split('-')
    const [yearB, monthB] = b.split('-')
    
    // Comparar primero por año
    if (yearA !== yearB) {
      return parseInt(yearB) - parseInt(yearA)
    }
    
    // Si el año es igual, comparar por mes
    return MONTH_CODES.indexOf(monthB) - MONTH_CODES.indexOf(monthA)
  })
})

// Función para formatear el mes utilizando MONTH_NAMES
const formatearMes = (mes) => {
  if (!mes) return ''
  
  const [year, monthCode] = mes.split('-')
  return `${MONTH_NAMES[monthCode]} ${year}`
}

// Función para obtener el mes actual en formato 'YYYY-MMM'
const obtenerMesActual = () => {
  const fecha = new Date()
  const year = fecha.getFullYear()
  const monthIndex = fecha.getMonth()
  return `${year}-${MONTH_CODES[monthIndex]}`
}

// Función para obtener el mes anterior en formato 'YYYY-MMM'
const obtenerMesAnterior = () => {
  const fecha = new Date()
  fecha.setMonth(fecha.getMonth() - 1)
  const year = fecha.getFullYear()
  const monthIndex = fecha.getMonth()
  return `${year}-${MONTH_CODES[monthIndex]}`
}

// Verificar si el periodo actual es el mes actual
const isPeriodoActual = computed(() => {
  return props.periodo === obtenerMesActual()
})

// Verificar si el periodo actual es el mes anterior
const isPeriodoAnterior = computed(() => {
  return props.periodo === obtenerMesAnterior()
})

// Función para encontrar el mes más cercano disponible
const encontrarMesMasCercano = () => {
  const hoy = new Date()
  const mesMasCercano = { mes: null, diferencia: Infinity }
  
  meses.value.forEach(mes => {
    const [year, monthCode] = mes.split('-')
    const monthIndex = MONTH_CODES.indexOf(monthCode)
    const fechaMes = new Date(parseInt(year), monthIndex, 1)
    
    // Calcular diferencia absoluta en milisegundos
    const diferencia = Math.abs(fechaMes.getTime() - hoy.getTime())
    
    if (diferencia < mesMasCercano.diferencia) {
      mesMasCercano.mes = mes
      mesMasCercano.diferencia = diferencia
    }
  })
  
  return mesMasCercano.mes
}

// Función para seleccionar el mes actual
const selectCurrentMonth = () => {
  const mesActual = obtenerMesActual()
  if (meses.value.includes(mesActual)) {
    emit('update:periodo', mesActual)
    saveFilters()
  }
}

// Función para seleccionar el mes anterior
const selectPreviousMonth = () => {
  const mesAnterior = obtenerMesAnterior()
  if (meses.value.includes(mesAnterior)) {
    emit('update:periodo', mesAnterior)
    saveFilters()
  }
}

// Función para manejar el cambio de periodo con efectos visuales
const handlePeriodChange = (value) => {
  isLoading.value = true
  emit('update:periodo', value)
  saveFilters()
  // Simular tiempo de carga para feedback visual
  setTimeout(() => {
    isLoading.value = false
  }, 300)
}

// Función para resetear todos los filtros
const resetFilters = () => {
  emit('update:modelo', '')
  emit('update:subperiodo', '')
  saveFilters()
}

// Guardar filtros en localStorage
const saveFilters = () => {
  if (process.client) {
    localStorage.setItem('dailyStatsFilters', JSON.stringify({
      periodo: props.periodo,
      subperiodo: props.subperiodo,
      modelo: props.modelo
    }))
  }
}

// Cargar filtros guardados
const loadSavedFilters = () => {
  if (process.client) {
    try {
      const savedFilters = JSON.parse(localStorage.getItem('dailyStatsFilters'))
      if (savedFilters) {
        // Solo aplicar si el periodo guardado existe en los meses disponibles
        if (savedFilters.periodo && meses.value.includes(savedFilters.periodo)) {
          emit('update:periodo', savedFilters.periodo)
        }
        
        if (savedFilters.subperiodo) {
          emit('update:subperiodo', savedFilters.subperiodo)
        }
        
        if (savedFilters.modelo && modelos.value.includes(savedFilters.modelo)) {
          emit('update:modelo', savedFilters.modelo)
        }
        
        return savedFilters.periodo && meses.value.includes(savedFilters.periodo)
      }
    } catch (e) {
      console.error('Error al cargar filtros guardados', e)
    }
    return false
  }
  return false
}

// Inicialización: cargar filtros guardados o seleccionar mes inteligente
onMounted(() => {
  if (meses.value.length > 0 && !props.periodo) {
    // Intentar cargar filtros guardados primero
    const filtrosCargados = loadSavedFilters()
    
    // Si no hay filtros guardados, seleccionar mes inteligente
    if (!filtrosCargados) {
      const mesActual = obtenerMesActual()
      const mesAnterior = obtenerMesAnterior()
      
      // Intentar seleccionar mes actual
      if (meses.value.includes(mesActual)) {
        emit('update:periodo', mesActual)
      }
      // Intentar seleccionar mes anterior
      else if (meses.value.includes(mesAnterior)) {
        emit('update:periodo', mesAnterior)
      }
      // Seleccionar el mes más cercano a la fecha actual
      else {
        const mesMasCercano = encontrarMesMasCercano()
        emit('update:periodo', mesMasCercano || mesesOrdenados.value[0])
      }
      
      // Guardar la selección inicial
      saveFilters()
    }
  }
})

// Estilos para transiciones
const styles = `
<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
`
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>