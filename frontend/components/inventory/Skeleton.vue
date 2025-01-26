<template>
  <div class="animate-pulse">
    <!-- Header Skeleton -->
    <div class="flex flex-col gap-4 mb-8 md:flex-row md:items-center md:justify-between">
      <div>
        <div class="w-48 h-8 bg-gray-200 rounded-lg"></div>
        <div class="w-64 h-4 mt-2 bg-gray-200 rounded-lg"></div>
      </div>
      <div class="flex flex-col gap-3 sm:flex-row">
        <div class="w-32 h-10 bg-gray-200 rounded-lg"></div>
        <div class="w-32 h-10 bg-gray-200 rounded-lg"></div>
      </div>
    </div>

    <!-- Filters Skeleton -->
    <div class="p-6 mb-6 bg-white shadow-sm rounded-xl">
      <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
        <div class="space-y-2">
          <div class="w-20 h-4 bg-gray-200 rounded"></div>
          <div class="w-full h-10 bg-gray-200 rounded-lg"></div>
        </div>
        <div class="space-y-2">
          <div class="w-20 h-4 bg-gray-200 rounded"></div>
          <div class="w-full h-10 bg-gray-200 rounded-lg"></div>
        </div>
        <div class="space-y-2">
          <div class="w-20 h-4 bg-gray-200 rounded"></div>
          <div class="w-full h-10 bg-gray-200 rounded-lg"></div>
        </div>
      </div>
    </div>

    <!-- Table Skeleton -->
    <div class="overflow-hidden bg-white shadow-sm rounded-xl">
      <div class="overflow-x-auto">
        <!-- Table Header -->
        <div class="grid grid-cols-1 gap-4 p-4 md:hidden">
          <div v-for="i in 3" :key="i" class="p-4 rounded-lg bg-gray-50">
            <div class="w-32 h-4 mb-2 bg-gray-200 rounded"></div>
            <div class="w-24 h-4 mb-2 bg-gray-200 rounded"></div>
            <div class="w-20 h-4 bg-gray-200 rounded"></div>
          </div>
        </div>

        <table class="hidden min-w-full divide-y divide-gray-200 md:table">
          <thead class="bg-gray-50">
            <tr>
              <th v-for="i in 7" :key="i" class="px-6 py-4">
                <div class="w-24 h-4 bg-gray-200 rounded"></div>
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="i in 5" :key="i">
              <td class="px-6 py-4">
                <div class="w-32 h-4 mb-1 bg-gray-200 rounded"></div>
                <div class="w-24 h-4 bg-gray-200 rounded"></div>
              </td>
              <td class="px-6 py-4">
                <div class="w-24 h-6 bg-gray-200 rounded-full"></div>
              </td>
              <td class="px-6 py-4">
                <div class="w-16 h-6 bg-gray-200 rounded-full"></div>
              </td>
              <td class="px-6 py-4">
                <div class="w-20 h-4 bg-gray-200 rounded"></div>
              </td>
              <td class="px-6 py-4">
                <div class="w-24 h-6 bg-gray-200 rounded-full"></div>
              </td>
              <td class="px-6 py-4">
                <div class="w-32 h-4 bg-gray-200 rounded"></div>
              </td>
              <td class="px-6 py-4">
                <div class="flex justify-end space-x-3">
                  <div class="w-8 h-8 bg-gray-200 rounded-lg"></div>
                  <div class="w-8 h-8 bg-gray-200 rounded-lg"></div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>