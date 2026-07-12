<script setup>
import { ref, onMounted } from 'vue';

const visits = ref([]);
const patients = ref([]); // Pour lier une visite à un patient
const currentVisit = ref({ patient: '', date: '', diagnostic: '', traitement: '' });

// Récupération des données
const fetchVisits = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/visites/');
  if (response.ok) visits.value = await response.json();
};

const saveVisit = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/visites/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(currentVisit.value)
  });
  if (response.ok) {
    alert("Visite enregistrée !");
    currentVisit.value = { patient: '', date: '', diagnostic: '', traitement: '' };
    fetchVisits();
  }
};

onMounted(fetchVisits);
</script>

<template>
  <div class="visit-container">
    <h3>Nouvelle Visite Médicale</h3>
    <div class="visit-form">
      <input v-model="currentVisit.date" type="date" class="sghl-input" />
      <textarea v-model="currentVisit.diagnostic" placeholder="Diagnostic" class="sghl-input"></textarea>
      <textarea v-model="currentVisit.traitement" placeholder="Traitement prescrit" class="sghl-input"></textarea>
      <button @click="saveVisit" class="btn-save">Enregistrer la visite</button>
    </div>

    <table class="visit-table">
      <tr v-for="v in visits" :key="v.id">
        <td>{{ v.date }}</td>
        <td>{{ v.diagnostic }}</td>
      </tr>
    </table>
  </div>
</template>

<style scoped>
.visit-container { background: white; padding: 20px; border-radius: 8px; }
.visit-form { display: flex; flex-direction: column; gap: 10px; max-width: 500px; }
.sghl-input { padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
.btn-save { background: #3b82f6; color: white; padding: 10px; border: none; border-radius: 4px; cursor: pointer; }
</style>