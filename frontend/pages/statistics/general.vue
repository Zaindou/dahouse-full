<template>
    <NuxtLayout>
        <div class="min-h-screen p-4 bg-gradient-to-br from-gray-50 to-gray-100 sm:p-6 lg:p-8">
            <!-- Skeleton Loading State -->
            <DashboardSkeleton v-if="loading" />

            <!-- Error State -->
            <div v-else-if="error"
                class="p-4 mb-4 border border-red-200 rounded-xl bg-red-50/80 backdrop-blur-sm sm:p-6 sm:mb-6">
                <div class="flex items-center gap-3">
                    <Icon name="uil:exclamation-circle" class="w-5 h-5 text-red-500 sm:w-6 sm:h-6" />
                    <p class="text-sm text-red-700 sm:text-base">{{ error }}</p>
                </div>
            </div>

            <template v-else>
                <!-- Filters -->
                <DashboardFilters :available-years="store.availableYears" :available-months="store.availableMonths"
                    :available-periods="store.availablePeriods" @update:filters="handleFiltersUpdate"
                    @reset="handleFiltersReset"
                    class="p-4 mb-6 border shadow-md bg-white/80 backdrop-blur-lg rounded-xl border-gray-100/50 sm:p-6 sm:mb-8 sm:rounded-2xl" />

                <!-- Summary Cards -->
                <div class="grid grid-cols-1 gap-4 mb-6 sm:grid-cols-2 lg:grid-cols-4 sm:gap-6 sm:mb-8">
                    <!-- Ganancia Bruta Total -->
                    <div
                        class="p-4 transition-all duration-300 transform border border-gray-100 shadow-sm group bg-white/90 backdrop-blur-sm rounded-xl sm:p-6 sm:rounded-2xl hover:shadow-xl hover:-translate-y-1">
                        <div class="flex items-center justify-between">
                            <h3 class="text-xs font-medium text-gray-600 sm:text-sm">Ganancia Bruta Total</h3>
                            <div
                                class="flex items-center justify-center w-8 h-8 transition-colors duration-300 bg-green-100 rounded-full sm:w-10 sm:h-10 group-hover:bg-green-200">
                                <Icon name="uil:money-bill" class="w-5 h-5 text-green-600 sm:w-6 sm:h-6" />
                            </div>
                        </div>
                        <p class="mt-3 text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl sm:mt-4">
                            {{ formatCurrency(totalGananciaBruta) }}
                        </p>
                        <div class="flex items-center mt-2 text-xs sm:text-sm">
                            <span :class="[
                                tendenciaGananciaBruta > 0 ? 'text-green-500' : 'text-red-500',
                                'font-medium flex items-center'
                            ]">
                                <Icon :name="tendenciaGananciaBruta > 0 ? 'uil:arrow-up' : 'uil:arrow-down'"
                                    class="w-3 h-3 mr-1 sm:w-4 sm:h-4" />
                                {{ Math.abs(tendenciaGananciaBruta).toFixed(1) }}%
                            </span>
                            <span class="ml-2 text-gray-500">vs periodo anterior</span>
                        </div>
                    </div>

                    <!-- Total Tokens -->
                    <div
                        class="p-4 transition-all duration-300 transform border border-gray-100 shadow-sm group bg-white/90 backdrop-blur-sm rounded-xl sm:p-6 sm:rounded-2xl hover:shadow-xl hover:-translate-y-1">
                        <div class="flex items-center justify-between">
                            <h3 class="text-xs font-medium text-gray-600 sm:text-sm">Total Tokens</h3>
                            <div
                                class="flex items-center justify-center w-8 h-8 transition-colors duration-300 bg-blue-100 rounded-full sm:w-10 sm:h-10 group-hover:bg-blue-200">
                                <Icon name="ph:coins" class="w-5 h-5 text-blue-600 sm:w-6 sm:h-6" />
                            </div>
                        </div>
                        <p class="mt-3 text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl sm:mt-4">
                            {{ formatNumber(totalTokens) }}
                        </p>
                        <div class="flex items-center mt-2 text-xs sm:text-sm">
                            <span :class="[
                                tendenciaTokens > 0 ? 'text-green-500' : 'text-red-500',
                                'font-medium flex items-center'
                            ]">
                                <Icon :name="tendenciaTokens > 0 ? 'uil:arrow-up' : 'uil:arrow-down'"
                                    class="w-3 h-3 mr-1 sm:w-4 sm:h-4" />
                                {{ Math.abs(tendenciaTokens).toFixed(1) }}%
                            </span>
                            <span class="ml-2 text-gray-500">vs periodo anterior</span>
                        </div>
                    </div>

                    <!-- Ganancia Modelos -->
                    <div
                        class="p-4 transition-all duration-300 transform border border-gray-100 shadow-sm group bg-white/90 backdrop-blur-sm rounded-xl sm:p-6 sm:rounded-2xl hover:shadow-xl hover:-translate-y-1">
                        <div class="flex items-center justify-between">
                            <h3 class="text-xs font-medium text-gray-600 sm:text-sm">Ganancia Modelos</h3>
                            <div
                                class="flex items-center justify-center w-8 h-8 transition-colors duration-300 bg-purple-100 rounded-full sm:w-10 sm:h-10 group-hover:bg-purple-200">
                                <Icon name="gravity-ui:face-fun" class="w-5 h-5 text-purple-600 sm:w-6 sm:h-6" />
                            </div>
                        </div>
                        <p class="mt-3 text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl sm:mt-4">
                            {{ formatCurrency(latestStats?.ganancia_modelos || 0) }}
                        </p>
                        <p class="mt-2 text-xs text-gray-500 sm:text-sm">
                            {{ porcentajeModelos.toFixed(1) }}% del total
                        </p>
                    </div>

                    <!-- Ganancia Estudio -->
                    <div
                        class="p-4 transition-all duration-300 transform border border-gray-100 shadow-sm group bg-white/90 backdrop-blur-sm rounded-xl sm:p-6 sm:rounded-2xl hover:shadow-xl hover:-translate-y-1">
                        <div class="flex items-center justify-between">
                            <h3 class="text-xs font-medium text-gray-600 sm:text-sm">Ganancia Estudio</h3>
                            <div
                                class="flex items-center justify-center w-8 h-8 transition-colors duration-300 bg-orange-100 rounded-full sm:w-10 sm:h-10 group-hover:bg-orange-200">
                                <Icon name="uil:building" class="w-5 h-5 text-orange-600 sm:w-6 sm:h-6" />
                            </div>
                        </div>
                        <p class="mt-3 text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl sm:mt-4">
                            {{ formatCurrency(latestStats?.ganancia_estudio || 0) }}
                        </p>
                        <p class="mt-2 text-xs text-gray-500 sm:text-sm">
                            {{ porcentajeEstudio.toFixed(1) }}% del total
                        </p>
                    </div>
                </div>

                <!-- Charts -->
                <div class="grid grid-cols-1 gap-4 mb-6 lg:grid-cols-2 sm:gap-6 sm:mb-8">
                    <!-- Ganancias Chart -->
                    <GananciasChart :data="filteredStats" @period-change="handlePeriodChange"
                        class="min-h-[300px] sm:min-h-[400px]" />

                    <!-- Tokens Chart -->
                    <TokensChart :data="filteredStats" :filters="store.filters"
                        class="min-h-[300px] sm:min-h-[400px]" />

                    <!-- Tokens Distribution -->
                    <TokensDistribution :token-data="getTokensPorPagina" :loading="loading"
                        class="min-h-[300px] sm:min-h-[400px]" />

                    <!-- Podium -->
                    <Podium :data="podiumData" class="min-h-[300px] sm:min-h-[400px]" />
                </div>

                <!-- Deductions Table -->
                <div
                    class="overflow-hidden border border-gray-100 shadow-md bg-white/90 backdrop-blur-sm rounded-xl sm:rounded-2xl">
                    <div class="px-4 py-3 border-b border-gray-100 bg-gray-50/80 sm:px-6 sm:py-4">
                        <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                            <h3 class="text-base font-semibold text-gray-900 sm:text-lg">Deducciones</h3>
                            <span
                                class="px-3 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-full sm:px-4 sm:py-1.5 sm:text-sm">
                                Total: {{ formatCurrency(totalDeducciones) }}
                            </span>
                        </div>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50/80">
                                <tr>
                                    <th
                                        class="px-4 py-2 text-xs font-medium tracking-wider text-left text-gray-500 uppercase sm:px-6 sm:py-3">
                                        Periodo
                                    </th>
                                    <th
                                        class="px-4 py-2 text-xs font-medium tracking-wider text-left text-gray-500 uppercase sm:px-6 sm:py-3">
                                        Concepto
                                    </th>
                                    <th
                                        class="px-4 py-2 text-xs font-medium tracking-wider text-left text-gray-500 uppercase sm:px-6 sm:py-3">
                                        Total
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                <tr v-for="(deduccion, index) in lastDeducciones" :key="index"
                                    class="transition-colors duration-200 hover:bg-gray-50/80">
                                    <td
                                        class="px-4 py-3 text-xs text-gray-900 whitespace-nowrap sm:px-6 sm:py-4 sm:text-sm">
                                        {{ formatPeriodo(deduccion.periodo) }}
                                    </td>
                                    <td
                                        class="px-4 py-3 text-xs text-gray-600 whitespace-nowrap sm:px-6 sm:py-4 sm:text-sm">
                                        {{ deduccion.concepto }}
                                    </td>
                                    <td
                                        class="px-4 py-3 text-xs text-gray-900 whitespace-nowrap sm:px-6 sm:py-4 sm:text-sm">
                                        {{ formatCurrency(deduccion.total_deducciones) }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </template>
        </div>
    </NuxtLayout>
</template>
<script setup>
import { computed, ref, onMounted } from 'vue'
import { useBusinessStatsStore } from '~/stores/businessStats'
import Podium from '~/components/statistics/Podium.vue'
import DashboardFilters from '~/components/statistics/Filters.vue'
import GananciasChart from '~/components/statistics/GananciasChart.vue'
import TokensChart from '~/components/statistics/TokensChart.vue'
import TokensDistribution from '~/components/statistics/DistribucionTokens.vue'
import DashboardSkeleton from '~/components/statistics/SkeletonIndex.vue'


import { storeToRefs } from 'pinia'

const store = useBusinessStatsStore()
const { loading, error, stats, filteredStats } = storeToRefs(store)
const chartKey = ref(0);
const podiumKey = ref(0);
const selectedPeriod = ref('3M')
const showTokensTotal = ref(true)

// Constantes y funciones de utilidad
const MONTH_NAMES = {
    'JAN': 'Enero', 'FEB': 'Febrero', 'MAR': 'Marzo', 'APR': 'Abril', 'MAY': 'Mayo', 'JUN': 'Junio',
    'JUL': 'Julio', 'AUG': 'Agosto', 'SEP': 'Septiembre', 'OCT': 'Octubre', 'NOV': 'Noviembre', 'DEC': 'Diciembre'
}

const MONTH_NUMBERS = {
    'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
    'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
}

const handleFiltersUpdate = (newFilters) => {
    store.filters = newFilters;
};

const handleFiltersReset = () => {
    store.resetFilters();
};

// Funciones de utilidad
const ordenarPorFecha = (data) => {
    return [...data].sort((a, b) => {
        const [yearA, monthA] = a.mes_año.split('-')
        const [yearB, monthB] = b.mes_año.split('-')

        const yearDiff = Number(yearA) - Number(yearB)
        if (yearDiff !== 0) return yearDiff

        return MONTH_NUMBERS[monthA] - MONTH_NUMBERS[monthB]
    })
}

// Computed Properties
const totalGananciaBruta = computed(() => store.totalGananciaBruta)
const totalTokens = computed(() => store.totalTokens)

const latestStats = computed(() => {
    const filtered = filteredStats.value?.estadisticas_por_mes || [];
    if (!filtered.length) return null;

    const { year, month } = store.filters;

    if (year && !month) {
        // Sumar todas las estadísticas del año seleccionado
        const statsForYear = filtered.filter(stat => stat.mes_año.startsWith(year));
        return statsForYear.reduce((acc, stat) => {
            acc.ganancia_modelos += stat.ganancia_modelos || 0;
            acc.ganancia_estudio += stat.ganancia_estudio || 0;
            acc.ganancia_bruta += stat.ganancia_bruta || 0;
            return acc;
        }, { ganancia_modelos: 0, ganancia_estudio: 0, ganancia_bruta: 0 });
    }

    if (!year && !month) {
        // Sumar todas las estadísticas si no hay filtros aplicados
        return filtered.reduce((acc, stat) => {
            acc.ganancia_modelos += stat.ganancia_modelos || 0;
            acc.ganancia_estudio += stat.ganancia_estudio || 0;
            acc.ganancia_bruta += stat.ganancia_bruta || 0;
            return acc;
        }, { ganancia_modelos: 0, ganancia_estudio: 0, ganancia_bruta: 0 });
    }

    return filtered[filtered.length - 1]; // Último mes si no hay otro filtro
});



const lastDeducciones = computed(() => {
    const periodos = filteredStats.value?.estadisticas_por_periodo || []
    if (!periodos.length) return []

    return periodos.flatMap(periodo =>
        periodo.deducciones.map(d => ({
            ...d,
            periodo: periodo.periodo
        }))
    )
})

const totalDeducciones = computed(() => {
    return lastDeducciones.value.reduce((total, d) => total + d.total_deducciones, 0)
})

const porcentajeModelos = computed(() => {
    if (!latestStats.value?.ganancia_bruta) return 0
    return (latestStats.value.ganancia_modelos / latestStats.value.ganancia_bruta) * 100
})

const porcentajeEstudio = computed(() => {
    if (!latestStats.value?.ganancia_bruta) return 0
    return (latestStats.value.ganancia_estudio / latestStats.value.ganancia_bruta) * 100
})

const tendenciaGananciaBruta = computed(() => {
    if (!filteredStats.value?.estadisticas_por_mes) return 0

    const periodosOrdenados = ordenarPorFecha(filteredStats.value.estadisticas_por_mes)
    if (periodosOrdenados.length < 1) return 0

    const periodoActual = periodosOrdenados[periodosOrdenados.length - 1]
    return periodoActual.tendencia || 0
})

const tendenciaTokens = computed(() => {
    if (!filteredStats.value?.estadisticas_por_mes) return 0

    const periodosOrdenados = ordenarPorFecha(filteredStats.value.estadisticas_por_mes)
    if (periodosOrdenados.length < 1) return 0

    const periodoActual = periodosOrdenados[periodosOrdenados.length - 1]
    return periodoActual.tendencia || 0
})



// Pie Chart Configuration
const getTokensPorPagina = computed(() => {
    const { year, month, period } = store.filters;

    const { estadisticas_por_mes, estadisticas_por_periodo } = filteredStats.value || {};

    if (period) {
        const periodoData = estadisticas_por_periodo?.find(p => p.periodo.endsWith(period));
        return periodoData?.tokens_totales_por_pagina || {};
    }

    if (month) {
        const mesData = estadisticas_por_mes?.find(m => {
            const [mYear, mMonth] = m.mes_año.split('-');
            return mMonth === month && (!year || mYear === year);
        });
        return mesData?.tokens_totales_por_pagina || {};
    }

    if (year) {
        const añoData = estadisticas_por_mes?.filter(m => m.mes_año.startsWith(year));
        return sumarTokensPorPagina(añoData);
    }

    return sumarTokensPorPagina(estadisticas_por_mes);
});

const sumarTokensPorPagina = (data) => {
    const resultado = {};
    data?.forEach(item => {
        Object.entries(item.tokens_totales_por_pagina || {}).forEach(([pagina, tokens]) => {
            resultado[pagina] = (resultado[pagina] || 0) + Number(tokens);
        });
    });
    return resultado;
};


const seriesPie = computed(() => {
    const data = getTokensPorPagina.value || {};
    if (Object.keys(data).length === 0) {
        return [0]; // Valor predeterminado si no hay datos
    }
    return Object.values(data).map(Number);
});

const pageColors = {
    Chaturbate: '#FF9900', // Naranja
    Camsoda: '#00BFFF', // Azul cielo
    Streamate: '#345beb', // Rojo anaranjado
    Stripchat: '#eb4034', // Azul púrpura
    CherryTV: '#6A5ACD',
};

const chartOptionsPie = computed(() => ({
    chart: {
        type: 'pie',
        height: 350,
        animations: {
            enabled: true,
            dynamicAnimation: {
                speed: 350,
            },
        },
    },
    labels: Object.keys(getTokensPorPagina.value), // Etiquetas basadas en los datos filtrados
    colors: Object.keys(getTokensPorPagina.value).map(
        (page) => pageColors[page] || '#CCCCCC' // Color específico o gris por defecto
    ),
    legend: {
        position: 'bottom',
        formatter: function (val, opts) {
            const value = opts.w.globals.series[opts.seriesIndex];
            return `${val}`;
        },
    },
    dataLabels: {
        enabled: true,
        formatter: function (val, opts) {
            const series = opts.w.globals.series;
            const total = series.reduce((a, b) => a + b, 0);
            if (total === 0) return '0%';
            return `${((series[opts.seriesIndex] / total) * 100).toFixed(1)}%`;
        },
    },
    tooltip: {
        y: {
            formatter: (val) => `${val} tokens`,
        },
    },
    noData: {
        text: 'No hay datos disponibles',
        align: 'center',
        verticalAlign: 'middle',
        style: {
            fontSize: '16px',
        },
    },
}));


// Utility Functions
const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value)
}

