// src/store/financieroStore.js
import { defineStore } from "pinia";
import axios from "axios";

export const useFinancieroStore = defineStore("financiero", {
  state: () => ({
    datosFinancieros: null,
    error: null,
  }),
  actions: {
    async fetchDatosFinancieros() {
      try {
        const response = await axios.get(
          `${useRuntimeConfig().public.apiUrl}/financiero`
        );
        this.datosFinancieros = response.data;
        return response.data;
      } catch (error) {
        this.error = error.message;
      }
    },
  },
});
