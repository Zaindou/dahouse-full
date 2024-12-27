<template>
    <div class="space-y-8">
        <!-- Info Cards Skeleton -->
        <div class="grid gap-6 md:grid-cols-3">
            <div v-for="i in 3" :key="i" class="p-6 bg-white rounded-lg shadow">
                <div class="w-24 h-4 bg-gray-200 rounded animate-pulse"></div>
                <div class="w-32 h-6 mt-2 bg-gray-200 rounded animate-pulse"></div>
                <div class="w-40 h-4 mt-2 bg-gray-200 rounded animate-pulse"></div>
            </div>
        </div>

        <!-- Filter Skeleton -->
        <div class="p-4 bg-white rounded-lg shadow">
            <div class="flex flex-col space-y-4 md:flex-row md:items-center md:space-x-4 md:space-y-0">
                <div class="flex-1">
                    <div class="w-32 h-4 bg-gray-200 rounded animate-pulse"></div>
                    <div class="w-full h-10 mt-2 bg-gray-200 rounded animate-pulse"></div>
                </div>
                <div class="w-24 h-4 bg-gray-200 rounded animate-pulse"></div>
            </div>
        </div>

        <!-- Timeline Skeleton -->
        <div class="flow-root">
            <ul role="list" class="-mb-8">
                <li v-for="i in 3" :key="i" class="relative pb-8">
                    <!-- Timeline connector -->
                    <span v-if="i !== 3" class="absolute left-4 top-4 -ml-px h-full w-0.5 bg-gray-200"></span>

                    <div class="relative flex space-x-3">
                        <!-- Timeline dot -->
                        <div
                            class="flex items-center justify-center w-8 h-8 bg-gray-200 rounded-full ring-8 ring-white animate-pulse">
                        </div>

                        <!-- Content -->
                        <div class="flex-1 min-w-0">
                            <div class="p-4 bg-white rounded-lg shadow">
                                <!-- Header -->
                                <div class="flex items-center justify-between mb-4">
                                    <div class="space-y-2">
                                        <div class="w-48 h-5 bg-gray-200 rounded animate-pulse"></div>
                                        <div class="w-32 h-4 bg-gray-200 rounded animate-pulse"></div>
                                    </div>
                                    <div class="w-24 h-6 bg-gray-200 rounded animate-pulse"></div>
                                </div>

                                <!-- Details grid -->
                                <div class="grid gap-4 mb-4 md:grid-cols-3">
                                    <div v-for="j in 3" :key="j" class="p-3 rounded-lg bg-gray-50">
                                        <div class="flex items-center justify-between mb-2">
                                            <div class="w-24 h-4 bg-gray-200 rounded animate-pulse"></div>
                                            <div class="w-16 h-4 bg-gray-200 rounded animate-pulse"></div>
                                        </div>
                                        <div class="flex items-center justify-between">
                                            <div class="w-20 h-4 bg-gray-200 rounded animate-pulse"></div>
                                            <div class="w-24 h-4 bg-gray-200 rounded animate-pulse"></div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Footer -->
                                <div class="pt-4 mt-4 border-t border-gray-200">
                                    <div class="flex items-center justify-between">
                                        <div class="w-32 h-4 bg-gray-200 rounded animate-pulse"></div>
                                        <div class="w-24 h-4 bg-gray-200 rounded animate-pulse"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>