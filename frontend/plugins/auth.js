// plugins/auth.js
import { useAuthStore } from "~/stores/auth";

export default defineNuxtPlugin((nuxtApp) => {
  const authStore = useAuthStore();

  // Configurar el token en app:created
  nuxtApp.hook("app:created", () => {
    const token = useCookie("token").value;
    if (token) {
      authStore.token = token;
      authStore.fetchUser();
    }
  });

  // Interceptor para manejar respuestas no autorizadas (401)
  nuxtApp.hook("fetch:response", (response) => {
    if (response.status === 401) {
      // El token ha expirado o es inválido
      authStore.logout(); // Limpia el estado de autenticación y cookies
      navigateTo("/login"); // Redirige al usuario al login
    }
  });
});
