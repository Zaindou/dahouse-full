<template>
    <NuxtLayout>
        <div class="max-w-4xl mx-auto p-4">
            <div class="bg-white shadow-lg rounded-lg p-6">
                <!-- Formulario de entrada -->
                <div class="space-y-4 mb-6">
                    <h2 class="text-2xl font-bold text-gray-800">Simulador de Préstamos</h2>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="space-y-2">
                            <label class="block text-sm font-medium text-gray-700">Valor Total</label>
                            <input v-model="valorFormateado" @input="handleValorInput" type="text"
                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                placeholder="$0">
                        </div>
                        <div class="space-y-2">
                            <label class="block text-sm font-medium text-gray-700">Plazo (Quincenas)</label>
                            <input v-model="deduccion.plazo" type="number"
                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                placeholder="Número de quincenas">
                        </div>
                        <div class="space-y-2">
                            <label class="block text-sm font-medium text-gray-700">Tasa de Interés (%)</label>
                            <input v-model="deduccion.tasa" type="number"
                                class="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                placeholder="Tasa de interés">
                        </div>
                    </div>
                </div>

                <!-- Resumen del préstamo -->
                <div v-if="resumenPrestamo" class="mb-8 bg-gray-50 p-4 rounded-lg">
                    <h3 class="text-xl font-semibold mb-4">Resumen del Préstamo</h3>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div class="bg-white p-3 rounded shadow">
                            <p class="text-sm text-gray-600">Períodos</p>
                            <p class="text-lg font-bold">{{ resumenPrestamo.numeroPeriodos }}</p>
                        </div>
                        <div class="bg-white p-3 rounded shadow">
                            <p class="text-sm text-gray-600">Valor a Prestar</p>
                            <p class="text-lg font-bold">{{ formatCurrency(resumenPrestamo.valorAdeudar) }}</p>
                        </div>
                        <div class="bg-white p-3 rounded shadow">
                            <p class="text-sm text-gray-600">Total con Intereses</p>
                            <p class="text-lg font-bold">{{ formatCurrency(resumenPrestamo.valorConIntereses) }}</p>
                        </div>
                        <div class="bg-white p-3 rounded shadow">
                            <p class="text-sm text-gray-600">Cuota Quincenal</p>
                            <p class="text-lg font-bold">{{ formatCurrency(resumenPrestamo.cuotaQuincenal) }}</p>
                        </div>
                    </div>
                </div>

                <!-- Tabla de amortización -->
                <div v-if="pagosDetalle.length" class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Período</th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Cuota</th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Capital</th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Interés</th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Saldo</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr v-for="pago in pagosDetalle" :key="pago.periodo">
                                <td class="px-6 py-4 whitespace-nowrap">{{ pago.periodo }}</td>
                                <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.cuotaQuincenal) }}</td>
                                <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.principal) }}</td>
                                <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.interes) }}</td>
                                <td class="px-6 py-4 whitespace-nowrap">{{ formatCurrency(pago.saldoCapital) }}</td>
                            </tr>
                        </tbody>
                    </table>
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

// Watch reactivo para todos los campos
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
    pagosDetalle.value = [];

    for (let i = 1; i <= plazo; i++) {
        const interes = saldoCapital * tasaQuincenal;
        const principal = cuotaQuincenal - interes;
        saldoCapital -= principal;

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
        cuotaQuincenal: cuotaQuincenal.toFixed(2)
    };
};
</script>