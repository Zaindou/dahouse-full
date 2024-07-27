<template>
    <div>
        <h1>Gestión de Ganancias</h1>

        <div>
            <h2>Jornadas</h2>
            <select v-model="selectedJornada" @change="fetchModelosPorJornada">
                <option v-for="jornada in jornadas" :key="jornada">{{ jornada }}</option>
            </select>
        </div>

        <div v-if="modelos.length">
            <h2>Modelos en {{ selectedJornada }}</h2>
            <select v-model="selectedModelo" @change="fetchPaginasPorModelo">
                <option v-for="modelo in modelos" :key="modelo.id" :value="modelo.id">
                    {{ modelo.nombre_usuario }}
                </option>
            </select>
        </div>

        <div v-if="paginas.length">
            <h2>Páginas Disponibles para {{ selectedModeloNombre }}</h2>
            <form @submit.prevent="registrarSupuestoGanancia">
                <div v-for="pagina in paginas" :key="pagina.id">
                    <label :for="`tokens-${pagina.id}`">{{ pagina.nombre }}</label>
                    <input type="number" :id="`tokens-${pagina.id}`" v-model="tokens[pagina.id]"
                        placeholder="Tokens generados" />
                </div>
                <button type="submit">Registrar Ganancias</button>
            </form>
        </div>

        <div>
            <h2>Cierres de Páginas</h2>
            <ul>
                <li v-for="cierre in cierres" :key="cierre.pagina">
                    {{ cierre.pagina }}: Próximo cierre el {{ cierre.proximo_cierre }} ({{ cierre.dias_restantes }} días
                    restantes).
                    Inicio del periodo: {{ cierre.inicio_periodo }}.
                </li>
            </ul>
        </div>

        <div v-if="error" class="error-message">
            <p>Error: {{ error }}</p>
        </div>
    </div>
</template>

<script>
import { useModelosStore } from '~/stores/modelo'

export default {
    data() {
        return {
            jornadas: ["Tarde", "Tarde Satélite", "Noche", "Noche Satélite"],
            selectedJornada: "",
            modelos: [],
            selectedModelo: null,
            selectedModeloNombre: "",
            paginas: [],
            tokens: {},
            cierres: [],
            error: null,
        };
    },
    computed: {
        modelosStore() {
            return useModelosStore();
        },
    },
    methods: {
        async fetchModelosPorJornada() {
            if (this.selectedJornada) {
                this.modelos = await this.modelosStore.fetchModelosPorJornada(this.selectedJornada);
                this.selectedModelo = null;
                this.paginas = [];
            }
        },
        async fetchPaginasPorModelo() {
            if (this.selectedModelo) {
                this.paginas = await this.modelosStore.fetchPaginasPorModelo(this.selectedModelo);
                this.tokens = {};
                this.selectedModeloNombre = this.modelos.find(modelo => modelo.id === this.selectedModelo).nombre_usuario;
            }
        },
        async registrarSupuestoGanancia() {
            try {
                const supuestoGananciaData = {
                    modelo_id: this.selectedModelo,
                    fecha: new Date().toISOString().split('T')[0],
                    paginas: this.paginas.map(pagina => ({
                        pagina_id: pagina.id,
                        tokens: this.tokens[pagina.id] || 0,
                    })),
                };
                await this.modelosStore.registrarSupuestoGanancia(supuestoGananciaData);
                this.tokens = {};
                this.selectedModelo = null;
                this.paginas = [];
                alert("Supuestos de ganancias registrados correctamente");
            } catch (error) {
                this.error = error.message;
            }
        },
        async fetchCierresPaginas() {
            await this.modelosStore.fetchCierresPaginas();
            this.cierres = this.modelosStore.cierres;
        },
    },
    mounted() {
        this.fetchCierresPaginas();
    },
};
</script>

<style scoped>
.error-message {
    color: red;
}
</style>
