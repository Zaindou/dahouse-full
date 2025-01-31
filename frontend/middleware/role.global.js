export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  const userRole = authStore.user?.rol;

  // Definir qué roles pueden acceder a qué rutas
  const routePermissions = {
    "/admin/users": ["Administrador"],
    "/finance/loans": ["Administrador", 'Monitor', 'Inventario'],
    "/finance/liquidacion": ["Administrador"],
    "/finance/historial-pagos": ["Administrador"],
    "/finance/simulador": ["Administrador", 'Monitor', 'Inventario'],
    "/inventory": ["Administrador", 'Inventario'],
    "/mantenimiento": ["Administrador"],
  };

  // Si la ruta actual requiere un rol específico y el usuario no lo tiene, redirigir
  if (routePermissions[to.path] && !routePermissions[to.path].includes(userRole)) {
    return navigateTo("/dashboard"); // Redirigir a una página segura
  }
});
