<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-full p-4">
      <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" @click="$emit('close')"></div>
      
      <div class="relative w-full max-w-lg bg-white rounded-lg shadow-xl">
        <div class="p-6">
          <div class="mb-4">
            <slot name="header"></slot>
          </div>

          <div class="mb-4">
            <slot name="body"></slot>
          </div>

          <div class="flex justify-end gap-3">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineEmits(['close'])
</script>