<!-- components/DailyStats/Filters.vue -->
<template>
  <div class="p-4 mb-6 transition-shadow bg-white rounded-lg shadow hover:shadow-md">
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
            @change="$emit('update:periodo', $event.target.value)"
            class="w-full py-2 pl-4 pr-10 transition-colors border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50 hover:border-gray-400"
          >
            <option v-for="mes in meses" :key="mes" :value="mes">
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
            @change="$emit('update:subperiodo', $event.target.value)"
            class="w-full py-2 pl-4 pr-10 transition-colors border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50 hover:border-gray-400"
          >
            <option value="">Todo el mes</option>
            <option value="periodo_1">Periodo 1 (Semanas 1 y 2)</option>
            <option value="periodo_2">Periodo 2 (Semanas 3 y 4)</option>
          </select>
          <Icon name="ph:caret-down" class="absolute w-4 h-4 text-gray-400 -translate-y-1/2 pointer-events-none right-3 top-1/2" />
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
            @change="$emit('update:modelo', $event.target.value)"
            class="w-full py-2 pl-4 pr-10 transition-colors border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500 focus:ring-opacity-50 hover:border-gray-400"
          >
            <option value="">Todos los modelos</option>
            <option v-for="modelo in modelos" :key="modelo" :value="modelo">
              {{ modelo }}
            </option>
          </select>
          <Icon name="ph:caret-down" class="absolute w-4 h-4 text-gray-400 -translate-y-1/2 pointer-events-none right-3 top-1/2" />
        </div>
      </div>

      <!-- Botón Reset -->
      <div v-if="modelo || subperiodo" class="flex items-end">
        <button 
          @click="$emit('update:modelo', ''); $emit('update:subperiodo', '')"
          class="flex items-center gap-2 px-3 py-2 text-sm text-gray-500 transition-colors hover:text-gray-700"
          type="button"
        >
          <Icon name="ph:eraser" class="w-4 h-4" />
          Limpiar filtros
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useEarningsStore } from '~/stores/earnings'

const store = useEarningsStore()

const props = defineProps({
  periodo: { type: String, required: true },
  subperiodo: { type: String, default: '' },
  modelo: { type: String, default: '' }
})

defineEmits(['update:periodo', 'update:subperiodo', 'update:modelo'])

const meses = computed(() => store.meses)
const modelos = computed(() => store.modelos)

const formatearMes = (mes) => {
  const [year, month] = mes.split('-')
  return `${month} ${year}`
}
</script>
