<template>
  <div class="appointment-wrapper">
    <header class="header">
      <h2><i class="fas fa-calendar-alt"></i> Prise de Rendez-vous</h2>
      <button @click="showModal = true" class="btn-primary">Nouveau RDV</button>
    </header>

    <!-- Liste des rendez-vous existants -->
    <div class="card">
      <table class="table">
        <thead>
          <tr>
            <th>Patient</th>
            <th>Docteur</th>
            <th>Date & Heure</th>
            <th>Statut</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rdv in rendezVous" :key="rdv.id">
            <td>{{ rdv.patient_nom }}</td>
            <td>Dr. {{ rdv.docteur_nom }}</td>
            <td>{{ new Date(rdv.date_heure).toLocaleString() }}</td>
            <td><span class="badge">{{ rdv.statut }}</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modale de création -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-card">
        <h3>Réserver un rendez-vous</h3>
        
        <select v-model="form.docteur" class="input" @change="chargerHoraires">
          <option value="" disabled>Sélectionner un docteur</option>
          <option v-for="doc in docteurs" :key="doc.id" :value="doc.id">Dr. {{ doc.nom }}</option>
        </select>

        <p v-if="horaires">Disponibilités : {{ horaires }}</p>

        <input type="datetime-local" v-model="form.date_heure" class="input" />

        <div class="actions">
          <button @click="showModal = false" class="btn-cancel">Annuler</button>
          <button @click="creerRendezVous" class="btn-primary">Confirmer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const rendezVous = ref([])
const docteurs = ref([])
const showModal = ref(false)
const horaires = ref('')
const form = ref({ docteur: '', date_heure: '' })

const chargerDonnees = async () => {
  const [resRDV, resDoc] = await Promise.all([
    fetch('http://127.0.0.1:8000/api/rendez-vous/'),
    fetch('http://127.0.0.1:8000/api/docteurs/')
  ])
  rendezVous.value = await resRDV.json()
  docteurs.value = await resDoc.json()
}

const chargerHoraires = (event) => {
  const doc = docteurs.value.find(d => d.id === parseInt(event.target.value))
  horaires.value = doc ? doc.horaires_travail : 'Non spécifié'
}

const creerRendezVous = async () => {
  await fetch('http://127.0.0.1:8000/api/rendez-vous/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value)
  })
  showModal.value = false
  chargerDonnees()
}

onMounted(chargerDonnees)
</script>

<style scoped>
.appointment-wrapper { padding: 20px; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 12px; border-bottom: 1px solid #eee; text-align: left; }
.modal-overlay { position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; }
.modal-card { background: white; padding: 25px; border-radius: 12px; width: 400px; display: flex; flex-direction: column; gap: 15px; }
.input { padding: 10px; border: 1px solid #ccc; border-radius: 6px; }
.btn-primary { background: #3b82f6; color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; }
.btn-cancel { background: #64748b; color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; }
.actions { display: flex; justify-content: flex-end; gap: 10px; }
.badge { background: #dcfce7; color: #166534; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; }
</style>