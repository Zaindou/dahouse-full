// En tu tienda Pinia (stores/modelos.js)
import { defineStore } from "pinia";
import axios from "axios";

export const useModelosStore = defineStore("modelos", {
  state: () => ({
    modelos: [],
    error: null,
    gananciaInfo: null,
  }),
  actions: {
    async fetchModelos() {
      try {
        const response = await axios.get(
          `${useRuntimeConfig().public.apiUrl}/modelos`
        );
        this.modelos = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async addModelo(modeloData) {
      try {
        const response = await axios.post(
          `${useRuntimeConfig().public.apiUrl}/modelos`,
          modeloData
        );
        this.modelos.push(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async editModelo(modeloData) {
      try {
        const response = await axios.put(
          `${useRuntimeConfig().public.apiUrl}/modelos/${modeloData.id}`,
          modeloData
        );
        const index = this.modelos.findIndex(
          (modelo) => modelo.id === modeloData.id
        );
        this.modelos[index] = response.data;

        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
        console.log(error.response?.data?.mensaje || error.message);
      }
    },
    async deleteModelo(modeloId) {
      try {
        const response = await axios.delete(
          `${useRuntimeConfig().public.apiUrl}/modelos/${modeloId}`
        );
        this.modelos = this.modelos.filter((modelo) => modelo.id !== modeloId);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async fetchRolesDisponibles() {
      try {
        const response = await axios.get(
          `${useRuntimeConfig().public.apiUrl}/roles`
        );
        console.log(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async fetchPaginasDisponibles() {
      try {
        const response = await axios.get(
          `${useRuntimeConfig().public.apiUrl}/paginas`
        );
        console.log(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async liquidarGanancias(gananciaForm) {
      try {
        const response = await axios.post(
          `${useRuntimeConfig().public.apiUrl}/ganancias`,
          gananciaForm
        );
        console.log(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async fetchGananciaInfo(nombreUsuario, nombrePeriodo) {
      try {
        const response = await axios.get(
          `${
            useRuntimeConfig().public.apiUrl
          }/ganancias/usuario/${nombreUsuario}/periodo/${nombrePeriodo}`
        );
        this.gananciaInfo = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
        this.gananciaInfo = null;
      }
    },
    async crearDeduccion(nombreUsuario, DeducibleData) {
      try {
        const response = await axios.post(
          `${
            useRuntimeConfig().public.apiUrl
          }/modelos/${nombreUsuario}/creardeducible`,
          DeducibleData
        );
        console.log(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
  },
});
