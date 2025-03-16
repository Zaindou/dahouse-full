<template>
    <NuxtLayout>
        <div class="container mx-auto sm:px-6 md:px-8">
            <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
                <!-- Módulo Financiero con fondo blanco -->
                <div class="col-span-1 bg-white rounded-lg shadow-md lg:col-span-2">
                    <div class="p-4">
                        <Financiero />
                    </div>
                </div>
                <!-- <div class="col-span-1 bg-white rounded-lg shadow-md lg:col-span-2">
                    <div class="p-4">
                        <Bussines />
                    </div>
                </div> -->
            </div>
        </div>
    </NuxtLayout>
</template>

<script setup>
import Financiero from '@/components/dashboard/Financiero.vue'
import Bussines from '~/components/dashboard/Bussines.vue';
</script>