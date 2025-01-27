<template>
    <div class="flex h-full bg-gray-100">
        <Sidebar />
        <div class="flex flex-col flex-1">
                <Toaster 
      richColors
      expand
      closeButton
      position="bottom-center"
    />
            <Navbar />
            <slot />
        </div>

    </div>

</template>

<script>
import { toast } from 'vue-sonner';
</script>
