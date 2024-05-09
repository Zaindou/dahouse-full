// src/store/financieroStore.js
import { defineStore } from "pinia";
import axios from "axios";

const baseUrl = "https://da.dahouse.co";

export const useFinancieroStore = defineStore("financiero", {
  state: () => ({
    datosFinancieros: null,
    error: null,
  }),
  actions: {
    async fetchDatosFinancieros() {
      try {
        const response = await axios.get(`${baseUrl}/financiero`);
        console.log(response);

        this.datosFinancieros = response.data;
        return response.data;
      } catch (error) {
        this.error = error.message;
      }
    },
  },
});
