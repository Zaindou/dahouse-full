<template>
    <NuxtLayout>
        <div class="max-w-4xl p-4 mx-auto">
            <div class="p-4 bg-white rounded-lg shadow-lg md:p-6">
                <!-- Formulario de entrada -->
                <div class="mb-6 space-y-4">
                    <h2 class="text-xl font-bold text-gray-800 md:text-2xl">Simulador de Préstamos</h2>
                    <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
                        <div class="space-y-2">
                            <label class="block text-sm font-medium text-gray-700">Valor Total</label>
                            <input v-model="valorFormateado" @input="handleValorInput" type="text"
                                class="w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                placeholder="$0">
                        </div>
                        <div class="space-y-2">
                            <label class="block text-sm font-medium text-gray-700">Plazo (Quincenas)</label>
                            <input v-model="deduccion.plazo" type="number"
                                class="w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                placeholder="Número de quincenas">
                        </div>
                        <div class="space-y-2">
                            <label class="block text-sm font-medium text-gray-700">Tasa de Interés (%)</label>
                            <input v-model="deduccion.tasa" type="number"
                                class="w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                placeholder="Tasa de interés">
                        </div>
                    </div>
                </div>

                <!-- Resumen del préstamo -->
                <div v-if="resumenPrestamo" class="mb-8">
                    <h3 class="mb-4 text-lg font-semibold md:text-xl">Resumen del Préstamo</h3>
                    <div class="grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-5">
                        <div class="p-3 rounded-lg bg-gray-50">
                            <p class="text-xs text-gray-600">Períodos</p>
                            <p class="text-base font-bold md:text-lg">{{ resumenPrestamo.numeroPeriodos }}</p>
                        </div>
                        <div class="p-3 rounded-lg bg-gray-50">
                            <p class="text-xs text-gray-600">Valor a Prestar</p>
                            <p class="text-base font-bold md:text-lg">{{ formatCurrency(resumenPrestamo.valorAdeudar) }}
                            </p>
                        </div>
                        <div class="p-3 rounded-lg bg-gray-50">
                            <p class="text-xs text-gray-600">Total Intereses</p>
                            <p class="text-base font-bold text-orange-600 md:text-lg">
                                {{ formatCurrency(resumenPrestamo.totalIntereses) }}
                            </p>
                        </div>
                        <div class="p-3 rounded-lg bg-gray-50">
                            <p class="text-xs text-gray-600">Total con Intereses</p>
                            <p class="text-base font-bold md:text-lg">{{
                                formatCurrency(resumenPrestamo.valorConIntereses) }}</p>
                        </div>
                        <div class="p-3 rounded-lg bg-gray-50">
                            <p class="text-xs text-gray-600">Cuota Quincenal</p>
                            <p class="text-base font-bold md:text-lg">{{ formatCurrency(resumenPrestamo.cuotaQuincenal)
                                }}</p>
                        </div>
                    </div>
                </div>

                <!-- Tabla de amortización -->
                <div v-if="pagosDetalle.length" class="-mx-4 overflow-x-auto md:mx-0">
                    <div class="inline-block min-w-full align-middle">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-3 py-3 text-xs font-medium text-left text-gray-500 uppercase md:px-6">
                                        Período</th>
                                    <th class="px-3 py-3 text-xs font-medium text-left text-gray-500 uppercase md:px-6">
                                        Cuota</th>
                                    <th class="px-3 py-3 text-xs font-medium text-left text-gray-500 uppercase md:px-6">
                                        Capital</th>
                                    <th class="px-3 py-3 text-xs font-medium text-left text-gray-500 uppercase md:px-6">
                                        Interés</th>
                                    <th class="px-3 py-3 text-xs font-medium text-left text-gray-500 uppercase md:px-6">
                                        Saldo</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                <tr v-for="pago in pagosDetalle" :key="pago.periodo" class="hover:bg-gray-50">
                                    <td class="px-3 py-2 text-sm md:px-6 md:py-4">{{ pago.periodo }}</td>
                                    <td class="px-3 py-2 text-sm md:px-6 md:py-4">{{ formatCurrency(pago.cuotaQuincenal)
                                        }}</td>
                                    <td class="px-3 py-2 text-sm md:px-6 md:py-4">{{ formatCurrency(pago.principal) }}
                                    </td>
                                    <td class="px-3 py-2 text-sm md:px-6 md:py-4">{{ formatCurrency(pago.interes) }}
                                    </td>
                                    <td class="px-3 py-2 text-sm md:px-6 md:py-4">{{ formatCurrency(pago.saldoCapital)
                                        }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </NuxtLayout>
</template>

<script setup>
const deduccion = ref({
    valor_total: '',
    plazo: '',
    tasa: ''
});

const valorFormateado = ref('');
const pagosDetalle = ref([]);
const resumenPrestamo = ref(null);

const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
    }).format(value);
};

const unformatCurrency = (value) => {
    return value.replace(/[^\d]/g, '');
};

const handleValorInput = (event) => {
    const rawValue = unformatCurrency(event.target.value);
    deduccion.value.valor_total = rawValue;

    if (rawValue) {
        valorFormateado.value = formatCurrency(rawValue);
    } else {
        valorFormateado.value = '';
    }
};

watch(() => deduccion.value.valor_total, (newValue) => {
    if (newValue) {
        valorFormateado.value = formatCurrency(newValue);
    } else {
        valorFormateado.value = '';
    }
});

watch([
    () => deduccion.value.valor_total,
    () => deduccion.value.plazo,
    () => deduccion.value.tasa
], ([valorTotal, plazo, tasa]) => {
    if (valorTotal && plazo && tasa) {
        simularDeduccion();
    }
}, { deep: true });

const simularDeduccion = () => {
    const valorTotal = parseFloat(deduccion.value.valor_total) || 0;
    const plazo = parseInt(deduccion.value.plazo, 10) || 0;
    let tasa = parseFloat(deduccion.value.tasa) || 0;

    if (tasa > 1) {
        tasa = tasa / 100;
    }

    if (valorTotal <= 0 || plazo <= 0 || tasa < 0) {
        resumenPrestamo.value = null;
        pagosDetalle.value = [];
        return;
    }

    const tasaQuincenal = tasa / 2;
    const cuotaQuincenal = valorTotal * ((tasaQuincenal * Math.pow(1 + tasaQuincenal, plazo)) / (Math.pow(1 + tasaQuincenal, plazo) - 1));
    let saldoCapital = valorTotal;
    let totalIntereses = 0;
    pagosDetalle.value = [];

    for (let i = 1; i <= plazo; i++) {
        const interes = saldoCapital * tasaQuincenal;
        const principal = cuotaQuincenal - interes;
        saldoCapital -= principal;
        totalIntereses += interes;

        if (saldoCapital < 0) saldoCapital = 0;

        pagosDetalle.value.push({
            periodo: i,
            cuotaQuincenal: cuotaQuincenal.toFixed(2),
            principal: principal.toFixed(2),
            interes: interes.toFixed(2),
            saldoCapital: saldoCapital.toFixed(2),
            balanceRestante: (saldoCapital > 0 ? saldoCapital : 0).toFixed(2)
        });
    }

    resumenPrestamo.value = {
        numeroPeriodos: plazo,
        valorAdeudar: valorTotal.toFixed(2),
        valorConIntereses: (cuotaQuincenal * plazo).toFixed(2),
        cuotaQuincenal: cuotaQuincenal.toFixed(2),
        totalIntereses: totalIntereses.toFixed(2)
    };
};
</script>