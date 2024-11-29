<template>
    <div class="w-full">
        <!-- Skeleton Loading -->
        <div v-if="isLoading" class="animate-pulse">
            <div class="flex items-center space-x-4 mb-6">
                <div class="h-8 w-48 bg-gray-200 rounded"></div>
                <div class="h-4 w-24 bg-gray-200 rounded"></div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
                <!-- TRM Actual Skeleton -->
                <div class="bg-gray-50 p-4 rounded-xl shadow-sm border border-gray-100">
                    <div class="flex items-center space-x-2 mb-3">
                        <div class="h-4 w-4 bg-gray-300 rounded-full"></div>
                        <div class="h-4 w-32 bg-gray-300 rounded"></div>
                    </div>
                    <div class="space-y-2">
                        <div class="h-8 w-36 bg-gray-200 rounded"></div>
                        <div class="h-3 w-24 bg-gray-200 rounded"></div>
                    </div>
                </div>
                <!-- TRM de Pago Skeleton -->
                <div class="bg-gray-50 p-4 rounded-xl shadow-sm border border-gray-100">
                    <div class="flex items-center space-x-2 mb-3">
                        <div class="h-4 w-4 bg-gray-300 rounded-full"></div>
                        <div class="h-4 w-32 bg-gray-300 rounded"></div>
                    </div>
                    <div class="space-y-2">
                        <div class="h-8 w-36 bg-gray-200 rounded"></div>
                        <div class="h-3 w-24 bg-gray-200 rounded"></div>
                    </div>
                </div>
                <!-- Período Actual Skeleton -->
                <div class="bg-gray-50 p-4 rounded-xl shadow-sm border border-gray-100">
                    <div class="flex items-center space-x-2 mb-3">
                        <div class="h-4 w-4 bg-gray-300 rounded-full"></div>
                        <div class="h-4 w-32 bg-gray-300 rounded"></div>
                    </div>
                    <div class="space-y-2">
                        <div class="h-8 w-36 bg-gray-200 rounded"></div>
                        <div class="h-3 w-full bg-gray-200 rounded"></div>
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
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
                    <div
                        class="bg-gradient-to-br from-blue-50 to-blue-50/50 p-4 rounded-xl shadow-sm border border-blue-100 transition-all hover:shadow-md">
                        <div class="flex items-center space-x-2 mb-3">
                            <div class="w-2 h-2 bg-blue-400 rounded-full"></div>
                            <h3 class="text-sm font-semibold text-blue-700">TRM actual</h3>
                        </div>
                        <p class="text-2xl font-bold text-blue-800 mb-1">
                            {{ formatCurrency(datosFinancieros.trm_actual) }}
                        </p>
                        <p class="text-xs text-blue-600">Valor de referencia</p>
                    </div>

                    <div
                        class="bg-gradient-to-br from-green-50 to-green-50/50 p-4 rounded-xl shadow-sm border border-green-100 transition-all hover:shadow-md">
                        <div class="flex items-center space-x-2 mb-3">
                            <div class="w-2 h-2 bg-green-400 rounded-full"></div>
                            <h3 class="text-sm font-semibold text-green-700">TRM de pago</h3>
                        </div>
                        <p class="text-2xl font-bold text-green-800 mb-1">
                            {{ formatCurrency(datosFinancieros.trm_liquidacion) }}
                        </p>
                        <p class="text-xs text-green-600">Valor de liquidación</p>
                    </div>

                    <div
                        class="bg-gradient-to-br from-purple-50 to-purple-50/50 p-4 rounded-xl shadow-sm border border-purple-100 transition-all hover:shadow-md">
                        <div class="flex items-center space-x-2 mb-3">
                            <div class="w-2 h-2 bg-purple-400 rounded-full"></div>
                            <h3 class="text-sm font-semibold text-purple-700">Período actual</h3>
                        </div>
                        <p class="text-1xl font-bold text-purple-800 mb-1">
                            {{ datosFinancieros.periodo_actual[0] }}
                        </p>
                        <p class="text-xs text-purple-600">
                            {{ datosFinancieros.periodo_actual[1] }} a {{ datosFinancieros.periodo_actual[2] }}
                        </p>
                    </div>
                </div>
            </div>
            <div v-if="error" class="mt-6 p-4 bg-red-50 border-l-4 border-red-400 rounded-r-lg">
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
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
    }).format(value)
}

const formatDate = (date) => {
    return new Intl.DateTimeFormat('es-CO', {
        hour: '2-digit',
        minute: '2-digit',
    }).format(date)
}

const datosFinancieros = computed(() => financieroStore.datosFinancieros)
const error = computed(() => financieroStore.error)
</script>