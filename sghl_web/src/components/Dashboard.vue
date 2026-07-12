<script setup>
import HomeView from './HomeView.vue'
import PatientsManager from './PatientsManager.vue'
import DoctorsManager from './DoctorsManager.vue'
import Services from './Services.vue'
import { globalStats } from '../store.js'

defineProps({
  currentView: { type: String, default: 'home' },
  medicamentsCount: { type: Number, default: 0 }
})
</script>

<template>
  <div class="dashboard-layout">
    <main class="main-content">
      <header class="header">
        <h1>{{ currentView.replace('-', ' ').toUpperCase() }}</h1>
      </header>

      <div class="content-box">
        <!-- On passe medicamentsCount à HomeView -->
        <HomeView 
          v-if="currentView === 'home'" 
          :medicamentsCount="medicamentsCount"
          :key="globalStats.doctorCount + globalStats.patientCount" 
        />
        <PatientsManager v-else-if="currentView === 'patients'" />
        <DoctorsManager v-else-if="currentView === 'doctors'" />
        <Services v-else-if="currentView === 'services'" />
        <div v-else><h3>Section {{ currentView }} en développement.</h3></div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.dashboard-layout { display: flex; min-height: 100vh; background: #f1f5f9; }
.main-content { flex: 1; padding: 30px; }
.header { margin-bottom: 30px; color: #1e293b; }
.content-box { background: white; padding: 20px; border-radius: 8px; }
</style>