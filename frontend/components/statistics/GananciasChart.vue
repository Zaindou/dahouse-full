<template>
    <div class="p-6 bg-white border border-gray-100 shadow-lg rounded-xl">
        <div class="flex flex-col gap-4 mb-6 sm:flex-row sm:items-center sm:justify-between">
            <!-- Título y Totales -->
            <div>
                <h3 class="mb-2 text-xl font-bold text-gray-900">Evolución de Ganancias</h3>
                <div class="flex flex-wrap gap-4">
                    <div v-for="(item, index) in legendItems" :key="index" class="flex items-center gap-2">
                        <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: item.color }" />
                        <span class="text-sm text-gray-600">{{ item.name }}</span>
                    </div>
                </div>
            </div>

            <!-- Filtros de Período -->
            <!-- <div class="flex items-center p-1 border border-gray-200 rounded-lg bg-gray-50">
                <button v-for="periodo in ['1M', '3M', '6M', '1Y', 'MAX']" :key="periodo"
                    @click="setChartPeriod(periodo)" :class="[
                        'px-3 py-1.5 text-sm font-medium rounded-md transition-all duration-200',
                        selectedPeriod === periodo
                            ? 'bg-white text-blue-600 shadow-sm'
                            : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    ]">
                    {{ periodo }}
                </button>
            </div> -->
        </div>

        <!-- Gráfico -->
        <div class="">
            <apexchart type="area" :height="350" :options="chartOptions" :series="series" />
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
    data: {
        type: Object,
        required: true
    }
});

const selectedPeriod = ref('3M');
const MONTH_NAMES = {
    'JAN': 'Enero', 'FEB': 'Febrero', 'MAR': 'Marzo', 'APR': 'Abril',
    'MAY': 'Mayo', 'JUN': 'Junio', 'JUL': 'Julio', 'AUG': 'Agosto',
    'SEP': 'Septiembre', 'OCT': 'Octubre', 'NOV': 'Noviembre', 'DEC': 'Diciembre'
};

const legendItems = [
    { name: 'Ganancia Bruta', color: '#0EA5E9' },
    { name: 'Ganancia Modelos', color: '#8B5CF6' },
    { name: 'Ganancia Estudio', color: '#F59E0B' }
];

const chartOptions = computed(() => ({
    chart: {
        type: 'area',
        height: 350,
        toolbar: {
            show: false
        },
        zoom: { enabled: false },
        fontFamily: 'Inter, sans-serif'
    },
    stroke: {
        curve: 'smooth',
        width: 3
    },
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.45,
            opacityTo: 0.05,
            stops: [50, 100]
        }
    },
    colors: ['#0EA5E9', '#8B5CF6', '#F59E0B'],
    dataLabels: { enabled: false },
    grid: {
        borderColor: '#f1f1f1',
        strokeDashArray: 4,
        xaxis: {
            lines: { show: false }
        }
    },
    xaxis: {
        type: 'category',
        tickAmount: 6,
        labels: {
            style: {
                fontSize: '12px',
                fontFamily: 'Inter, sans-serif',
                colors: '#64748b'
            },
            formatter: (value) => {
                if (!value) return ''
                const [year, month] = value.split('-')
                return `${MONTH_NAMES[month]?.slice(0, 3) || month} ${year}`
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
            formatter: formatCurrencyShort
        }
    },
    tooltip: {
        shared: true,
        intersect: false,
        theme: 'light',
        y: {
            formatter: formatCurrency
        },
        style: {
            fontSize: '12px',
            fontFamily: 'Inter, sans-serif'
        }
    },
    legend: {
        show: false
    },
    markers: {
        size: 5,
        strokeWidth: 0,
        hover: {
            size: 7
        }
    }
}));

const series = computed(() => {
    if (!props.data?.estadisticas_por_mes) return [];

    const data = props.data.estadisticas_por_mes;

    return [
        {
            name: 'Ganancia Bruta',
            data: data.map(mes => ({
                x: mes.mes_año,
                y: Number(mes.ganancia_bruta) || 0
            }))
        },
        {
            name: 'Ganancia Modelos',
            data: data.map(mes => ({
                x: mes.mes_año,
                y: Number(mes.ganancia_modelos) || 0
            }))
        },
        {
            name: 'Ganancia Estudio',
            data: data.map(mes => ({
                x: mes.mes_año,
                y: Number(mes.ganancia_estudio) || 0
            }))
        }
    ];
});

function formatCurrencyShort(value) {
    if (value >= 1e9) return `${(value / 1e9).toFixed(1)}B`;
    if (value >= 1e6) return `${(value / 1e6).toFixed(1)}M`;
    if (value >= 1e3) return `${(value / 1e3).toFixed(1)}K`;
    return value.toString();
}

function formatCurrency(value) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

const setChartPeriod = (period) => {
    selectedPeriod.value = period;
    // Aquí puedes implementar la lógica para filtrar los datos según el período
};
</script>