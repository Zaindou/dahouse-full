<!-- TokensDistribution.vue -->
<template>
    <div class="p-6 bg-white border border-gray-100 shadow-lg rounded-xl">
        <div class="flex items-center justify-between mb-6">
            <div>
                <h3 class="text-lg font-semibold text-gray-900">Distribución de Tokens por Página</h3>
                <p class="mt-1 text-sm text-gray-500">Porcentaje de tokens generados en cada plataforma</p>
            </div>
            <div class="flex items-center space-x-2">
                <button @click="toggleView" class="px-3 py-1.5 text-sm font-medium rounded-md transition-colors"
                    :class="showPercentage ? 'bg-blue-50 text-blue-600' : 'bg-gray-50 text-gray-600 hover:bg-gray-100'">
                    {{ showPercentage ? 'Ver Tokens' : 'Ver Porcentajes' }}
                </button>
            </div>
        </div>

        <div class="h-[400px] relative">
            <!-- Loading State -->
            <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75">
                <div class="w-8 h-8 border-b-2 border-blue-500 rounded-full animate-spin"></div>
            </div>

            <!-- No Data State -->
            <div v-else-if="!hasData" class="absolute inset-0 flex items-center justify-center">
                <div class="text-center">
                    <Icon name="uil:chart-pie" class="w-12 h-12 mx-auto mb-3 text-gray-300" />
                    <p class="text-gray-500">No hay datos disponibles para el período seleccionado</p>
                </div>
            </div>

            <!-- Chart -->
            <apexchart v-else :key="chartKey" type="pie" :height="350" :options="chartOptions"
                :series="chartData.series" />
        </div>

        <!-- Legend -->
        <div class="grid grid-cols-2 gap-4 mt-6 sm:grid-cols-3 lg:grid-cols-5">
            <div v-for="(value, platform) in tokenData" :key="platform"
                class="flex items-center p-2 space-x-2 rounded-lg"
                :style="{ backgroundColor: getPlatformColor(platform, '10') }">
                <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: getPlatformColor(platform) }"></div>
                <div class="flex flex-col">
                    <span class="text-sm font-medium text-gray-700">{{ platform }}</span>
                    <span class="text-xs text-gray-500">
                        {{ formatValue(value) }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
    tokenData: {
        type: Object,
        required: true
    },
    loading: {
        type: Boolean,
        default: false
    }
});

const chartKey = ref(0);
const showPercentage = ref(true);

// Platform-specific colors with opacity support
const platformColors = {
    Chaturbate: {
        base: '#FF9900',
        light: '#FFF4E6'
    },
    Camsoda: {
        base: '#00BFFF',
        light: '#E6F7FF'
    },
    Streamate: {
        base: '#345beb',
        light: '#EBF0FF'
    },
    Stripchat: {
        base: '#eb4034',
        light: '#FFEBE6'
    },
    CherryTV: {
        base: '#6A5ACD',
        light: '#F0EFFF'
    }
};

const getPlatformColor = (platform, opacity) => {
    const color = platformColors[platform] || { base: '#CCCCCC', light: '#F5F5F5' };
    return opacity === '10' ? color.light : color.base;
};

const hasData = computed(() => {
    return Object.values(props.tokenData || {}).some(value => value > 0);
});

const chartData = computed(() => {
    const data = props.tokenData || {};
    const total = Object.values(data).reduce((sum, value) => sum + value, 0);

    return {
        labels: Object.keys(data),
        series: Object.values(data),
        total
    };
});

const formatValue = (value) => {
    if (showPercentage.value) {
        const percentage = (value / chartData.value.total * 100).toFixed(1);
        return `${percentage}%`;
    }
    return new Intl.NumberFormat().format(value);
};

const chartOptions = computed(() => ({
    chart: {
        type: 'pie',
        animations: {
            enabled: true,
            dynamicAnimation: {
                speed: 350
            }
        },
        fontFamily: 'Inter, system-ui, sans-serif'
    },
    labels: chartData.value.labels,
    colors: chartData.value.labels.map(platform => getPlatformColor(platform)),
    legend: {
        show: false
    },
    dataLabels: {
        enabled: true,
        formatter: function (val, opts) {
            if (showPercentage.value) {
                return `${val.toFixed(1)}%`;
            }
            const value = opts.w.globals.series[opts.seriesIndex];
            return new Intl.NumberFormat('es-CO', {
                notation: 'compact',
                maximumFractionDigits: 1
            }).format(value);
        },
        style: {
            fontSize: '14px',
            fontFamily: 'Inter, system-ui, sans-serif',
            fontWeight: 500
        }
    },
    tooltip: {
        enabled: true,
        y: {
            formatter: function (value) {
                if (showPercentage.value) {
                    return `${(value / chartData.value.total * 100).toFixed(1)}%`;
                }
                return new Intl.NumberFormat().format(value) + ' tokens';
            }
        },
        style: {
            fontSize: '12px',
            fontFamily: 'Inter, system-ui, sans-serif'
        }
    },
    stroke: {
        width: 2,
        colors: ['#ffffff']
    },
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 300
            },
            legend: {
                position: 'bottom'
            }
        }
    }]
}));

const toggleView = () => {
    showPercentage.value = !showPercentage.value;
    chartKey.value += 1;
};

// Watch for data changes to update the chart
watch(() => props.tokenData, () => {
    chartKey.value += 1;
}, { deep: true });
</script>