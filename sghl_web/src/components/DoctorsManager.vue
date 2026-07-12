<script setup>
import { ref, onMounted } from 'vue'
import { globalStats } from '../store.js'

const doctors = ref([])
const showModal = ref(false)
const showInfoModal = ref(false) // Nouvelle modale Info
const isEditing = ref(false)
const editingId = ref(null)

const formData = ref({ 
  nom: '', prenom: '', specialite: '', telephone: '', email: '', sexe: '', 
  salaire: '', horaire: '', date_naissance: '' 
})

const fetchDoctors = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/doctors/')
    if (response.ok) {
      doctors.value = await response.json()
      globalStats.value.doctorCount = doctors.value.length
    }
  } catch (error) { 
    console.error("Erreur chargement:", error) 
  }
}

const openAddModal = () => {
  isEditing.value = false
  formData.value = { nom: '', prenom: '', specialite: '', telephone: '', email: '', sexe: '', salaire: '', horaire: '', date_naissance: '' }
  showModal.value = true
}

const editDoctor = (doctor) => {
  isEditing.value = true
  editingId.value = doctor.id
  formData.value = { ...doctor }
  showModal.value = true
}

const openInfoModal = (doctor) => {
  formData.value = { ...doctor }
  showInfoModal.value = true
}

const saveDoctor = async () => {
  // 1. Créer une copie pour ne pas modifier l'affichage original
  const payload = { ...formData.value };

  // 2. Nettoyer le salaire : extraire uniquement les chiffres
  // Cela transforme "200000franc cfa" en 200000
  if (payload.salaire) {
    payload.salaire = parseFloat(String(payload.salaire).replace(/[^0-9.]/g, ''));
  } else {
    payload.salaire = null;
  }

  // 3. S'assurer que la date est null si vide
  if (!payload.date_naissance) payload.date_naissance = null;

  const url = isEditing.value 
    ? `http://127.0.0.1:8000/api/doctors/${editingId.value}/` 
    : 'http://127.0.0.1:8000/api/doctors/';
  
  const response = await fetch(url, {
    method: isEditing.value ? 'PUT' : 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload) // On envoie le payload nettoyé
  });

  if (response.ok) {
    showModal.value = false;
    await fetchDoctors();
  } else {
    const errorData = await response.json();
    console.error("Détail de l'erreur API :", errorData);
    alert("Erreur : " + JSON.stringify(errorData));
  }
};
const deleteDoctor = async (id) => {
  if (confirm("Supprimer ce médecin ?")) {
    const response = await fetch(`http://127.0.0.1:8000/api/doctors/${id}/`, { method: 'DELETE' })
    if (response.ok) await fetchDoctors()
  }
}

onMounted(fetchDoctors)
</script>

<template>
  <div class="doctors-manager">
    <div class="header-section">
      <h3>Liste des médecins</h3>
      <button class="btn-add" @click="openAddModal">+ Ajouter Médecin</button>
    </div>
    
    <table class="modern-table">
      <thead>
        <tr>
          <th>Nom / Prénom</th>
          <th>Spécialité</th>
          <th>Téléphone</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="d in doctors" :key="d.id">
          <td>{{ d.nom }} {{ d.prenom }}</td>
          <td>{{ d.specialite }}</td>
          <td>{{ d.telephone }}</td>
          <td>
            <button class="btn-info" @click="openInfoModal(d)">Info</button>
            <button class="btn-edit" @click="editDoctor(d)">Modifier</button>
            <button class="btn-delete" @click="deleteDoctor(d.id)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>

