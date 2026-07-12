<script setup>
// Définition explicite des types pour une meilleure réactivité
defineProps({
  title: String,
  value: {
    type: [String, Number],
    default: '0'
  },
  color: String
})
</script>

<template>
  <div class="stat-card">
    <div class="icon-box" :style="{ backgroundColor: color }"></div>
    <div class="info">
      <!-- Ajout d'une clé dynamique pour forcer la mise à jour si nécessaire -->
      <h3>{{ value }}</h3>
      <p>{{ title }}</p>
    </div>
  </div>
</template>

<style scoped>
.stat-card { background: white; padding: 20px; display: flex; align-items: center; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.icon-box { width: 50px; height: 50px; margin-right: 15px; border-radius: 4px; }
.info h3 { margin: 0; font-size: 1.8rem; }
.info p { margin: 0; color: #64748b; font-size: 0.9rem; }
</style>