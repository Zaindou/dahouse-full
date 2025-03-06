
// componentes/rules/PercentageSection.vue - Componente para la sección de porcentajes
<template>
  <RuleCard :title="title" icon="uil:percentage" :headerClass="headerClass">
    <p class="mb-4 text-gray-700">{{ description }}</p>
    <div class="flex justify-between p-4 bg-gray-100 rounded-lg">
      <span class="font-medium">Modelo:</span>
      <span class="font-medium">{{ modelPercentage }}%</span>
    </div>
    <div class="flex justify-between p-4">
      <span class="font-medium">Estudio:</span>
      <span class="font-medium">{{ studioPercentage }}%</span>
    </div>
  </RuleCard>
</template>

<script setup>
import RuleCard from './RuleCard.vue';

const props = defineProps({
  title: {
    type: String,
    default: 'Porcentajes de Ganancia'
  },
  description: {
    type: String,
    required: true
  },
  modelPercentage: {
    type: Number,
    required: true
  },
  studioPercentage: {
    type: Number,
    required: true
  },
  headerClass: {
    type: String,
    default: 'bg-purple-700'
  }
});
</script>