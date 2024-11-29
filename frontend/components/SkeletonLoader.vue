<template>
    <div class="animate-pulse m-5">
        <!-- Header and Search Skeleton -->
        <div class="mb-4 flex flex-col sm:flex-row justify-between items-center">
            <div class="h-8 w-48 bg-gray-200 rounded mb-4 sm:mb-0"></div>
            <div class="relative w-full sm:w-64">
                <div class="h-10 w-full bg-gray-200 rounded-full"></div>
            </div>
        </div>

        <!-- Table Skeleton - Hidden on Mobile -->
        <div class="hidden md:block overflow-x-auto bg-white shadow-md rounded-lg">
            <div class="min-w-full">
                <div class="border-b border-gray-200 bg-gray-50 h-12"></div>
                <div class="divide-y divide-gray-200">
                    <div v-for="i in 5" :key="i" class="bg-white">
                        <div class="px-6 py-4">
                            <div class="flex items-center">
                                <div class="flex-shrink-0 h-10 w-10 bg-gray-200 rounded-full"></div>
                                <div class="ml-4 flex-1">
                                    <div class="h-4 w-48 bg-gray-200 rounded mb-2"></div>
                                    <div class="h-3 w-32 bg-gray-200 rounded"></div>
                                </div>
                                <div class="flex space-x-3">
                                    <div class="h-8 w-24 bg-gray-200 rounded"></div>
                                    <div class="h-8 w-24 bg-gray-200 rounded"></div>
                                    <div class="h-8 w-24 bg-gray-200 rounded"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Cards Skeleton - Shown on Mobile -->
        <div class="md:hidden space-y-4">
            <div v-for="i in 3" :key="i" class="bg-white shadow overflow-hidden sm:rounded-lg">
                <div class="px-4 py-5 sm:px-6">
                    <div class="flex items-center">
                        <div class="flex-shrink-0 h-10 w-10 bg-gray-200 rounded-full"></div>
                        <div class="ml-4 flex-1">
                            <div class="h-4 w-32 bg-gray-200 rounded mb-2"></div>
                            <div class="h-3 w-24 bg-gray-200 rounded"></div>
                        </div>
                    </div>
                </div>
                <div class="border-t border-gray-200 px-4 py-5">
                    <div class="space-y-3">
                        <div class="h-8 w-full bg-gray-200 rounded"></div>
                        <div class="h-8 w-full bg-gray-200 rounded"></div>
                        <div class="h-8 w-full bg-gray-200 rounded"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pagination Skeleton -->
        <div class="mt-4 flex items-center justify-between">
            <div class="h-4 w-48 bg-gray-200 rounded"></div>
            <div class="flex space-x-2">
                <div class="h-8 w-20 bg-gray-200 rounded"></div>
                <div class="h-8 w-20 bg-gray-200 rounded"></div>
            </div>
        </div>
    </div>
</template>

<script setup>
// No need for props or additional logic
</script>