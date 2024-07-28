<template>
    <div class="container mx-auto p-4">
        <h1 class="text-3xl font-bold mb-8 text-gray-800">Gestión de Ganancias</h1>

        <div class="grid md:grid-cols-2 gap-8">
            <!-- Sección de Jornadas y Modelos -->
            <div class="bg-white shadow-md rounded-lg p-6">
                <h2 class="text-xl font-semibold mb-4 text-gray-700">Selección de Modelo</h2>
                <div class="mb-4">
                    <label for="jornada" class="block text-sm font-medium text-gray-700 mb-2">Jornada</label>
                    <select id="jornada" v-model="selectedJornada" @change="fetchModelosPorJornada"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                        <option value="">Seleccione una jornada</option>
                        <option v-for="jornada in jornadas" :key="jornada" :value="jornada">{{ jornada }}</option>
                    </select>
                </div>

                <div v-if="modelos.length" class="mb-4">
                    <label for="modelo" class="block text-sm font-medium text-gray-700 mb-2">Modelo en {{
                        selectedJornada }}</label>
                    <select id="modelo" v-model="selectedModelo" @change="fetchPaginasPorModelo"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                        <option value="">Seleccione un modelo</option>
                        <option v-for="modelo in modelos" :key="modelo.id" :value="modelo.id">
                            {{ modelo.nombre_usuario }}
                        </option>
                    </select>
                </div>
            </div>

            <!-- Sección de Registro de Ganancias -->
            <div v-if="paginas.length" class="bg-white shadow-md rounded-lg p-6">
                <h2 class="text-xl font-semibold mb-4 text-gray-700">Registro de Ganancias para {{ selectedModeloNombre
                    }}</h2>
                <form @submit.prevent="registrarSupuestoGanancia">
                    <div class="grid gap-4">
                        <div v-for="pagina in paginas" :key="pagina.id" class="flex flex-col">
                            <label :for="`tokens-${pagina.id}`" class="text-sm font-medium text-gray-700 mb-1">{{
                                pagina.nombre }}</label>
                            <input type="number" :id="`tokens-${pagina.id}`" v-model="tokens[pagina.id]"
                                placeholder="Tokens generados"
                                class="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
                        </div>
                    </div>
                    <button type="submit"
                        class="mt-4 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                        Registrar Ganancias
                    </button>
                </form>
            </div>
        </div>

        <!-- Sección de Cierres de Páginas -->
        <div class="mt-8 bg-white shadow-md rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-700">Cierres de Páginas</h2>
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="cierre in cierres" :key="cierre.pagina" class="bg-gray-100 p-4 rounded-lg">
                    <h3 class="font-semibold text-lg mb-2">{{ cierre.pagina }}</h3>
                    <p class="text-sm text-gray-600">Próximo cierre: {{ formatFechaHora(cierre.proximo_cierre) }}</p>
                    <p class="text-sm text-gray-600">Días restantes: {{ cierre.dias_restantes }}</p>
                    <p class="text-sm text-gray-600">Inicio del periodo: {{ formatFechaHora(cierre.inicio_periodio) }}
                    </p>
                    <p class="text-sm text-gray-600">Fin del periodo: {{ formatFechaHora(cierre.fin_periodio) }}</p>
                </div>
            </div>
        </div>

        <!-- Sección de Establecer Meta -->
        <div class="mt-8 bg-white shadow-md rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-700">Establecer Meta por Periodo</h2>
            <form @submit.prevent="establecerMeta" class="flex items-end space-x-4">
                <div class="flex-grow">
                    <label for="meta" class="block text-sm font-medium text-gray-700 mb-1">Meta en Tokens</label>
                    <input type="number" id="meta" v-model="meta" placeholder="Meta"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
                </div>
                <button type="submit"
                    class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                    Establecer Meta
                </button>
            </form>
        </div>

        <!-- Sección de Ganancias Consolidadas -->
        <div class="mt-8 bg-white shadow-md rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-700">Ganancias Consolidadas</h2>
            <div class="flex space-x-4 mb-4">
                <div class="flex-grow">
                    <label for="periodo" class="block text-sm font-medium text-gray-700 mb-1">Periodo</label>
                    <select id="periodo" v-model="selectedPeriodo" @change="fetchGananciasConsolidadas"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                        <option value="">Seleccione un periodo</option>
                        <option v-for="periodo in periodosDisponibles" :key="periodo.id" :value="periodo.id">
                            {{ periodo.nombre }}: {{ formatFechaHora(periodo.fecha_inicio) }} - {{
                                formatFechaHora(periodo.fecha_fin) }}
                        </option>
                    </select>
                </div>
                <div>
                    <label for="tipoPeriodo" class="block text-sm font-medium text-gray-700 mb-1">Filtrar por</label>
                    <select id="tipoPeriodo" v-model="tipoPeriodo" @change="fetchGananciasConsolidadas"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                        <option value="dia">Día</option>
                        <option value="semana">Semana</option>
                        <option value="mes">Mes</option>
                    </select>
                </div>
            </div>

            <div v-if="gananciasConsolidadas" class="mt-4">
                <p class="text-lg font-semibold">Total Ganancias en Tokens: {{ gananciasConsolidadas.total_ganancias }}
                </p>
                <p class="text-lg font-semibold">Promedio de Tokens: {{ promedioTokens }}</p>
                <div class="mt-4 grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div v-for="(ganancia, modelo) in gananciasConsolidadas.ganancias_por_modelo" :key="modelo"
                        class="bg-gray-100 p-4 rounded-lg">
                        <h3 class="font-semibold">{{ modelo }}</h3>
                        <p>{{ ganancia }} tokens</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import { useModelosStore } from '~/stores/modelo';
