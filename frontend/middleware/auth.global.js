// middleware/auth.global.js
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  const token = useCookie("token").value;

  // Si hay token pero no está en el store, actualiza el store
  if (token && !authStore.token) {
    authStore.token = token;
    authStore.fetchUser();
  }

  // Lista de rutas públicas que no requieren autenticación
  const publicRoutes = ["/login/password-reset", "/rules/*", "/assets/*", "/"];

  // Función para verificar si una ruta coincide con un patrón
  const isRoutePublic = (path) => {
    return publicRoutes.some((route) => {
      if (route.endsWith("/*")) {
        const baseRoute = route.slice(0, -2); // Elimina el "/*"
        return path.startsWith(baseRoute);
      }
      // Si no tiene "/*", verifica coincidencia exacta
      return path === route;
    });
  };

  // Permite acceder a rutas públicas sin autenticación
  if (isRoutePublic(to.path)) {
    return;
  }

  // Redirige al dashboard si está autenticado y va al login
  if ((authStore.isAuthenticated || token) && to.path === "/login") {
    return navigateTo("/dashboard");
  }

  // Redirige al login si no está autenticado y no va al login
  if (!authStore.isAuthenticated && !token && to.path !== "/login") {
    return navigateTo("/login");
  }
});
