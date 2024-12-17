<template>
    <div class="w-full">
        <!-- Skeleton Loading -->
        <div v-if="isLoading" class="animate-pulse">
            <div class="flex items-center mb-6 space-x-4">
                <div class="w-48 h-8 bg-gray-200 rounded"></div>
                <div class="w-24 h-4 bg-gray-200 rounded"></div>
            </div>
            <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
                <!-- TRM Actual Skeleton -->
                <div class="p-4 border border-gray-100 shadow-sm bg-gray-50 rounded-xl">
                    <div class="flex items-center mb-3 space-x-2">
                        <div class="w-4 h-4 bg-gray-300 rounded-full"></div>
                        <div class="w-32 h-4 bg-gray-300 rounded"></div>
                    </div>
                    <div class="space-y-2">
                        <div class="h-8 bg-gray-200 rounded w-36"></div>
                        <div class="w-24 h-3 bg-gray-200 rounded"></div>
                    </div>
                </div>
                <!-- TRM de Pago Skeleton -->
                <div class="p-4 border border-gray-100 shadow-sm bg-gray-50 rounded-xl">
                    <div class="flex items-center mb-3 space-x-2">
                        <div class="w-4 h-4 bg-gray-300 rounded-full"></div>
                        <div class="w-32 h-4 bg-gray-300 rounded"></div>
                    </div>
                    <div class="space-y-2">
                        <div class="h-8 bg-gray-200 rounded w-36"></div>
                        <div class="w-24 h-3 bg-gray-200 rounded"></div>
                    </div>
                </div>
                <!-- Período Actual Skeleton -->
                <div class="p-4 border border-gray-100 shadow-sm bg-gray-50 rounded-xl">
                    <div class="flex items-center mb-3 space-x-2">
                        <div class="w-4 h-4 bg-gray-300 rounded-full"></div>
                        <div class="w-32 h-4 bg-gray-300 rounded"></div>
                    </div>
                    <div class="space-y-2">
                        <div class="h-8 bg-gray-200 rounded w-36"></div>
                        <div class="w-full h-3 bg-gray-200 rounded"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Contenido Real -->
        <template v-else>
            <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-bold text-gray-800">Datos financieros</h2>
                <span class="text-sm text-gray-500">Actualizado: Hoy, {{ formatDate(new Date()) }}</span>
            </div>
            <div v-if="datosFinancieros" class="space-y-4">
                <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
                    <div
                        class="p-4 transition-all border border-blue-100 shadow-sm bg-gradient-to-br from-blue-50 to-blue-50/50 rounded-xl hover:shadow-md">
                        <div class="flex items-center mb-3 space-x-2">
                            <div class="w-2 h-2 bg-blue-400 rounded-full"></div>
                            <h3 class="text-sm font-semibold text-blue-700">TRM actual</h3>
                        </div>
                        <p class="mb-1 text-2xl font-bold text-blue-800">
                            {{ formatCurrency(datosFinancieros.trm_actual) }}
                        </p>
                        <p class="text-xs text-blue-600">Valor de referencia</p>
                    </div>

                    <div
                        class="p-4 transition-all border border-green-100 shadow-sm bg-gradient-to-br from-green-50 to-green-50/50 rounded-xl hover:shadow-md">
                        <div class="flex items-center mb-3 space-x-2">
                            <div class="w-2 h-2 bg-green-400 rounded-full"></div>
                            <h3 class="text-sm font-semibold text-green-700">TRM de pago</h3>
                        </div>
                        <p class="mb-1 text-2xl font-bold text-green-800">
                            {{ formatCurrency(datosFinancieros.trm_liquidacion) }}
                        </p>
                        <p class="text-xs text-green-600">Valor de liquidación</p>
                    </div>

                    <div
                        class="p-4 transition-all border border-purple-100 shadow-sm bg-gradient-to-br from-purple-50 to-purple-50/50 rounded-xl hover:shadow-md">
                        <div class="flex items-center mb-3 space-x-2">
                            <div class="w-2 h-2 bg-purple-400 rounded-full"></div>
                            <h3 class="text-sm font-semibold text-purple-700">Período actual</h3>
                        </div>
                        <p class="mb-1 font-bold text-purple-800 text-1xl">
                            {{ datosFinancieros.periodo_actual[0] }}
                        </p>
                        <p class="text-xs text-purple-600">
                            {{ datosFinancieros.periodo_actual[1] }} a {{ datosFinancieros.periodo_actual[2] }}
                        </p>
                    </div>
                </div>
            </div>
            <div v-if="error" class="p-4 mt-6 border-l-4 border-red-400 rounded-r-lg bg-red-50">
                <div class="flex items-center space-x-3">
                    <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div>
                        <p class="font-semibold text-red-800">Error</p>
                        <p class="text-sm text-red-600">{{ error }}</p>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<script setup>
import { useFinancieroStore } from '~/stores/financiero'
import { computed, onMounted } from 'vue'

const financieroStore = useFinancieroStore()
const isLoading = ref(true)

onMounted(async () => {
    try {
        await financieroStore.fetchDatosFinancieros()
    } finally {
        isLoading.value = false
    }
})

const formatCurrency = (value) => {
    // Primero formateamos con Intl.NumberFormat
    const formatted = new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
    }).format(value);

    // Removemos el espacio entre el símbolo y el número
    return formatted.replace(/\s+/g, '');
};

const formatDate = (date) => {
    return new Intl.DateTimeFormat('es-CO', {
        hour: '2-digit',
        minute: '2-digit',
    }).format(date)
}

const datosFinancieros = computed(() => financieroStore.datosFinancieros)
const error = computed(() => financieroStore.error)
</script>