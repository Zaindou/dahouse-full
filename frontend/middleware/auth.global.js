// middleware/auth.global.js
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  const token = useCookie("token").value;

  // Si hay token pero no está en el store, actualiza el store
  if (token && !authStore.token) {
    authStore.token = token;
    authStore.fetchUser();
  }

  // Permite acceder a la ruta /password-reset sin autenticación
  if (to.path === "/password-reset") {
    return;
  }

  // Redirige al dashboard si está autenticado y va al login
  if ((authStore.isAuthenticated || token) && to.path === "/") {
    return navigateTo("/dashboard");
  }

  // Redirige al login si no está autenticado y no va al login
  if (!authStore.isAuthenticated && !token && to.path !== "/") {
    return navigateTo("/");
  }
});
