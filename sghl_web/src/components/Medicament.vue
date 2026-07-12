<script setup>
import { ref, computed } from 'vue';

// On reçoit la liste via les props depuis App.vue
const props = defineProps(['list']);
const emit = defineEmits(['update:list']);

// Propriété calculée pour synchroniser les changements avec App.vue
const medicaments = computed({
  get: () => props.list,
  set: (value) => emit('update:list', value)
});

const editMode = ref(false);
const currentMedoc = ref({ id: null, nom: '', stock: 0, prix: 0 });

// Actions
const sauvegarderMedicament = () => {
  if (!currentMedoc.value.nom.trim()) {
    alert("Veuillez entrer un nom de médicament.");
    return;
  }

  // Création d'une copie pour éviter les problèmes de mutation directe
  let newList = [...medicaments.value];

  if (currentMedoc.value.id) {
    // Mode Modification
    const index = newList.findIndex(m => m.id === currentMedoc.value.id);
    if (index !== -1) {
      newList[index] = { ...currentMedoc.value };
    }
  } else {
    // Mode Ajout
    newList.push({ ...currentMedoc.value, id: Date.now() });
  }
  
  medicaments.value = newList;
  resetForm();
};

const editerMedicament = (m) => {
  editMode.value = true;
  currentMedoc.value = { ...m };
};

const supprimerMedicament = (id) => {
  if (confirm("Voulez-vous vraiment supprimer ce médicament ?")) {
    medicaments.value = medicaments.value.filter(m => m.id !== id);
  }
};

const vendreMedicament = (m) => {
  if (m.stock > 0) {
    m.stock--;
    alert(`Vente effectuée : ${m.nom}. Stock restant : ${m.stock}`);
  } else {
    alert("Rupture de stock !");
  }
};

const resetForm = () => {
  currentMedoc.value = { id: null, nom: '', stock: 0, prix: 0 };
  editMode.value = false;
};
</script>

<template>
  <div class="medicament-container">
    <h3>Gestion des Médicaments</h3>

    <!-- Formulaire d'ajout / modification -->
    <div class="admin-section">
      <input v-model="currentMedoc.nom" placeholder="Nom du médicament" class="inline-input" />
      <input v-model.number="currentMedoc.stock" type="number" placeholder="Stock" class="inline-input" style="width: 80px;" />
      <input v-model.number="currentMedoc.prix" type="number" placeholder="Prix" class="inline-input" style="width: 100px;" />
      
      <button class="med-btn" :class="editMode ? 'med-btn--blue' : 'med-btn--green'" @click="sauvegarderMedicament">
        {{ editMode ? 'Modifier' : 'Ajouter' }}
      </button>
      
      <button v-if="editMode" class="med-btn" @click="resetForm" style="margin-left: 5px;">Annuler</button>
    </div>

    <!-- Liste des médicaments -->
    <div v-for="m in medicaments" :key="m.id" class="patient-item">
      <div>
        <strong>{{ m.nom }}</strong> <br>
        <small>Stock: {{ m.stock }} | Prix: {{ m.prix }} FCFA</small>
      </div>
      <div style="display: flex; gap: 8px;">
        <button class="med-btn med-btn--blue" @click="vendreMedicament(m)" :disabled="m.stock === 0">Vendre</button>
        <button class="med-btn" @click="editerMedicament(m)">Éditer</button>
        <button class="med-btn med-btn--red" @click="supprimerMedicament(m.id)">Supprimer</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.medicament-container { padding: 20px; background: white; border-radius: 8px; border: 1px solid #e2e8f0; }
.admin-section { display: flex; gap: 10px; margin-bottom: 20px; padding: 15px; background: #f8fafc; border-radius: 6px; }
.inline-input { padding: 8px; border: 1px solid #cbd5e1; border-radius: 4px; }
.patient-item { display: flex; justify-content: space-between; padding: 12px; border-bottom: 1px solid #f1f5f9; align-items: center; }

.med-btn { padding: 8px 12px; border: none; border-radius: 4px; cursor: pointer; font-weight: 600; }
.med-btn--green { background: #22c55e; color: white; }
.med-btn--blue { background: #3b82f6; color: white; }
.med-btn--red { background: #ef4444; color: white; }
.med-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>