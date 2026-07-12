<script setup>
import { ref, onMounted } from 'vue'

const stats = ref({ patients: 0, ordonnances: 0, stocksCritiques: 0 })
const loading = ref(true)
const typeSelection = ref('patient')
const listeSelection = ref([])
const selectedId = ref(null)

const fetchStats = async () => {
  loading.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/api/rapport-stats/')
    if (res.ok) stats.value = await res.json()
  } finally { loading.value = false }
}


const chargerSelection = async () => {
  const endpoint = typeSelection.value === 'patient' ? 'patients' : 'ordonnances'
  const res = await fetch('http://127.0.0.1:8000/clinical/rapport-stats/')
  const data = await res.json()
  
  // Si vous utilisez Django Rest Framework par défaut, les données sont souvent dans "data.results"
  // Sinon, c'est juste "data"
  listeSelection.value = data.results ? data.results : data
  console.log("Données chargées :", listeSelection.value) // Vérifiez ici ce que vous recevez
}

const rapportDetail = ref(null) // Pour stocker les infos du patient ou ordonnance

const fetchDetails = async () => {
  if (!selectedId.value) return alert("Veuillez sélectionner un élément")
  
  try {
    // Appel vers votre API (ex: /api/patients/ID/ ou /api/ordonnances/ID/)
    const endpoint = typeSelection.value === 'patient' ? 'patients' : 'ordonnances'
    const res = await fetch(`http://127.0.0.1:8000/api/${endpoint}/${selectedId.value}/`)
    
    if (res.ok) {
      rapportDetail.value = await res.json()
      // Ici, vous pouvez ouvrir une modale ou naviguer vers une page de rapport
      console.log("Détails reçus :", rapportDetail.value)
    }
  } catch (e) {
    console.error("Erreur récupération détails:", e)
  }
}
</script>

<template>
  <div class="dashboard-wrapper">
    <!-- Header avec effet de transparence -->
    <header class="glass-header">
      <h1>Rapport d'Activité</h1>
      <button class="btn-refresh" @click="fetchStats">Actualiser</button>
    </header>

    <!-- Stats avec design moderne -->
    <div class="stats-grid">
      <div class="card" v-for="(val, key) in stats" :key="key">
        <span class="label">{{ key.toUpperCase() }}</span>
        <span class="value">{{ val }}</span>
        <div class="card-line"></div>
      </div>
    </div>

    <!-- Section de sélection stylisée -->
    <div class="control-panel">
      <h3>Générer un rapport ciblé</h3>
      <div class="input-group">
        <select v-model="typeSelection" @change="chargerSelection">
          <option value="patient">Patient</option>
          <option value="ordonnance">Ordonnance</option>
        </select>
        <select v-model="selectedId">
  <option v-for="item in listeSelection" :key="item.id" :value="item.id">
    {{ item.nom }} {{ item.prenom }} ({{ item.code_sghl }})
  </option>
</select>
        <!-- Dans le template, remplacez le bouton par celui-ci -->
<button class="btn-action" @click="fetchDetails">Afficher Détails</button>

<!-- Zone d'affichage des résultats -->
<div v-if="rapportDetail" class="report-result">
  <h3>Détails du {{ typeSelection }}</h3>
  <pre>{{ rapportDetail }}</pre> <!-- Affiche les données brutes pour commencer -->
  
  <!-- Exemple d'affichage propre pour un patient -->
  <div v-if="typeSelection === 'patient'" class="details-card">
    <p><strong>Nom:</strong> {{ rapportDetail.nom }} {{ rapportDetail.prenom }}</p>
    <p><strong>IPP:</strong> {{ rapportDetail.ipp }}</p>
    <p><strong>Code SGHL:</strong> {{ rapportDetail.code_sghl }}</p>
  </div>
</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.report-result {
  margin-top: 30px;
  padding: 25px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  border: 1px solid #38bdf8;
}

.details-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-top: 15px;
}

.dashboard-wrapper { padding: 40px; background: #0f172a; min-height: 100vh; color: white; }

.glass-header { 
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 30px; background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px); border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);
}

.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px; }

.card { 
  padding: 30px; background: linear-gradient(145deg, #1e293b, #0f172a);
  border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);
  display: flex; flex-direction: column; transition: 0.4s;
}
.card:hover { transform: scale(1.02); border-color: #38bdf8; }
.value { font-size: 3rem; font-weight: 800; margin-top: 10px; color: #38bdf8; }

.control-panel { 
  margin-top: 40px; padding: 30px; background: rgba(255,255,255,0.02);
  border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);
}

.input-group { display: flex; gap: 15px; margin-top: 20px; }
select { 
  padding: 12px 20px; border-radius: 10px; background: #1e293b; 
  border: 1px solid #334155; color: white; cursor: pointer;
}

.btn-action { 
  padding: 12px 25px; border-radius: 10px; border: none;
  background: linear-gradient(to right, #38bdf8, #818cf8);
  color: white; font-weight: bold; cursor: pointer; transition: 0.3s;
}
.btn-action:hover { box-shadow: 0 0 20px rgba(56, 189, 248, 0.4); }
</style>