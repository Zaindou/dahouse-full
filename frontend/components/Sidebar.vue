<template>
    <div class="flex flex-col w-64 h-full py-4 px-3 bg-gray-800">
        <div class="flex items-center justify-center mb-6">
            <!-- Un texto en blanco que diga Dahouse -->
            <h1 class="text-white text-2xl font-bold">DAHOUSE</h1>
        </div>
        <nuxt-link to="/" class="flex items-center text-white p-2 mb-2 rounded hover:bg-gray-700">
            <Icon class="menu-icon" name="ic:sharp-menu" />
            Inicio
        </nuxt-link>
        <nuxt-link to="/admcreadoras" class="flex items-center text-white p-2 mb-2 rounded hover:bg-gray-700">
            <Icon class="menu-icon" name="ic:sharp-people" />
            Usuarios
        </nuxt-link>
        <nuxt-link to="/prestamos" class="flex items-center text-white p-2 mb-2 rounded hover:bg-gray-700">
            <Icon class="menu-icon" name="material-symbols:account-balance" />
            Deducción
        </nuxt-link>
        <nuxt-link to="/liquidacion" class="flex items-center text-white p-2 mb-2 rounded hover:bg-gray-700">
            <Icon class="menu-icon" name="ic:sharp-attach-money" />
            Liquidación
        </nuxt-link>
    </div>
</template>

<style>
.menu-icon {
    width: 25px;
    height: 25px;
    margin-right: 10px;
}
</style>