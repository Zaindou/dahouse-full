<template>
    <NuxtLayout>
        <div class="container px-4 py-6 mx-auto">
            <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
                <!-- Módulo Financiero con fondo blanco -->
                <div class="col-span-1 bg-white rounded-lg shadow-md lg:col-span-2">
                    <div class="p-4">
                        <Financiero />
                    </div>
                </div>

                <!-- Espacio para futuros módulos -->
                <!-- <div class="p-6 bg-white rounded-lg shadow-md">
                    <h2 class="mb-4 text-xl font-bold">Otro Módulo</h2>
                    <p>Contenido del módulo...</p>
                </div> -->
            </div>
        </div>
    </NuxtLayout>
</template>

<script setup>
</script>