<!-- Modale Formulaire -->
<div v-if="showModal" class="modal-overlay">
  <div class="modal-content">
    <h4>{{ isEditing ? 'Modifier' : 'Nouveau' }} Médecin</h4>
    <input v-model="formData.nom" placeholder="Nom" class="sghl-input">
    <input v-model="formData.prenom" placeholder="Prénom" class="sghl-input">
    <input v-model="formData.date_naissance" type="date" class="sghl-input">
    
    <select v-model="formData.specialite" class="sghl-input">
      <option value="" disabled>Choisir une spécialité</option>
      <option value="Maternité">Maternité</option>
      <option value="Pédiatrie">Pédiatrie</option>
      <option value="Ophtalmologie">Ophtalmologie</option>
      <option value="Consultation">Consultation</option>
      <option value="Cardiologie">Cardiologie</option>
      <option value="Neurologie">Neurologie</option>
      <option value="Gynécologie">Gynécologie</option>
    </select>

    <input v-model="formData.salaire" placeholder="Salaire" class="sghl-input">
    <!-- Nouveau champ ajouté ici -->
    <input v-model="formData.jours_travail" placeholder="Jours de travail (ex: Lundi-Vendredi)" class="sghl-input">
    <input v-model="formData.horaire" placeholder="Horaire" class="sghl-input">
    <input v-model="formData.telephone" placeholder="Téléphone" class="sghl-input">
    <input v-model="formData.email" placeholder="Email" class="sghl-input">
    
    <select v-model="formData.sexe" class="sghl-input">
      <option value="" disabled>Sexe</option>
      <option value="M">Masculin</option>
      <option value="F">Féminin</option>
    </select>
    <div class="modal-actions">
      <button @click="showModal = false">Annuler</button>
      <button class="btn-add" @click="saveDoctor">Enregistrer</button>
    </div>
  </div>
</div>

<!-- Modale Info -->
<div v-if="showInfoModal" class="modal-overlay">
  <div class="modal-content">
    <h3>Détails du Médecin</h3>
    <p><strong>Nom:</strong> {{ formData.nom }}</p>
    <p><strong>Prénom:</strong> {{ formData.prenom }}</p>
    <p><strong>Spécialité:</strong> {{ formData.specialite }}</p>
    <p><strong>Date Naissance:</strong> {{ formData.date_naissance }}</p>
    <p><strong>Salaire:</strong> {{ formData.salaire }}</p>
    <!-- Nouveau champ ajouté avant horaire -->
    <p><strong>Jours de travail:</strong> {{ formData.jours_travail }}</p>
    <p><strong>Horaire:</strong> {{ formData.horaire }}</p>
    <div class="modal-actions">
      <button @click="showInfoModal = false">Fermer</button>
    </div>
  </div>
</div>

<!-- Modale Info (Ajoute la ligne Spécialité ici) -->
<div v-if="showInfoModal" class="modal-overlay">
  <div class="modal-content">
    <h3>Détails du Médecin</h3>
    <p><strong>Nom:</strong> {{ formData.nom }}</p>
    <p><strong>Prénom:</strong> {{ formData.prenom }}</p>
    <p><strong>Spécialité:</strong> {{ formData.specialite }}</p> <!-- Nouvelle ligne ajoutée -->
    <p><strong>Date Naissance:</strong> {{ formData.date_naissance }}</p>
    <p><strong>Salaire:</strong> {{ formData.salaire }}</p>
    <p><strong>Jours de travail:</strong> {{ formData.jours_travail }}</p>
    <p><strong>Horaire:</strong> {{ formData.horaire }}</p>
    <div class="modal-actions">
      <button @click="showInfoModal = false">Fermer</button>
    </div>
  </div>
</div>

 
  </div>
</template>

<style scoped>
.doctors-manager { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.header-section { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.modern-table { width: 100%; border-collapse: collapse; }
.modern-table th, .modern-table td { padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: left; }
.sghl-input { padding: 8px; border: 1px solid #d1d5db; border-radius: 4px; margin-bottom: 5px; width: 100%; box-sizing: border-box; }
.btn-add { background: #3b82f6; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
.btn-edit { background: #f3f4f6; border: 1px solid #d1d5db; padding: 4px 8px; border-radius: 4px; margin-right: 5px; cursor: pointer; }
.btn-delete { background: #fee2e2; color: #ef4444; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; }
.btn-info { background: #6366f1; color: white; border: none; padding: 4px 8px; border-radius: 4px; margin-right: 5px; cursor: pointer; }
.modal-overlay { position: fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; z-index: 1000; }
.modal-content { background:white; padding:20px; border-radius:8px; display:flex; flex-direction:column; gap:10px; width:400px; }
.modal-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 10px; }
</style>