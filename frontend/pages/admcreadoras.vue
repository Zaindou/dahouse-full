<template>
    <NuxtLayout>
        <div class="container mx-auto">
            <Modelo />
        </div>
    </NuxtLayout>

</template>

<script setup>

useHead({
    titleTemplate: '%s - Administración de usuarios',
})
import Modelo from '~/components/Modelo.vue'
</script>
