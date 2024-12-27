<template>
    <NuxtLayout>
        <div class="min-h-screen py-4 bg-gray-50 sm:py-8">
            <div class="px-2 mx-auto max-w-7xl sm:px-4 lg:px-8">
                <!-- Card Principal -->
                <div class="overflow-hidden bg-white shadow-lg rounded-xl">
                    <!-- Header -->
                    <div class="p-4 border-b border-gray-200 sm:p-6">
                        <h2 class="flex items-center gap-2 text-xl font-bold text-gray-900 sm:text-2xl">
                            <Icon name="heroicons:calculator" class="w-6 h-6 text-blue-600 sm:w-8 sm:h-8" />
                            Simulador de Préstamos
                        </h2>
                    </div>

                    <!-- Contenido -->
                    <div class="p-4 sm:p-6">
                        <!-- Formulario de entrada -->
                        <div class="grid grid-cols-1 gap-4 mb-6 sm:gap-6 md:grid-cols-3 sm:mb-8">
                            <div class="space-y-2">
                                <label for="totalValue" class="block text-sm font-medium text-gray-700">
                                    Valor Total
                                </label>
                                <input id="totalValue" v-model="valorFormateado" @input="handleValorInput" type="text"
                                    inputmode="decimal"
                                    class="w-full text-base border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                    placeholder="$0" />
                            </div>

                            <div class="space-y-2">
                                <label for="term" class="block text-sm font-medium text-gray-700">
                                    Plazo (Quincenas)
                                </label>
                                <input id="term" v-model="deduccion.plazo" type="number" inputmode="numeric"
                                    class="w-full text-base border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                    placeholder="Número de quincenas" />
                            </div>

                            <div class="space-y-2">
                                <label for="rate" class="block text-sm font-medium text-gray-700">
                                    Tasa de Interés (%)
                                </label>
                                <input id="rate" v-model="deduccion.tasa" type="number" inputmode="decimal"
                                    class="w-full text-base border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                    placeholder="Tasa de interés" />
                            </div>
                        </div>

                        <!-- Resumen del préstamo -->
                        <div v-if="resumenPrestamo" class="mb-8">
                            <h3 class="mb-4 text-xl font-semibold">Resumen del Préstamo</h3>
                            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
                                <!-- Resumen Card Component inline -->
                                <div
                                    class="p-4 transition-colors bg-white border border-gray-200 rounded-lg shadow hover:border-blue-500">
                                    <div class="flex items-center gap-2 mb-2 text-sm text-gray-500">
                                        <Icon name="heroicons:clock" class="w-4 h-4" />
                                        Períodos
                                    </div>
                                    <p class="text-lg font-bold text-gray-900">
                                        {{ resumenPrestamo.numeroPeriodos }}
                                    </p>
                                </div>

                                <div
                                    class="p-4 transition-colors bg-white border border-gray-200 rounded-lg shadow hover:border-blue-500">
                                    <div class="flex items-center gap-2 mb-2 text-sm text-gray-500">
                                        <Icon name="heroicons:banknotes" class="w-4 h-4" />
                                        Valor a Prestar
                                    </div>
                                    <p class="text-lg font-bold text-gray-900">
                                        {{ formatCurrency(resumenPrestamo.valorAdeudar) }}
                                    </p>
                                </div>

                                <div
                                    class="p-4 transition-colors bg-white border border-gray-200 rounded-lg shadow hover:border-blue-500">
                                    <div class="flex items-center gap-2 mb-2 text-sm text-gray-500">
                                        <Icon name="heroicons:chart-bar" class="w-4 h-4" />
                                        Total Intereses
                                    </div>
                                    <p class="text-lg font-bold text-orange-600">
                                        {{ formatCurrency(resumenPrestamo.totalIntereses) }}
                                    </p>
                                </div>

                                <div
                                    class="p-4 transition-colors bg-white border border-gray-200 rounded-lg shadow hover:border-blue-500">
                                    <div class="flex items-center gap-2 mb-2 text-sm text-gray-500">
                                        <Icon name="heroicons:currency-dollar" class="w-4 h-4" />
                                        Total con Intereses
                                    </div>
                                    <p class="text-lg font-bold text-gray-900">
                                        {{ formatCurrency(resumenPrestamo.valorConIntereses) }}
                                    </p>
                                </div>

                                <div
                                    class="p-4 transition-colors bg-white border border-gray-200 rounded-lg shadow hover:border-blue-500">
                                    <div class="flex items-center gap-2 mb-2 text-sm text-gray-500">
                                        <Icon name="heroicons:calendar" class="w-4 h-4" />
                                        Cuota Quincenal
                                    </div>
                                    <p class="text-lg font-bold text-gray-900">
                                        {{ formatCurrency(resumenPrestamo.cuotaQuincenal) }}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Tabla de amortización -->
                        <div v-if="pagosDetalle.length" class="overflow-hidden">
                            <div class="flex items-center justify-between mb-4">
                                <h3 class="flex items-center gap-2 text-xl font-semibold">
                                    <Icon name="heroicons:table-cells" class="w-6 h-6 text-blue-600" />
                                    Tabla de Amortización
                                </h3>
                                <div class="flex items-center gap-2">
                                    <button @click="descargarTabla"
                                        class="inline-flex items-center gap-1 px-3 py-2 text-sm font-medium text-gray-700 transition-colors bg-white border border-gray-300 rounded-md hover:bg-gray-50 hover:text-blue-600"
                                        title="Descargar tabla">
                                        <Icon name="heroicons:arrow-down-tray" class="w-5 h-5" />
                                        Descargar CSV
                                    </button>
                                    <button @click="imprimirTabla"
                                        class="inline-flex items-center gap-1 px-3 py-2 text-sm font-medium text-gray-700 transition-colors bg-white border border-gray-300 rounded-md hover:bg-gray-50 hover:text-blue-600"
                                        title="Imprimir tabla">
                                        <Icon name="heroicons:printer" class="w-5 h-5" />
                                        Imprimir
                                    </button>
                                </div>
                            </div>

                            <div class="overflow-x-auto border border-gray-200 rounded-lg">
                                <table class="min-w-full divide-y divide-gray-200">
                                    <thead class="bg-gray-50">
                                        <tr>
                                            <th scope="col"
                                                class="px-6 py-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                                                <div class="flex items-center gap-2">
                                                    <Icon name="heroicons:hashtag" class="w-4 h-4" />
                                                    N°
                                                </div>
                                            </th>
                                            <th scope="col"
                                                class="px-6 py-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                                                <div class="flex items-center gap-2">
                                                    <Icon name="heroicons:banknotes" class="w-4 h-4" />
                                                    Cuota
                                                </div>
                                            </th>
                                            <th scope="col"
                                                class="px-6 py-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                                                <div class="flex items-center gap-2">
                                                    <Icon name="heroicons:building-library" class="w-4 h-4" />
                                                    Capital
                                                </div>
                                            </th>
                                            <th scope="col"
                                                class="px-6 py-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                                                <div class="flex items-center gap-2">
                                                    <Icon name="heroicons:chart-bar" class="w-4 h-4" />
                                                    Interés
                                                </div>
                                            </th>
                                            <th scope="col"
                                                class="px-6 py-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase">
                                                <div class="flex items-center gap-2">
                                                    <Icon name="heroicons:calculator" class="w-4 h-4" />
                                                    Saldo
                                                </div>
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody class="bg-white divide-y divide-gray-200">
                                        <tr v-for="pago in pagosDetalle" :key="pago.periodo"
                                            class="transition-colors hover:bg-blue-50">
                                            <td class="px-6 py-4 text-sm font-medium text-gray-900 whitespace-nowrap">
                                                {{ pago.periodo }}
                                            </td>
                                            <td class="px-6 py-4 text-sm text-gray-900 whitespace-nowrap">
                                                {{ formatCurrency(pago.cuotaQuincenal) }}
                                            </td>
                                            <td class="px-6 py-4 text-sm text-gray-900 whitespace-nowrap">
                                                {{ formatCurrency(pago.principal) }}
                                            </td>
                                            <td class="px-6 py-4 text-sm text-green-600 whitespace-nowrap">
                                                {{ formatCurrency(pago.interes) }}
                                            </td>
                                            <td class="px-6 py-4 text-sm font-medium text-blue-600 whitespace-nowrap">
                                                {{ formatCurrency(pago.saldoCapital) }}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
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

