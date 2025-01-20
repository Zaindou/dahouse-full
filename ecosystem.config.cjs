module.exports = {
  apps: [
    {
      name: "NuxtFrontend", // Nombre del proceso del frontend
      port: 3001, // Puerto donde correrá el frontend
      exec_mode: "cluster", // Modo cluster
      instances: "6", // Usa todas las CPU disponibles
      script: "/var/www/dahouse-full/frontend/.output/server/index.mjs", // Ruta al servidor Nuxt
      env: {
        NODE_ENV: "production",
      },
    },
    {
      name: "Backend", // Nombre del proceso del backend
      script: "/var/www/dahouse-full/env/bin/gunicorn", // Ruta a Gunicorn dentro del entorno virtual
      args: "--bind 0.0.0.0:8000 app:app", // Cambia 'app:app' si el archivo principal tiene otro nombre
      cwd: "/var/www/dahouse-full", // Ruta al backend
      env: {
        NODE_ENV: "production",
      },
    },
  ],
  deploy: {
    production: {
      user: "dahouse", // Usuario SSH
      host: "152.201.100.105", // IP del servidor
      ref: "origin/main", // Rama principal
      repo: "git@github.com:Zaindou/dahouse-full.git", // Repositorio
      path: "/var/www/dahouse-full", // Ruta de despliegue
      "post-deploy":
        "yarn install --cwd ./frontend && yarn build --cwd ./frontend && pm2 reload ecosystem.config.js --env production",
    },
  },
};
