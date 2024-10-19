<template>
    <div class="flex items-center justify-between p-4">
        <h1 :class="[
            'text-white font-bold transition-all duration-300 ease-in-out',
            isSidebarOpen ? 'text-2xl' : 'text-xs md:text-2xl'
        ]">
            {{ isSidebarOpen ? 'DAHOUSE' : 'DH' }}
        </h1>
        <button @click="$emit('toggle')" class="text-white hidden md:block">
            <Icon :name="isSidebarOpen ? 'ic:baseline-chevron-left' : 'ic:baseline-chevron-right'" class="w-6 h-6" />
        </button>
    </div>
</template>

<script setup>
defineProps({
    isSidebarOpen: Boolean
})

defineEmits(['toggle'])
</script>