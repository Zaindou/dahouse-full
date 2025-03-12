// pages/index.vue
<template>
  <div class="min-h-screen bg-gradient-to-b from-pink-50 to-purple-50">
<!-- Hero con experiencia móvil mejorada -->
<div class="relative w-full overflow-hidden">
  <!-- Sección de fotos a pantalla casi completa como fondo -->
  <div class="relative h-[91vh] md:h-screen">
    <!-- Grid de imágenes con efecto de transición suave (escritorio) -->
    <div class="relative hidden h-full grid-cols-3 md:grid">
      <!-- Primera imagen -->
      <div class="relative h-full overflow-hidden group">
        <img src="/landing-images/Xia-Jacuzzi.webp" alt="DAHOUSE Studio Webcam" class="object-cover w-full h-full transition-transform duration-700 group-hover:scale-105"/>
        <!-- Degradado vertical estándar -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/30 to-transparent"></div>
        
        <!-- Degradado lateral derecho para transición suave -->
        <div class="absolute top-0 bottom-0 right-0 w-8 bg-gradient-to-r from-transparent to-black/20"></div>
      </div>
      
      <!-- Segunda imagen -->
      <div class="relative h-full overflow-hidden group">
        <img src="/landing-images/Aly-mirada.webp" alt="DAHOUSE Studio Webcam" class="object-cover w-full h-full transition-transform duration-700 group-hover:scale-105"/>
        <!-- Degradado vertical estándar -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/30 to-transparent"></div>
        
        <!-- Degradados laterales para transición suave en ambos lados -->
        <div class="absolute top-0 bottom-0 left-0 w-8 bg-gradient-to-l from-transparent to-black/20"></div>
        <div class="absolute top-0 bottom-0 right-0 w-8 bg-gradient-to-r from-transparent to-black/20"></div>
      </div>
      
      <!-- Tercera imagen -->
      <div class="relative h-full overflow-hidden group">
        <img src="/landing-images/LilithJacob-mirada.webp" alt="DAHOUSE Studio Webcam Bogotá" class="object-cover w-full h-full transition-transform duration-700 group-hover:scale-105"/>
        <!-- Degradado vertical estándar -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/30 to-transparent"></div>
        
        <!-- Degradado lateral izquierdo para transición suave -->
        <div class="absolute top-0 bottom-0 left-0 w-8 bg-gradient-to-l from-transparent to-black/20"></div>
      </div>
      
      <!-- Overlay sutil que unifica las tres imágenes -->
      <div class="absolute inset-0 pointer-events-none bg-black/5"></div>
    </div>
    
    <!-- Versión móvil mejorada (autocarrusel simulado) -->
<div class="h-full md:hidden">
  <div class="relative h-full overflow-hidden">
    <!-- Imagen principal (se elige aleatoriamente) -->
    <ClientOnly>
      <img :src="randomImage" alt="DAHOUSE Studio Webcam" class="object-cover w-full h-full animate-slow-fade"/>
    </ClientOnly>
    
    <!-- Degradado optimizado para texto -->
    <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-black/20"></div>
    
    <!-- Indicador de scroll para mejorar UX -->
    <div class="absolute left-0 right-0 flex justify-center bottom-3 animate-bounce">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-white opacity-80">
        <path d="M7 13l5 5 5-5M7 7l5 5 5-5"/>
      </svg>
    </div>
  </div>
