<template>
    <NuxtLink :to="to" :class="[
        'flex items-center text-white p-4 hover:bg-gray-700',
        { 'justify-center': !isSidebarOpen }
    ]" @click="$emit('click')">
        <Icon :name="icon" :class="iconClasses" />
        <span v-if="isSidebarOpen">{{ text }}</span>
    </NuxtLink>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    to: String,
    icon: String,
    text: String,
    isSidebarOpen: Boolean
})

defineEmits(['click'])

const iconClasses = computed(() => [
    'transition-all duration-300 ease-in-out',
    props.isSidebarOpen ? 'mr-3 w-6 h-6' : 'w-6 h-6'
])
</script>