// pages/rules/index.vue
<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
    <!-- Hero Section -->
    <div class="relative py-16 overflow-hidden md:py-20 bg-gradient-to-r from-purple-900 to-indigo-900">
      <div class="absolute inset-0 opacity-20">
        <div class="absolute inset-0 bg-black opacity-20"></div>
        <div class="absolute inset-0" style="background-image: url('/backdrop-pattern.svg'); background-size: cover;"></div>
      </div>
      <div class="relative max-w-5xl px-4 mx-auto text-center sm:px-6">
        <h1 class="mb-4 text-3xl font-extrabold tracking-tight text-white sm:text-4xl md:text-5xl">
          DAHOUSE
        </h1>
        <p class="mb-6 text-lg text-purple-100 sm:mb-8 sm:text-xl">Descubre nuestras reglas y condiciones</p>
        
        <!-- Menú de navegación para móvil -->
        <div class="flex flex-wrap justify-center gap-2 md:hidden">
          <NuxtLink to="#modalidades" class="px-4 py-2 text-sm font-medium text-white rounded-lg bg-purple-800/50 backdrop-blur-sm hover:bg-purple-800/70">
            Modalidades
          </NuxtLink>
          <NuxtLink to="#pagos" class="px-4 py-2 text-sm font-medium text-white rounded-lg bg-purple-800/50 backdrop-blur-sm hover:bg-purple-800/70">
            Pagos
          </NuxtLink>
          <NuxtLink to="#plataformas" class="px-4 py-2 text-sm font-medium text-white rounded-lg bg-purple-800/50 backdrop-blur-sm hover:bg-purple-800/70">
            Plataformas
          </NuxtLink>
          <NuxtLink to="#faq" class="px-4 py-2 text-sm font-medium text-white rounded-lg bg-purple-800/50 backdrop-blur-sm hover:bg-purple-800/70">
            FAQ
          </NuxtLink>
        </div>
        
        <!-- Menú de navegación para tablet/desktop -->
        <div class="hidden p-1 space-x-1 bg-white rounded-full shadow-lg md:inline-flex">
          <NuxtLink to="#modalidades" class="px-6 py-3 text-sm font-medium text-purple-900 transition-colors rounded-full hover:bg-purple-100">
            Modalidades
          </NuxtLink>
          <NuxtLink to="#pagos" class="px-6 py-3 text-sm font-medium text-purple-900 transition-colors rounded-full hover:bg-purple-100">
            Pagos
          </NuxtLink>
          <NuxtLink to="#plataformas" class="px-6 py-3 text-sm font-medium text-purple-900 transition-colors rounded-full hover:bg-purple-100">
            Plataformas
          </NuxtLink>
          <NuxtLink to="#faq" class="px-6 py-3 text-sm font-medium text-purple-900 transition-colors rounded-full hover:bg-purple-100">
            FAQ
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- Modalidades Section -->
    <section id="modalidades" class="py-16">
      <div class="max-w-6xl px-6 mx-auto">
        <div class="text-center">
          <h2 class="mb-2 text-3xl font-bold text-gray-900">Modalidades de Trabajo</h2>
          <p class="max-w-2xl mx-auto mb-12 text-lg text-gray-600">
            Ofrecemos diferentes opciones para que trabajes de la manera que mejor se adapte a ti
          </p>
        </div>

        <div class="grid max-w-4xl grid-cols-1 gap-6 mx-auto sm:gap-8 md:grid-cols-2">
          <!-- Tarjeta de Trabajo Remoto -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border-t-4 border-purple-600 rounded-lg shadow-lg group hover:-translate-y-2 hover:shadow-xl">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-purple-500/10 to-indigo-500/10 group-hover:opacity-100"></div>
            <div class="relative p-5 sm:p-8">
              <div class="flex items-center justify-center w-16 h-16 mx-auto mb-4 text-white sm:w-20 sm:h-20 sm:mb-6 bg-gradient-to-br from-purple-600 to-indigo-600 rounded-xl">
                <Icon name="uil:laptop" class="text-2xl sm:text-3xl" />
              </div>
              <h3 class="mb-2 text-xl font-bold text-center text-gray-900 sm:mb-3 sm:text-2xl">Trabajo Remoto</h3>
              <p class="mb-4 text-sm text-center text-gray-600 sm:mb-6 sm:text-base">Trabaja desde la comodidad de tu hogar con tu propio equipo y horarios flexibles.</p>
              
              <div class="p-3 mb-4 rounded-lg sm:p-4 sm:mb-6 bg-gray-50">
                <div class="text-center">
                  <span class="block text-2xl font-bold text-purple-600 sm:text-3xl">60%</span>
                  <span class="text-xs text-gray-500 sm:text-sm">de ganancias para ti</span>
                </div>
              </div>
              
              <ul class="mb-6 space-y-2 text-sm sm:mb-8 sm:space-y-3 sm:text-base">
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-2 text-green-500 sm:mr-3" />
                  <span class="text-gray-600">Soporte técnico 24/7</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-2 text-green-500 sm:mr-3" />
                  <span class="text-gray-600">Horarios flexibles</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-2 text-green-500 sm:mr-3" />
                  <span class="text-gray-600">Asesoría profesional</span>
                </li>
              </ul>
              
              <NuxtLink to="/rules/remote" class="flex items-center justify-center w-full px-4 sm:px-6 py-2.5 sm:py-3 text-sm sm:text-base text-white transition-colors bg-purple-600 rounded-lg hover:bg-purple-700">
                Ver todas las reglas
                <Icon name="uil:arrow-right" class="ml-2" />
              </NuxtLink>
            </div>
          </div>

          <!-- Tarjeta de Trabajo Presencial -->
          <div class="relative overflow-hidden transition-all duration-300 bg-white border-t-4 border-indigo-600 rounded-lg shadow-lg group hover:-translate-y-2 hover:shadow-xl">
            <div class="absolute inset-0 transition-opacity opacity-0 bg-gradient-to-br from-indigo-500/10 to-blue-500/10 group-hover:opacity-100"></div>
            <div class="relative p-5 sm:p-8">
              <div class="flex items-center justify-center w-16 h-16 mx-auto mb-4 text-white sm:w-20 sm:h-20 sm:mb-6 bg-gradient-to-br from-indigo-600 to-blue-600 rounded-xl">
                <Icon name="uil:building" class="text-2xl sm:text-3xl" />
              </div>
              <h3 class="mb-2 text-xl font-bold text-center text-gray-900 sm:mb-3 sm:text-2xl">Trabajo Presencial</h3>
              <p class="mb-4 text-sm text-center text-gray-600 sm:mb-6 sm:text-base">Trabaja en nuestras instalaciones con equipamiento profesional completo.</p>
              
              <div class="p-3 mb-4 rounded-lg sm:p-4 sm:mb-6 bg-gray-50">
                <div class="text-center">
                  <span class="block text-2xl font-bold text-indigo-600 sm:text-3xl">50%</span>
                  <span class="text-xs text-gray-500 sm:text-sm">de ganancias para ti</span>
                </div>
              </div>
              
              <ul class="mb-6 space-y-2 text-sm sm:mb-8 sm:space-y-3 sm:text-base">
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-2 text-green-500 sm:mr-3" />
                  <span class="text-gray-600">Equipos de alta gama</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-2 text-green-500 sm:mr-3" />
                  <span class="text-gray-600">Sets profesionales</span>
                </li>
                <li class="flex items-start">
                  <Icon name="uil:check-circle" class="flex-shrink-0 mt-1 mr-2 text-green-500 sm:mr-3" />
                  <span class="text-gray-600">Ambiente controlado</span>
                </li>
              </ul>
              
              <NuxtLink to="/rules/presencial" class="flex items-center justify-center w-full px-4 sm:px-6 py-2.5 sm:py-3 text-sm sm:text-base text-white transition-colors bg-indigo-600 rounded-lg hover:bg-indigo-700">
                Ver todas las reglas
                <Icon name="uil:arrow-right" class="ml-2" />
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pagos Section -->
    <section id="pagos" class="py-16 bg-white">
      <div class="max-w-6xl px-6 mx-auto">
        <div class="max-w-3xl mx-auto text-center">
          <h2 class="mb-2 text-3xl font-bold text-gray-900">Información de Pagos</h2>
          <p class="mb-12 text-lg text-gray-600">
            En DAHOUSE valoramos la transparencia y te ofrecemos información detallada sobre tus pagos
          </p>
        </div>

        <div class="overflow-hidden shadow-lg rounded-xl" v-if="datosFinancieros">
          <div class="px-6 py-5 bg-gradient-to-r from-blue-700 to-indigo-800">
            <h3 class="text-xl font-semibold text-white">Próximo Periodo de Pago</h3>
          </div>

          <div class="p-4 sm:p-6 bg-gradient-to-b from-blue-50 to-white">
            <div class="grid grid-cols-1 gap-4 sm:gap-6 md:grid-cols-2">
              <div class="p-4 bg-white rounded-lg shadow-sm sm:p-6">
                <div class="flex items-center mb-4">
                  <div class="flex items-center justify-center w-10 h-10 mr-3 text-white bg-blue-600 rounded-full sm:w-12 sm:h-12 sm:mr-4">
                    <Icon name="uil:calendar-alt" size="20" class="sm:text-2xl" />
                  </div>
                  <h4 class="text-lg font-semibold text-gray-800 sm:text-xl">Fechas Importantes</h4>
                </div>

                <ul class="space-y-2 sm:space-y-4">
                  <li class="flex flex-col p-2 rounded-md sm:flex-row sm:items-center sm:justify-between sm:p-3 bg-blue-50">
                    <span class="mb-1 text-sm text-gray-600 sm:text-base sm:mb-0">Periodo:</span>
                    <span class="text-sm font-medium text-gray-900 sm:text-base">{{ periodoActual[0] || 'Cargando...' }}</span>
                  </li>
                  <li class="flex flex-col p-2 rounded-md sm:flex-row sm:items-center sm:justify-between sm:p-3 bg-blue-50">
                    <span class="mb-1 text-sm text-gray-600 sm:text-base sm:mb-0">Fecha inicio:</span>
                    <span class="text-sm font-medium text-gray-900 sm:text-base">{{ formatDate(periodoActual[1]) || 'Cargando...' }}</span>
                  </li>
                  <li class="flex flex-col p-2 rounded-md sm:flex-row sm:items-center sm:justify-between sm:p-3 bg-blue-50">
                    <span class="mb-1 text-sm text-gray-600 sm:text-base sm:mb-0">Fecha corte:</span>
                    <span class="text-sm font-medium text-gray-900 sm:text-base">{{ formatDate(periodoActual[2]) || 'Cargando...' }}</span>
                  </li>
                  <li class="flex flex-col p-2 text-white bg-blue-600 rounded-md sm:flex-row sm:items-center sm:justify-between sm:p-3">
                    <span class="mb-1 text-sm sm:text-base sm:mb-0">Fecha de pago:</span>
                    <span class="text-sm font-medium sm:text-base">{{ calcularFechaPago || 'Cargando...' }}</span>
                  </li>
                </ul>
              </div>

              <div class="p-4 bg-white rounded-lg shadow-sm sm:p-6">
                <div class="flex items-center mb-4">
                  <div class="flex items-center justify-center w-10 h-10 mr-3 text-white bg-blue-600 rounded-full sm:w-12 sm:h-12 sm:mr-4">
                    <Icon name="uil:money-withdraw" size="20" class="sm:text-2xl" />
                  </div>
                  <h4 class="text-lg font-semibold text-gray-800 sm:text-xl">Información de TRM</h4>
                </div>

                <div class="flex flex-col items-center justify-center h-auto py-4 sm:h-44">
                  <div class="mb-4 text-center">
                    <div class="text-xs font-medium text-gray-500 sm:text-sm">TRM actual</div>
                    <div class="text-xl font-bold text-gray-800 sm:text-2xl">{{ formatearPesos(trmActual) }}</div>
                  </div>
                  
                  <div class="w-12 h-px my-2 bg-gray-200 sm:w-16"></div>
                  
                  <div class="text-center">
                    <div class="text-xs font-medium text-gray-500 sm:text-sm">TRM de liquidación</div>
                    <div class="text-2xl font-bold text-green-600 sm:text-3xl">{{ formatearPesos(trmLiquidacion) }}</div>
                    <div class="mt-2 text-xs text-gray-500">* La TRM utilizada para tu pago</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="p-8 mt-8 text-center rounded-lg bg-gray-50" v-else>
          <Icon name="uil:sync" class="mx-auto mb-4 text-4xl text-gray-400 animate-spin" />
          <p class="text-gray-600">Cargando información de pagos...</p>
        </div>
      </div>
    </section>

    <!-- Plataformas Section -->
    <section id="plataformas" class="py-16 bg-gradient-to-b from-gray-100 to-white">
      <div class="max-w-6xl px-6 mx-auto">
        <div class="max-w-3xl mx-auto text-center">
          <h2 class="mb-2 text-3xl font-bold text-gray-900">Plataformas con las que Trabajamos</h2>
          <p class="mb-10 text-lg text-gray-600">
            Colaboramos con las mejores plataformas del sector para maximizar tu alcance e ingresos
          </p>
        </div>

        <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5 sm:gap-6">
          <div v-for="(plataforma, index) in plataformas" :key="index" 
               class="flex flex-col items-center p-3 transition-all duration-300 bg-white border border-gray-200 rounded-lg shadow-sm sm:p-6 hover:shadow-md hover:-translate-y-1">
            <div class="flex items-center justify-center w-12 h-12 mb-2 text-white rounded-full sm:w-16 sm:h-16 sm:mb-4 bg-gradient-to-br from-purple-600 to-indigo-600">
              <Icon :name="plataforma.icon" size="20" class="sm:text-3xl" />
            </div>
            <h3 class="mb-1 text-sm font-semibold text-gray-800 sm:text-lg">{{ plataforma.nombre }}</h3>
            <!-- <p class="text-xs text-center text-gray-500 sm:text-sm">Plataforma global</p> -->
          </div>
        </div>
      </div>
    </section>

