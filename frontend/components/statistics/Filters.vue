<template>
    <div class="p-6 bg-white border border-gray-100 shadow-lg rounded-xl">
        <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-800">
                <span class="flex items-center gap-2">
                    <Icon name="ph:funnel" class="w-5 h-5 text-blue-500" />
                    Filtros
                </span>
            </h3>
            <button @click="handleReset"
                class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-600 transition-colors duration-200 border border-gray-200 rounded-lg bg-gray-50 hover:bg-gray-100">
                <Icon name="ph:eraser" class="w-4 h-4" />
                Limpiar filtros
            </button>
        </div>

        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
            <!-- Año -->
            <div class="relative">
                <label class="block mb-2 text-sm font-medium text-gray-700">
                    <span class="flex items-center gap-2">
                        <Icon name="ph:calendar" class="w-4 h-4 text-gray-400" />
                        Año
                    </span>
                </label>
                <select v-model="filters.year" @change="handleYearChange" class="w-full pl-4 pr-10 py-2.5 bg-gray-50 border-gray-200 rounded-lg 
                               text-gray-700 cursor-pointer transition-all duration-200
                               hover:bg-gray-100 focus:border-blue-500 focus:ring-blue-500 focus:ring-1">
                    <option value="">Todos los años</option>
                    <option v-for="year in availableYears" :key="year" :value="year">
                        {{ year }}
                    </option>
                </select>
                <Icon name="ph:caret-down"
                    class="absolute w-4 h-4 text-gray-400 pointer-events-none right-3 bottom-3" />
            </div>

            <!-- Mes -->
            <div class="relative">
                <label class="block mb-2 text-sm font-medium text-gray-700">
                    <span class="flex items-center gap-2">
                        <Icon name="ph:clock" class="w-4 h-4 text-gray-400" />
                        Mes
                    </span>
                </label>
                <select v-model="filters.month" @change="handleMonthChange" :disabled="!filters.year" :class="[
                    'w-full pl-4 pr-10 py-2.5 border rounded-lg transition-all duration-200',
                    !filters.year
                        ? 'bg-gray-100 border-gray-200 text-gray-400 cursor-not-allowed'
                        : 'bg-gray-50 border-gray-200 text-gray-700 cursor-pointer hover:bg-gray-100',
                    'focus:border-blue-500 focus:ring-blue-500 focus:ring-1'
                ]">
                    <option value="">Todos los meses</option>
                    <option v-for="month in availableMonths" :key="month" :value="month">
                        {{ MONTH_NAMES[month] }}
                    </option>
                </select>
                <Icon name="ph:caret-down"
                    class="absolute w-4 h-4 text-gray-400 pointer-events-none right-3 bottom-3" />
            </div>

            <!-- Período -->
            <div class="relative">
                <label class="block mb-2 text-sm font-medium text-gray-700">
                    <span class="flex items-center gap-2">
                        <Icon name="ph:timer" class="w-4 h-4 text-gray-400" />
                        Período
                    </span>
                </label>
                <select v-model="filters.period" @change="handlePeriodChange" :disabled="!filters.month" :class="[
                    'w-full pl-4 pr-10 py-2.5 border rounded-lg transition-all duration-200',
                    !filters.month
                        ? 'bg-gray-100 border-gray-200 text-gray-400 cursor-not-allowed'
                        : 'bg-gray-50 border-gray-200 text-gray-700 cursor-pointer hover:bg-gray-100',
                    'focus:border-blue-500 focus:ring-blue-500 focus:ring-1'
                ]">
                    <option value="">Todos los períodos</option>
                    <option v-for="period in availablePeriods" :key="period" :value="period">
                        Período {{ period }}
                    </option>
                </select>
                <Icon name="ph:caret-down"
                    class="absolute w-4 h-4 text-gray-400 pointer-events-none right-3 bottom-3" />
            </div>
        </div>

        <!-- Indicador de filtros activos -->
        <div v-if="hasActiveFilters" class="pt-4 mt-4 border-t border-gray-100">
            <div class="flex flex-wrap items-center gap-2 text-sm text-gray-600">
                <span class="font-medium">Filtros activos:</span>
                <div v-if="filters.year" class="flex items-center gap-1 px-2 py-1 text-blue-700 rounded-md bg-blue-50">
                    <span>{{ filters.year }}</span>
                </div>
                <div v-if="filters.month" class="flex items-center gap-1 px-2 py-1 text-blue-700 rounded-md bg-blue-50">
                    <span>{{ MONTH_NAMES[filters.month] }}</span>
                </div>
                <div v-if="filters.period"
                    class="flex items-center gap-1 px-2 py-1 text-blue-700 rounded-md bg-blue-50">
                    <span>Período {{ filters.period }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const MONTH_NAMES = {
    'JAN': 'Enero', 'FEB': 'Febrero', 'MAR': 'Marzo', 'APR': 'Abril',
    'MAY': 'Mayo', 'JUN': 'Junio', 'JUL': 'Julio', 'AUG': 'Agosto',
    'SEP': 'Septiembre', 'OCT': 'Octubre', 'NOV': 'Noviembre', 'DEC': 'Diciembre'
};

const props = defineProps({
    availableYears: {
        type: Array,
        default: () => []
    },
    availableMonths: {
        type: Array,
        default: () => []
    },
    availablePeriods: {
        type: Array,
        default: () => []
    }
});

const emit = defineEmits(['update:filters', 'reset']);

const filters = ref({
    year: '',
    month: '',
    period: ''
});

const hasActiveFilters = computed(() => {
    return filters.value.year || filters.value.month || filters.value.period;
});

const handleYearChange = () => {
    if (!filters.value.year) {
        filters.value.month = '';
        filters.value.period = '';
    }
    emit('update:filters', { ...filters.value });
};

const handleMonthChange = () => {
    if (!filters.value.month) {
        filters.value.period = '';
    }
    emit('update:filters', { ...filters.value });
};

const handlePeriodChange = () => {
    emit('update:filters', { ...filters.value });
};

const handleReset = () => {
    filters.value = {
        year: '',
        month: '',
        period: ''
    };
    emit('reset');
};
</script>