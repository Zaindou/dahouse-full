// stores/version.js
import { defineStore } from "pinia";

export const useVersionStore = defineStore("version", {
  state: () => ({
    api: "0.0.0",
    frontend: "0.0.0",
    isLoading: false,
    error: null,
  }),

  actions: {
    async fetchVersion() {
      this.isLoading = true;
      this.error = null;

      try {
        // Usar useFetch directamente sin destructuring
        const response = await $fetch("/api/");

        // Verificar la respuesta y actualizar el estado
        if (response) {
          this.api = response.api_version;
          this.frontend = response.frontend_version;
        }

        return true;
      } catch (error) {
        console.error("Error al obtener versiones:", error);
        this.error = "Error al cargar las versiones";
        return false;
      } finally {
        this.isLoading = false;
      }
    },
  },

  getters: {
    apiVersion: (state) => state.api,
    frontVersion: (state) => state.frontend,
    hasError: (state) => state.error !== null,
  },
});

// Composable para usar el store
export const useVersion = () => {
  const store = useVersionStore();

  return {
    fetchVersion: store.fetchVersion,
    apiVersion: computed(() => store.apiVersion),
    frontVersion: computed(() => store.frontVersion),
    isLoading: computed(() => store.isLoading),
    error: computed(() => store.error),
    hasError: computed(() => store.hasError),
  };
};
