import { defineStore } from "pinia";
import axios from "axios";

export const useFinancieroStore = defineStore("financiero", {
  state: () => ({
    datosFinancieros: null, // Datos generales para "financiero"
    estadisticasPorPeriodo: null, // Datos agrupados por periodo
    estadisticasPorMes: null, // Datos agrupados por mes
    tokensPorPagina: null, // Tokens por página
    deducciones: null, // Deducciones
    error: null, // Manejo de errores
  }),
  actions: {
    // Acción original para datos generales financieros
    async fetchDatosFinancieros() {
      try {
        const response = await axios.get(
          `${useRuntimeConfig().public.apiUrl}/financiero`
        );
        this.datosFinancieros = response.data;
        return response.data; // Retorna los datos para uso adicional en componentes
      } catch (error) {
        this.error = error.message;
        console.error("Error al obtener datos financieros generales:", error);
      }
    },

    // Nueva acción para estadísticas de negocio
    async fetchEstadisticasNegocio() {
      try {
        const response = await axios.get(
          `${useRuntimeConfig().public.apiUrl}/estadisticas-negocio`
        );

        // Asignar cada sección del endpoint a las propiedades del estado
        this.estadisticasPorPeriodo = response.data.estadisticas_por_periodo;
        this.estadisticasPorMes = response.data.estadisticas_por_mes;
        this.tokensPorPagina = response.data.tokens_por_pagina;
        this.deducciones = response.data.deducciones;

        return response.data; // Devuelve los datos en caso de que se necesite en el componente
      } catch (error) {
        this.error = error.message; // Manejo del error
        console.error("Error al obtener estadísticas del negocio:", error);
      }
    },
  },
});
