import { defineStore } from "pinia";
import { useCookie } from "#app";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: useCookie("token").value || null,
    refreshToken: useCookie("refresh_token").value || null,
    tokenExpiration: useCookie("tokenExpiration").value || null,
  }),

  actions: {
    async login(credentials) {
      try {
        const data = await $fetch(`/api/auth/login`, {
          method: "POST",
          body: credentials,
        });

        this.token = data.access_token;
        this.refreshToken = data.refresh_token;

        // Decodificar el token para obtener la fecha de expiración
        const tokenPayload = JSON.parse(atob(this.token.split(".")[1]));
        const expiration = tokenPayload.exp * 1000;

        // Guardar en cookies
        useCookie("token").value = this.token;
        useCookie("refresh_token").value = this.refreshToken;
        useCookie("tokenExpiration").value = expiration;

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
          `/api/auth/user`,
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );

        this.user = userData;
      } catch (error) {
        console.error("Error al obtener datos del usuario:", error);

        if (error.response?.status === 401) {
          console.warn("Token expirado. Intentando renovar...");
          await this.refreshTokenRequest();
        }
      }
    },

    async refreshTokenRequest() {
      if (!this.refreshToken) {
        console.warn("No hay refresh token. Cerrando sesión.");
        this.logout();
        return;
      }

      try {
        const data = await $fetch(`/api/auth/refresh`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${this.refreshToken}`,
          },
        });

        this.token = data.access_token;

        // Decodificar el nuevo token
        const tokenPayload = JSON.parse(atob(this.token.split(".")[1]));
        const expiration = tokenPayload.exp * 1000;

        // Actualizar cookies
        useCookie("token").value = this.token;
        useCookie("tokenExpiration").value = expiration;

        await this.fetchUser();
      } catch (error) {
        console.error("Error al refrescar el token:", error);
        this.logout();
      }
    },

    checkTokenExpiration() {
      const now = Date.now();
      const expiration = this.tokenExpiration ? Number(this.tokenExpiration) : null;

      if (expiration && now >= expiration) {
        console.warn("Token expirado. Intentando renovar...");
        this.refreshTokenRequest();
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      this.refreshToken = null;
      this.tokenExpiration = null;

      useCookie("token").value = null;
      useCookie("refresh_token").value = null;
      useCookie("tokenExpiration").value = null;

      navigateTo("/login");
    },
  },

  getters: {
    isAuthenticated: (state) =>
      !!state.token && Date.now() < (state.tokenExpiration || 0),
    userName: (state) => (state.user ? `${state.user.nombre_usuario}` : "No identificado"),
    mail: (state) => (state.user ? `${state.user.correo_electronico}` : ""),
  },
});
