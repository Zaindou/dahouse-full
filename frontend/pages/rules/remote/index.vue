<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
    <!-- Hero Section -->
    <div class="relative py-12 overflow-hidden bg-gradient-to-r from-purple-900 to-purple-800">
      <div class="absolute inset-0 opacity-20">
        <div class="absolute inset-0 bg-black opacity-20"></div>
        <div class="absolute inset-0" style="background-image: url('/backdrop-pattern.svg'); background-size: cover;"></div>
      </div>
      <div class="relative max-w-4xl px-4 mx-auto text-center sm:px-6">
        <h1 class="mb-4 text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
          Reglas y Condiciones - Trabajo Remoto (Satélite)
        </h1>
        <p class="mb-6 text-lg text-purple-100">Conoce los lineamientos para trabajar desde casa</p>
        
        <!-- Menú de navegación para móvil -->
        <div class="flex flex-wrap justify-center gap-2 md:hidden">
          <a href="#horarios" class="px-4 py-2 text-sm font-medium text-white rounded-lg bg-purple-700/50 backdrop-blur-sm hover:bg-purple-700/70">
            Horarios
          </a>
          <a href="#porcentajes" class="px-4 py-2 text-sm font-medium text-white rounded-lg bg-purple-700/50 backdrop-blur-sm hover:bg-purple-700/70">
            Porcentajes
          </a>
          <a href="#normas" class="px-4 py-2 text-sm font-medium text-white rounded-lg bg-purple-700/50 backdrop-blur-sm hover:bg-purple-700/70">
            Normas
          </a>
        </div>
        
        <!-- Menú de navegación para tablet/desktop -->
        <div class="hidden p-1 space-x-1 bg-white rounded-full shadow-lg md:inline-flex">
          <a href="#horarios" class="px-6 py-3 text-sm font-medium text-purple-900 transition-colors rounded-full hover:bg-purple-100">
            Horarios de Conexión
          </a>
          <a href="#porcentajes" class="px-6 py-3 text-sm font-medium text-purple-900 transition-colors rounded-full hover:bg-purple-100">
            Porcentajes de Ganancia
          </a>
          <a href="#normas" class="px-6 py-3 text-sm font-medium text-purple-900 transition-colors rounded-full hover:bg-purple-100">
            Normas Generales
          </a>
        </div>
      </div>
    </div>

    <!-- Horarios Section -->
    <section id="horarios" class="py-12">
      <div class="max-w-4xl px-6 mx-auto">
        <div class="mb-8 text-center">
          <h2 class="mb-2 text-2xl font-bold text-gray-900 sm:text-3xl">Horarios de Conexión</h2>
          <p class="max-w-2xl mx-auto text-gray-600">
            Ofrecemos turnos flexibles para adaptarnos a tus necesidades
          </p>
        </div>

        <div class="grid gap-6 md:grid-cols-2">
          <!-- Tarjeta Turno Tarde -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border-t-4 border-purple-600 rounded-lg shadow-lg group hover:-translate-y-1 hover:shadow-xl">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-purple-500/10 to-pink-500/10 group-hover:opacity-100"></div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-16 h-16 mx-auto mb-4 text-white sm:mb-6 bg-gradient-to-br from-purple-600 to-pink-600 rounded-xl">
                <Icon name="uil:sun" class="text-2xl" />
              </div>
              <h3 class="mb-3 text-xl font-bold text-center text-gray-900">Turno Tarde</h3>
              
              <div class="p-4 mb-4 text-center rounded-lg bg-purple-50">
                <span class="block text-xl font-bold text-purple-700">14:00 - 22:00</span>
                <span class="text-sm text-gray-600">8 horas de trabajo efectivo</span>
              </div>
              
              <ul class="space-y-3">
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-3 text-green-500" />
                  <span class="text-gray-700">Tiempo de gracia: Máximo <span class="font-medium">2 horas</span> después del horario pactado</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-3 text-green-500" />
                  <span class="text-gray-700">Flexibilidad para adaptarse a tu rutina diaria</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Tarjeta Turno Noche -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border-t-4 border-pink-600 rounded-lg shadow-lg group hover:-translate-y-1 hover:shadow-xl">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-pink-500/10 to-purple-500/10 group-hover:opacity-100"></div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-16 h-16 mx-auto mb-4 text-white sm:mb-6 bg-gradient-to-br from-pink-600 to-purple-600 rounded-xl">
                <Icon name="uil:moon" class="text-2xl" />
              </div>
              <h3 class="mb-3 text-xl font-bold text-center text-gray-900">Turno Noche</h3>
              
              <div class="p-4 mb-4 text-center rounded-lg bg-pink-50">
                <span class="block text-xl font-bold text-pink-700">22:00 - 06:00</span>
                <span class="text-sm text-gray-600">8 horas de trabajo efectivo</span>
              </div>
              
              <ul class="space-y-3">
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-3 text-green-500" />
                  <span class="text-gray-700">Tiempo de gracia: Máximo <span class="font-medium">2 horas</span> después del horario pactado</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-3 text-green-500" />
                  <span class="text-gray-700">Mayor tráfico y potencial de ganancias</span>
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
            La mejor tasa fija de comisión del mercado
          </p>
        </div>

        <div class="overflow-hidden bg-white border border-gray-200 rounded-lg shadow-lg">
          <div class="px-6 py-5 bg-gradient-to-r from-purple-700 to-purple-800">
            <h3 class="text-xl font-semibold text-white">Distribución de Ganancias</h3>
          </div>

          <div class="p-6 bg-gradient-to-b from-purple-50 to-white">
            <!-- Banner destacando 70% al inicio -->
            <div class="p-4 text-white rounded-lg bg-gradient-to-r from-purple-600 to-purple-700">
              <div class="flex items-center justify-between">
                <h4 class="flex items-center font-medium">
                  <Icon name="uil:trophy" class="mr-2" /> Comisión Líder del Mercado
                </h4>
                <div class="text-2xl font-bold">70%</div>
              </div>
              <p class="mt-1 text-sm text-purple-100">
                Una de las tasas más competitivas de la industria
              </p>
            </div>
            
            <p class="mb-6 text-gray-700">
              Para el trabajo en modalidad remota, ofrecemos un <span class="font-medium">porcentaje fijo superior</span> a la media del mercado, distribuido de la siguiente manera:
            </p>

            <div class="grid grid-cols-2 gap-4 mb-8">
              <div class="p-5 text-center transition-all duration-300 rounded-lg bg-purple-50 hover:bg-purple-100">
                <div class="mb-2 text-purple-800">
                  <Icon name="uil:user" class="mx-auto text-4xl" />
                </div>
                <p class="mb-1 text-sm font-medium text-gray-500">Modelo</p>
                <p class="text-3xl font-bold text-purple-700">70%</p>
                <p class="mt-2 text-xs text-gray-500">ganancia fija garantizada</p>
              </div>
              
              <div class="p-5 text-center transition-all duration-300 rounded-lg bg-purple-50 hover:bg-purple-100">
                <div class="mb-2 text-purple-800">
                  <Icon name="uil:building" class="mx-auto text-4xl" />
                </div>
                <p class="mb-1 text-sm font-medium text-gray-500">Estudio</p>
                <p class="text-3xl font-bold text-purple-700">30%</p>
                <p class="mt-2 text-xs text-gray-500">para soporte y servicios</p>
              </div>
            </div>
            
            <!-- Sistema de Ventajas -->
            <div class="mb-6 overflow-hidden border border-purple-200 rounded-lg">
              <div class="px-4 py-3 bg-purple-100">
                <h4 class="flex items-center text-lg font-medium text-purple-800">
                  <Icon name="uil:star" class="mr-2" /> Ventajas de Nuestra Comisión
                </h4>
              </div>
              
              <div class="p-4 sm:p-5">
                <p class="mb-4 text-sm text-gray-700">
                  En DAHOUSE te ofrecemos una de las mejores comisiones del mercado con un <b>70%</b> fijo garantizado:
                </p>
                
                <!-- Ventajas en formato de lista vertical -->
                <div class="mb-5 space-y-3">
                  <!-- Ventaja 1 -->
                  <div class="p-3 bg-white border border-purple-100 rounded-lg shadow-sm">
                    <div class="flex items-center">
                      <div class="flex items-center justify-center flex-shrink-0 mr-3 text-sm font-bold text-white bg-purple-600 rounded-full w-7 h-7 sm:w-8 sm:h-8 sm:text-base">1</div>
                      <div>
                        <h5 class="text-sm font-medium text-purple-900 sm:text-base">Sin letras pequeñas</h5>
                        <p class="mt-1 text-xs text-gray-600 sm:text-sm">
                          Comisión fija sin sistemas complejos ni condiciones ocultas.
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Ventaja 2 -->
                  <div class="p-3 bg-white border border-purple-100 rounded-lg shadow-sm">
                    <div class="flex items-center">
                      <div class="flex items-center justify-center flex-shrink-0 mr-3 text-sm font-bold text-white bg-purple-600 rounded-full w-7 h-7 sm:w-8 sm:h-8 sm:text-base">2</div>
                      <div>
                        <h5 class="text-sm font-medium text-purple-900 sm:text-base">Soporte Técnico Completo</h5>
                        <p class="mt-1 text-xs text-gray-600 sm:text-sm">
                          Asesoría profesional y soporte técnico 24/7 incluidos.
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Ventaja 3 -->
                  <div class="p-3 bg-white border border-purple-100 rounded-lg shadow-sm">
                    <div class="flex items-center">
                      <div class="flex items-center justify-center flex-shrink-0 mr-3 text-sm font-bold text-white bg-purple-600 rounded-full w-7 h-7 sm:w-8 sm:h-8 sm:text-base">3</div>
                      <div>
                        <h5 class="text-sm font-medium text-purple-900 sm:text-base">Pagos Puntuales</h5>
                        <p class="mt-1 text-xs text-gray-600 sm:text-sm">
                          Pagos quincenales garantizados cada martes.
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Ventaja 4 -->
                  <div class="p-3 bg-white border border-purple-100 rounded-lg shadow-sm">
                    <div class="flex items-center">
                      <div class="flex items-center justify-center flex-shrink-0 mr-3 text-sm font-bold text-white bg-purple-600 rounded-full w-7 h-7 sm:w-8 sm:h-8 sm:text-base">4</div>
                      <div>
                        <h5 class="text-sm font-medium text-purple-900 sm:text-base">Estabilidad Financiera</h5>
                        <p class="mt-1 text-xs text-gray-600 sm:text-sm">
                          Comisión superior y estable desde el primer día.
                        </p>
                      </div>
                    </div>
                  </div>
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
          <h2 class="mb-2 text-2xl font-bold text-gray-900 sm:text-3xl">Normas Generales</h2>
          <p class="max-w-2xl mx-auto text-gray-600">
            Lineamientos para mantener un trabajo profesional desde casa
          </p>
        </div>

        <div class="grid gap-6 md:grid-cols-3">
          <!-- Tarjeta de Asistencia -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border border-gray-200 rounded-lg shadow-md group hover:-translate-y-1 hover:shadow-lg">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-purple-500/5 to-pink-500/5 group-hover:opacity-100"></div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-12 h-12 mb-4 text-white bg-gradient-to-br from-purple-600 to-pink-600 rounded-xl">
                <Icon name="uil:calendar-alt" class="text-xl" />
              </div>
              <h3 class="mb-3 text-lg font-semibold text-gray-900">Asistencia</h3>
              <ul class="space-y-2">
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-purple-600" />
                  <span class="text-sm text-gray-700">Las inasistencias deben notificarse con 24 horas de anticipación</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-purple-600" />
                  <span class="text-sm text-gray-700">Se sugiere mantener un horario consistente para fidelizar audiencia</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:exclamation-triangle" class="flex-shrink-0 mt-1 mr-2 text-yellow-600" />
                  <span class="text-sm text-gray-700">Inasistencias no notificadas podrían resultar en penalizaciones</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Tarjeta de Equipamiento -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border border-gray-200 rounded-lg shadow-md group hover:-translate-y-1 hover:shadow-lg">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-purple-500/5 to-pink-500/5 group-hover:opacity-100"></div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-12 h-12 mb-4 text-white bg-gradient-to-br from-purple-600 to-pink-600 rounded-xl">
                <Icon name="uil:desktop" class="text-xl" />
              </div>
              <h3 class="mb-3 text-lg font-semibold text-gray-900">Equipamiento</h3>
              <ul class="space-y-2">
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-purple-600" />
                  <span class="text-sm text-gray-700">Debes contar con cámara, micrófono e iluminación adecuada</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-purple-600" />
                  <span class="text-sm text-gray-700">Conexión a internet estable (mínimo 10 Mbps de subida)</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-purple-600" />
                  <span class="text-sm text-gray-700">Espacio privado, silencioso y adecuadamente decorado</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Tarjeta de Pagos -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border border-gray-200 rounded-lg shadow-md group hover:-translate-y-1 hover:shadow-lg">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-purple-500/5 to-pink-500/5 group-hover:opacity-100"></div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-12 h-12 mb-4 text-white bg-gradient-to-br from-purple-600 to-pink-600 rounded-xl">
                <Icon name="uil:money-bill" class="text-xl" />
              </div>
              <h3 class="mb-3 text-lg font-semibold text-gray-900">Pagos</h3>
              <ul class="space-y-2">
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-purple-600" />
                  <span class="text-sm text-gray-700">Los pagos se realizan semanalmente cada viernes</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-purple-600" />
                  <span class="text-sm text-gray-700">Se requiere enviar factura o comprobante según indicaciones</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check" class="flex-shrink-0 mt-1 mr-2 text-purple-600" />
                  <span class="text-sm text-gray-700">Transferencia bancaria directa a tu cuenta personal</span>
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
        <div class="flex flex-col items-center justify-between gap-4 p-6 border border-gray-200 rounded-lg shadow-md sm:flex-row bg-gradient-to-r from-purple-50 to-white">
          <div>
            <h3 class="mb-1 text-lg font-semibold text-gray-900">¿Necesitas más información?</h3>
            <p class="text-sm text-gray-600">Contáctanos o consulta todas nuestras opciones</p>
          </div>
          
          <div class="flex flex-wrap gap-3">
            <NuxtLink to="/rules" class="inline-flex items-center px-4 py-2 text-sm font-medium text-purple-700 transition-colors bg-white border border-purple-600 rounded-lg hover:bg-purple-50">
              <Icon name="uil:arrow-left" class="mr-2" />
              Volver a Reglas
            </NuxtLink>
            
            <NuxtLink to="/rules/presencial" class="inline-flex items-center px-4 py-2 text-sm font-medium text-white transition-colors bg-purple-600 rounded-lg hover:bg-purple-700">
              Ver reglas Presenciales
              <Icon name="uil:arrow-right" class="ml-2" />
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-12 bg-gradient-to-r from-purple-900 to-purple-800">
      <div class="max-w-4xl px-6 mx-auto text-center">
        <h2 class="mb-4 text-2xl font-bold text-white sm:text-3xl">¿Listo para trabajar desde casa?</h2>
        <p class="mb-8 text-lg text-purple-100">
          Únete a DAHOUSE y comienza a generar ingresos con la mejor comisión del mercado
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <NuxtLink to="/registro" class="px-8 py-3 font-medium text-purple-900 transition-colors bg-white border-2 border-white rounded-lg hover:bg-purple-50">
            Registrarme ahora
          </NuxtLink>
          <NuxtLink to="/contacto" class="px-8 py-3 font-medium text-white transition-colors bg-transparent border-2 border-white rounded-lg hover:bg-white/10">
            Solicitar información
          </NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>