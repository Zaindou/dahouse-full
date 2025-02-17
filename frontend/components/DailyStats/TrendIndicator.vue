# components/DailyStats/TrendIndicator.vue
<template>
  <div class="flex items-center">
    <Icon
      :name="trendIcon"
      :class="[
        'w-4 h-4',
        value === 'up' ? 'text-green-500' : 
        value === 'down' ? 'text-red-500' : 
        'text-gray-500'
      ]"
    />
  </div>
</template>

<script setup>
const props = defineProps({
  value: {
    type: String,
    required: true,
    validator: (value) => ['up', 'down', 'neutral'].includes(value)
  }
})

const trendIcon = computed(() => {
  switch (props.value) {
    case 'up':
      return 'heroicons:arrow-trending-up'
    case 'down':
      return 'heroicons:arrow-trending-down'
    default:
      return 'heroicons:minus'
  }
})
</script>