</div>
    
    <!-- Overlay decorativo para mejorar la transición -->
    <div class="absolute inset-0 pointer-events-none bg-gradient-to-b from-pink-600/30 to-transparent"></div>
    
    <!-- Contenido: Logo, menú y texto central integrados -->
    <div class="absolute inset-0 flex flex-col">
      <!-- Sección superior con logo y menú -->
      <div class="w-full pt-6 pb-3 md:pt-12 md:pb-8">
        <div class="relative max-w-5xl px-4 mx-auto text-center sm:px-6">
          <h1 class="mb-4 text-3xl font-extrabold tracking-tight text-white drop-shadow-md sm:text-4xl md:text-5xl">
            DAHOUSE
          </h1>
          
          <!-- Menú de navegación para móvil mejorado -->
          <div class="flex flex-wrap justify-center gap-2 md:hidden">
            <NuxtLink to="#modalidades" class="px-4 py-2 text-sm font-medium text-white transition-transform rounded-full shadow-md backdrop-blur-sm bg-gradient-to-r from-pink-500/40 to-purple-500/20 active:scale-95">
              Modalidades
            </NuxtLink>
            <NuxtLink to="#beneficios" class="px-4 py-2 text-sm font-medium text-white transition-transform rounded-full shadow-md backdrop-blur-sm bg-gradient-to-r from-pink-500/40 to-purple-500/20 active:scale-95">
              Beneficios
            </NuxtLink>
            <NuxtLink to="#pagos" class="px-4 py-2 text-sm font-medium text-white transition-transform rounded-full shadow-md backdrop-blur-sm bg-gradient-to-r from-pink-500/40 to-purple-500/20 active:scale-95">
              Pagos
            </NuxtLink>
            <NuxtLink to="#plataformas" class="px-4 py-2 text-sm font-medium text-white transition-transform rounded-full shadow-md backdrop-blur-sm bg-gradient-to-r from-pink-500/40 to-purple-500/20 active:scale-95">
              Plataformas
            </NuxtLink>
            <NuxtLink to="#faq" class="px-4 py-2 text-sm font-medium text-white transition-transform rounded-full shadow-md backdrop-blur-sm bg-gradient-to-r from-pink-500/40 to-purple-500/20 active:scale-95">
              FAQ
            </NuxtLink>
            
          </div>
          
          <!-- Menú de navegación para tablet/desktop con estilo integrado -->
          <div class="hidden p-1 space-x-1 rounded-full shadow-lg backdrop-blur-sm bg-white/90 md:inline-flex">
            <NuxtLink to="#modalidades" class="px-6 py-3 text-sm font-medium text-pink-700 transition-colors rounded-full hover:bg-pink-100">
              Modalidades
            </NuxtLink>
            <NuxtLink to="#beneficios" class="px-6 py-3 text-sm font-medium text-pink-700 transition-colors rounded-full hover:bg-pink-100">
              Beneficios
            </NuxtLink>
            <NuxtLink to="#pagos" class="px-6 py-3 text-sm font-medium text-pink-700 transition-colors rounded-full hover:bg-pink-100">
              Pagos
            </NuxtLink>
            <NuxtLink to="#plataformas" class="px-6 py-3 text-sm font-medium text-pink-700 transition-colors rounded-full hover:bg-pink-100">
              Plataformas
            </NuxtLink>
            <NuxtLink to="#faq" class="px-6 py-3 text-sm font-medium text-pink-700 transition-colors rounded-full hover:bg-pink-100">
              FAQ
            </NuxtLink>
          </div>
        </div>
      </div>
      
      <!-- Espacio flexible para centrar el texto descriptivo -->
      <div class="flex-grow"></div>
      
      <!-- Texto central descriptivo optimizado para móvil -->
      <div class="z-10 flex flex-col items-center justify-center p-4 mb-12 md:mb-24">
        <div class="text-center text-white">
          <!-- Versión móvil mejorada con mejor espaciado -->
          <div class="flex items-center justify-center gap-3 text-xl font-semibold drop-shadow-lg sm:hidden">
            <span>Studio</span>
            <span class="text-white-300">•</span>
            <span>Webcam</span>
            <span class="text-white-300">•</span>
            <span>Bogotá</span>
          </div>
          
          <!-- Versión tablet/desktop (con puntos) -->
          <div class="flex-row items-center justify-center hidden gap-6 text-2xl font-semibold sm:flex md:text-3xl">
            <span class="drop-shadow-md">Studio</span>
            <span>•</span>
            <span class="drop-shadow-md">Webcam</span>
            <span>•</span>
            <span class="drop-shadow-md">Bogotá</span>
          </div>
        </div>
      </div>
      
      
      <!-- Degradado inferior para suavizar la transición a la siguiente sección -->
      <div class="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-white/30 to-transparent"></div>
    </div>
  </div>
