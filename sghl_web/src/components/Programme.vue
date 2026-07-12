<script setup>
import { ref, onMounted } from 'vue';

// État pour stocker la liste des docteurs et l'état de chargement
const docteurs = ref([]);
const loading = ref(true);

// Fonction pour récupérer les docteurs depuis votre API
const chargerPlanning = async () => {
  loading.value = true;
  try {
    const res = await fetch('http://127.0.0.1:8000/api/doctors/');
    if (res.ok) {
      const data = await res.json();
      // On ajoute un champ 'statut' localement pour la gestion du planning
      docteurs.value = data.map(doc => ({
        ...doc,
        statut: doc.statut || 'Disponible' // Valeur par défaut
      }));
    }
  } catch (e) {
    console.error("Erreur lors du chargement des docteurs:", e);
    alert("Impossible de charger la liste des docteurs.");
  } finally {
    loading.value = false;
  }
};

// Fonction pour sauvegarder le changement de statut (à adapter selon votre API)
const sauvegarderDisponibilite = (doc) => {
  console.log(`Sauvegarde pour ${doc.nom} : nouveau statut = ${doc.statut}`);
  // Ici, vous pourriez faire un fetch('...', { method: 'PATCH', body: JSON.stringify(...) })
  alert(`Statut de ${doc.nom} mis à jour vers : ${doc.statut}`);
};

// Chargement initial
onMounted(chargerPlanning);
</script>

<template>
  <div class="programme-container">
    <div class="header-prog">
      <h3>Programme et Disponibilités</h3>
      <button @click="chargerPlanning" class="refresh-btn">Actualiser la liste</button>
    </div>

    <div v-if="loading" class="loading">Chargement en cours...</div>

    <table v-else class="prog-table">
      <thead>
        <tr>
          <th>Nom du Docteur</th>
          <th>Spécialité</th>
          <th>Disponibilité</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="doc in docteurs" :key="doc.id">
          <td><strong>{{ doc.nom }}</strong></td>
          <td>{{ doc.specialite || 'N/A' }}</td>
          <td>
            <select v-model="doc.statut" class="status-select">
              <option value="Disponible">Disponible</option>
              <option value="En Consultation">En Consultation</option>
              <option value="En Garde">En Garde</option>
              <option value="Congés">Congés</option>
            </select>
          </td>
          <td>
            <button class="save-btn" @click="sauvegarderDisponibilite(doc)">Enregistrer</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.programme-container { padding: 20px; background: white; border-radius: 8px; border: 1px solid #e2e8f0; }
.header-prog { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.loading { text-align: center; padding: 20px; color: #64748b; }

.prog-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
.prog-table th, .prog-table td { padding: 15px; border-bottom: 1px solid #f1f5f9; text-align: left; }
.prog-table th { background: #f8fafc; font-weight: 600; color: #475569; }

.status-select { padding: 6px; border-radius: 4px; border: 1px solid #cbd5e1; cursor: pointer; }
.refresh-btn { padding: 8px 16px; background: #64748b; color: white; border: none; border-radius: 5px; cursor: pointer; }
.save-btn { padding: 6px 12px; background: #3b82f6; color: white; border: none; border-radius: 4px; cursor: pointer; }
.save-btn:hover { background: #2563eb; }
</style>