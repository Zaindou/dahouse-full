<template>
    <div class="flex h-full bg-gray-100">
        <Sidebar />
        <div class="flex-1 flex flex-col">
            <Navbar />
            <slot />
        </div>

    </div>

</template>
