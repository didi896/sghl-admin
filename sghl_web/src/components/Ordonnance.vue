<template>
  <div class="ordonnance-dashboard">
    <div class="header">
      <h2><i class="fas fa-prescription-bottle-alt"></i> Nouvelle Ordonnance</h2>
    </div>

    <div class="form-section">
      <div class="input-group">
        <label>Nom du Patient</label>
        <input v-model="form.patient" type="text" placeholder="Entrez le nom du patient" />
      </div>

      <div class="medicaments-section">
        <label>Médicaments prescrits</label>
        <div v-for="(item, index) in form.lignes" :key="index" class="ligne-med">
          <input v-model="item.nom" placeholder="Nom du médicament" class="input-field" />
          <input v-model="item.posologie" placeholder="Posologie (ex: 2x/jour)" class="input-field" />
          <button @click="supprimerLigne(index)" class="btn-del">×</button>
        </div>
        <button @click="ajouterLigne" class="btn-add-ligne">
          <i class="fas fa-plus"></i> Ajouter un médicament
        </button>
      </div>

      <div class="actions">
        <button class="btn-save" @click="imprimerOrdonnance">
          <i class="fas fa-print"></i> Imprimer (PDF)
        </button>
        <button class="btn-csv" @click="exporterCSV">
          <i class="fas fa-file-csv"></i> Exporter CSV
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const form = ref({
  patient: '',
  lignes: [{ nom: '', posologie: '' }]
});

const ajouterLigne = () => form.value.lignes.push({ nom: '', posologie: '' });
const supprimerLigne = (index) => form.value.lignes.length > 1 && form.value.lignes.splice(index, 1);

// Fonction Impression
const imprimerOrdonnance = () => {
  window.print(); // Ouvre la fenêtre d'impression du navigateur
};

// Fonction Export CSV
const exporterCSV = () => {
  let csvContent = "data:text/csv;charset=utf-8,Patient,Medicament,Posologie\n";
  form.value.lignes.forEach(l => {
    csvContent += `${form.value.patient},${l.nom},${l.posologie}\n`;
  });
  
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `ordonnance_${form.value.patient || 'patient'}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
</script>

<style scoped>
/* Ajoutez ces styles pour gérer l'impression */
@media print {
  .btn-add-ligne, .btn-del, .btn-save, .btn-csv, .sidebar { display: none !important; }
  .ordonnance-dashboard { box-shadow: none; width: 100%; }
}

.ordonnance-dashboard { padding: 25px; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); max-width: 800px; margin: auto; }
.actions { display: flex; gap: 10px; margin-top: 20px; }
.btn-save { background: #3b82f6; color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; flex: 1; }
.btn-csv { background: #10b981; color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; flex: 1; }
.input-group, .medicaments-section { margin-bottom: 20px; }
.input-field { padding: 10px; border: 1px solid #e2e8f0; border-radius: 6px; flex: 1; }
.ligne-med { display: flex; gap: 10px; margin-bottom: 10px; }
.btn-add-ligne { background: #f1f5f9; color: #475569; border: none; padding: 8px; border-radius: 6px; cursor: pointer; }
.btn-del { background: #fee2e2; color: #dc2626; border: none; padding: 0 15px; border-radius: 6px; cursor: pointer; }
</style>