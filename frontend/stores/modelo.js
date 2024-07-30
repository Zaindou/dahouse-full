import { defineStore } from "pinia";
import { useRuntimeConfig } from "#imports";

export const useModelosStore = defineStore("modelos", {
  state: () => ({
    modelos: [],
    error: null,
    gananciaInfo: null,
    cierres: [],
    jornadas: ["Tarde", "Tarde Satélite", "Noche", "Noche Satélite"],
    paginas: [],
    periodosSupuestos: [],
    gananciasSupuestasPeriodo: [],
  }),
  actions: {
    async fetchModelos() {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/modelos`
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        this.modelos = await response.json();
        return this.modelos;
      } catch (error) {
        this.error = error.message;
      }
    },
    async crearDeduccion(nombreUsuario, DeducibleData) {
      try {
        const response = await fetch(
          `${
            useRuntimeConfig().public.apiUrl
          }/modelos/${nombreUsuario}/creardeducible`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(DeducibleData),
          }
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        return await response.json();
      } catch (error) {
        this.error = error.message;
      }
    },
    async fetchGananciaInfo(nombreUsuario, nombrePeriodo) {
      try {
        const response = await fetch(
          `${
            useRuntimeConfig().public.apiUrl
          }/ganancias/usuario/${nombreUsuario}/periodo/${nombrePeriodo}`
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        this.gananciaInfo = await response.json();
        return this.gananciaInfo;
      } catch (error) {
        this.error = error.message;
        this.gananciaInfo = null;
      }
    },
    async fetchModelosPorJornada(jornada) {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/modelos/jornada/${jornada}`
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        return await response.json();
      } catch (error) {
        this.error = error.message;
      }
    },
    async fetchPaginasPorModelo(modeloId) {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/modelos/${modeloId}/paginas`
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        return await response.json();
      } catch (error) {
        this.error = error.message;
      }
    },
    async registrarSupuestoGanancia(supuestoGananciaData) {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/modelos/${
            supuestoGananciaData.modelo_id
          }/ganancias`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(supuestoGananciaData),
          }
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        return await response.json();
      } catch (error) {
        this.error = error.message;
        throw new Error(this.error); // Lanzar el error para manejarlo en el componente
      }
    },
    async fetchCierresPaginas() {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/paginas/cierres`
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        this.cierres = await response.json();
        return this.cierres;
      } catch (error) {
        this.error = error.message;
      }
    },
    async fetchPeriodosSupuestos() {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/periodos/supuestos`
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        this.periodosSupuestos = await response.json();
        return this.periodosSupuestos;
      } catch (error) {
        this.error = error.message;
      }
    },
    async fetchGananciasSupuestasPorPeriodo(inicioPeriodo, finPeriodo) {
      try {
        const response = await fetch(
          `${
            useRuntimeConfig().public.apiUrl
          }/supuestos/ganancias/periodo/${inicioPeriodo}/${finPeriodo}`
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        this.gananciasSupuestasPeriodo = await response.json();
        return this.gananciasSupuestasPeriodo;
      } catch (error) {
        this.error = error.message;
      }
    },
    async addModelo(modeloData) {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/modelos`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(modeloData),
          }
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        const nuevoModelo = await response.json();
        this.modelos.push(nuevoModelo);
        return nuevoModelo;
      } catch (error) {
        this.error = error.message;
      }
    },
    async editModelo(modeloData) {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/modelos/${modeloData.id}`,
          {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(modeloData),
          }
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        const modeloEditado = await response.json();
        const index = this.modelos.findIndex(
          (modelo) => modelo.id === modeloData.id
        );
        this.modelos[index] = modeloEditado;
        return modeloEditado;
      } catch (error) {
        this.error = error.message;
      }
    },
    async deleteModelo(modeloId) {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/modelos/${modeloId}`,
          {
            method: "DELETE",
          }
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        this.modelos = this.modelos.filter((modelo) => modelo.id !== modeloId);
        return await response.json();
      } catch (error) {
        this.error = error.message;
      }
    },
    async fetchRolesDisponibles() {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/roles`
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        return await response.json();
      } catch (error) {
        this.error = error.message;
      }
    },
    async fetchPaginasDisponibles() {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/paginas`
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        return await response.json();
      } catch (error) {
        this.error = error.message;
      }
    },
    async liquidarGanancias(gananciaForm) {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/ganancias`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(gananciaForm),
          }
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        return await response.json();
      } catch (error) {
        this.error = error.message;
      }
    },
    async fetchPeriodosDisponibles() {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/periodos`
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        this.periodosDisponibles = await response.json();
        return this.periodosDisponibles;
      } catch (error) {
        this.error = error.message;
        throw new Error(this.error);
      }
    },
    async fetchDiasDisponibles(periodoId) {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/periodos/${periodoId}/dias`
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        this.diasDisponibles = await response.json();
        return this.diasDisponibles;
      } catch (error) {
        this.error = error.message;
        throw new Error(this.error);
      }
    },
    async fetchGananciasConsolidadas(periodoId, tipoPeriodo, fecha = null) {
      try {
        let url = `${
          useRuntimeConfig().public.apiUrl
        }/ganancias/consolidadas?periodo_id=${periodoId}&tipo_periodo=${tipoPeriodo}`;
        if (fecha) {
          url += `&fecha=${fecha}`;
        }
        const response = await fetch(url);
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        return await response.json();
      } catch (error) {
        this.error = error.message;
        throw new Error(this.error);
      }
    },
    async fetchUltimoPeriodo() {
      try {
        const response = await fetch(
          `${useRuntimeConfig().public.apiUrl}/periodos/ultimo`
        );
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message);
        }
        return await response.json();
      } catch (error) {
        this.error = error.message;
        throw new Error(this.error);
      }
    },
  },
});