// Funciones de utilidad
const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
    }).format(value).replace(/\s+/g, '');
};

const unformatCurrency = (value) => {
    return value.replace(/[^\d]/g, '');
};

// Manejadores de eventos
const handleValorInput = (event) => {
    const rawValue = unformatCurrency(event.target.value);
    deduccion.value.valor_total = rawValue;
    valorFormateado.value = rawValue ? formatCurrency(rawValue) : '';
};

// Watchers
watch(() => deduccion.value.valor_total, (newValue) => {
    valorFormateado.value = newValue ? formatCurrency(newValue) : '';
});

watch(
    [
        () => deduccion.value.valor_total,
        () => deduccion.value.plazo,
        () => deduccion.value.tasa
    ],
    ([valorTotal, plazo, tasa]) => {
        if (valorTotal && plazo && tasa) {
            simularDeduccion();
        }
    },
    { deep: true }
);

// Funciones para exportar e imprimir
const descargarTabla = () => {
    // Crear el contenido CSV
    const headers = ['N°', 'Cuota', 'Capital', 'Interés', 'Saldo'];
    const rows = pagosDetalle.value.map(pago => [
        pago.periodo,
        pago.cuotaQuincenal,
        pago.principal,
        pago.interes,
        pago.saldoCapital
    ]);

    // Generar contenido CSV
    const csvContent = [
        headers.join(','),
        ...rows.map(row => row.join(','))
    ].join('\n');

    // Crear el blob y descargar
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);

    link.setAttribute('href', url);
    link.setAttribute('download', `tabla_amortizacion_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};

const imprimirTabla = () => {
    // Crear una ventana de impresión
    const printWindow = window.open('', '_blank');
    const tableHTML = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Tabla de Amortización</title>
      <style>
        body { font-family: Arial, sans-serif; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f8f9fa; }
        .header { margin-bottom: 20px; }
        .summary { margin-bottom: 20px; }
        .summary-item { margin-bottom: 10px; }
        @media print {
          body { padding: 20px; }
          button { display: none; }
        }
      </style>
    </head>
    <body>
      <div class="header">
        <h2>Tabla de Amortización</h2>
        <p>Fecha: ${new Date().toLocaleDateString()}</p>
      </div>
      
      <div class="summary">
        <div class="summary-item">Valor del Préstamo: ${formatCurrency(resumenPrestamo.value.valorAdeudar)}</div>
        <div class="summary-item">Plazo: ${resumenPrestamo.value.numeroPeriodos} quincenas</div>
        <div class="summary-item">Cuota Quincenal: ${formatCurrency(resumenPrestamo.value.cuotaQuincenal)}</div>
      </div>

      <table>
        <thead>
          <tr>
            <th>N°</th>
            <th>Cuota</th>
            <th>Capital</th>
            <th>Interés</th>
            <th>Saldo</th>
          </tr>
        </thead>
        <tbody>
          ${pagosDetalle.value.map(pago => `
            <tr>
              <td>${pago.periodo}</td>
              <td>${formatCurrency(pago.cuotaQuincenal)}</td>
              <td>${formatCurrency(pago.principal)}</td>
              <td>${formatCurrency(pago.interes)}</td>
              <td>${formatCurrency(pago.saldoCapital)}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    
</body>

</html>
`;

    printWindow.document.write(tableHTML);
    printWindow.document.close();
};

// Lógica de negocio
const simularDeduccion = () => {
    const valorTotal = parseFloat(deduccion.value.valor_total) || 0;
    const plazo = parseInt(deduccion.value.plazo, 10) || 0;
    let tasa = parseFloat(deduccion.value.tasa) || 0;

    if (tasa > 1) {
        tasa = tasa / 100;
    }

    if (valorTotal <= 0 || plazo <= 0 || tasa < 0) { resumenPrestamo.value = null; pagosDetalle.value = []; return; } const
        tasaQuincenal = tasa / 2; const cuotaQuincenal = valorTotal * ((tasaQuincenal * Math.pow(1 + tasaQuincenal, plazo)) /
            (Math.pow(1 + tasaQuincenal, plazo) - 1)); let saldoCapital = valorTotal; let totalIntereses = 0;
    pagosDetalle.value = []; for (let i = 1; i <= plazo; i++) {
        const interes = saldoCapital * tasaQuincenal; const
            principal = cuotaQuincenal - interes; saldoCapital -= principal; totalIntereses += interes; if (saldoCapital < 0)
            saldoCapital = 0; pagosDetalle.value.push({
                periodo: i, cuotaQuincenal: cuotaQuincenal.toFixed(2), principal:
                    principal.toFixed(2), interes: interes.toFixed(2), saldoCapital: saldoCapital.toFixed(2)
            });
    }
    resumenPrestamo.value = {
        numeroPeriodos: plazo, valorAdeudar: valorTotal.toFixed(2), valorConIntereses:
            (cuotaQuincenal * plazo).toFixed(2), cuotaQuincenal: cuotaQuincenal.toFixed(2), totalIntereses:
            totalIntereses.toFixed(2)
    };
}; </script>