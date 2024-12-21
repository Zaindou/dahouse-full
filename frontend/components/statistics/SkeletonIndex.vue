<template>
    <div class="w-full space-y-8">
        <!-- Skeleton para Filtros -->
        <div class="p-6 border shadow-md bg-white/80 backdrop-blur-lg rounded-2xl border-gray-100/50">
            <div class="flex flex-wrap gap-4">
                <div v-for="i in 3" :key="`filter-${i}`" class="w-32 h-10 bg-gray-200 rounded-lg animate-pulse">
                </div>
            </div>
        </div>

        <!-- Skeleton para Tarjetas de Resumen -->
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
            <div v-for="i in 4" :key="`card-${i}`" class="p-6 border border-gray-100 shadow-sm bg-white/90 rounded-2xl">
                <div class="flex items-center justify-between mb-4">
                    <div class="w-24 h-4 bg-gray-200 rounded animate-pulse"></div>
                    <div class="w-10 h-10 bg-gray-200 rounded-full animate-pulse"></div>
                </div>
                <div class="space-y-3">
                    <div class="h-8 bg-gray-200 rounded w-36 animate-pulse"></div>
                    <div class="w-20 h-4 bg-gray-200 rounded animate-pulse"></div>
                </div>
            </div>
        </div>

        <!-- Skeleton para Gráficos -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div v-for="i in 4" :key="`chart-${i}`" class="p-6 bg-white border border-gray-100 shadow-md rounded-2xl">
                <div class="w-32 h-6 mb-4 bg-gray-200 rounded animate-pulse"></div>
                <div class="h-[300px] bg-gray-200 rounded-lg animate-pulse"></div>
            </div>
        </div>

        <!-- Skeleton para Tabla -->
        <div class="overflow-hidden border border-gray-100 shadow-md bg-white/90 rounded-2xl">
            <div class="px-6 py-4 border-b border-gray-100 bg-gray-50/80">
                <div class="flex items-center justify-between">
                    <div class="w-32 h-6 bg-gray-200 rounded animate-pulse"></div>
                    <div class="w-24 h-6 bg-gray-200 rounded animate-pulse"></div>
                </div>
            </div>
            <div class="p-6">
                <div v-for="i in 5" :key="`row-${i}`" class="flex gap-4 mb-4 last:mb-0">
                    <div class="w-24 h-4 bg-gray-200 rounded animate-pulse"></div>
                    <div class="w-32 h-4 bg-gray-200 rounded animate-pulse"></div>
                    <div class="w-20 h-4 bg-gray-200 rounded animate-pulse"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
defineOptions({
    name: 'DashboardSkeleton'
})
</script>

<style scoped>
@keyframes shimmer {
    0% {
        background-position: -1000px 0;
    }

    100% {
        background-position: 1000px 0;
    }
}

.animate-shimmer {
    animation: shimmer 2s infinite linear;
    background: linear-gradient(to right, #f6f7f8 0%, #edeef1 20%, #f6f7f8 40%, #f6f7f8 100%);
    background-size: 1000px 100%;
}
</style>