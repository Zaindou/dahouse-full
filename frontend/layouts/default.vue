<template>
    <div class="flex h-screen bg-gray-100">
        <Sidebar />
        <div class="flex-1 flex flex-col">
            <Navbar />
            <slot />
        </div>

    </div>

</template>

<script setup>
import Sidebar from '~/components/Sidebar.vue';
import Navbar from '~/components/Navbar.vue';
import Footer from '~/components/Footer.vue';
</script>