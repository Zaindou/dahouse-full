// stores/earnings.js
import { defineStore } from "pinia";

export const useEarningsStore = defineStore("earnings", {
  state: () => ({
    meses: [],
    modelos: [],
    selectedMes: null,
    selectedSubPeriodo: "",
    earningsData: null,
    summaryData: null,
    distributionData: null,
    goalProgress: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchInitialData() {
      try {
        this.loading = true;
        const response = await fetch("/api/earnings/initial-data");
        const data = await response.json();
        this.meses = data.meses_disponibles;
        this.modelos = data.modelos_con_ganancias;
        this.selectedMes = this.meses[0];
      } catch (error) {
        this.error = "Error al cargar datos iniciales";
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async fetchEarnings(periodo, subperiodo = "", nickname = "") {
      try {
        this.loading = true;
        let url = `/api/earnings/?periodo=${periodo}`;
        if (subperiodo) url += `&subperiodo=${subperiodo}`;
        if (nickname) url += `&nickname=${nickname}`;

        const response = await fetch(url);
        const data = await response.json();
        this.earningsData = data;
      } catch (error) {
        this.error = "Error al cargar ganancias";
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async fetchSummary(periodo, nickname) {
      if (!periodo || !nickname) return;

      try {
        this.loading = true;
        const response = await fetch(
          `/api/earnings/summary?periodo=${periodo}&nickname=${nickname}`
        );
        const data = await response.json();
        this.summaryData = data;
      } catch (error) {
        this.error = "Error al cargar resumen";
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async fetchDistribution(
      periodo,
      subperiodo = "",
      nickname = "",
      date = ""
    ) {
      try {
        this.loading = true;

        let url = new URL("/api/earnings/distribution", window.location.origin);
        url.searchParams.append("periodo", periodo);

        if (subperiodo) url.searchParams.append("subperiodo", subperiodo);
        if (nickname) url.searchParams.append("nickname", nickname);
        if (date) url.searchParams.append("date", date);

        const response = await fetch(url);
        const data = await response.json();
        this.distributionData = data;
      } catch (error) {
        this.error = "Error al cargar distribución";
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async fetchGoalProgress(periodo) {
      try {
        this.loading = true;
        const response = await fetch(
          `/api/earnings/goal_progress?periodo=${periodo}`
        );
        const data = await response.json();
        this.goalProgress = data;
      } catch (error) {
        this.error = "Error al cargar progreso de metas";
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
  },
});
