<template>
    <div class="flex flex-col w-64 h-full py-4 px-3 bg-gray-800">
        <div class="flex items-center justify-center mb-6">
            <!-- Un texto en blanco que diga Dahouse -->
            <h1 class="text-white text-2xl font-bold">DAHOUSE</h1>
        </div>
        <nuxt-link to="/" class="flex items-center text-white p-2 mb-2 rounded hover:bg-gray-700">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path>
            </svg>
            Inicio
        </nuxt-link>
        <nuxt-link to="/admcreadoras" class="flex items-center text-white p-2 mb-2 rounded hover:bg-gray-700">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6">
                </path>
            </svg>
            Administrar creadoras
        </nuxt-link>
        <nuxt-link to="/liquidacion" class="flex items-center text-white p-2 mb-2 rounded hover:bg-gray-700">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6">
                </path>
            </svg>
            Liquidar ganancias
        </nuxt-link>
    </div>
</template>