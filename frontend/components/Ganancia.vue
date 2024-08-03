<template>
    <div class="container mx-auto p-4">
        <h1 class="text-3xl font-bold mb-8 text-gray-800">Gestión de Ganancias</h1>

        <!-- Sección de Jornadas y Modelos -->
        <div class="grid md:grid-cols-2 gap-8 mb-8">
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
                            <input type="text" :id="`tokens-${pagina.id}`" v-model="tokens[pagina.id]"
                                placeholder="Tokens generados"
                                class="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />

                        </div>
                    </div>
                    <div class="flex flex-col mb-4">
                        <label for="fechaRegistro" class="text-sm font-medium text-gray-700 mb-1">Fecha</label>
                        <input type="date" id="fechaRegistro" v-model="fechaRegistro"
                            :min="periodoActual.fecha_inicio - 1" :max="periodoActual.fecha_fin"
                            class="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
                    </div>
                    <button type="submit"
                        class="mt-4 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                        Registrar Ganancias
                    </button>
                </form>
            </div>
        </div>

        <!-- Sección de Cierres de Páginas -->
        <div class="bg-white shadow-md rounded-lg p-6 mb-8">
            <h2 class="text-xl font-semibold mb-4 text-gray-700">Cierres de Páginas</h2>
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="cierre in cierres" :key="cierre.pagina"
                    class="bg-gradient-to-br from-blue-50 to-blue-100 p-5 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300">
                    <h3 class="font-semibold text-lg mb-3 text-blue-800">{{ cierre.pagina }}</h3>
                    <div class="space-y-2">
                        <div class="flex items-center">
                            <CalendarIcon class="h-5 w-5 text-blue-600 mr-2" />
                            <p class="text-sm text-gray-700">
                                <span class="font-medium">Próximo cierre:</span>
                                {{ formatFechaHora(cierre.proximo_cierre) }}
                            </p>
                        </div>
                        <div class="flex items-center">
                            <ClockIcon class="h-5 w-5 text-blue-600 mr-2" />
                            <p class="text-sm text-gray-700">
                                <span class="font-medium">Días restantes:</span>
                                <span class="text-blue-600 font-bold">{{ cierre.dias_restantes }}</span>
                            </p>
                        </div>
                        <div class="flex items-center">
                            <CalendarIcon class="h-5 w-5 text-blue-600 mr-2" />
                            <p class="text-sm text-gray-700">
                                <span class="font-medium">Inicio del periodo:</span>
                                {{ formatFecha(cierre.inicio_periodo) }}
                            </p>
                        </div>
                        <div class="flex items-center">
                            <CalendarIcon class="h-5 w-5 text-blue-600 mr-2" />
                            <p class="text-sm text-gray-700">
                                <span class="font-medium">Fin del periodo:</span>
                                {{ formatFecha(cierre.fin_periodo) }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Sección de filtros mejorada -->

        <div class="bg-white shadow-md rounded-lg p-6 mb-8">
            <h2 class="text-xl font-semibold mb-4 text-gray-700">Filtros</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
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
                    <select id="tipoPeriodo" v-model="tipoPeriodo" @change="fetchDiasDisponibles"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                        <option value="dia">Día</option>
                        <option value="semana">Semana</option>
                        <option value="mes">Mes</option>
                    </select>
                </div>
                <div v-if="tipoPeriodo === 'dia'">
                    <label for="fechaFiltro" class="block text-sm font-medium text-gray-700 mb-1">Fecha</label>
                    <select id="fechaFiltro" v-model="fechaFiltro" @change="fetchGananciasConsolidadas"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                        <option value="">Seleccione una fecha</option>
                        <option v-for="fecha in diasDisponibles" :key="fecha" :value="fecha">{{ formatFecha(fecha) }}
                        </option>
                    </select>
                </div>
                <div v-if="tipoPeriodo === 'semana'">
                    <label for="semanaFiltro" class="block text-sm font-medium text-gray-700 mb-1">Semana</label>
                    <select id="semanaFiltro" v-model="semanaFiltro" @change="fetchGananciasConsolidadas"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                        <option value="">Seleccione una semana</option>
                        <option v-for="semana in semanasDisponibles" :key="semana.inicio_semana" :value="semana">
                            {{ semana.descripcion }}
                        </option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Sección de ganancias consolidadas mejorada -->
        <div v-if="gananciasConsolidadas" class="bg-white shadow-md rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-700">Ganancias Consolidadas</h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div class="bg-blue-100 p-4 rounded-lg">
                    <p class="text-lg font-semibold">Total Ganancias en Tokens</p>
                    <p class="text-3xl font-bold text-blue-600">{{ gananciasConsolidadas.total_ganancias }}</p>
                </div>
                <div class="bg-green-100 p-4 rounded-lg">
                    <p class="text-lg font-semibold">Promedio de Tokens</p>
                    <p class="text-3xl font-bold text-green-600">{{ promedioTokens }}</p>
                </div>
            </div>

            <!-- Ganancias detalladas por turno -->
            <div v-for="turno in ['Tarde', 'Tarde Satélite', 'Noche', 'Noche Satélite']" :key="turno" class="mb-6">
                <h3 class="text-xl font-semibold mt-4 mb-2">Turno {{ turno }}</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div v-for="(ganancia, modelo) in modelosPorTurno(turno)" :key="modelo"
                        class="bg-gray-100 p-4 rounded-lg hover:shadow-lg transition-shadow duration-300">
                        <h4 class="font-semibold text-lg mb-2">{{ modelo }}</h4>
                        <div class="space-y-1">
                            <p v-for="(tokens, pagina) in ganancia.por_pagina" :key="pagina" class="text-sm">
                                <span class="font-medium">{{ pagina }}:</span> {{ tokens }} tokens
                            </p>
                        </div>
                        <p class="mt-2 text-lg font-semibold text-indigo-600">Total: {{ ganancia.total }} tokens</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
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
const selectedPeriodo = ref("");
const tipoPeriodo = ref("dia");
const fechaFiltro = ref("");
const semanaFiltro = ref("");
const fechaRegistro = ref("");
const gananciasConsolidadas = ref(null);
const periodosDisponibles = ref([]);
const diasDisponibles = ref([]);
const semanasDisponibles = ref([]);

const periodoActual = computed(() => {
    const datosFinancieros = financieroStore.datosFinancieros;
    return datosFinancieros && datosFinancieros.periodo_actual
        ? {
            fecha_inicio: datosFinancieros.periodo_actual[1],
            fecha_fin: datosFinancieros.periodo_actual[2],
        }
        : { fecha_inicio: "", fecha_fin: "" };
});

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
        return format(date, "EEEE, dd 'de' MMMM 'del' yyyy HH:mm:ss", { locale: es });
    } catch (error) {
        console.error('Error formateando la fecha:', fecha, error);
        return 'Fecha inválida';
    }
};

