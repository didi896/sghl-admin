<script setup>
import { onMounted } from 'vue'
import { globalStats } from '../store.js'

// Récupération de la prop passée par Dashboard.vue pour le compteur de médicaments
defineProps(['medicamentsCount'])

const refresh = async () => {
  try {
    const [resDoc, resPat] = await Promise.all([
      fetch('http://127.0.0.1:8000/api/doctors/'),
      fetch('http://127.0.0.1:8000/api/patients/')
    ])
    
    if (resDoc.ok) {
      const doctors = await resDoc.json()
      globalStats.value.doctorCount = doctors.length
    }
    if (resPat.ok) {
      const patients = await resPat.json()
      globalStats.value.patientCount = patients.length
    }
  } catch (e) {
    console.error("Erreur HomeView:", e)
  }
}

onMounted(refresh)
</script>

<template>
  <div class="home-container">
    <div class="header-section">
      <h3>Bienvenue sur Didi hospital</h3>
      <button @click="refresh" class="refresh-btn">Actualiser</button>
    </div>
    
    <div class="stats-grid">
      <!-- Carte Docteurs -->
      <div class="stat-box">
        <p>Docteurs</p>
        <div class="count-display">{{ globalStats.doctorCount }}</div>
      </div>
      
      <!-- Carte Patients -->
      <div class="stat-box">
        <p>Patients</p>
        <div class="count-display">{{ globalStats.patientCount }}</div>
      </div>

      <!-- Carte Médicaments (alignée avec les autres) -->
      <div class="stat-box">
        <p>Médicaments</p>
        <div class="count-display">{{ medicamentsCount }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container { padding: 20px; }
.header-section { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.refresh-btn { padding: 8px 16px; background: #3b82f6; color: white; border: none; border-radius: 5px; cursor: pointer; }

/* Grille alignée */
.stats-grid { display: flex; gap: 20px; }
.stat-box { 
  background: #f8fafc; 
  padding: 30px; 
  border-radius: 8px; 
  border-left: 5px solid #3b82f6; 
  width: 150px; 
  text-align: center; 
}
.count-display { font-size: 2rem; font-weight: bold; color: #1e293b; }
</style>