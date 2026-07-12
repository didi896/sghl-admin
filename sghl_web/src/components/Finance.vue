<template>
  <div class="finance-wrapper">
    <header class="finance-header">
      <h2><i class="fas fa-file-invoice-dollar"></i> Activités Financières</h2>
      <div class="stats-summary">
        <div class="stat-card">
          <span>Revenu Total</span>
          <h3>{{ totalRevenu }} FCFA</h3>
        </div>
      </div>
    </header>

    <div class="finance-card">
      <h3>Dernières transactions</h3>
      <table class="finance-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Patient</th>
            <th>Type</th>
            <th>Montant</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="facture in factures" :key="facture.id">
            <td>{{ new Date(facture.date).toLocaleDateString() }}</td>
            <td>{{ facture.patient_nom }}</td>
            <td>{{ facture.type_service }}</td>
            <td><strong>{{ facture.montant }} FCFA</strong></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const factures = ref([])

// Calcul du total en temps réel
const totalRevenu = computed(() => {
  return factures.value.reduce((sum, f) => sum + parseFloat(f.montant || 0), 0)
})

const chargerFinance = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/factures/')
    factures.value = await res.json()
  } catch (e) {
    console.error("Erreur de chargement des finances", e)
  }
}

onMounted(chargerFinance)
</script>

<style scoped>
.finance-wrapper { padding: 20px; }
.finance-header { margin-bottom: 25px; }
.stats-summary { display: flex; gap: 20px; margin-top: 15px; }
.stat-card { background: #3b82f6; color: white; padding: 20px; border-radius: 12px; min-width: 200px; }
.finance-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
.finance-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
.finance-table th, .finance-table td { padding: 15px; border-bottom: 1px solid #f1f5f9; text-align: left; }
</style>