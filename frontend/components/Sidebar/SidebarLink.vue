<template>
    <div>
        <!-- Para elementos con submenú -->
        <div v-if="hasSubmenu" :class="[
            'flex items-center text-white p-4 hover:bg-gray-700',
            { 'justify-center': !isSidebarOpen },
            { 'cursor-pointer': hasSubmenu }
        ]" @click="toggleSubmenu">
            <Icon :name="icon" :class="iconClasses" />
            <template v-if="isSidebarOpen">
                <span class="flex-grow">{{ text }}</span>
                <Icon :name="isSubmenuOpen ? 'mdi:chevron-up' : 'mdi:chevron-down'"
                    class="w-4 h-4 transition-transform duration-300" />
            </template>
        </div>

        <!-- Para elementos sin submenú -->
        <NuxtLink v-else :to="to" :class="[
            'flex items-center text-white p-4 hover:bg-gray-700',
            { 'justify-center': !isSidebarOpen }
        ]" @click="$emit('click')">
            <Icon :name="icon" :class="iconClasses" />
            <span v-if="isSidebarOpen">{{ text }}</span>
        </NuxtLink>

        <!-- Submenú -->
        <div v-if="hasSubmenu && isSidebarOpen" class="overflow-hidden transition-all duration-300"
            :class="{ 'max-h-0': !isSubmenuOpen, 'max-h-[500px]': isSubmenuOpen }">
            <NuxtLink v-for="item in submenu" :key="item.to" :to="item.to"
                class="flex items-center text-white p-4 pl-12 hover:bg-gray-700" @click="$emit('click')">
                <Icon :name="item.iconSubmenu" :class="iconClasses" />
                <span>{{ item.text }}</span>
            </NuxtLink>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
    to: String,
    icon: String,
    iconSubmenu: String,
    text: String,
    isSidebarOpen: Boolean,
    hasSubmenu: Boolean,
    submenu: {
        type: Array,
        default: () => []
    }
})

const emit = defineEmits(['click'])

const isSubmenuOpen = ref(false)

const iconClasses = computed(() => [
    'transition-all duration-300 ease-in-out',
    props.isSidebarOpen ? 'mr-3 w-6 h-6' : 'w-6 h-6'
])

const toggleSubmenu = () => {
    isSubmenuOpen.value = !isSubmenuOpen.value
}
</script>