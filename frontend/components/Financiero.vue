<template>
    <loading :is-loading="isLoading"></loading>
    <h2 class="text-xl font-bold mb-4 text-gray-800">Datos de Liquidación</h2>
    <div v-if="datosFinancieros" class="space-y-4">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="bg-blue-50 p-2 rounded-md shadow-sm">
                <h3 class="text-sm font-semibold text-blue-700 mb-1">TRM Actual</h3>
                <p class="text-lg font-bold text-blue-800">{{ formatCurrency(datosFinancieros.trm_actual) }}</p>
            </div>
            <div class="bg-green-50 p-2 rounded-md shadow-sm">
                <h3 class="text-sm font-semibold text-green-700 mb-1">TRM de Liquidación</h3>
                <p class="text-lg font-bold text-green-800">{{ formatCurrency(datosFinancieros.trm_liquidacion) }}
                </p>
            </div>
            <div class="bg-purple-50 p-2 rounded-md shadow-sm">
                <h3 class="text-sm font-semibold text-purple-700 mb-1">Período Actual</h3>
                <p class="text-base font-bold text-purple-800 text-center">{{ datosFinancieros.periodo_actual[0] }}
                </p>
                <p class="text-xs text-purple-600 text-center">
                    {{ datosFinancieros.periodo_actual[1] }} a {{ datosFinancieros.periodo_actual[2] }}
                </p>
            </div>
        </div>

        <!-- Espacio para futuras adiciones como ganancias totales -->
        <!-- <div class="bg-yellow-50 p-3 rounded-md shadow-sm">
        <h3 class="text-sm font-semibold text-yellow-700 mb-1">Ganancias Totales Modelos</h3>
        <p class="text-lg font-bold text-yellow-800">{{ formatCurrency(datosFinancieros.ganancias_totales_periodo) }}</p>
      </div> -->
    </div>
    <div v-if="error" class="mt-4 p-3 bg-red-100 border-l-4 border-red-500 text-red-700 text-sm">
        <p class="font-bold">Error</p>
        <p>{{ error }}</p>
    </div>
</template>



<script>
import { useFinancieroStore } from '~/stores/financiero';
import { onMounted } from 'vue';


export default {
    data() {
        return {
            isLoading: false,
        };
    },
    setup() {
        const financieroStore = useFinancieroStore();
        onMounted(async () => {
            await financieroStore.fetchDatosFinancieros();
        });

        function formatDate(dateString) {
            const date = new Date(dateString);
            const day = date.getDate().toString().padStart(2, '0');
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const year = date.getFullYear();
            return `${day}-${month}-${year}`;
        }

        function formatCurrency(value) {
            return new Intl.NumberFormat('es-CO', {
                style: 'currency',
                currency: 'COP',
                minimumFractionDigits: 0,

            }).format(value);
        }

        const datosFinancieros = computed(() => financieroStore.datosFinancieros);

        return {
            datosFinancieros,
            error: financieroStore.error,
            formatDate,
            formatCurrency,
        };
    }
}
</script>
