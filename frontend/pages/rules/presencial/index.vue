// pages/rules/presencial/index.vue
<template>
  <div class="max-w-4xl px-4 py-10 mx-auto sm:px-6 lg:px-8">
    <h1 class="mb-8 text-3xl font-bold text-center text-indigo-700">
      Reglas y Condiciones - Trabajo Presencial
    </h1>
    
    <div class="mb-8 overflow-hidden bg-white rounded-lg shadow-lg">
      <div class="px-6 py-4 bg-indigo-700">
        <h2 class="flex items-center text-xl font-semibold text-white">
          <Icon name="uil:clock" class="mr-2 text-2xl" /> Horarios de Trabajo
        </h2>
      </div>
      
      <div class="p-6 space-y-4">
        <div class="pb-4 border-b">
          <h3 class="mb-2 text-lg font-medium text-gray-800">Turno Tarde</h3>
          <p class="text-gray-600">Horario: 14:00 - 22:00</p>
          <p class="mt-1 text-gray-600">Llegada: Se permite hasta 30 minutos de retraso</p>
        </div>
        
        <div>
          <h3 class="mb-2 text-lg font-medium text-gray-800">Turno Noche</h3>
          <p class="text-gray-600">Horario: 22:00 - 06:00</p>
          <p class="mt-1 text-gray-600">Llegada: Se permite hasta 30 minutos de retraso</p>
        </div>
      </div>
    </div>
    
    <div class="mb-8 overflow-hidden bg-white rounded-lg shadow-lg">
      <div class="px-6 py-4 bg-indigo-700">
        <h2 class="flex items-center text-xl font-semibold text-white">
          <Icon name="uil:percentage" class="mr-2 text-2xl" /> Porcentajes de Ganancia
        </h2>
      </div>
      
      <div class="p-6">
        <p class="mb-4 text-gray-700">Para el trabajo en modalidad presencial, los porcentajes de ganancia se distribuyen de la siguiente manera:</p>
        <div class="flex justify-between p-4 bg-gray-100 rounded-lg">
          <span class="font-medium">Modelo:</span>
          <span class="font-medium">50%</span>
        </div>
        <div class="flex justify-between p-4">
          <span class="font-medium">Estudio:</span>
          <span class="font-medium">50%</span>
        </div>
      </div>
    </div>
    
    <div class="overflow-hidden bg-white rounded-lg shadow-lg">
      <div class="px-6 py-4 bg-indigo-700">
        <h2 class="flex items-center text-xl font-semibold text-white">
          <Icon name="uil:file-alt" class="mr-2 text-2xl" /> Normas del Estudio
        </h2>
      </div>
      
      <div class="p-6 space-y-4">
        <div class="pb-4 border-b">
          <h3 class="mb-2 text-lg font-medium text-gray-800">Instalaciones</h3>
          <p class="text-gray-600">
            El estudio proporciona todo el equipamiento necesario: cámaras, iluminación, decoración y conexión a internet.
            Se debe mantener limpio y ordenado el espacio de trabajo.
          </p>
        </div>
        
        <div class="pb-4 border-b">
          <h3 class="mb-2 text-lg font-medium text-gray-800">Asistencia</h3>
          <p class="text-gray-600">
            Las inasistencias deben ser notificadas con 48 horas de anticipación.
            Tres inasistencias sin justificación en un mes pueden resultar en la terminación del contrato.
          </p>
        </div>
        
        <div>
          <h3 class="mb-2 text-lg font-medium text-gray-800">Pagos</h3>
          <p class="text-gray-600">
            Los pagos se realizan semanalmente, cada viernes.
            El estudio se encarga de todos los trámites administrativos.
          </p>
        </div>
      </div>
    </div>
    
    <div class="mt-8 text-center">
      <NuxtLink to="/rules/remote" class="font-medium text-indigo-600 hover:text-indigo-800">
        Ver reglas para trabajo remoto →
      </NuxtLink>
    </div>
  </div>
</template>

