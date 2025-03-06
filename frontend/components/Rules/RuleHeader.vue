// componentes/rules/RuleHeader.vue - Componente para el encabezado de la página
<template>
  <header class="text-white bg-gray-800">
    <div class="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <h1 class="text-xl font-bold">Estudio Webcams</h1>
          </div>
        </div>
        
        <nav class="flex space-x-4">
          <NuxtLink to="/" class="px-3 py-2 text-sm font-medium rounded-md hover:bg-gray-700">
            Inicio
          </NuxtLink>
          <div class="relative group">
            <button class="flex items-center px-3 py-2 text-sm font-medium rounded-md hover:bg-gray-700">
              Reglas <Icon name="uil:angle-down" class="ml-1" />
            </button>
            <div class="absolute right-0 z-10 hidden w-48 py-1 mt-2 bg-white rounded-md shadow-lg group-hover:block">
              <NuxtLink to="/rules/remote" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                Trabajo Remoto
              </NuxtLink>
              <NuxtLink to="/rules/presencial" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                Trabajo Presencial
              </NuxtLink>
            </div>
          </div>
          <NuxtLink to="/contacto" class="px-3 py-2 text-sm font-medium rounded-md hover:bg-gray-700">
            Contacto
          </NuxtLink>
        </nav>
      </div>
    </div>
  </header>
</template>