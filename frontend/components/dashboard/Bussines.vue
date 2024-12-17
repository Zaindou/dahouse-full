<template>
    <div v-if="!estadisticasPorMes" class="flex items-center justify-center min-h-screen">
        <div class="text-gray-500">Cargando estadísticas...</div>
    </div>

    <div v-else class="min-h-screen p-6 space-y-8 bg-gray-50">
        <!-- Header Section -->
        <div class="flex flex-col gap-6">
            <h2 class="text-2xl font-bold text-gray-900">Dashboard de Estadísticas</h2>

            <!-- Filtros -->
            <div class="flex flex-col gap-4 md:flex-row md:items-end">
                <!-- Selector de Mes -->
                <div class="flex-1">
                    <label class="block mb-1 text-sm font-medium text-gray-700">
                        Filtrar por Mes
                    </label>
                    <select v-model="mesSeleccionado" @change="handleMesChange(mesSeleccionado)"
                        class="block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                        <option :value="null">Todos los meses</option>
                        <option v-for="mes in mesesDisponibles" :key="`${mes.año}-${mes.mes}`" :value="mes">
                            {{ mes.label }}
                        </option>
                    </select>
                </div>

                <!-- Selector de Período -->
                <div class="flex-1">
                    <label class="block mb-1 text-sm font-medium text-gray-700">
                        Filtrar por Período
                    </label>
                    <select v-model="periodoSeleccionado" :disabled="!mesSeleccionado"
                        @change="handlePeriodoChange(periodoSeleccionado)"
                        class="block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed">
                        <option :value="null">Todos los períodos</option>
                        <option v-for="periodo in periodosDisponibles" :key="periodo.periodo" :value="periodo">
                            {{ periodo.periodo }}
                        </option>
                    </select>
                </div>

                <!-- Botón para resetear filtros -->
                <button @click="() => { mesSeleccionado = null; periodoSeleccionado = null; }"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Resetear filtros
                </button>
            </div>
        </div>

        <!-- Métricas Principales -->
        <div class="grid gap-6 md:grid-cols-4">
            <!-- Total Ganancias -->
            <div class="p-6 bg-white rounded-lg shadow">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-500">Total Ganancias</p>
                        <p class="mt-1 text-2xl font-semibold">
                            {{ formatCurrency(getTotalGananciasAño) }}
                        </p>
                    </div>
                    <Icon name="ph:money" class="w-8 h-8 text-green-500" />
                </div>
            </div>

            <!-- Total Tokens -->
            <div class="p-6 bg-white rounded-lg shadow">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-500">Total Tokens</p>
                        <p class="mt-1 text-2xl font-semibold">
                            {{ formatNumber(getTotalTokens) }}
                        </p>
                    </div>
                    <Icon name="ph:coins" class="w-8 h-8 text-blue-500" />
                </div>
            </div>

            <!-- Modelos Activas -->
            <div class="p-6 bg-white rounded-lg shadow">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-500">Modelos Activas</p>
                        <p class="mt-1 text-2xl font-semibold">
                            {{ getMaxModelosActivas }}
                        </p>
                    </div>
                    <Icon name="ph:users-three" class="w-8 h-8 text-purple-500" />
                </div>
            </div>

            <!-- Promedio Mensual -->
            <div class="p-6 bg-white rounded-lg shadow">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-500">Promedio Mensual</p>
                        <p class="mt-1 text-2xl font-semibold">
                            {{ formatCurrency(getPromedioMensual) }}
                        </p>
                    </div>
                    <Icon name="ph:chart-line-up" class="w-8 h-8 text-orange-500" />
                </div>
            </div>
        </div>

        <!-- Gráficas Principales -->
        <div class="grid gap-6 md:grid-cols-2">
            <!-- Gráfica de Ganancias por Mes -->
            <div class="p-6 bg-white rounded-lg shadow">
                <h3 class="mb-4 text-lg font-semibold">Ganancias por Período</h3>
                <client-only>
                    <div class="h-80">
                        <apexchart type="area" :options="gananciasChartOptions" :series="gananciasChartSeries"
                            height="100%" />
                    </div>
                </client-only>
            </div>

            <!-- Gráfica de Tokens por Página -->
            <div class="p-6 bg-white rounded-lg shadow">
                <h3 class="mb-4 text-lg font-semibold">Distribución de Tokens por Página</h3>
                <client-only>
                    <div class="h-80">
                        <apexchart type="pie" :options="tokensPieOptions" :series="tokensPieSeries" height="100%" />
                    </div>
                </client-only>
            </div>
        </div>

        <!-- Tabla de Rendimiento por Página -->
        <div class="p-6 bg-white rounded-lg shadow">
            <h3 class="mb-4 text-lg font-semibold">Rendimiento por Página</h3>
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="p-4 text-sm font-medium text-left text-gray-500">Página</th>
                            <th class="p-4 text-sm font-medium text-right text-gray-500">Tokens</th>
                            <th class="p-4 text-sm font-medium text-right text-gray-500">Ganancia Total</th>
                            <th class="p-4 text-sm font-medium text-right text-gray-500">Promedio por Token</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <tr v-for="pagina in tokensPorPagina" :key="pagina.pagina">
                            <td class="p-4 text-sm font-medium text-gray-900">{{ pagina.pagina }}</td>
                            <td class="p-4 text-sm text-right text-gray-500">
                                {{ formatNumber(pagina.total_tokens) }}
                            </td>
                            <td class="p-4 text-sm text-right text-gray-500">
                                {{ formatCurrency(pagina.total_ganado) }}
                            </td>
                            <td class="p-4 text-sm text-right text-gray-500">
                                {{ formatCurrency(pagina.total_ganado / pagina.total_tokens) }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Deducciones -->
        <div class="p-6 bg-white rounded-lg shadow">
            <h3 class="mb-4 text-lg font-semibold">Resumen de Deducciones</h3>

            <!-- Cards de resumen -->
            <div class="grid gap-6 mb-6 md:grid-cols-2">
                <div class="p-4 rounded-lg bg-gray-50">
                    <p class="text-sm text-gray-500">Total Deducido</p>
                    <p class="mt-1 text-xl font-semibold text-red-600">
                        {{ formatCurrency(resumenDeducciones.totalDeducido) }}
                    </p>
                </div>
                <div class="p-4 rounded-lg bg-gray-50">
                    <p class="text-sm text-gray-500">Total Modelos con Deducciones</p>
                    <p class="mt-1 text-xl font-semibold text-gray-900">
                        {{ resumenDeducciones.totalModelos }}
                    </p>
                </div>
            </div>

            <!-- Tabla de detalles -->
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="p-4 text-sm font-medium text-left text-gray-500">Concepto</th>
                            <th class="p-4 text-sm font-medium text-right text-gray-500">Total Deducido</th>
                            <th class="p-4 text-sm font-medium text-right text-gray-500">Modelos Afectados</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <tr v-for="deduccion in deducciones" :key="deduccion.concepto">
                            <td class="p-4 text-sm font-medium text-gray-900">
                                {{ deduccion.concepto }}
                            </td>
                            <td class="p-4 text-sm text-right text-red-600">
                                {{ formatCurrency(deduccion.total_deducido) }}
                            </td>
                            <td class="p-4 text-sm text-right text-gray-500">
                                {{ deduccion.total_modelos }}
                            </td>
                        </tr>
                    </tbody>
                    <tfoot class="bg-gray-50">
                        <tr>
                            <td class="p-4 text-sm font-medium text-gray-900">Total</td>
                            <td class="p-4 text-sm font-medium text-right text-red-600">
                                {{ formatCurrency(resumenDeducciones.totalDeducido) }}
                            </td>
                            <td class="p-4 text-sm font-medium text-right text-gray-900">
                                {{ resumenDeducciones.totalModelos }}
                            </td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useFinancieroStore } from '@/stores/financiero'
