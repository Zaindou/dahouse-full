<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
    <!-- Hero Section -->
    <div class="relative py-12 overflow-hidden bg-gradient-to-r from-indigo-900 to-indigo-800">
      <div class="absolute inset-0 opacity-20">
        <div class="absolute inset-0 bg-black opacity-20"></div>
        <div class="absolute inset-0" style="background-image: url('/backdrop-pattern.svg'); background-size: cover;"></div>
      </div>
      <div class="relative max-w-4xl px-4 mx-auto text-center sm:px-6">
        <h1 class="mb-4 text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
          Reglas y Condiciones - Trabajo Presencial
        </h1>
        <p class="mb-6 text-lg text-indigo-100">Conoce los lineamientos para trabajar en nuestro estudio</p>
        
        <!-- Menú de navegación para móvil -->
        <div class="flex flex-wrap justify-center gap-2 md:hidden">
          <a href="#horarios" class="px-4 py-2 text-sm font-medium text-white rounded-lg bg-indigo-700/50 backdrop-blur-sm hover:bg-indigo-700/70">
            Horarios
          </a>
          <a href="#porcentajes" class="px-4 py-2 text-sm font-medium text-white rounded-lg bg-indigo-700/50 backdrop-blur-sm hover:bg-indigo-700/70">
            Porcentajes
          </a>
          <a href="#normas" class="px-4 py-2 text-sm font-medium text-white rounded-lg bg-indigo-700/50 backdrop-blur-sm hover:bg-indigo-700/70">
            Normas
          </a>
        </div>
        
        <!-- Menú de navegación para tablet/desktop -->
        <div class="hidden p-1 space-x-1 bg-white rounded-full shadow-lg md:inline-flex">
          <a href="#horarios" class="px-6 py-3 text-sm font-medium text-indigo-900 transition-colors rounded-full hover:bg-indigo-100">
            Horarios de Trabajo
          </a>
          <a href="#porcentajes" class="px-6 py-3 text-sm font-medium text-indigo-900 transition-colors rounded-full hover:bg-indigo-100">
            Porcentajes de Ganancia
          </a>
          <a href="#normas" class="px-6 py-3 text-sm font-medium text-indigo-900 transition-colors rounded-full hover:bg-indigo-100">
            Normas del Estudio
          </a>
        </div>
      </div>
    </div>

    <!-- Horarios Section -->
    <section id="horarios" class="py-12">
      <div class="max-w-4xl px-6 mx-auto">
        <div class="mb-8 text-center">
          <h2 class="mb-2 text-2xl font-bold text-gray-900 sm:text-3xl">Horarios de Trabajo</h2>
          <p class="max-w-2xl mx-auto text-gray-600">
            Ofrecemos turnos flexibles para adaptarnos a tus necesidades
          </p>
        </div>

        <div class="grid gap-6 md:grid-cols-2">
          <!-- Tarjeta Turno Tarde -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border-t-4 border-indigo-600 rounded-lg shadow-lg group hover:-translate-y-1 hover:shadow-xl">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-indigo-500/10 to-blue-500/10 group-hover:opacity-100"></div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-16 h-16 mx-auto mb-4 text-white sm:mb-6 bg-gradient-to-br from-indigo-600 to-blue-600 rounded-xl">
                <Icon name="uil:sun" class="text-2xl" />
              </div>
              <h3 class="mb-3 text-xl font-bold text-center text-gray-900">Turno Tarde</h3>
              
              <div class="p-4 mb-4 text-center rounded-lg bg-indigo-50">
                <span class="block text-xl font-bold text-indigo-700">14:00 - 21:30</span>
                <span class="text-sm text-gray-600">6 horas de trabajo efectivo</span>
              </div>
              
              <ul class="space-y-3">
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-3 text-green-500" />
                  <span class="text-gray-700">Se permite hasta <span class="font-medium">45 minutos</span> de retraso</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-3 text-green-500" />
                  <span class="text-gray-700">Incluye tiempo para descanso.</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Tarjeta Turno Noche -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border-t-4 border-blue-600 rounded-lg shadow-lg group hover:-translate-y-1 hover:shadow-xl">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 group-hover:opacity-100"></div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-16 h-16 mx-auto mb-4 text-white sm:mb-6 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-xl">
                <Icon name="uil:moon" class="text-2xl" />
              </div>
              <h3 class="mb-3 text-xl font-bold text-center text-gray-900">Turno Noche</h3>
              
              <div class="p-4 mb-4 text-center rounded-lg bg-blue-50">
                <span class="block text-xl font-bold text-blue-700">22:00 - 06:00</span>
                <span class="text-sm text-gray-600">7 horas de trabajo efectivo</span>
              </div>
              
              <ul class="space-y-3">
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-3 text-green-500" />
                  <span class="text-gray-700">Se permite hasta <span class="font-medium">1 hora</span> de retraso</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Porcentajes Section -->
    <section id="porcentajes" class="py-12 bg-white">
      <div class="max-w-4xl px-6 mx-auto">
        <div class="mb-8 text-center">
          <h2 class="mb-2 text-2xl font-bold text-gray-900 sm:text-3xl">Porcentajes de Ganancia</h2>
          <p class="max-w-2xl mx-auto text-gray-600">
            Sistema de ingresos con bonificaciones progresivas
          </p>
        </div>

        <div class="overflow-hidden bg-white border border-gray-200 rounded-lg shadow-lg">
          <div class="px-6 py-5 bg-gradient-to-r from-indigo-700 to-indigo-800">
            <h3 class="text-xl font-semibold text-white">Distribución Base de Ganancias</h3>
          </div>

          <div class="p-6 bg-gradient-to-b from-indigo-50 to-white">
            <!-- Banner destacando 70% al inicio -->
            <div class="p-4 mb-2 text-white rounded-lg bg-gradient-to-r from-indigo-600 to-indigo-700">
              <div class="flex items-center justify-between">
                <h4 class="flex items-center font-medium">
                  <Icon name="uil:trophy" class="mr-2" /> Máxima Ganancia Posible
                </h4>
                <div class="text-2xl font-bold">70%</div>
              </div>
              <p class="mt-1 text-sm text-indigo-100">
                50% base + 20% en bonos (4 bonos de 5% cada uno)
              </p>
            </div>
            
            <p class="mb-6 text-gray-700">
              Para el trabajo en modalidad presencial, los porcentajes <span class="font-medium">base</span> de ganancia se distribuyen de la siguiente manera:
            </p>

            <div class="grid grid-cols-2 gap-4 mb-8">
              <div class="p-5 text-center transition-all duration-300 rounded-lg bg-indigo-50 hover:bg-indigo-100">
                <div class="mb-2 text-indigo-800">
                  <Icon name="uil:user" class="mx-auto text-4xl" />
                </div>
                <p class="mb-1 text-sm font-medium text-gray-500">Modelo</p>
                <p class="text-3xl font-bold text-indigo-700">50%</p>
                <p class="mt-2 text-xs text-gray-500">porcentaje base garantizado</p>
              </div>
              
              <div class="p-5 text-center transition-all duration-300 rounded-lg bg-indigo-50 hover:bg-indigo-100">
                <div class="mb-2 text-indigo-800">
                  <Icon name="uil:building" class="mx-auto text-4xl" />
                </div>
                <p class="mb-1 text-sm font-medium text-gray-500">Estudio</p>
                <p class="text-3xl font-bold text-indigo-700">50%</p>
                <p class="mt-2 text-xs text-gray-500">para mantenimiento y servicios</p>
              </div>
            </div>
            
            <!-- Sistema de Bonos -->
            <div class="mb-6 overflow-hidden border border-indigo-200 rounded-lg">
              <div class="px-4 py-3 bg-indigo-100">
                <h4 class="flex items-center text-lg font-medium text-indigo-800">
                  <Icon name="uil:star" class="mr-2" /> Sistema de Bonificaciones
                </h4>
              </div>
              
              <div class="p-4 sm:p-5">
                <p class="mb-4 text-sm text-gray-700">
                  Nuestro sistema de bonos te permite aumentar tu ganancia base de 50% hasta un 70% de comisión:
                </p>
                
                <!-- Bonos en formato de lista vertical para mejor visualización en móvil -->
                <div class="mb-5 space-y-3">
                  <!-- Bono 1 -->
                  <div class="p-3 bg-white border border-indigo-100 rounded-lg shadow-sm">
                    <div class="flex items-center">
                      <div class="flex items-center justify-center flex-shrink-0 mr-3 text-sm font-bold text-white bg-indigo-600 rounded-full w-7 h-7 sm:w-8 sm:h-8 sm:text-base">1</div>
                      <div>
                        <h5 class="text-sm font-medium text-indigo-900 sm:text-base">Bono de Asistencia (+5%)</h5>
                        <p class="mt-1 text-xs text-gray-600 sm:text-sm">
                          Por cumplir con al menos el 90% de las horas programadas.
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Bono 2 -->
                  <div class="p-3 bg-white border border-indigo-100 rounded-lg shadow-sm">
                    <div class="flex items-center">
                      <div class="flex items-center justify-center flex-shrink-0 mr-3 text-sm font-bold text-white bg-indigo-600 rounded-full w-7 h-7 sm:w-8 sm:h-8 sm:text-base">2</div>
                      <div>
                        <h5 class="text-sm font-medium text-indigo-900 sm:text-base">Bono Meta Básica (+5%)</h5>
                        <p class="mt-1 text-xs text-gray-600 sm:text-sm">
                          Al superar tu meta base personalizada de tokens.
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Bono 3 -->
                  <div class="p-3 bg-white border border-indigo-100 rounded-lg shadow-sm">
                    <div class="flex items-center">
                      <div class="flex items-center justify-center flex-shrink-0 mr-3 text-sm font-bold text-white bg-indigo-600 rounded-full w-7 h-7 sm:w-8 sm:h-8 sm:text-base">3</div>
                      <div>
                        <h5 class="text-sm font-medium text-indigo-900 sm:text-base">Bono Meta Intermedia (+5%)</h5>
                        <p class="mt-1 text-xs text-gray-600 sm:text-sm">
                          Al superar tu meta base + 50% adicional.
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Bono 4 -->
                  <div class="p-3 bg-white border border-indigo-100 rounded-lg shadow-sm">
                    <div class="flex items-center">
                      <div class="flex items-center justify-center flex-shrink-0 mr-3 text-sm font-bold text-white bg-indigo-600 rounded-full w-7 h-7 sm:w-8 sm:h-8 sm:text-base">4</div>
                      <div>
                        <h5 class="text-sm font-medium text-indigo-900 sm:text-base">Bono Meta Top (+5%)</h5>
                        <p class="mt-1 text-xs text-gray-600 sm:text-sm">
                          Al superar tu meta base + 100% adicional.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Ejemplo simplificado -->
                <div class="p-3 rounded-lg bg-indigo-50">
                  <h5 class="mb-2 text-sm font-medium text-indigo-800 sm:text-base">Ejemplo de Metas</h5>
                  
                  <div class="overflow-x-auto">
                    <table class="w-full bg-white border border-indigo-100 rounded-lg">
                      <thead>
                        <tr class="text-left text-white bg-indigo-600">
                          <th class="p-2 text-xs font-medium sm:text-sm">Meta</th>
                          <th class="p-2 text-xs font-medium text-right sm:text-sm">Tokens</th>
                          <th class="p-2 text-xs font-medium text-right sm:text-sm">Bono</th>
                        </tr>
                      </thead>
                      <tbody class="divide-y divide-indigo-50">
                        <tr>
                          <td class="p-2 text-xs text-gray-800 sm:text-sm">Base</td>
                          <td class="p-2 text-xs text-right text-gray-800 sm:text-sm">10,000</td>
                          <td class="p-2 text-xs font-medium text-right text-indigo-700 sm:text-sm">+5%</td>
                        </tr>
                        <tr>
                          <td class="p-2 text-xs text-gray-800 sm:text-sm">Intermedia</td>
                          <td class="p-2 text-xs text-right text-gray-800 sm:text-sm">15,000</td>
                          <td class="p-2 text-xs font-medium text-right text-indigo-700 sm:text-sm">+5%</td>
                        </tr>
                        <tr>
                          <td class="p-2 text-xs text-gray-800 sm:text-sm">Top</td>
                          <td class="p-2 text-xs text-right text-gray-800 sm:text-sm">20,000</td>
                          <td class="p-2 text-xs font-medium text-right text-indigo-700 sm:text-sm">+5%</td>
                        </tr>
                      </tbody>
                      <tfoot>
                        <tr class="bg-indigo-100">
                          <td class="p-2 text-xs font-medium text-indigo-800 sm:text-sm">Comisión Total</td>
                          <td class="p-2 text-xs text-right sm:text-sm"></td>
                          <td class="p-2 text-xs font-bold text-right text-indigo-800 sm:text-sm">50% + 15% = 65%</td>
                        </tr>
                      </tfoot>
                    </table>
                  </div>
                  
                  <p class="mt-2 text-xs text-center text-gray-500">Las metas se personalizan según tu historial y potencial.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Normas Section -->
    <section id="normas" class="py-12 bg-gradient-to-b from-gray-100 to-white">
      <div class="max-w-4xl px-6 mx-auto">
        <div class="mb-8 text-center">
          <h2 class="mb-2 text-2xl font-bold text-gray-900 sm:text-3xl">Normas del Estudio</h2>
          <p class="max-w-2xl mx-auto text-gray-600">
            Lineamientos para mantener un ambiente de trabajo profesional
          </p>
        </div>

        <div class="grid gap-6 md:grid-cols-3">
          <!-- Tarjeta de Instalaciones -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border border-gray-200 rounded-lg shadow-md group hover:-translate-y-1 hover:shadow-lg">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-indigo-500/5 to-blue-500/5 group-hover:opacity-100"></div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-12 h-12 mb-4 text-white bg-gradient-to-br from-indigo-600 to-blue-600 rounded-xl">
                <Icon name="uil:desktop" class="text-xl" />
              </div>
              <h3 class="mb-3 text-lg font-semibold text-gray-900">Instalaciones</h3>
              <ul class="space-y-2">
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-indigo-600" />
                  <span class="text-sm text-gray-700">El estudio proporciona todo el equipamiento necesario</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-indigo-600" />
                  <span class="text-sm text-gray-700">Incluye cámaras, iluminación y decoración</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-indigo-600" />
                  <span class="text-sm text-gray-700">Conexión a internet de alta velocidad</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-indigo-600" />
                  <span class="text-sm text-gray-700">Se debe mantener limpio el espacio de trabajo</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Tarjeta de Asistencia -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border border-gray-200 rounded-lg shadow-md group hover:-translate-y-1 hover:shadow-lg">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-indigo-500/5 to-blue-500/5 group-hover:opacity-100"></div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-12 h-12 mb-4 text-white bg-gradient-to-br from-indigo-600 to-blue-600 rounded-xl">
                <Icon name="uil:calendar-alt" class="text-xl" />
              </div>
              <h3 class="mb-3 text-lg font-semibold text-gray-900">Asistencia</h3>
              <ul class="space-y-2">
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-indigo-600" />
                  <span class="text-sm text-gray-700">Las inasistencias deben notificarse con 48 horas de anticipación</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-indigo-600" />
                  <span class="text-sm text-gray-700">Se permiten cambios de turno con previo aviso</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:exclamation-triangle" class="flex-shrink-0 mt-1 mr-2 text-yellow-600" />
                  <span class="text-sm text-gray-700">Inasistencias no notificadas podrían resultar en penalizaciones</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Tarjeta de Pagos -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border border-gray-200 rounded-lg shadow-md group hover:-translate-y-1 hover:shadow-lg">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-indigo-500/5 to-blue-500/5 group-hover:opacity-100"></div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-12 h-12 mb-4 text-white bg-gradient-to-br from-indigo-600 to-blue-600 rounded-xl">
                <Icon name="uil:money-bill" class="text-xl" />
              </div>
              <h3 class="mb-3 text-lg font-semibold text-gray-900">Pagos</h3>
              <ul class="space-y-2">
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-indigo-600" />
                  <span class="text-sm text-gray-700">Los pagos se realizan quincenalmente cada martes</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-indigo-600" />
                  <span class="text-sm text-gray-700">El estudio se encarga de todos los trámites administrativos</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-indigo-600" />
                  <span class="text-sm text-gray-700">El pago se realiza mediante transferencia bancaria</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Botones de navegación -->
    <section class="py-10 bg-white">
      <div class="max-w-4xl px-6 mx-auto">
        <div class="flex flex-col items-center justify-between gap-4 p-6 border border-gray-200 rounded-lg shadow-md sm:flex-row bg-gradient-to-r from-indigo-50 to-white">
          <div>
            <h3 class="mb-1 text-lg font-semibold text-gray-900">¿Necesitas más información?</h3>
            <p class="text-sm text-gray-600">Contáctanos o consulta todas nuestras opciones</p>
          </div>
          
          <div class="flex flex-wrap gap-3">
            <NuxtLink to="/rules" class="inline-flex items-center px-4 py-2 text-sm font-medium text-indigo-700 transition-colors bg-white border border-indigo-600 rounded-lg hover:bg-indigo-50">
              <Icon name="uil:arrow-left" class="mr-2" />
              Volver a Reglas
            </NuxtLink>
            
            <NuxtLink to="/rules/remote" class="inline-flex items-center px-4 py-2 text-sm font-medium text-white transition-colors bg-indigo-600 rounded-lg hover:bg-indigo-700">
              Ver reglas para Remoto
              <Icon name="uil:arrow-right" class="ml-2" />
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-12 bg-gradient-to-r from-indigo-900 to-indigo-800">
      <div class="max-w-4xl px-6 mx-auto text-center">
        <h2 class="mb-4 text-2xl font-bold text-white sm:text-3xl">¿Listo para unirte a nuestro estudio?</h2>
        <p class="mb-8 text-lg text-indigo-100">
          Trabaja con el mejor equipo y en las mejores instalaciones
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <NuxtLink to="/registro" class="px-8 py-3 font-medium text-indigo-900 transition-colors bg-white border-2 border-white rounded-lg hover:bg-indigo-50">
            Registrarme ahora
          </NuxtLink>
          <NuxtLink to="/contacto" class="px-8 py-3 font-medium text-white transition-colors bg-transparent border-2 border-white rounded-lg hover:bg-white/10">
            Agendar una visita
          </NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// Puedes agregar cualquier lógica necesaria aquí si se requiere
</script>