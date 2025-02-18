<template>
    <div class="p-6 space-y-6 bg-gray-50">
        <!-- Summary Cards -->
        <div class="grid gap-6 md:grid-cols-4">
            <!-- Total Earnings -->
            <div class="p-6 bg-white rounded-lg shadow">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-500">Ganancias Totales</p>
                        <p class="mt-1 text-2xl font-semibold">{{ formatCurrency(statistics.totalEarnings) }}</p>
                    </div>
                    <Icon name="uil:dollar-sign" class="w-8 h-8 text-green-500" />
                </div>
            </div>

            <!-- Total Tokens -->
            <div class="p-6 bg-white rounded-lg shadow">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-500">Tokens Totales</p>
                        <p class="mt-1 text-2xl font-semibold">{{ formatNumber(statistics.totalTokens) }}</p>
                    </div>
                    <Icon name="ph:coins" class="w-8 h-8 text-blue-500" />
                </div>
            </div>

            <!-- Total Deductions -->
            <div class="p-6 bg-white rounded-lg shadow">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-500">Deducciones Totales</p>
                        <p class="mt-1 text-2xl font-semibold">{{ formatCurrency(statistics.totalDeductions) }}</p>
                    </div>
                    <Icon name="uil:exclamation-circle" class="w-8 h-8 text-red-500" />
                </div>
            </div>

            <!-- Trend -->
            <div class="p-6 bg-white rounded-lg shadow">
                <div class="flex items-center justify-between">
                    <div>
                        <div class="flex items-center gap-2">
                            <p class="text-sm text-gray-500">Tendencia</p>
                            <!-- Reemplazamos el Popover por un tooltip más simple -->
                            <div class="relative">
                                <button @mouseenter="showTooltip = true" @mouseleave="showTooltip = false"
                                    @focus="showTooltip = true" @blur="showTooltip = false"
                                    class="flex items-center justify-center w-5 h-5 text-gray-400 rounded-full hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500">
                                    <Icon name="ph:info" class="w-4 h-4" />
                                </button>

                                <div v-if="showTooltip"
                                    class="absolute z-50 p-4 mt-2 transform -translate-x-1/2 bg-white rounded-lg shadow-lg w-72 left-1/2 ring-1 ring-black ring-opacity-5">
                                    <div class="space-y-2">
                                        <p class="text-sm font-medium text-gray-900">
                                            ¿Cómo se calcula la tendencia?
                                        </p>
                                        <p class="text-sm text-gray-500">
                                            La tendencia muestra el promedio de cambio en los últimos 3 períodos:
                                        </p>
                                        <div class="pl-4 space-y-1">
                                            <p v-for="(change, index) in trendChanges" :key="index" class="text-sm">
                                                <span
                                                    :class="change.percentage >= 0 ? 'text-green-600' : 'text-red-600'">
                                                    {{ change.percentage >= 0 ? '↑' : '↓' }}
                                                    {{ Math.abs(change.percentage).toFixed(1) }}%
                                                </span>
                                                <span class="text-gray-500">
                                                    : {{ change.periodName }}
                                                </span>
                                            </p>
                                        </div>
                                        <div class="pt-2 mt-2 border-t border-gray-200">
                                            <p class="text-sm text-gray-500">
                                                <span class="font-medium">Promedio:</span>
                                                <span
                                                    :class="statistics.earningsTrend >= 0 ? 'text-green-600' : 'text-red-600'">
                                                    {{ statistics.earningsTrend >= 0 ? '↑' : '↓' }}
                                                    {{ Math.abs(statistics.earningsTrend).toFixed(1) }}%
                                                </span>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="flex items-center mt-1">
                            <p class="text-2xl font-semibold">
                                {{ Math.abs(statistics.earningsTrend).toFixed(1) }}%
                            </p>
                            <Icon :name="statistics.earningsTrend > 0 ? 'ph:trend-up' : 'ph:trend-down'"
                                class="w-6 h-6 ml-2"
                                :class="statistics.earningsTrend > 0 ? 'text-green-500' : 'text-red-500'" />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts -->
        <div class="grid gap-6 md:grid-cols-2">
            <!-- Earnings Chart -->
            <div class="bg-white rounded-lg shadow p-7">
                <h3 class="mb-4 text-lg font-semibold">Ganancias por Período</h3>
                <client-only>
                    <div class="h-64">
                        <apexchart type="line" :options="earningsChartOptions" :series="earningsChartSeries" />
                    </div>
                </client-only>
            </div>

            <!-- Tokens Chart -->
            <div class="bg-white rounded-lg shadow p-7">
                <h3 class="mb-4 text-lg font-semibold">Tokens por mes</h3>
                <client-only>
                    <div class="h-64">
                        <apexchart type="bar" :options="tokensChartOptions" :series="tokensChartSeries" />
                    </div>
                </client-only>
            </div>
        </div>

        <!-- Platform Performance -->
        <div class="p-6 bg-white rounded-lg shadow">
            <h3 class="mb-4 text-lg font-semibold">Rendimiento por Plataforma</h3>
            <div class="grid gap-4 md:grid-cols-3">
                <div v-for="(stats, platform) in statistics.platformStats" :key="platform"
                    class="p-4 rounded-lg bg-gray-50">
                    <h4 class="mb-2 text-lg font-semibold">{{ platform }}</h4>
                    <div class="space-y-2">
                        <p class="text-sm text-gray-600">
                            Tokens: <span class="font-medium">{{ formatNumber(stats.tokens) }}</span>
                        </p>
                        <p class="text-sm text-gray-600">
                            Ganancias: <span class="font-medium">{{ formatCurrency(stats.earnings) }}</span>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    historialPagos: {
        type: Array,
        required: true
    }
});

