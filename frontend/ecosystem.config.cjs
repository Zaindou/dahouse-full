module.exports = {
  apps: [
    {
      name: 'NuxtFrontend', // Nombre del proceso en PM2
      port: 3001, // Puerto en el que escuchará la aplicación
      exec_mode: 'cluster', // Modo cluster para usar múltiples instancias
      instances: 'max', // Número de instancias, puedes usar 'max' para todas las CPU disponibles
      script: '/var/www/dahouse-full/frontend/.output/server/index.mjs', // Ruta al servidor de salida generado por Nuxt3
      env: {
        NODE_ENV: 'production', // Asegúrate de que Nuxt corra en producción
      },
    },
  ],
};