import { useFinancieroStore } from '~/stores/financiero';

const { $notify } = useNuxtApp();
const modelosStore = useModelosStore();
const financieroStore = useFinancieroStore();

const jornadas = ref(["Tarde", "Tarde Satélite", "Noche", "Noche Satélite"]);
const selectedJornada = ref("");
const modelos = ref([]);
const selectedModelo = ref(null);
const selectedModeloNombre = ref("");
const paginas = ref([]);
const tokens = ref({});
const cierres = ref([]);
const meta = ref(0);
const selectedPeriodo = ref("");
const tipoPeriodo = ref("dia");
const gananciasConsolidadas = ref(null);
const periodosDisponibles = ref([]);

const promedioTokens = computed(() => {
    if (!gananciasConsolidadas.value) return 0;
    const totalDias = tipoPeriodo.value === "mes" ? 25 : 6;
    return (gananciasConsolidadas.value.total_ganancias / totalDias).toFixed(2);
});

const formatFechaHora = (fecha) => {
    try {
        const date = new Date(fecha);
        if (isNaN(date)) {
            console.error('Fecha inválida:', fecha);
            return 'Fecha inválida';
        }
        return format(date, "EEEE, dd 'de' MMMM 'del' yyyy HH:mm", { locale: es });
    } catch (error) {
        console.error('Error formateando la fecha:', fecha, error);
        return 'Fecha inválida';
    }
};

const fetchModelosPorJornada = async () => {
    if (selectedJornada.value) {
        try {
            modelos.value = await modelosStore.fetchModelosPorJornada(selectedJornada.value);
            selectedModelo.value = null;
            paginas.value = [];
        } catch (error) {
            $notify.error(`Error al obtener modelos: ${error.message}`);
        }
    }
};

const fetchPaginasPorModelo = async () => {
    if (selectedModelo.value) {
        try {
            paginas.value = await modelosStore.fetchPaginasPorModelo(selectedModelo.value);
            tokens.value = {};
            selectedModeloNombre.value = modelos.value.find(modelo => modelo.id === selectedModelo.value).nombre_usuario;
        } catch (error) {
            $notify.error(`Error al obtener páginas: ${error.message}`);
        }
    }
};

const registrarSupuestoGanancia = async () => {
    try {
        const supuestoGananciaData = {
            modelo_id: selectedModelo.value,
            fecha: new Date().toISOString().split('T')[0],
            paginas: paginas.value.map(pagina => ({
                pagina_id: pagina.id,
                tokens: tokens.value[pagina.id] || 0,
            })),
        };
        await modelosStore.registrarSupuestoGanancia(supuestoGananciaData);
        tokens.value = {};
        selectedModelo.value = null;
        paginas.value = [];
        $notify.success("Supuestos de ganancias registrados correctamente");
    } catch (error) {
        $notify.error(`Error al registrar ganancias: ${error.message}`);
    }
};

const fetchCierresPaginas = async () => {
    try {
        await modelosStore.fetchCierresPaginas();
        cierres.value = modelosStore.cierres;
    } catch (error) {
        $notify.error(`Error al obtener cierres de páginas: ${error.message}`);
    }
};

const establecerMeta = async () => {
    try {
        const ultimoPeriodo = await modelosStore.fetchUltimoPeriodo();
        const metaData = {
            periodo: ultimoPeriodo.periodo,
            meta: meta.value,
            fecha_inicio: ultimoPeriodo.fecha_inicio,
            fecha_fin: ultimoPeriodo.fecha_fin,
        };
        await modelosStore.establecerMeta(metaData);
        $notify.success("Meta establecida correctamente");
    } catch (error) {
        $notify.error(`Error al establecer meta: ${error.message}`);
    }
};

const fetchGananciasConsolidadas = async () => {
    try {
        if (selectedPeriodo.value) {
            gananciasConsolidadas.value = await modelosStore.fetchGananciasConsolidadas(selectedPeriodo.value, tipoPeriodo.value);
        }
    } catch (error) {
        $notify.error(`Error al obtener ganancias consolidadas: ${error.message}`);
    }
};

const fetchPeriodosDisponibles = async () => {
    try {
        periodosDisponibles.value = await modelosStore.fetchPeriodosDisponibles();
    } catch (error) {
        $notify.error(`Error al obtener periodos disponibles: ${error.message}`);
    }
};

onMounted(() => {
    fetchCierresPaginas();
    fetchPeriodosDisponibles();
});
</script>

<style scoped>
.error-message {
    color: red;
}
</style>
