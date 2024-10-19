// stores/auth.js
import { defineStore } from "pinia";
import { useCookie } from "#app";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: null,
  }),
  actions: {
    async login(credentials) {
      try {
        const data = await $fetch(`${useRuntimeConfig().public.apiUrl}/login`, {
          method: "POST",
          body: credentials,
        });

        this.token = data.access_token;
        useCookie("token").value = this.token;

        await this.fetchUser();
        return true;
      } catch (error) {
        console.error("Error al iniciar sesión:", error);
        return false;
      }
    },
    async fetchUser() {
      if (!this.token) return;

      try {
        const userData = await $fetch(
          `${useRuntimeConfig().public.apiUrl}/user`,
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );

        this.user = userData;
      } catch (error) {
        console.error("Error al obtener datos del usuario:", error);
        this.logout(); // Si hay un error, cerrar sesión automáticamente
      }
    },
    logout() {
      this.user = null;
      this.token = null;
      useCookie("token").value = null; // Elimina la cookie del token
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
});