const formatCurrencyShort = (value) => {
    if (value >= 1e9) return `${(value / 1e9).toFixed(1)}B`
    if (value >= 1e6) return `${(value / 1e6).toFixed(1)}M`
    if (value >= 1e3) return `${(value / 1e3).toFixed(1)}K`
    return value.toString()
}

const formatNumber = (value) => {
    return new Intl.NumberFormat('es-CO').format(value)
}

const formatNumberShort = (value) => {
    if (value >= 1e9) return `${(value / 1e9).toFixed(1)}B`
    if (value >= 1e6) return `${(value / 1e6).toFixed(1)}M`
    if (value >= 1e3) return `${(value / 1e3).toFixed(1)}K`
    return value.toString()
}

const formatPeriodo = (periodo) => {
    if (!periodo) return ''
    const [year, month, part] = periodo.split('-')
    return `${MONTH_NAMES[month] || month} ${year} - P${part}`
}

const setChartPeriod = (period) => {
    selectedPeriod.value = period
}

const podiumData = computed(() => {
    const { year, month, period } = store.filters;
    const { mejores_modelos } = filteredStats.value || {};

    if (!mejores_modelos) return [];

    if (period) {
        const key = `${year}-${month}-${period}`;
        return mejores_modelos.mejor_modelo_por_periodo?.[key] || [];
    }

    if (month) {
        const key = `${year}-${month}`;
        return mejores_modelos.mejor_modelo_por_mes?.[key] || [];
    }

    if (year) {
        return mejores_modelos.mejor_modelo_año || [];
    }

    else {
        return mejores_modelos.mejor_modelo_año || [];
    }

    return [];
});


// Lifecycle
onMounted(() => {
    store.fetchStats()
    if (!store.filters.year) {
        store.filters.year = new Date().getFullYear().toString(); // Configura el año actual como filtro inicial
    }
})



watch(
    () => seriesPie.value,
    (newSeries) => {
        console.log('Datos del gráfico pie:', newSeries);
    }
);

watch(seriesPie, () => {
    chartKey.value += 1;
});

watch(
    () => podiumData.value,
    () => {
        podiumKey.value += 1;
    }
);

</script>