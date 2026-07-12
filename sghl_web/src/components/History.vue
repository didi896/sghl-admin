<template>
  <div class="history-container">
    <h2><i class="fas fa-history"></i> Journal des Activités</h2>
    <div class="card">
      <table class="table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Catégorie</th>
            <th>Action</th>
            <th>Montant</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.id">
            <td>{{ new Date(log.date_creation).toLocaleString() }}</td>
            <td>{{ log.categorie }}</td>
            <td>{{ log.action }}</td>
            <td>{{ log.montant ? log.montant + ' FCFA' : '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const logs = ref([])

onMounted(async () => {
  const res = await fetch('http://127.0.0.1:8000/api/historique/')
  logs.value = await res.json()
})
const enregistrerAction = async (action, categorie, montant = 0) => {
  await fetch('http://127.0.0.1:8000/api/historique/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action, categorie, montant })
  });
};

// EXEMPLE : Appelez ceci après une vente réussie
// enregistrerAction('Vente Paracétamol', 'Vente', 500);
</script>

<style scoped>
.history-container { padding: 20px; }
.card { background: white; padding: 20px; border-radius: 12px; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 12px; border-bottom: 1px solid #eee; }
</style>