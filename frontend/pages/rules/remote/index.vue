// pages/rules/remote/index.vue
<template>
  <div class="max-w-4xl px-4 py-10 mx-auto sm:px-6 lg:px-8">
    <h1 class="mb-8 text-3xl font-bold text-center text-purple-700">
      Reglas y Condiciones - Trabajo Remoto
    </h1>
    
    <div class="mb-8 overflow-hidden bg-white rounded-lg shadow-lg">
      <div class="px-6 py-4 bg-purple-700">
        <h2 class="flex items-center text-xl font-semibold text-white">
          <Icon name="uil:clock" class="mr-2 text-2xl" /> Horarios de Conexión
        </h2>
      </div>
      
      <div class="p-6 space-y-4">
        <div class="pb-4 border-b">
          <h3 class="mb-2 text-lg font-medium text-gray-800">Turno Tarde</h3>
          <p class="text-gray-600">Horario de conexión: 14:00 - 22:00</p>
          <p class="mt-1 text-gray-600">Tiempo de gracia: Máximo 2 horas después del horario pactado</p>
        </div>
        
        <div>
          <h3 class="mb-2 text-lg font-medium text-gray-800">Turno Noche</h3>
          <p class="text-gray-600">Horario de conexión: 22:00 - 06:00</p>
          <p class="mt-1 text-gray-600">Tiempo de gracia: Máximo 2 horas después del horario pactado</p>
        </div>
      </div>
    </div>
    
    <div class="mb-8 overflow-hidden bg-white rounded-lg shadow-lg">
      <div class="px-6 py-4 bg-purple-700">
        <h2 class="flex items-center text-xl font-semibold text-white">
          <Icon name="uil:percentage" class="mr-2 text-2xl" /> Porcentajes de Ganancia
        </h2>
      </div>
      
      <div class="p-6">
        <p class="mb-4 text-gray-700">Para el trabajo en modalidad remota, los porcentajes de ganancia se distribuyen de la siguiente manera:</p>
        <div class="flex justify-between p-4 bg-gray-100 rounded-lg">
          <span class="font-medium">Modelo:</span>
          <span class="font-medium">60%</span>
        </div>
        <div class="flex justify-between p-4">
          <span class="font-medium">Estudio:</span>
          <span class="font-medium">40%</span>
        </div>
      </div>
    </div>
    
    <div class="overflow-hidden bg-white rounded-lg shadow-lg">
      <div class="px-6 py-4 bg-purple-700">
        <h2 class="flex items-center text-xl font-semibold text-white">
          <Icon name="uil:file-alt" class="mr-2 text-2xl" /> Normas Generales
        </h2>
      </div>
      
      <div class="p-6 space-y-4">
        <div class="pb-4 border-b">
          <h3 class="mb-2 text-lg font-medium text-gray-800">Asistencia</h3>
          <p class="text-gray-600">
            Se debe notificar con al menos 24 horas de anticipación cualquier inasistencia.
            Inasistencias no notificadas podrían resultar en penalizaciones.
          </p>
        </div>
        
        <div class="pb-4 border-b">
          <h3 class="mb-2 text-lg font-medium text-gray-800">Equipamiento</h3>
          <p class="text-gray-600">
            El modelo es responsable de mantener su equipo (cámara, micrófono, iluminación) en óptimas condiciones.
            Se debe contar con una conexión a internet estable.
          </p>
        </div>
        
        <div>
          <h3 class="mb-2 text-lg font-medium text-gray-800">Pagos</h3>
          <p class="text-gray-600">
            Los pagos se realizan semanalmente, cada viernes.
            Se requiere enviar factura o comprobante según las indicaciones del estudio.
          </p>
        </div>
      </div>
    </div>
    
    <div class="mt-8 text-center">
      <NuxtLink to="/rules/presencial" class="font-medium text-purple-600 hover:text-purple-800">
        Ver reglas para trabajo presencial →
      </NuxtLink>
    </div>
  </div>
</template>

