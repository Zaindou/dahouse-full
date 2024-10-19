<template>
    <NuxtLayout>
        <div class="container mx-auto">
            <UserManagement />
        </div>
    </NuxtLayout>
</template>

<script setup>
useHead({
    titleTemplate: '%s - Administración de usuarios',
})

import UserManagement from '~/components/UserManagement/index.vue'
</script>