<!-- FAQ Section -->
<section id="faq" class="py-16 bg-white">
  <div class="max-w-4xl px-6 mx-auto">
    <div class="max-w-3xl mx-auto text-center">
      <h2 class="mb-2 text-3xl font-bold text-gray-900">Preguntas Frecuentes</h2>
      <p class="mb-12 text¿Tienes más preguntas?-lg text-gray-600">
        Respuestas a las dudas más comunes sobre nuestras reglas y condiciones
      </p>
    </div>

    <div class="space-y-6">
      <div v-for="(faq, index) in faqs" :key="index"
        class="overflow-hidden transition-all duration-300 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md">
        <div class="p-6">
          <h3 class="mb-3 text-xl font-semibold text-gray-900">{{ faq.pregunta }}</h3>
          <p class="text-gray-600">{{ faq.respuesta }}</p>
        </div>
      </div>
    </div>

    <div class="p-8 mt-12 text-center rounded-lg bg-purple-50">
      <h3 class="mb-4 text-xl font-semibold text-purple-900">¿Tienes más preguntas?</h3>
      <p class="mb-6 text-gray-600">Nuestro equipo está listo para ayudarte con cualquier duda adicional</p>
      <NuxtLink to="/contacto"
        class="inline-flex items-center px-6 py-3 text-white transition-colors bg-purple-600 rounded-lg hover:bg-purple-700">
        Contáctanos
        <Icon name="uil:arrow-right" class="ml-2" />
      </NuxtLink>
    </div>
  </div>
</section>

    <!-- CTA Section -->
    <section class="py-12 bg-gradient-to-r from-purple-900 to-indigo-900">
      <div class="max-w-4xl px-6 mx-auto text-center">
        <h2 class="mb-4 text-3xl font-bold text-white">¿Listo para comenzar?</h2>
        <p class="mb-8 text-lg text-purple-100">
          Únete a DAHOUSE y lleva tu carrera al siguiente nivel
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <NuxtLink to="/registro" class="px-8 py-3 font-medium text-purple-900 transition-colors bg-white border-2 border-white rounded-lg hover:bg-purple-50">
            Registrarme
          </NuxtLink>
          <NuxtLink to="/contacto" class="px-8 py-3 font-medium text-white transition-colors bg-transparent border-2 border-white rounded-lg hover:bg-white/10">
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