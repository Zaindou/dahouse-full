// En tu tienda Pinia (stores/modelos.js)
import { defineStore } from "pinia";
import axios from "axios";

export const useModelosStore = defineStore("modelos", {
  state: () => ({
    modelos: [],
    error: null,
  }),
  actions: {
    async fetchModelos() {
      try {
        const response = await axios.get("http://localhost:5000/modelos");
        this.modelos = response.data;
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async addModelo(modeloData) {
      try {
        const response = await axios.post(
          "http://localhost:5000/modelos",
          modeloData
        );
        this.modelos.push(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    // Agrega aquí más acciones como editar y eliminar modelos
    async editModelo(modeloData) {
      try {
        const response = await axios.put(
          `http://localhost:5000/modelos/${modeloData.id}`,
          modeloData
        );
        const index = this.modelos.findIndex(
          (modelo) => modelo.id === modeloData.id
        );
        this.modelos[index] = response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async deleteModelo(modeloId) {
      try {
        const response = await axios.delete(
          `http://localhost:5000/modelos/${modeloId}`
        );
        this.modelos = this.modelos.filter((modelo) => modelo.id !== modeloId);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async fetchRolesDisponibles() {
      try {
        const response = await axios.get("http://localhost:5000/roles");
        console.log(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
    async fetchPaginasDisponibles() {
      try {
        const response = await axios.get("http://localhost:5000/paginas");
        console.log(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data?.mensaje || error.message;
      }
    },
  },
});
