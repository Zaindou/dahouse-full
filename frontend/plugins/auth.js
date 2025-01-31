import { useAuthStore } from "~/stores/auth";
import { onMounted } from "vue";

export default defineNuxtPlugin((nuxtApp) => {
  const authStore = useAuthStore();

  // Configurar el token en app:created
  nuxtApp.hook("app:created", async () => {
    if (process.client) {
      const token = useCookie("token").value;

      if (token) {
        authStore.token = token;
        authStore.checkTokenExpiration();
        await authStore.fetchUser();
      }
    }
  });

  // Interceptor para agregar el token en cada solicitud
  nuxtApp.hook("fetch:request", (request) => {
    if (authStore.token) {
      request.options.headers = {
        ...request.options.headers,
        Authorization: `Bearer ${authStore.token}`,
      };
    }
  });

  // Interceptor para manejar respuestas no autorizadas (401)
  nuxtApp.hook("fetch:response", async (response) => {
    if (response.status === 401) {
      console.warn("Token expirado o inválido. Intentando refrescar...");

      // Intentar renovar el token
      const refreshed = await authStore.refreshTokenRequest();

      if (!refreshed) {
        authStore.logout();
        navigateTo("/login");
      }
    }
  });

  // ✅ Ejecutar `setInterval` solo en el cliente
  onMounted(() => {
    setInterval(() => {
      authStore.checkTokenExpiration();
    }, 60 * 1000); // Verificar cada 60 segundos
  });
});
