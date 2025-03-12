// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["@nuxtjs/tailwindcss", "@pinia/nuxt", 'nuxt-icon'],

  pinia: {
    storesDirs: ['./stores/**', './custom-folder/stores/**'],
  },

  plugins: [
    '~/plugins/notyf.client.js',
    '~/plugins/auth.js',
  ],

  vue: {
    compilerOptions: {
      isCustomElement: (tag) => tag === 'vue-apexcharts',
    },
  },

  build: {
    transpile: ['vue-sonner'],
  },

  nitro: {
    devProxy: {
      '/api': {
        target: process.env.API_URL, // Ajusta esto a la URL de tu backend
        changeOrigin: true,
        prependPath: true,
      }
    }
  },

  runtimeConfig: {
    public: {
      apiUrl: process.env.API_URL
    }
  },

  app: {
    head: {
      title: 'DAHOUSE',
      script: [
        // <script src="https://myawesome-lib.js"></script>
        { src: 'https://cdn.jsdelivr.net/npm/sweetalert2@11' },
        { src: 'https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js' }
      ],
      link: [
        // <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11">
        { rel: 'stylesheet', href: 'https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css' },
      ]
    }
  },

})