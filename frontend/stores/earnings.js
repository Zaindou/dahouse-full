// stores/earnings.js
import { defineStore } from 'pinia'

export const useEarningsStore = defineStore('earnings', {
  state: () => ({
    meses: [],
    modelos: [],
    selectedMes: null,
    earningsData: null,
    summaryData: null,
    distributionData: null,
    goalProgress: null,
    loading: false,
    error: null
  }),

  actions: {
    async fetchInitialData() {
      try {
        this.loading = true
        const response = await fetch('/api/earnings/initial-data')
        const data = await response.json()
        this.meses = data.meses_disponibles
        this.modelos = data.modelos_con_ganancias
        this.selectedMes = this.meses[0]
      } catch (error) {
        this.error = 'Error al cargar datos iniciales'
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    async fetchEarnings(periodo, nickname = '') {
      try {
        this.loading = true
        const url = `/api/earnings/?periodo=${periodo}${nickname ? `&nickname=${nickname}` : ''}`
        const response = await fetch(url)
        const data = await response.json()
        this.earningsData = data
      } catch (error) {
        this.error = 'Error al cargar ganancias'
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    async fetchSummary(periodo, nickname) {
      if (!periodo || !nickname) return
      
      try {
        this.loading = true
        const response = await fetch(`/api/earnings/summary?periodo=${periodo}&nickname=${nickname}`)
        const data = await response.json()
        this.summaryData = data
      } catch (error) {
        this.error = 'Error al cargar resumen'
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    async fetchDistribution(periodo, nickname = '', date = null) {
      try {
        this.loading = true
        let url = `/api/earnings/distribution?periodo=${periodo}`
        if (nickname) url += `&nickname=${nickname}`
        if (date) url += `&date=${date}`
        
        const response = await fetch(url)
        const data = await response.json()
        this.distributionData = data
      } catch (error) {
        this.error = 'Error al cargar distribución'
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    async fetchGoalProgress(periodo) {
      try {
        this.loading = true
        const response = await fetch(`/api/earnings/goal_progress?periodo=${periodo}`)
        const data = await response.json()
        this.goalProgress = data
      } catch (error) {
        this.error = 'Error al cargar progreso de metas'
        console.error(error)
      } finally {
        this.loading = false
      }
    }
  }
})