const showTooltip = ref(false);

const calculateTrend = (payments) => {
    // Obtener los últimos 3 períodos para un cálculo más estable
    const recentPayments = payments.slice(0, 3);

    if (recentPayments.length < 2) return 0;

    // Calcular el promedio de cambio porcentual
    const changes = [];
    for (let i = 0; i < recentPayments.length - 1; i++) {
        const current = recentPayments[i].total_cop;
        const previous = recentPayments[i + 1].total_cop;
        const change = ((current - previous) / previous) * 100;
        changes.push(change);
    }

    // Retornar el promedio de los cambios
    return changes.reduce((sum, change) => sum + change, 0) / changes.length;
};


// Calcular estadísticas
const statistics = computed(() => {
    const payments = props.historialPagos.slice(1); // Ignorar info del usuario

    // Cálculos totales
    const totalEarnings = payments.reduce((sum, p) => sum + p.total_cop, 0);
    const totalTokens = payments.reduce((sum, p) =>
        sum + p.detalles_paginas.reduce((s, d) => s + d.tokens, 0), 0);
    const totalDeductions = payments.reduce((sum, p) =>
        sum + p.deducciones_asociadas.reduce((s, d) => s + d.monto_pagado, 0), 0);

    // Promedios
    const avgEarningsPerPeriod = totalEarnings / payments.length;
    const avgTokensPerPeriod = totalTokens / payments.length;

    // Tendencias
    const earningsTrend = calculateTrend(payments);

    // Estadísticas por plataforma
    const platformStats = payments.reduce((acc, p) => {
        p.detalles_paginas.forEach(d => {
            if (!acc[d.nombre_pagina]) {
                acc[d.nombre_pagina] = { tokens: 0, earnings: 0 };
            }
            acc[d.nombre_pagina].tokens += d.tokens;
            acc[d.nombre_pagina].earnings += d.total_cop;
        });
        return acc;
    }, {});

    return {
        totalEarnings,
        totalTokens,
        totalDeductions,
        avgEarningsPerPeriod,
        avgTokensPerPeriod,
        earningsTrend,
        platformStats
    };
});