import { onMounted, computed, ref } from 'vue'

const financieroStore = useFinancieroStore()

// Estados para filtros
const mesSeleccionado = ref(null)
const periodoSeleccionado = ref(null)

// Constante para orden de meses
const MONTH_ORDER = {
    'JAN': 1,
    'FEB': 2,
    'MAR': 3,
    'APR': 4,
    'MAY': 5,
    'JUN': 6,
    'JUL': 7,
    'AUG': 8,
    'SEP': 9,
    'OCT': 10,
    'NOV': 11,
    'DEC': 12
}

onMounted(async () => {
    await financieroStore.fetchEstadisticasNegocio()
})

// Computed properties para datos del store
const estadisticasPorMes = computed(() => financieroStore.estadisticasPorMes)
const estadisticasPorPeriodo = computed(() => financieroStore.estadisticasPorPeriodo)
const tokensPorPagina = computed(() => financieroStore.tokensPorPagina)
const deducciones = computed(() => financieroStore.deducciones)

// Computed para filtros
const mesesDisponibles = computed(() => {
    if (!estadisticasPorMes.value) return []

    return [...new Set(estadisticasPorMes.value.map(mes => ({
        año: mes.año,
        mes: mes.mes,
        label: `${mes.mes} ${mes.año}`
    })))].sort((a, b) => {
        if (a.año !== b.año) return a.año - b.año
        return MONTH_ORDER[a.mes] - MONTH_ORDER[b.mes]
    })
})

const periodosDisponibles = computed(() => {
    if (!estadisticasPorPeriodo.value || !mesSeleccionado.value) return []

    return estadisticasPorPeriodo.value.filter(periodo => {
        const [año, mes] = periodo.periodo.split('-')
        return año === mesSeleccionado.value.año.toString() &&
            mes === mesSeleccionado.value.mes
    }).sort((a, b) => {
        const periodoA = parseInt(a.periodo.split('-')[2])
        const periodoB = parseInt(b.periodo.split('-')[2])
        return periodoA - periodoB
    })
})

