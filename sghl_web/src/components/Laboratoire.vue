<template>
  <div class="labo-container">
    <!-- Header avec bouton Ajouter -->
    <header class="labo-header">
      <div class="title-section">
        <h2><i class="fas fa-flask"></i> Laboratoire</h2>
        <p>Gestion des analyses et résultats</p>
      </div>
      <button @click="showAddModal = true" class="btn-primary">
        <i class="fas fa-plus"></i> Nouvelle Prescription
      </button>
    </header>

    <!-- Tableau des examens -->
    <div class="labo-card">
      <table class="labo-table">
        <thead>
          <tr>
            <th>Patient</th>
            <th>Examen</th>
            <th>Date</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ex in examens" :key="ex.id">
            <td><strong>{{ ex.patient_nom }}</strong></td>
            <td>{{ ex.test_nom }}</td>
            <td>{{ new Date(ex.date_prescription).toLocaleDateString() }}</td>
            <td>
              <button @click="ouvrirModalResultat(ex)" class="btn-edit">
                <i class="fas fa-edit"></i> Saisir résultat
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modale Ajouter Prescription -->
    <div v-if="showAddModal" class="modal-backdrop">
      <div class="modal-box">
        <h3>Nouvelle Prescription</h3>
        <select v-model="newExamen.patient" class="form-input">
  <option value="" disabled>Choisir un patient</option>
  <!-- On affiche le nom et le prénom pour plus de clarté -->
  <option v-for="p in patients" :key="p.id" :value="p.id">
    {{ p.first_name }} {{ p.last_name }} (ID: {{ p.id }})
  </option>
</select>
        <select v-model="newExamen.test" class="form-input">
          <option value="" disabled>Choisir le type de test</option>
          <option v-for="t in typesTests" :key="t.id" :value="t.id">{{ t.nom }}</option>
        </select>
        <div class="modal-footer">
          <button @click="showAddModal = false" class="btn-secondary">Annuler</button>
          <button @click="ajouterPrescription" class="btn-primary">Valider</button>
        </div>
      </div>
    </div>

    <!-- Modale Saisir Résultat -->
    <div v-if="showResultModal" class="modal-backdrop">
      <div class="modal-box">
        <h3>Saisie : {{ selectedExamen.test_nom }}</h3>
        <p>Patient : {{ selectedExamen.patient_nom }}</p>
        <input type="number" v-model="resultat" placeholder="Résultat numérique" class="form-input" />
        <textarea v-model="commentaire" placeholder="Observations..." class="form-input"></textarea>
        <div class="modal-footer">
          <button @click="showResultModal = false" class="btn-secondary">Fermer</button>
          <button @click="validerExamen" class="btn-success">Enregistrer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const examens = ref([])
const patients = ref([])
const typesTests = ref([])
const showAddModal = ref(false)
const showResultModal = ref(false)
const selectedExamen = ref({})
const newExamen = ref({ patient: '', test: '' })
const resultat = ref('')
const commentaire = ref('')

const chargerDonnees = async () => {
  try {
    const [resEx, resP, resT] = await Promise.all([
      fetch('http://127.0.0.1:8000/api/examens-labo/?statut=EN_ATTENTE'),
      fetch('http://127.0.0.1:8000/api/patients/'),
      fetch('http://127.0.0.1:8000/api/type-tests/')
    ])
    examens.value = await resEx.json()
    patients.value = await resP.json()
    typesTests.value = await resT.json()
  } catch (err) {
    console.error("Erreur chargement:", err)
  }
}

const ajouterPrescription = async () => {
  await fetch('http://127.0.0.1:8000/api/examens-labo/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newExamen.value)
  })
  showAddModal.value = false
  chargerDonnees()
}

const ouvrirModalResultat = (ex) => {
  selectedExamen.value = ex
  showResultModal.value = true
}

const validerExamen = async () => {
  await fetch(`http://127.0.0.1:8000/api/examens-labo/${selectedExamen.value.id}/`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resultat_valeur: resultat.value,
      commentaire: commentaire.value,
      statut: 'TERMINE'
    })
  })
  showResultModal.value = false
  chargerDonnees()
}

onMounted(chargerDonnees)
</script>

<style scoped>
.labo-container { padding: 20px; }
.labo-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
.labo-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
.labo-table { width: 100%; border-collapse: collapse; }
.labo-table th, .labo-table td { padding: 15px; border-bottom: 1px solid #e2e8f0; text-align: left; }

/* Boutons */
.btn-primary { background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; }
.btn-success { background: #10b981; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; }
.btn-edit { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
.btn-secondary { background: #64748b; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; }

/* Modales */
.modal-backdrop { position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; }
.modal-box { background: white; padding: 25px; border-radius: 12px; width: 400px; }
.form-input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #cbd5e1; border-radius: 6px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
</style>