</div>

    <!-- Modalidades Section with reordered cards and softer corners -->
    <section id="modalidades" class="py-16">
      <div class="max-w-6xl px-6 mx-auto">
        <div class="text-center">
          <h2 class="mb-2 text-3xl font-bold text-gray-900">Modalidades de Trabajo</h2>
          <p class="max-w-2xl mx-auto mb-12 text-lg text-gray-600">
            Ofrecemos diferentes opciones para que trabajes de la manera que mejor se adapte a ti
          </p>
        </div>

        <div class="grid max-w-4xl grid-cols-1 gap-6 mx-auto sm:gap-8 md:grid-cols-2">
          <!-- Tarjeta de Trabajo Presencial (AHORA PRIMERO) -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border-t-4 border-pink-500 shadow-lg rounded-2xl group hover:-translate-y-2 hover:shadow-xl">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-pink-500/10 to-purple-500/10 group-hover:opacity-100"></div>
            <div class="relative p-5 sm:p-8">
              <div class="flex items-center justify-center w-16 h-16 mx-auto mb-4 text-white rounded-full sm:w-20 sm:h-20 sm:mb-6 bg-gradient-to-br from-pink-500 to-purple-600">
                <Icon name="uil:building" class="text-2xl sm:text-3xl" />
              </div>
              <h3 class="mb-2 text-xl font-bold text-center text-gray-900 sm:mb-3 sm:text-2xl">Trabajo Presencial</h3>
              <p class="mb-4 text-sm text-center text-gray-600 sm:mb-6 sm:text-base">Trabaja en nuestras instalaciones con equipamiento profesional completo.</p>
              
              <div class="p-3 mb-4 rounded-full sm:p-4 sm:mb-6 bg-pink-50">
                <div class="text-center">
                  <span class="block text-2xl font-bold text-pink-600 sm:text-3xl">50%</span>
                  <span class="text-xs text-gray-500 sm:text-sm">de ganancias para ti</span>
                </div>
              </div>
              
              <ul class="mb-6 space-y-2 text-sm sm:mb-8 sm:space-y-3 sm:text-base">
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-2 text-pink-500 sm:mr-3" />
                  <span class="text-gray-600">Equipos de alta gama</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-2 text-pink-500 sm:mr-3" />
                  <span class="text-gray-600">Sets profesionales</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-2 text-pink-500 sm:mr-3" />
                  <span class="text-gray-600">Ambiente controlado</span>
                </li>
              </ul>
              
              <NuxtLink to="/rules/presencial" class="flex items-center justify-center w-full px-4 sm:px-6 py-2.5 sm:py-3 text-sm sm:text-base text-white transition-colors bg-pink-500 rounded-full hover:bg-pink-600 shadow-md">
                Ver todas las reglas
                <Icon name="uil:arrow-right" class="ml-2" />
              </NuxtLink>
            </div>
          </div>

          <!-- Tarjeta de Trabajo Remoto (AHORA SEGUNDO) -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border-t-4 border-purple-500 shadow-lg rounded-2xl group hover:-translate-y-2 hover:shadow-xl">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-purple-500/10 to-indigo-500/10 group-hover:opacity-100"></div>
            <div class="relative p-5 sm:p-8">
              <div class="flex items-center justify-center w-16 h-16 mx-auto mb-4 text-white rounded-full sm:w-20 sm:h-20 sm:mb-6 bg-gradient-to-br from-purple-500 to-indigo-600">
                <Icon name="uil:laptop" class="text-2xl sm:text-3xl" />
              </div>
              <h3 class="mb-2 text-xl font-bold text-center text-gray-900 sm:mb-3 sm:text-2xl">Trabajo Remoto (Satélite)</h3>
              <p class="mb-4 text-sm text-center text-gray-600 sm:mb-6 sm:text-base">Trabaja desde la comodidad de tu hogar con tu propio equipo y horarios flexibles.</p>
              
              <div class="p-3 mb-4 rounded-full sm:p-4 sm:mb-6 bg-purple-50">
                <div class="text-center">
                  <span class="block text-2xl font-bold text-purple-600 sm:text-3xl">70%</span>
                  <span class="text-xs text-gray-500 sm:text-sm">de ganancias para ti</span>
                </div>
              </div>
              
              <ul class="mb-6 space-y-2 text-sm sm:mb-8 sm:space-y-3 sm:text-base">
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-2 text-purple-500 sm:mr-3" />
                  <span class="text-gray-600">Soporte técnico 24/7</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-2 text-purple-500 sm:mr-3" />
                  <span class="text-gray-600">Horarios flexibles</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-2 text-purple-500 sm:mr-3" />
                  <span class="text-gray-600">Asesoría profesional</span>
                </li>
              </ul>
              
              <NuxtLink to="/rules/remote" class="flex items-center justify-center w-full px-4 sm:px-6 py-2.5 sm:py-3 text-sm sm:text-base text-white transition-colors bg-purple-500 rounded-full hover:bg-purple-600 shadow-md">
                Ver todas las reglas
                <Icon name="uil:arrow-right" class="ml-2" />
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- NUEVA SECCIÓN: Beneficios Section con estilo femenino y cute -->
    <section id="beneficios" class="py-16 bg-gradient-to-b from-pink-50 to-white">
      <div class="max-w-6xl px-6 mx-auto">
        <div class="max-w-3xl mx-auto text-center">
          <h2 class="mb-2 text-3xl font-bold text-gray-900">Nuestros Beneficios</h2>
          <p class="mb-12 text-lg text-gray-600">
            En DAHOUSE nos preocupamos por tu bienestar y crecimiento profesional
          </p>
        </div>

        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          <!-- Beneficio 1: Psicóloga Personal -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white shadow-md rounded-2xl hover:-translate-y-2 hover:shadow-lg">
            <div class="absolute top-0 right-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-pink-100">
                <path d="M12 2a8 8 0 0 0-8 8c0 5.2 8 12 8 12s8-6.8 8-12a8 8 0 0 0-8-8z"></path>
              </svg>
            </div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-16 h-16 mb-4 text-white rounded-full bg-gradient-to-br from-pink-500 to-purple-500">
                <Icon name="uil:heart" class="text-2xl" />
              </div>
              <h3 class="mb-2 text-xl font-bold text-gray-900">Psicóloga Personal</h3>
              <p class="text-gray-600">Sabemos la importancia de la salud mental, siempre cuenta con nosotros. Acceso a profesionales que te apoyarán en tu desarrollo personal y profesional.</p>
            </div>
          </div>

          <!-- Beneficio 2: Programa de Crecimiento -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white shadow-md rounded-2xl hover:-translate-y-2 hover:shadow-lg">
            <div class="absolute top-0 right-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-100">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                <line x1="9" y1="9" x2="9.01" y2="9"></line>
                <line x1="15" y1="9" x2="15.01" y2="9"></line>
              </svg>
            </div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-16 h-16 mb-4 text-white rounded-full bg-gradient-to-br from-purple-500 to-indigo-500">
                <Icon name="uil:chart-line" class="text-2xl" />
              </div>
              <h3 class="mb-2 text-xl font-bold text-gray-900">Programa de Crecimiento</h3>
              <p class="text-gray-600">Desde que ingresas haces parte de un programa personalizado para garantizar tu crecimiento. Mentoras expertas te guiarán en cada paso del camino.</p>
            </div>
          </div>

          <!-- Beneficio 3: Facilidades de Pago -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white shadow-md rounded-2xl hover:-translate-y-2 hover:shadow-lg">
            <div class="absolute top-0 right-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-pink-100">
                <rect x="2" y="6" width="20" height="12" rx="2"></rect>
                <circle cx="12" cy="12" r="2"></circle>
                <path d="M6 12h.01M18 12h.01"></path>
              </svg>
            </div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-16 h-16 mb-4 text-white rounded-full bg-gradient-to-br from-pink-500 to-purple-500">
                <Icon name="uil:tag" class="text-2xl" />
              </div>
              <h3 class="mb-2 text-xl font-bold text-gray-900">Facilidades de Pago</h3>
              <p class="text-gray-600">Aprovecha tarifas especiales en lencería, juguetes y págalo a cuotas o por descuento de nómina. Queremos hacerte la vida más fácil con opciones flexibles.</p>
            </div>
          </div>

          <!-- Beneficio 4: Adelantos y Créditos -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white shadow-md rounded-2xl hover:-translate-y-2 hover:shadow-lg">
            <div class="absolute top-0 right-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-purple-100">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-16 h-16 mb-4 text-white rounded-full bg-gradient-to-br from-purple-500 to-indigo-500">
                <Icon name="uil:money-bill" class="text-2xl" />
              </div>
              <h3 class="mb-2 text-xl font-bold text-gray-900">Adelantos de Nómina y Créditos</h3>
              <p class="text-gray-600">Entendemos que a veces necesitas un poco de ayuda financiera. Ofrecemos adelantos de nómina y pequeños créditos con tasas preferenciales para nuestras modelos.</p>
            </div>
          </div>

          <!-- Beneficio 5: Fotografías Profesionales -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white shadow-md rounded-2xl hover:-translate-y-2 hover:shadow-lg">
            <div class="absolute top-0 right-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-pink-100">
                <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"></path>
                <circle cx="12" cy="13" r="3"></circle>
              </svg>
            </div>
            <div class="relative p-6">
              <div class="flex items-center justify-center w-16 h-16 mb-4 text-white rounded-full bg-gradient-to-br from-pink-500 to-purple-500">
                <Icon name="uil:camera" class="text-2xl" />
              </div>
              <h3 class="mb-2 text-xl font-bold text-gray-900">Fotografías Profesionales</h3>
              <p class="text-gray-600">Mejora tu perfil con nuestro servicio de fotografía profesional. Nuestro equipo de fotógrafos captará tu mejor ángulo para destacar tu belleza natural y autenticidad.</p>
            </div>
          </div>
          
          <!-- Espaciador para mantener la simetría en cuadrícula de 3 -->
          <div class="hidden lg:block"></div>
        </div>
      </div>
    </section>

    <!-- Pagos Section con diseño más femenino -->
    <section id="pagos" class="py-16 bg-white">
      <div class="max-w-6xl px-6 mx-auto">
        <div class="max-w-3xl mx-auto text-center">
          <h2 class="mb-2 text-3xl font-bold text-gray-900">Información de Pagos</h2>
          <p class="mb-12 text-lg text-gray-600">
            En DAHOUSE valoramos la transparencia y te ofrecemos información detallada sobre tus pagos
          </p>
        </div>

        <div class="overflow-hidden shadow-lg rounded-3xl" v-if="datosFinancieros">
          <div class="px-6 py-5 bg-gradient-to-r from-pink-500 to-purple-600">
            <h3 class="text-xl font-semibold text-white">Próximo Periodo de Pago</h3>
          </div>

          <div class="p-4 sm:p-6 bg-gradient-to-b from-pink-50 to-white">
            <div class="grid grid-cols-1 gap-4 sm:gap-6 md:grid-cols-2">
              <div class="p-4 bg-white shadow-sm rounded-2xl sm:p-6">
                <div class="flex items-center mb-4">
                  <div class="flex items-center justify-center w-10 h-10 mr-3 text-white bg-pink-500 rounded-full sm:w-12 sm:h-12 sm:mr-4">
                    <Icon name="uil:calendar-alt" size="20" class="sm:text-2xl" />
                  </div>
                  <h4 class="text-lg font-semibold text-gray-800 sm:text-xl">Fechas Importantes</h4>
                </div>

                <ul class="space-y-2 sm:space-y-4">
                  <li class="flex flex-col p-2 rounded-xl sm:flex-row sm:items-center sm:justify-between sm:p-3 bg-pink-50">
                    <span class="mb-1 text-sm text-gray-600 sm:text-base sm:mb-0">Periodo:</span>
                    <span class="text-sm font-medium text-gray-900 sm:text-base">{{ periodoActual[0] || 'Cargando...' }}</span>
                  </li>
                  <li class="flex flex-col p-2 rounded-xl sm:flex-row sm:items-center sm:justify-between sm:p-3 bg-pink-50">
                    <span class="mb-1 text-sm text-gray-600 sm:text-base sm:mb-0">Fecha inicio:</span>
                    <span class="text-sm font-medium text-gray-900 sm:text-base">{{ formatDate(periodoActual[1]) || 'Cargando...' }}</span>
                  </li>
                  <li class="flex flex-col p-2 rounded-xl sm:flex-row sm:items-center sm:justify-between sm:p-3 bg-pink-50">
                    <span class="mb-1 text-sm text-gray-600 sm:text-base sm:mb-0">Fecha corte:</span>
                    <span class="text-sm font-medium text-gray-900 sm:text-base">{{ formatDate(periodoActual[2]) || 'Cargando...' }}</span>
                  </li>
                  <li class="flex flex-col p-2 text-white bg-pink-500 rounded-xl sm:flex-row sm:items-center sm:justify-between sm:p-3">
                    <span class="mb-1 text-sm sm:text-base sm:mb-0">Fecha de pago:</span>
                    <span class="text-sm font-medium sm:text-base">{{ calcularFechaPago || 'Cargando...' }}</span>
                  </li>
                </ul>
              </div>

              <div class="p-4 bg-white shadow-sm rounded-2xl sm:p-6">
                <div class="flex items-center mb-4">
                  <div class="flex items-center justify-center w-10 h-10 mr-3 text-white bg-pink-500 rounded-full sm:w-12 sm:h-12 sm:mr-4">
                    <Icon name="uil:money-withdraw" size="20" class="sm:text-2xl" />
                  </div>
                  <h4 class="text-lg font-semibold text-gray-800 sm:text-xl">Información de TRM</h4>
                </div>

                <div class="flex flex-col items-center justify-center h-auto py-4 sm:h-44">
                  <div class="mb-4 text-center">
                    <div class="text-xs font-medium text-gray-500 sm:text-sm">TRM actual</div>
                    <div class="text-xl font-bold text-gray-800 sm:text-2xl">{{ formatearPesos(trmActual) }}</div>
                  </div>
                  
                  <div class="w-12 h-px my-2 bg-pink-200 sm:w-16"></div>
                  
                  <div class="text-center">
                    <div class="text-xs font-medium text-gray-500 sm:text-sm">TRM de liquidación</div>
                    <div class="text-2xl font-bold text-pink-600 sm:text-3xl">{{ formatearPesos(trmLiquidacion) }}</div>
                    <div class="mt-2 text-xs text-gray-500">* La TRM utilizada para tu pago</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="p-8 mt-8 text-center rounded-2xl bg-pink-50" v-else>
          <Icon name="uil:sync" class="mx-auto mb-4 text-4xl text-pink-400 animate-spin" />
          <p class="text-gray-600">Cargando información de pagos...</p>
        </div>
      </div>
    </section>

    <!-- Plataformas Section con diseño más redondeado -->
    <section id="plataformas" class="py-16 bg-gradient-to-b from-purple-50 to-white">
      <div class="max-w-6xl px-6 mx-auto">
        <div class="max-w-3xl mx-auto text-center">
          <h2 class="mb-2 text-3xl font-bold text-gray-900">Plataformas con las que Trabajamos</h2>
          <p class="mb-10 text-lg text-gray-600">
            Colaboramos con las mejores plataformas del sector para maximizar tu alcance e ingresos
          </p>
        </div>

        <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5 sm:gap-6">
          <div v-for="(plataforma, index) in plataformas" :key="index" 
               class="flex flex-col items-center p-3 transition-all duration-300 bg-white border border-pink-100 shadow-sm rounded-2xl sm:p-6 hover:shadow-md hover:-translate-y-1">
            <div class="flex items-center justify-center w-12 h-12 mb-2 text-white rounded-full sm:w-16 sm:h-16 sm:mb-4 bg-gradient-to-br from-pink-500 to-purple-500">
              <Icon :name="plataforma.icon" size="20" class="sm:text-3xl" />
            </div>
            <h3 class="mb-1 text-sm font-semibold text-gray-800 sm:text-lg">{{ plataforma.nombre }}</h3>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section con diseño cute -->
    <section id="faq" class="py-16 bg-white">
      <div class="max-w-4xl px-6 mx-auto">
        <div class="max-w-3xl mx-auto text-center">
          <h2 class="mb-2 text-3xl font-bold text-gray-900">Preguntas Frecuentes</h2>
          <p class="mb-12 text-lg text-gray-600">
            Respuestas a las dudas más comunes sobre nuestras reglas y condiciones
          </p>
        </div>

        <div class="space-y-6">
          <div v-for="(faq, index) in faqs" :key="index"
            class="overflow-hidden transition-all duration-300 bg-white border border-pink-200 shadow-sm rounded-2xl hover:shadow-md">
            <div class="p-6">
              <h3 class="mb-3 text-xl font-semibold text-gray-900">{{ faq.pregunta }}</h3>
              <p class="text-gray-600">{{ faq.respuesta }}</p>
            </div>
          </div>
        </div>

        <div class="p-8 mt-12 text-center rounded-2xl bg-pink-50">
          <h3 class="mb-4 text-xl font-semibold text-pink-900">¿Tienes más preguntas?</h3>
          <p class="mb-6 text-gray-600">Nuestro equipo está listo para ayudarte con cualquier duda adicional</p>
          <NuxtLink to="/contacto"
            class="inline-flex items-center px-6 py-3 text-white transition-colors bg-pink-500 rounded-full shadow-md hover:bg-pink-600">
            Contáctanos
            <Icon name="uil:arrow-right" class="ml-2" />
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- CTA Section con esquinas redondeadas -->
    <section class="py-12 bg-gradient-to-r from-pink-600 to-purple-700">
      <!-- Decoraciones cute en esquinas -->
      <div class="absolute top-0 left-0 w-full overflow-hidden">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none" class="absolute top-0 w-full h-20 text-white transform rotate-180 opacity-10">
          <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" fill="currentColor"></path>
        </svg>
      </div>
      
      <div class="relative max-w-4xl px-6 mx-auto text-center">
        <h2 class="mb-4 text-3xl font-bold text-white">¿Lista para comenzar?</h2>
        <p class="mb-8 text-lg text-pink-100">
          Únete a DAHOUSE y lleva tu carrera al siguiente nivel
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <NuxtLink to="/registro" class="px-8 py-3 font-medium text-pink-700 transition-colors bg-white border-2 border-white rounded-full shadow-md hover:bg-pink-50">
            Registrarme
          </NuxtLink>
          <NuxtLink to="/contacto" class="px-8 py-3 font-medium text-white transition-colors bg-transparent border-2 border-white rounded-full shadow-md hover:bg-white/10">
            Más información
          </NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFinancieroStore } from '~/stores/financiero';