const formatFecha = (fecha) => {
    try {
        const date = new Date(fecha);
        if (isNaN(date)) {
            console.error('Fecha inválida:', fecha);
            return 'Fecha inválida';
        }
        return format(date, "dd 'de' MMMM 'del' yyyy", { locale: es });
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
            fecha: fechaRegistro.value,
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

const fetchGananciasConsolidadas = async () => {
    try {
        if (selectedPeriodo.value) {
            let url = `${useRuntimeConfig().public.apiUrl}/ganancias/consolidadas?periodo_id=${selectedPeriodo.value}&tipo_periodo=${tipoPeriodo.value}`;
            if (tipoPeriodo.value === 'dia') {
                url += `&fecha=${fechaFiltro.value}`;
            }
            if (tipoPeriodo.value === 'semana') {
                url += `&inicio_semana=${semanaFiltro.value.inicio_semana}&fin_semana=${semanaFiltro.value.fin_semana}`;
            }
            const response = await fetch(url);
            if (!response.ok) {
                const message = await response.text();
                throw new Error(message);
            }
            gananciasConsolidadas.value = await response.json();
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

const fetchDiasDisponibles = async () => {
    try {
        if (selectedPeriodo.value && tipoPeriodo.value === 'dia') {
            const response = await fetch(`${useRuntimeConfig().public.apiUrl}/periodos/${selectedPeriodo.value}/dias`);
            if (!response.ok) {
                const message = await response.text();
                throw new Error(message);
            }
            diasDisponibles.value = await response.json();
            // Preselect the day before the current day for filtering
            const today = new Date();
            const dayBefore = new Date(today);
            dayBefore.setDate(today.getDate() - 1);
            fechaFiltro.value = dayBefore.toISOString().split('T')[0];
        }
        if (selectedPeriodo.value && tipoPeriodo.value === 'semana') {
            const response = await fetch(`${useRuntimeConfig().public.apiUrl}/periodos/${selectedPeriodo.value}/semanas`);
            if (!response.ok) {
                const message = await response.text();
                throw new Error(message);
            }
            semanasDisponibles.value = await response.json();
        }
    } catch (error) {
        $notify.error(`Error al obtener días disponibles: ${error.message}`);
    }
};

const modelosPorTurno = (turno) => {
    return Object.entries(gananciasConsolidadas.value?.ganancias_por_modelo || {})
        .filter(([_, ganancia]) => ganancia.turno === turno)
        .reduce((acc, [modelo, ganancia]) => {
            acc[modelo] = ganancia;
            return acc;
        }, {});
};

onMounted(async () => {
    await financieroStore.fetchDatosFinancieros();
    fetchCierresPaginas();
    fetchPeriodosDisponibles();
    fetchDiasDisponibles();
    if (fechaRegistro.value === "") {
        const today = new Date();
        const dayBefore = new Date(today);
        dayBefore.setDate(today.getDate() - 1);
        fechaRegistro.value = dayBefore.toISOString().split('T')[0];
    }
});

watch([selectedPeriodo, tipoPeriodo], () => {
    if (tipoPeriodo.value === 'dia' || tipoPeriodo.value === 'semana') {
        fetchDiasDisponibles();
    }
});

watch([selectedPeriodo, tipoPeriodo, fechaFiltro, semanaFiltro], () => {
    fetchGananciasConsolidadas();
});

</script>

<style scoped>
/* Estilos adicionales si son necesarios */
</style>