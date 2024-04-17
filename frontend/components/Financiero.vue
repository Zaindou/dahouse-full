<template>
    <div class="p-4">
        <loading :is-loading="isLoading"></loading>
        <h2 class="text-xl font-bold mb-2">Datos de liquidación</h2>
        <div v-if="datosFinancieros" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Descripción</th>
                        <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Valor</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr>
                        <td class="px-6 py-4 whitespace-nowrap">TRM Actual</td>
                        <td class="px-6 py-4 whitespace-nowrap text-right">{{
            formatCurrency(datosFinancieros.trm_actual) }}</td>
                    </tr>
                    <tr>
                        <td class="px-6 py-4 whitespace-nowrap">TRM de Liquidación</td>
                        <td class="px-6 py-4 whitespace-nowrap text-right">{{
            formatCurrency(datosFinancieros.trm_liquidacion) }}</td>
                    </tr>
                    <tr>
                        <td class="px-6 py-4 whitespace-nowrap">Período Actual</td>
                        <td class="px-6 py-4 whitespace-nowrap text-right">
                            {{ datosFinancieros.periodo_actual[0] }}
                            <br>
                            {{ datosFinancieros.periodo_actual[1] }} a
                            {{ datosFinancieros.periodo_actual[2] }}
                        </td>
                    </tr>
                    <!-- <tr>
                        <td class="px-6 py-4 whitespace-nowrap">Ganancias totales modelos</td>
                        <td class="px-6 py-4 whitespace-nowrap text-right">{{
            formatCurrency(datosFinancieros.ganancias_totales_periodo) }}</td>
                    </tr> -->
                </tbody>
            </table>
        </div>
        <div v-if="error" class="mt-4 text-red-500">
            Error: {{ error }}
        </div>
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
