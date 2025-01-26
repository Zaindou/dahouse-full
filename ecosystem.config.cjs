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
      env_production: {
        NODE_ENV: "production",
      },
    },
    {
      name: "Backend",
      script: "/var/www/dahouse-full/backend/start.sh",
      cwd: "/var/www/dahouse-full/backend",
      env: {
        NODE_ENV: "production",
      },
      env_production: {
        NODE_ENV: "production",
      },
    },
  ],
  deploy: {
    production: {
      user: "dahouse", // Usuario SSH
      host: "vnc.dahouse.co", // IP del servidor
      ref: "origin/main", // Rama principal
      repo: "git@github.com:Zaindou/dahouse-full.git", // Repositorio
      path: "/var/www/dahouse-full", // Ruta de despliegue
      "post-deploy":
        "yarn install --cwd ./frontend && yarn build --cwd ./frontend && pm2 reload ecosystem.config.cjs --env production",
    },
  },
};
