<template>
    <NuxtLayout>
        <div class="container mx-auto">
            <form @submit.prevent="liquidarGanancias" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <div class="mb-4">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="nombre_usuario">
                        Nombre de usuario:
                    </label>
                    <input
                        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        id="nombre_usuario" type="text" v-model="nombreUsuario" required>
                </div>
                <div class="flex items-center justify-between">
                    <button
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                        type="submit">
                        Liquidar Ganancias
                    </button>
                </div>
            </form>
        </div>
    </NuxtLayout>

</template>

<script>
export default {
    data() {
        return {
            nombreUsuario: ''
        }
    },
    methods: {
        liquidarGanancias() {
            alert('Hola ' + this.nombreUsuario + '!');
        }
    }
}
</script>