import { useServerSeoMeta } from 'nuxt/app'

useServerSeoMeta({
  title: 'DAHOUSE - Studio Webcam en Bogotá | Gana Dinero Seguro en Línea',
  ogTitle: 'DAHOUSE - Studio Webcam en Bogotá',
  description: 'Descubre DAHOUSE, el mejor estudio webcam en Bogotá. Gana dinero seguro trabajando en nuestras instalaciones o desde casa con asesoría profesional.',
  ogDescription: 'Descubre DAHOUSE, el mejor estudio webcam en Bogotá. Gana dinero seguro trabajando en nuestras instalaciones o desde casa con asesoría profesional.',
  ogImage: '/logo-og.webp',
  robots: 'index, follow',
  keywords: 'estudio webcam en Bogotá, ganar dinero en línea, DAHOUSE, trabajo webcam seguro, webcam studio',
  canonical: 'https://dahouse.co'
})

const financieroStore = useFinancieroStore();
const datosFinancieros = ref(null);
const periodoActual = ref(['', '', '']);
const trmActual = ref(0);
const trmLiquidacion = ref(0);

// Plataformas con las que trabajamos
const plataformas = [
  { nombre: 'Chaturbate', icon: 'uil:globe' },
  { nombre: 'Stripchat', icon: 'uil:globe' },
  { nombre: 'Bongacams', icon: 'uil:globe' },
  { nombre: 'Camsoda', icon: 'uil:globe' },
  { nombre: 'Streamate', icon: 'uil:globe' }
];