// Datos filtrados
const datosFiltrados = computed(() => {
    if (!estadisticasPorPeriodo.value) return []

    let datos = estadisticasPorPeriodo.value

    if (periodoSeleccionado.value) {
        return [periodoSeleccionado.value]
    }

    if (mesSeleccionado.value) {
        datos = datos.filter(periodo => {
            const [año, mes] = periodo.periodo.split('-')
            return año === mesSeleccionado.value.año.toString() &&
                mes === mesSeleccionado.value.mes
        })
    }

    return datos.sort((a, b) => {
        const [yearA, monthA, periodA] = a.periodo.split('-')
        const [yearB, monthB, periodB] = b.periodo.split('-')

        if (yearA !== yearB) return parseInt(yearA) - parseInt(yearB)
        if (monthA !== monthB) return MONTH_ORDER[monthA] - MONTH_ORDER[monthB]
        return parseInt(periodA) - parseInt(periodB)
    })
})

// Métricas calculadas
const getTotalGananciasAño = computed(() => {
    const datos = periodoSeleccionado.value ? [periodoSeleccionado.value] :
        mesSeleccionado.value ? periodosDisponibles.value :
            estadisticasPorMes.value

    if (!datos) return 0
    return datos.reduce((sum, item) => sum + item.total_ganancias_reales, 0)
})

const getTotalTokens = computed(() => {
    const datos = periodoSeleccionado.value ? [periodoSeleccionado.value] :
        mesSeleccionado.value ? periodosDisponibles.value :
            estadisticasPorMes.value

    if (!datos) return 0
    return datos.reduce((sum, item) => sum + item.total_tokens, 0)
})

const getMaxModelosActivas = computed(() => {
    const datos = periodoSeleccionado.value ? [periodoSeleccionado.value] :
        mesSeleccionado.value ? periodosDisponibles.value :
            estadisticasPorMes.value

    if (!datos) return 0
    return Math.max(...datos.map(item => item.total_modelos))
})

const getPromedioMensual = computed(() => {
    if (!datosFiltrados.value.length) return 0
    return getTotalGananciasAño.value / datosFiltrados.value.length
})

// Configuración de gráficas
const gananciasChartOptions = computed(() => ({
    chart: {
        type: 'area',
        toolbar: { show: false },
        zoom: { enabled: false }
    },
    dataLabels: { enabled: false },
    stroke: {
        curve: 'smooth',
        width: 2
    },
    colors: ['#3b82f6', '#ef4444'],
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.3,
            stops: [0, 90, 100]
        }
    },
    xaxis: {
        categories: datosFiltrados.value.map(item => item.periodo),
        labels: {
            rotate: -45,
            trim: false
        }
    },
    yaxis: {
        labels: {
            formatter: value => formatCurrency(value)
        }
    },
    tooltip: {
        y: {
            formatter: value => formatCurrency(value)
        }
    },
    legend: {
        position: 'top'
    }
}))

const gananciasChartSeries = computed(() => {
    if (!datosFiltrados.value.length) return []

    return [
        {
            name: 'Ganancias Totales',
            data: datosFiltrados.value.map(item => item.total_ganancias_reales)
        },
        {
            name: 'Ganancia Estudio',
            data: datosFiltrados.value.map(item => item.ganancia_estudio)
        }
    ]
})

const tokensPieOptions = computed(() => ({
    chart: {
        type: 'pie'
    },
    labels: tokensPorPagina.value?.map(p => p.pagina) || [],
    legend: {
        position: 'bottom',
        formatter: function (value, opts) {
            const tokens = formatNumber(opts.w.globals.series[opts.seriesIndex])
            return `${value} - ${tokens} tokens`
        }
    },
    tooltip: {
        y: {
            formatter: value => formatNumber(value) + ' tokens'
        }
    },
    responsive: [{
        breakpoint: 480,
        options: {
            chart: { width: 300 },
            legend: { position: 'bottom' }
        }
    }]
}))

const tokensPieSeries = computed(() =>
    tokensPorPagina.value?.map(p => p.total_tokens) || []
)

// Resumen de deducciones
const resumenDeducciones = computed(() => {
    if (!deducciones.value) return {
        totalDeducido: 0,
        totalModelos: 0
    }

    return {
        totalDeducido: deducciones.value.reduce((sum, d) => sum + d.total_deducido, 0),
        totalModelos: deducciones.value.reduce((sum, d) => sum + d.total_modelos, 0)
    }
})

// Métodos para manejar filtros
const handleMesChange = (mes) => {
    mesSeleccionado.value = mes
    periodoSeleccionado.value = null
}

const handlePeriodoChange = (periodo) => {
    periodoSeleccionado.value = periodo
}

// Funciones de utilidad para formato
const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value)
}

const formatNumber = (value) => {
    return new Intl.NumberFormat('es-CO', {
        maximumFractionDigits: 1
    }).format(Math.round(value * 10) / 10)
}

const formatPercent = (value) => {
    if (value === null || value === undefined) return '0%'
    return `${value > 0 ? '+' : ''}${value.toFixed(1)}%`
}

const getCrecimientoClass = (value) => {
    if (!value) return 'text-gray-500'
    if (value > 0) return 'text-green-600'
    if (value < 0) return 'text-red-600'
    return 'text-gray-500'
}
</script>
