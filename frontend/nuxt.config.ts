// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["@nuxtjs/tailwindcss","@pinia/nuxt", ],
  pinia: {
    storesDirs: ['./stores/**', './custom-folder/stores/**'],
  },

  app: {
  head: {

    script: [
      // <script src="https://myawesome-lib.js"></script>
      { src: 'https://cdn.jsdelivr.net/npm/sweetalert2@11' }
    ],


  }
}

})