// FAQs
const faqs = [
  {
    pregunta: '¿Cuándo se realizan los pagos?',
    respuesta: 'Los pagos se realizan el miércoles siguiente a la fecha de corte del periodo, garantizando siempre la máxima puntualidad y transparencia en el proceso.'
  },
  {
    pregunta: '¿Qué necesito para trabajar en modalidad remota?',
    respuesta: 'Para trabajar de forma remota, necesitas un computador con cámara HD, buena iluminación, conexión a internet estable (mínimo 10 Mbps de subida) y un espacio privado sin interrupciones.'
  },
  {
    pregunta: '¿Cómo se calcula mi pago?',
    respuesta: 'Tu pago se calcula según los tokens generados en las plataformas, convertidos a dólares según la tasa de cada plataforma, y luego a pesos colombianos usando la TRM de liquidación establecida por DAHOUSE.'
  },
  {
    pregunta: '¿Puedo cambiar de modalidad de trabajo?',
    respuesta: 'Sí, puedes solicitar un cambio de modalidad con un aviso previo de 15 días para que podamos hacer los ajustes necesarios. El cambio está sujeto a disponibilidad en el caso de trabajo presencial.'
  }
];

// Función para formatear fechas
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('es-CO', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  }).format(date);
};

// Formatear pesos colombianos
const formatearPesos = (valor) => {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 2
  }).format(valor);
};

