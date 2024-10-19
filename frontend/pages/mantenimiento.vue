<template>
    <NuxtLayout>
        <div class="container mx-auto">
            <mantenmiento />
        </div>
    </NuxtLayout>

</template>

<script setup>

useHead({
    titleTemplate: '%s - Administración de usuarios',
})
import Ganancia from '~/components/Mantenmiento.vue'
</script>