// Datos para gráficos
const chartData = computed(() => {
    return props.historialPagos.slice(1).map(p => ({
        period: p.periodo.nombre,
        earnings: p.total_cop,
        tokens: p.detalles_paginas.reduce((sum, d) => sum + d.tokens, 0),
        deductions: p.deducciones_asociadas.reduce((sum, d) => sum + d.monto_pagado, 0)
    })).reverse();
});

// Opciones gráfico de ganancias
const earningsChartOptions = computed(() => ({
    chart: {
        height: 350,
        type: 'line',
        toolbar: {
            show: false
        }
    },
    xaxis: {
        categories: chartData.value.map(d => d.period)
    },
    yaxis: {
        labels: {
            formatter: (value) => formatCurrency(value)
        }
    },
    tooltip: {
        y: {
            formatter: (value) => formatCurrency(value)
        }
    }
}));

const earningsChartSeries = computed(() => [
    {
        name: 'Ganancias',
        data: chartData.value.map(d => d.earnings)
    },
    {
        name: 'Deducciones',
        data: chartData.value.map(d => d.deductions)
    }
]);

// Opciones gráfico de tokens
const tokensChartOptions = computed(() => ({
    chart: {
        type: 'bar',
        height: 350,
        toolbar: { show: false }
    },
    plotOptions: {
        bar: {
            borderRadius: 4,
            columnWidth: '60%',
        }
    },
    colors: ['#3b82f6'],
    dataLabels: { enabled: false },
    xaxis: {
        categories: monthlyChartData.value.map(d => d.period),
        labels: {
            rotate: -45,
            trim: false
        }
    },
    yaxis: {
        labels: {
            formatter: (value) => formatNumber(value)
        },
        title: {
            text: 'Tokens Generados'
        }
    },
    tooltip: {
        y: {
            formatter: (value) => formatNumber(value) + ' tokens'
        }
    },
    title: {
        text: '',
        align: 'left',
        style: {
            fontSize: '16px',
            fontWeight: 600
        }
    }
}));

const tokensChartSeries = computed(() => [{
    name: 'Tokens',
    data: monthlyChartData.value.map(d => d.tokens)
}]);

// Utilidades de formato
const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(value);
};

const formatNumber = (value) => {
    return new Intl.NumberFormat('es-CO').format(value);
};

const monthlyChartData = computed(() => {
    const monthlyData = props.historialPagos.slice(1).reduce((acc, pago) => {
        const [year, month] = pago.periodo.nombre.split('-');
        const monthKey = `${year}-${month}`;

        if (!acc[monthKey]) {
            acc[monthKey] = {
                period: `${month} ${year}`,
                tokens: 0,
                earnings: pago.total_cop,
                deductions: pago.deducciones_asociadas.reduce((sum, d) => sum + d.monto_pagado, 0)
            };
        }

        // Sumar tokens del período
        const tokensInPeriod = pago.detalles_paginas.reduce((sum, d) => sum + d.tokens, 0);
        acc[monthKey].tokens += tokensInPeriod;
        acc[monthKey].earnings += pago.total_cop;

        return acc;
    }, {});

    // Convertir a array y ordenar por fecha
    return Object.values(monthlyData).reverse();
});

// Tendencias de cambio Popup informativo
const trendChanges = computed(() => {
    const payments = props.historialPagos.slice(1);
    const recentPayments = payments.slice(0, 3);
    const changes = [];

    for (let i = 0; i < recentPayments.length - 1; i++) {
        const current = recentPayments[i].total_cop;
        const previous = recentPayments[i + 1].total_cop;
        const percentage = ((current - previous) / previous) * 100;
        changes.push({
            percentage,
            periodName: `${recentPayments[i].periodo.nombre} vs ${recentPayments[i + 1].periodo.nombre}`
        });
    }

    return changes;
});
</script>