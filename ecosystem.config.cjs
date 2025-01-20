module.exports = {
  apps: [
    {
      name: "flask-backend",
      script: "gunicorn",
      args: "--bind 0.0.0.0:8000 app:app",
      interpreter: "python3",
      cwd: "./",
    },
  ],
};
