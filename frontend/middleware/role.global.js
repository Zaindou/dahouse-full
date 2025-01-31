export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();
  const userRole = authStore.user?.rol;

  // Definir qué roles pueden acceder a qué rutas
  const routePermissions = {
    "/admin/users": ["Administrador"],
    "/finance/loans": ["Administrador", 'Monitor', 'Inventario'],
    "/finance/liquidacion": ["Administrador"],
    "/finance/historial-pagos": ["Administrador"],
    "^/finance/historial-pagos/[0-9]+$": ["Administrador"],
    "/finance/simulador": ["Administrador", 'Monitor', 'Inventario'],
    "/inventory": ["Administrador", 'Inventario'],
    "/mantenimiento": ["Administrador"],
  };

  // Verificar permisos para la ruta actual
  const hasPermission = (() => {
    // Primero verificar rutas exactas
    if (routePermissions[to.path]) {
      return routePermissions[to.path].includes(userRole);
    }

    // Luego verificar rutas con patrones regex
    for (const [pattern, roles] of Object.entries(routePermissions)) {
      if (pattern.startsWith('^')) {
        const regex = new RegExp(pattern);
        if (regex.test(to.path)) {
          return roles.includes(userRole);
        }
      }
    }

    return true; // Si no hay reglas definidas para la ruta, permitir acceso
  })();

  if (!hasPermission) {
    return navigateTo("/dashboard");
  }
});