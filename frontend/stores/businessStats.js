import { defineStore } from 'pinia'

const MONTH_NUMBERS = {
  'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
  'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
};

export const useBusinessStatsStore = defineStore('businessStats', {
  state: () => ({
    stats: null, // Datos crudos de la API
    loading: false,
    error: null,
    filters: {
      year: '',
      month: '',
      period: ''
    }
  }),
  
  getters: {
    // Años disponibles para los filtros
    availableYears: (state) => {
      if (!state.stats?.estadisticas_por_periodo) return []
      return [...new Set(state.stats.estadisticas_por_periodo.map(
        stat => stat.periodo.split('-')[0]
      ))].sort((a, b) => b.localeCompare(a))
    },

    // Meses disponibles para los filtros
    availableMonths: (state) => {
      if (!state.stats?.estadisticas_por_periodo) return []
      
      const months = [...new Set(state.stats.estadisticas_por_periodo
        .filter(stat => !state.filters.year || stat.periodo.startsWith(state.filters.year))
        .map(stat => {
          const [, month] = stat.periodo.split('-')
          return month
        })
      )];

      return months.sort((a, b) => MONTH_NUMBERS[a] - MONTH_NUMBERS[b]);
    },

    // Períodos disponibles para los filtros
    availablePeriods: (state) => {
      if (!state.stats?.estadisticas_por_periodo) return []
      return [...new Set(state.stats.estadisticas_por_periodo
        .filter(stat => {
          const [year, month] = stat.periodo.split('-')
          return (!state.filters.year || year === state.filters.year) &&
                 (!state.filters.month || month === state.filters.month)
        })
        .map(stat => stat.periodo.split('-')[2])
      )].sort()
    },

    // Estadísticas filtradas
    filteredStats: (state) => {
      console.log("Estadísticas sin filtrar:", state.stats);

      if (!state.stats) return null;

      const { year, month, period } = state.filters;

      const filterPeriod = (periodo) => {
        const [filterYear, filterMonth, filterPeriod] = periodo.split('-');
        return (!year || filterYear === year) &&
               (!month || filterMonth === month) &&
               (!period || filterPeriod === period);
      };

      // Estadísticas por mes filtradas
      const estadisticas_por_mes = state.stats.estadisticas_por_mes?.filter(stat => {
        const [statYear, statMonth] = stat.mes_año.split('-');
        return (!year || statYear === year) &&
               (!month || statMonth === month);
      }) || [];

      // Estadísticas por período filtradas
      const estadisticas_por_periodo = state.stats.estadisticas_por_periodo?.filter(stat => 
        filterPeriod(stat.periodo)
      ) || [];

      // Mejores modelos filtrados
      const mejores_modelos = {
        mejor_modelo_año: state.stats?.mejores_modelos?.mejor_modelo_año || [],
        mejor_modelo_por_mes: state.stats?.mejores_modelos?.mejor_modelo_por_mes || {},
        mejor_modelo_por_periodo: state.stats?.mejores_modelos?.mejor_modelo_por_periodo || {}
    };

    console.log("Datos mejores_modelos desde el store:", mejores_modelos);

      return {
        estadisticas_por_mes,
        estadisticas_por_periodo,
        mejores_modelos,
      };
    },

    // Ganancia bruta total filtrada
    totalGananciaBruta: (state) => {
      if (!state.stats?.estadisticas_por_mes) return 0
      return state.stats.estadisticas_por_mes
        .filter(stat => {
          const [year, month] = stat.mes_año.split('-')
          return (!state.filters.year || year === state.filters.year) &&
                 (!state.filters.month || month === state.filters.month)
        })
        .reduce((total, mes) => total + Number(mes.ganancia_bruta), 0)
    },
    
    // Total de tokens filtrado
    totalTokens: (state) => {
      if (!state.stats?.estadisticas_por_mes) return 0
      return state.stats.estadisticas_por_mes
        .filter(stat => {
          const [year, month] = stat.mes_año.split('-')
          return (!state.filters.year || year === state.filters.year) &&
                 (!state.filters.month || month === state.filters.month)
        })
        .reduce((total, mes) => total + Number(mes.total_tokens), 0)
    }
  },
  
  actions: {
    // Cargar datos desde la API
    async fetchStats() {
      this.loading = true;
      this.error = null;

      try {
        const response = await fetch('/api/estadisticas-negocio');
        if (!response.ok) throw new Error('Error al obtener estadísticas');

        const data = await response.json();

        // Asignar datos desde la API
        this.stats = {
          estadisticas_por_mes: data.estadisticas_por_mes || [],
          estadisticas_por_periodo: data.estadisticas_por_periodo || [],
          mejores_modelos: data.mejores_modelos || {}, // Incluyendo los mejores modelos
        };

        console.log('Datos obtenidos desde la API:', this.stats);
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Error desconocido';
        console.error('Error en fetchStats:', error);
      } finally {
        this.loading = false;
      }
    },

    // Actualizar filtros
    setFilter(filter) {
      this.filters = { ...this.filters, ...filter };
    },

    // Resetear filtros
    resetFilters() {
      this.filters = {
        year: '',
        month: '',
        period: ''
      };
    }
  }
});
