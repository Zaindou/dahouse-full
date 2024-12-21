<template>
    <div class="p-6 bg-white border border-gray-100 shadow-lg rounded-xl">
        <!-- Encabezado con Métricas -->
        <div class="mb-6">
            <div class="flex items-center justify-between mb-4">
                <div>
                    <h3 class="text-xl font-bold text-gray-900">Tokens</h3>
                    <p class="mt-1 text-sm text-gray-500">Distribución mensual de tokens cargados</p>
                </div>

                <!-- Total de Tokens -->
                <div class="text-right">
                    <p class="text-sm text-gray-500">Total del período</p>
                    <p class="text-2xl font-bold text-gray-900">
                        {{ formatNumberShort(totalTokens) }}
                    </p>
                </div>
            </div>

            <!-- Indicadores de tendencia -->
            <div class="flex gap-4 mt-2">
                <div class="flex items-center gap-2">
                    <div class="w-3 h-3 bg-blue-500 rounded-full" />
                    <span class="text-sm text-gray-600">Tokens cargados</span>
                </div>
                <div v-if="tendencia !== 0" class="flex items-center gap-1 text-sm">
                    <Icon :name="tendencia > 0 ? 'ph:trend-up' : 'ph:trend-down'" :class="[
                        'w-4 h-4',
                        tendencia > 0 ? 'text-green-500' : 'text-red-500'
                    ]" />
                    <span :class="tendencia > 0 ? 'text-green-600' : 'text-red-600'">
                        {{ Math.abs(tendencia).toFixed(1) }}%
                    </span>
                    <span class="text-gray-500">vs. período anterior</span>
                </div>
            </div>
        </div>

        <!-- Gráfico -->
        <div>
            <apexchart type="bar" :height="350" :options="chartOptions" :series="series" />
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    data: {
        type: Object,
        required: true
    },
    filters: {
        type: Object,
        required: true
    }
});

const MONTH_NAMES = {
    'JAN': 'Enero', 'FEB': 'Febrero', 'MAR': 'Marzo', 'APR': 'Abril',
    'MAY': 'Mayo', 'JUN': 'Junio', 'JUL': 'Julio', 'AUG': 'Agosto',
    'SEP': 'Septiembre', 'OCT': 'Octubre', 'NOV': 'Noviembre', 'DEC': 'Diciembre'
};

const chartOptions = computed(() => ({
    chart: {
        type: 'bar',
        height: 350,
        toolbar: {
            show: false
        },
        zoom: { enabled: false },
        fontFamily: 'Inter, sans-serif'
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '60%',
            borderRadius: 4,
            dataLabels: {
                position: 'top'
            }
        }
    },
    colors: ['#3B82F6'],
    dataLabels: {
        enabled: true,
        formatter: (val) => formatNumberShort(val),
        offsetY: -20,
        style: {
            fontSize: '12px',
            colors: ['#64748b']
        }
    },
    grid: {
        borderColor: '#f1f1f1',
        strokeDashArray: 4,
        xaxis: {
            lines: { show: false }
        }
    },
    xaxis: {
        type: 'category',
        tickPlacement: 'on',
        labels: {
            style: {
                fontSize: '12px',
                fontFamily: 'Inter, sans-serif',
                colors: '#64748b'
            },
            formatter: (value) => {
                if (!value) return '';
                const [year, month] = value.split('-');
                return `${MONTH_NAMES[month]?.slice(0, 3) || month} ${year}`;
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
        labels: {
            style: {
                fontSize: '12px',
                fontFamily: 'Inter, sans-serif',
                colors: '#64748b'
            },
            formatter: formatNumberShort
        }
    },
    tooltip: {
        shared: true,
        intersect: false,
        theme: 'light',
        y: {
            formatter: (val) => formatNumber(val)
        },
        style: {
            fontSize: '12px',
            fontFamily: 'Inter, sans-serif'
        }
    },
    states: {
        hover: {
            filter: {
                type: 'darken',
                value: 0.1
            }
        }
    }
}));

const series = computed(() => {
    const { year, month } = props.filters;

    if (!props.data) return [];

    if (month) {
        const periodos = props.data.estadisticas_por_periodo.filter((periodo) => {
            const [pYear, pMonth] = periodo.periodo?.split('-') || [];
            return pMonth === month && (!year || pYear === year);
        });

        return [{
            name: 'Tokens por Período',
            data: periodos.map((periodo) => ({
                x: periodo.periodo?.split('-').slice(1).join('-') || 'Desconocido',
                y: Number(periodo.total_tokens) || 0,
            })),
        }];
    }

    const data = props.data.estadisticas_por_mes;

    return [{
        name: 'Total Tokens',
        data: data.map((mes) => ({
            x: mes.mes_año,
            y: Number(mes.total_tokens) || 0,
        })),
    }];
});

// Calcular total de tokens
const totalTokens = computed(() => {
    if (!series.value[0]?.data) return 0;
    return series.value[0].data.reduce((sum, item) => sum + (item.y || 0), 0);
});

// Calcular tendencia
const tendencia = computed(() => {
    if (!series.value[0]?.data || series.value[0].data.length < 2) return 0;
    const data = series.value[0].data;
    const actual = data[data.length - 1].y;
    const anterior = data[data.length - 2].y;
    return anterior ? ((actual - anterior) / anterior) * 100 : 0;
});

function formatNumberShort(value) {
    if (value >= 1e9) return `${(value / 1e9).toFixed(1)}B`;
    if (value >= 1e6) return `${(value / 1e6).toFixed(1)}M`;
    if (value >= 1e3) return `${(value / 1e3).toFixed(1)}K`;
    return value.toString();
}

function formatNumber(value) {
    return new Intl.NumberFormat('es-CO').format(value);
}
</script>