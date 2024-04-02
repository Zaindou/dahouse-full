<template>
    <div class="loading-container" v-if="isLoading">
        <div class="loading-text">
            <span v-for="(letra, index) in palabra" :key="index" :class="'letra-' + index">{{ letra }}</span>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        isLoading: {
            type: Boolean,
            required: true
        }
    },
    data() {
        return {
            palabra: 'DAHOUSE'.split('')
        };
    }
}
</script>

<style scoped>
.loading-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(255, 255, 255, 0.7);
    z-index: 9999;
}

.loading-text {
    font-size: 2rem;
    font-weight: bold;
}

@keyframes desaparecer {
    0% {
        opacity: 1;
    }

    100% {
        opacity: 0;
    }
}

.letra-0 {
    animation: desaparecer 1s infinite;
}

.letra-1 {
    animation: desaparecer 1s infinite 0.2s;
}

.letra-2 {
    animation: desaparecer 1s infinite 0.4s;
}

.letra-3 {
    animation: desaparecer 1s infinite 0.6s;
}

.letra-4 {
    animation: desaparecer 1s infinite 0.8s;
}

.letra-5 {
    animation: desaparecer 1s infinite 1s;
}
</style>
