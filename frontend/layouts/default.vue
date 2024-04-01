<template>
    <div class="flex h-screen bg-gray-100">
        <Sidebar />
        <div class="flex-1 flex flex-col">
            <Navbar />
            <slot />
        </div>

    </div>

</template>
