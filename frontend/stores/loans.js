import { defineStore } from "pinia";
import { useRuntimeConfig, useCookie } from "#imports";

export const useLoansStore = defineStore("loans", {
  state: () => ({
    error: null,
    loans: [],
  }),

  actions: {
    async crearDeduccion(nombreUsuario, DeducibleData) {
      try {
        const response = await fetch(
          `/api/loans/${nombreUsuario}/creardeducible`,
          {
            method: "POST",
            credentials: "omit",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${useCookie("token").value}`,
            },
            body: JSON.stringify(DeducibleData),
          }
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        const newLoan = await response.json();
        this.loans.push(newLoan);
        return newLoan;
      } catch (error) {
        this.error = error.message;
        throw new Error(error.message);
      }
    },

    async fetchHistorialPagos(modelo_id) {
      try {
        const response = await fetch(
          `/api/loans/historial-pagos/${modelo_id}`,
          {
            method: "GET",
          }
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        return await response.json();
      } catch (error) {
        this.error = error.message;
        throw new Error(error.message);
      }
    },
  },
});
