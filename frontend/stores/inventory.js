import { defineStore } from "pinia";

export const useInventoryStore = defineStore("inventory", {
  state: () => ({
    items: [],
    categories: [],
    loading: false,
  }),

  actions: {
    async fetchCategories() {
      try {
        this.loading = true;
        const categories = await $fetch("/api/categorias", {
          credentials: 'omit',
          headers: {
            'Authorization': `Bearer ${useCookie('token').value}`
          }
        });
        this.categories = categories || [];
      } catch (e) {
        console.error("Error al obtener categorías:", e);
      } finally {
        this.loading = false;
      }
    },

    async fetchItems() {
      try {
        this.loading = true;
        const items = await $fetch("/api/inventario", {
          credentials: 'omit',
          headers: {
            'Authorization': `Bearer ${useCookie('token').value}`
          }
        });
        this.items = items || [];
      } catch (e) {
        console.error("Error al obtener ítems:", e);
      } finally {
        this.loading = false;
      }
    },

    async addItem(item) {
      try {
        const data = await $fetch("/api/inventario", {
          method: "POST",
          body: item,
          credentials: 'omit',
          headers: {
            'Authorization': `Bearer ${useCookie('token').value}`,
            'Content-Type': 'application/json'
          }
        });
        await this.fetchItems();
        return data;
      } catch (e) {
        console.error("Error al crear ítem:", e);
        throw e;
      }
    },

    async updateItem(id, item) {
      try {
        const data = await $fetch(`/api/inventario/${id}`, {
          method: "PUT",
          body: item,
          credentials: 'omit',
          headers: {
            'Authorization': `Bearer ${useCookie('token').value}`,
            'Content-Type': 'application/json'
          }
        });
        await this.fetchItems();
        return data;
      } catch (e) {
        console.error("Error al actualizar ítem:", e);
        throw e;
      }
    },

    async deleteItem(id) {
      try {
        const data = await $fetch(`/api/inventario/${id}`, {
          method: "DELETE",
          credentials: 'omit',
          headers: {
            'Authorization': `Bearer ${useCookie('token').value}`
          }
        });
        await this.fetchItems();
        return data;
      } catch (e) {
        console.error("Error al eliminar ítem:", e);
        throw e;
      }
    },

    async addCategory(category) {
      try {
        const data = await $fetch("/api/categorias", {
          method: "POST",
          body: category,
          credentials: 'omit',
          headers: {
            'Authorization': `Bearer ${useCookie('token').value}`,
            'Content-Type': 'application/json'
          }
        });
        await this.fetchCategories();
        return data;
      } catch (e) {
        console.error("Error al crear categoría:", e);
        throw e;
      }
    }
  }
});