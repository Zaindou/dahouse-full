<template>
    <div class="bg-white shadow-md rounded-lg overflow-hidden">
        <!-- Vista de tabla para pantallas medianas y grandes -->
        <div class="hidden md:block overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th v-for="header in tableHeaders" :key="header.key" scope="col"
                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            :class="{ 'text-right': header.key === 'actions' }">
                            {{ header.label }}
                        </th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="modelo in modelos" :key="modelo.id">
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="flex items-center">
                                <div class="flex-shrink-0 h-10 w-10">
                                    <img class="h-10 w-10 rounded-full"
                                        :src="`https://ui-avatars.com/api/?name=${modelo.nombres}+${modelo.apellidos}&background=random`"
                                        :alt="`${modelo.nombres} ${modelo.apellidos}`">
                                </div>
                                <div class="ml-4">
                                    <div class="text-sm font-medium text-gray-900">
                                        {{ modelo.nombres }} {{ modelo.apellidos }}
                                    </div>
                                </div>
                            </div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="text-sm text-gray-900">{{ modelo.correo_electronico }}</div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <div class="text-sm text-gray-900">{{ modelo.rol }}</div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <span :class="modelo.habilitado ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                                class="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full">
                                {{ modelo.habilitado ? 'Activo' : 'Inactivo' }}
                            </span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                            <button @click="$emit('editar', modelo)" class="text-indigo-600 hover:text-indigo-900 mr-3">
                                Editar
                            </button>
                            <button @click="$emit('toggle-estado', modelo)"
                                :class="modelo.habilitado ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'">
                                {{ modelo.habilitado ? 'Desactivar' : 'Activar' }}
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Vista de tarjetas para móviles -->
        <div class="md:hidden">
            <div v-for="modelo in modelos" :key="modelo.id" class="bg-white shadow overflow-hidden sm:rounded-lg mb-4">
                <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
                    <div class="flex items-center">
                        <div class="flex-shrink-0 h-10 w-10">
                            <img class="h-10 w-10 rounded-full"
                                :src="`https://ui-avatars.com/api/?name=${modelo.nombres}+${modelo.apellidos}&background=random`"
                                :alt="`${modelo.nombres} ${modelo.apellidos}`">
                        </div>
                        <div class="ml-4">
                            <h3 class="text-lg leading-6 font-medium text-gray-900">
                                {{ modelo.nombres }} {{ modelo.apellidos }}
                            </h3>
                            <p class="text-sm text-gray-500">
                                {{ modelo.correo_electronico }}
                            </p>
                        </div>
                    </div>
                    <span :class="modelo.habilitado ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                        class="px-2 py-1 text-xs leading-5 font-semibold rounded-full">
                        {{ modelo.habilitado ? 'Activo' : 'Inactivo' }}
                    </span>
                </div>
                <div class="border-t border-gray-200">
                    <dl>
                        <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt class="text-sm font-medium text-gray-500">
                                Tipo de usuario
                            </dt>
                            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                {{ modelo.rol }}
                            </dd>
                        </div>
                    </dl>
                </div>
                <div class="px-4 py-3 bg-gray-50 text-right sm:px-6">
                    <button @click="$emit('editar', modelo)"
                        class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 mr-2">
                        Editar
                    </button>
                    <button @click="$emit('toggle-estado', modelo)"
                        :class="modelo.habilitado ? 'bg-red-600 hover:bg-red-700 focus:ring-red-500' : 'bg-green-600 hover:bg-green-700 focus:ring-green-500'"
                        class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2">
                        {{ modelo.habilitado ? 'Desactivar' : 'Activar' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
    modelos: {
        type: Array,
        required: true
    }
})

defineEmits(['editar', 'toggle-estado'])

const tableHeaders = ref([
    { key: 'usuario', label: 'Usuario' },
    { key: 'correo', label: 'Correo' },
    { key: 'tipo', label: 'Tipo' },
    { key: 'estado', label: 'Estado' },
    { key: 'actions', label: 'Acciones' }
])
</script>