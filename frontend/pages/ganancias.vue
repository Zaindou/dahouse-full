<template>
    <NuxtLayout>
        <div class="container mx-auto">
            <Ganancia />
        </div>
    </NuxtLayout>

</template>

<script setup>

useHead({
    titleTemplate: '%s - Administración de usuarios',
})
import Ganancia from '~/components/Ganancia.vue'
</script>
