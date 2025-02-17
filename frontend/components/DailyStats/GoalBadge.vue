# components/DailyStats/GoalBadge.vue
<template>
  <span :class="[
    'inline-flex items-center gap-1 px-2 py-1 rounded-full font-medium',
    size === 'small' ? 'text-xs' : 'text-sm',
    completed ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
  ]">
    <Icon
      :name="completed ? 'heroicons:check-circle' : 'heroicons:clock'"
      :class="size === 'small' ? 'w-3 h-3' : 'w-4 h-4'"
    />
    {{ completed ? 'Completado' : 'En progreso' }}
  </span>
</template>

<script setup>
defineProps({
  completed: {
    type: Boolean,
    default: false
  },
  size: {
    type: String,
    default: 'normal',
    validator: (value) => ['small', 'normal'].includes(value)
  }
})
</script>