<!-- components/UnderConstruction.vue -->
<template>
    <NuxtLayout>
        <div class="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
            <div class="bg-white rounded-lg shadow-xl p-8 max-w-2xl w-full text-center space-y-6">
                <!-- Íconos animados -->
                <div class="flex justify-center gap-4 mb-6">
                    <div class="animate-bounce">
                        <Icon name="lucide:hammer" class="w-12 h-12 text-yellow-500" />
                    </div>
                    <div class="animate-bounce" style="animation-delay: 100ms;">
                        <Icon name="lucide:wrench" class="w-12 h-12 text-blue-500" />
                    </div>
                    <div class="animate-bounce" style="animation-delay: 200ms;">
                        <Icon name="lucide:alert-circle" class="w-12 h-12 text-red-500" />
                    </div>
                </div>

                <!-- Texto principal -->
                <h1 class="text-4xl font-bold text-gray-800">
                    Página en Construcción
                </h1>

                <div class="space-y-4">
                    <p class="text-xl text-gray-600">
                        Estamos trabajando arduamente para traerte algo increíble.
                    </p>
                    <p class="text-gray-500">
                        Disculpa las molestias. ¡Vuelve pronto para ver los cambios!
                    </p>
                </div>

                <!-- Barra de progreso -->
                <div class="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                    <div class="bg-blue-500 h-full w-3/4 animate-pulse rounded-full"></div>
                </div>

            </div>
        </div>
    </NuxtLayout>

</template>

<script setup>
// No se necesita ninguna importación adicional gracias al auto-import de Nuxt
</script>