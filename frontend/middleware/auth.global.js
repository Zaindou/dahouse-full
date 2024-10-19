// middleware/auth.global.js
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  const token = useCookie("token").value;

  if (to.path === "/") {
    return;
  }

  if (!authStore.isAuthenticated && !token) {
    return navigateTo("/");
  }

  if (token && !authStore.token) {
    authStore.token = token;
    authStore.fetchUser();
  }
});
