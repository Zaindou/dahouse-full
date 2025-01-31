<template>
    <div class="flex h-screen overflow-hidden bg-gray-100">
        <!-- Sidebar: no fixed en móvil, fixed en lg -->
        <Sidebar class="h-screen lg:fixed lg:left-0 lg:top-0" />
        
        <!-- Contenedor principal: sin margen en móvil, con margen en lg -->
        <div class="flex flex-col flex-1 min-h-screen lg:ml-64">
            <Toaster 
                richColors
                expand
                closeButton
                position="bottom-center"
            />
            <Navbar class="sticky top-0 z-10" />
            
            <!-- Contenedor para el contenido scrolleable -->
            <div class="flex-1 p-2 overflow-y-auto">
                <slot />
            </div>
        </div>
    </div>
</template>

<script setup>
import { toast } from 'vue-sonner'
</script>