// Calcular la fecha de pago (día siguiente a la fecha de corte)
const calcularFechaPago = computed(() => {
  if (!periodoActual.value[2]) return '';
  
  const fechaCorte = new Date(periodoActual.value[2]);
  const fechaPago = new Date(fechaCorte);
  
  // Avanzar al día siguiente
  fechaPago.setDate(fechaCorte.getDate() + 1);
  
  return formatDate(fechaPago);
});

// Array de imágenes disponibles
const availableImages = [
  '/landing-images/Kim-mirada.webp',
  '/landing-images/Aly-mirada.webp',
  '/landing-images/Xia-Jacuzzi.webp',
  '/landing-images/Lilith-mirada.webp',
  '/landing-images/Stormy-mirada.webp',
  '/landing-images/Xia-rosa.webp',
  '/landing-images/LilithJacob-mirada.webp',



];

// Referencia para la imagen aleatoria
const randomImage = ref('');

// Función para elegir una imagen aleatoria del array
const selectRandomImage = () => {
  const randomIndex = Math.floor(Math.random() * availableImages.length);
  randomImage.value = availableImages[randomIndex];
};

// Inicializar con una imagen aleatoria al montar el componente
onMounted(() => {
  selectRandomImage();
});

onMounted(async () => {
  try {
    const datos = await financieroStore.fetchDatosFinancieros();
    datosFinancieros.value = datos;
    
    if (datos && datos.periodo_actual) {
      periodoActual.value = datos.periodo_actual;
      trmActual.value = datos.trm_actual;
      trmLiquidacion.value = datos.trm_liquidacion;
    }
  } catch (error) {
    console.error('Error al cargar datos financieros:', error);
  }
});


</script>

<style>
@keyframes slow-fade {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.9; }
}
.animate-slow-fade {
  animation: slow-fade 8s infinite;
}
</style>