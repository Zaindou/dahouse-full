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
        const response = await axios.get("http://127.0.0.1:5000/modelos");
        this.modelos = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async addModelo(modeloData) {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/modelos",
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
          `http://127.0.0.1:5000/modelos/${modeloData.id}`,
          modeloData
        );
        const index = this.modelos.findIndex(
          (modelo) => modelo.id === modeloData.id
        );
        this.modelos[index] = response.data;

        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
        console.log(error.response?.data?.mensaje || error.message, "XDDDD");
      }
    },
    async deleteModelo(modeloId) {
      try {
        const response = await axios.delete(
          `http://127.0.0.1:5000/modelos/${modeloId}`
        );
        this.modelos = this.modelos.filter((modelo) => modelo.id !== modeloId);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async fetchRolesDisponibles() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/roles");
        console.log(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async fetchPaginasDisponibles() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/paginas");
        console.log(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async liquidarGanancias(gananciaForm) {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/ganancias",
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
          `http://127.0.0.1:5000/ganancias/usuario/${nombreUsuario}/periodo/${nombrePeriodo}`
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
          `http://127.0.0.1:5000/modelos/${nombreUsuario}/creardeducible`,
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
