// components/DailyStats/ModelsPodium.vue
<template>
  <div class="p-6 bg-white border border-gray-100 rounded-lg shadow-lg">
    <div class="flex flex-col mb-8 space-y-2">
      <h3 class="text-xl font-bold text-gray-800">Top Modelos del Mes</h3>
                          <p class="text-xs text-gray-500">Los valores mostrados son aproximados y se actualizan periódicamente</p>
    </div>

    <!-- Podio Visual Mejorado -->
    <div class="relative flex items-end justify-center h-56 mb-0 space-x-4">
      <!-- Decoración de fondo -->
      <div class="absolute inset-0 bg-gradient-to-b from-blue-50/50 to-transparent rounded-xl" />
      
      <!-- Segundo Lugar -->
      <div v-if="rankings[1]" class="relative w-32 slide-up-delay-1">

        <div class="flex flex-col h-36">
          <div class="flex flex-col items-center justify-end flex-grow">
            <div class="w-full">
              <div class="relative">
                <div class="absolute z-10 transform -translate-x-1/2 -top-12 left-1/2">
                  <Avatar 
                    :initials="getInitials(rankings[1].nickname)"
                    class="bg-white ring-4 ring-gray-200 ring-offset-2"
                  />
                </div>
                <div class="w-full rounded-t-lg shadow-inner h-28 bg-gradient-to-b from-gray-100 to-gray-200">
                  <div class="absolute bottom-0 left-0 right-0 p-4 pb-3 text-center">
                    <span class="block font-semibold text-gray-800 truncate">
                      {{ rankings[1].nickname }}
                    </span>
                    <span class="block mt-1 text-sm text-gray-600">
                      {{ formatNumber(rankings[1].tokens) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Primer Lugar -->
      <div v-if="rankings[0]" class="relative -mt-8 w-36 slide-up">
        <div class="absolute transform -translate-x-1/2 -top-10 left-1/2 scale-up-delay-1">
          <div class="relative">
            <div class="relative flex items-center justify-center">
              <Icon name="ph:crown-fill" class="w-12 h-12 text-yellow-400 filter drop-shadow-lg" />
              <div class="absolute transform -translate-x-1/2 -top-1 left-1/2">
                <Icon name="ph:sparkle-fill" class="w-4 h-4 text-yellow-300 animate-pulse" />
              </div>
            </div>
          </div>
        </div>
        <div class="flex flex-col h-44">
          <div class="flex flex-col items-center justify-end flex-grow">
            <div class="w-full">
              <div class="relative">
                <div class="absolute z-10 transform -translate-x-1/2 -top-12 left-1/2">
                  <Avatar 
                    :initials="getInitials(rankings[0].nickname)"
                    size="lg"
                    class="bg-white ring-4 ring-yellow-300 ring-offset-2"
                  />
                </div>
                <div class="w-full rounded-t-lg shadow-inner h-36 bg-gradient-to-b from-yellow-50 to-yellow-100">
                  <div class="absolute bottom-0 left-0 right-0 p-4 pb-3 text-center">
                    <span class="block font-bold text-gray-800 truncate">
                      {{ rankings[0].nickname }}
                    </span>
                    <span class="block mt-1 text-sm text-gray-600">
                      {{ formatNumber(rankings[0].tokens) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tercer Lugar -->
      <div v-if="rankings[2]" class="relative w-32 slide-up-delay-2">

        <div class="flex flex-col h-32">
          <div class="flex flex-col items-center justify-end flex-grow">
            <div class="w-full">
              <div class="relative">
                <div class="absolute z-10 transform -translate-x-1/2 -top-12 left-1/2">
                  <Avatar 
                    :initials="getInitials(rankings[2].nickname)"
                    class="bg-white ring-4 ring-orange-200 ring-offset-2"
                  />
                </div>
                <div class="w-full h-24 rounded-t-lg shadow-inner bg-gradient-to-b from-orange-50 to-orange-100">
                  <div class="absolute bottom-0 left-0 right-0 p-4 pb-3 text-center">
                    <span class="block font-semibold text-gray-800 truncate">
                      {{ rankings[2].nickname }}
                    </span>
                    <span class="block mt-1 text-sm text-gray-600">
                      {{ formatNumber(rankings[2].tokens) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabla de Rankings -->
    <div class="mt-0 overflow-hidden border border-gray-200 rounded-lg bg-gray-50 fade-in">
      <table class="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            <th class="px-6 py-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase bg-gray-100">Posición</th>
            <th class="px-6 py-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase bg-gray-100">Modelo</th>
            <th class="px-6 py-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase bg-gray-100">Tokens</th>
            <th class="px-6 py-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase bg-gray-100">Horas</th>
            <th class="px-6 py-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase bg-gray-100">Tokens/Hora</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="(model, index) in rankings" 
              :key="model.nickname"
              class="transition-colors duration-150 hover:bg-gray-50"
              :class="{'bg-gray-50': index % 2 === 0}">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <span v-if="index < 3" 
                      class="flex items-center justify-center w-6 h-6 font-medium rounded-full"
                      :class="positionClass(index)">
                  {{ index + 1 }}
                </span>
                <span v-else class="font-medium text-gray-500">{{ index + 1 }}</span>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center space-x-3">
                <Avatar :initials="getInitials(model.nickname)" size="sm" />
                <div class="text-sm font-medium text-gray-900">{{ model.nickname }}</div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ formatNumber(model.tokens) }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ formatNumber(model.hours, 1) }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">
                {{ formatNumber(model.tokensPerHour, 1) }}
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed, defineComponent, h } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

// Rankings computation
const rankings = computed(() => {
  if (!props.data?.earnings) return []

  const modelStats = {}
  
  props.data.earnings.forEach(earning => {
    if (!modelStats[earning.nickname]) {
      modelStats[earning.nickname] = {
        nickname: earning.nickname,
        tokens: 0,
        hours: 0,
        tokensPerHour: 0
      }
    }
    
    modelStats[earning.nickname].tokens += earning.tokens
    modelStats[earning.nickname].hours += earning.hours_worked || 0
  })

  return Object.values(modelStats)
    .map(model => ({
      ...model,
      tokensPerHour: model.hours > 0 ? model.tokens / model.hours : 0
    }))
    .sort((a, b) => b.tokens - a.tokens)
    .slice(0, 10)
})

// Formatear nickname
const formatNickname = (nickname) => {
  if (nickname.length <= 12) return nickname
  return `${nickname.substring(0, 10)}...`
}

// Avatar component
const Avatar = defineComponent({
  props: {
    initials: {
      type: String,
      required: true
    },
    size: {
      type: String,
      default: 'md'
    }
  },
  setup(props) {
    const sizeClasses = {
      sm: 'w-7 h-7 text-sm',
      md: 'w-10 h-10 text-base',
      lg: 'w-12 h-12 text-lg'
    }

    return () => h('div', {
      class: [
        'flex items-center justify-center rounded-full bg-white text-gray-600 font-medium shadow-sm',
        sizeClasses[props.size]
      ]
    }, props.initials)
  }
})

const getInitials = (nickname) => {
  return nickname.substring(0, 2).toUpperCase()
}

const formatNumber = (num, decimals = 0) => {
  return Number(num).toLocaleString(undefined, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  })
}

const positionClass = (index) => {
  const classes = {
    0: 'bg-yellow-100 text-yellow-800',
    1: 'bg-gray-100 text-gray-800',
    2: 'bg-orange-100 text-orange-800'
  }
  return classes[index] || ''
}
</script>

<style scoped>
.slide-up {
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-up-delay-1 {
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.2s both;
}

.slide-up-delay-2 {
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.4s both;
}

.scale-up {
  animation: scaleUp 0.4s cubic-bezier(0.4, 0, 0.2, 1) 0.6s both;
}

.scale-up-delay-1 {
  animation: scaleUp 0.4s cubic-bezier(0.4, 0, 0.2, 1) 0.8s both;
}

.scale-up-delay-2 {
  animation: scaleUp 0.4s cubic-bezier(0.4, 0, 0.2, 1) 1s both;
}

.fade-in {
  animation: fadeIn 0.6s ease-out 1.2s both;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(2rem);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scaleUp {
  from {
    opacity: 0;
    transform: translate(-50%, 1rem) scale(0.8);
  }
  to {
    opacity: 1;
    transform: translate(-50%, 0) scale(1);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>