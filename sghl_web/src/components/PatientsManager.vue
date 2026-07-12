<script setup>
import { ref, onMounted } from 'vue';
import { globalStats } from '../store.js';

const patients = ref([]);
const showModal = ref(false);
const showInfoModal = ref(false);
const modalType = ref('add');

const groupesSanguins = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];

const currentPatient = ref({ 
  nom: '', prenom: '', telephone: '', password: '', 
  date_naissance: '', email: '', adresse: '', sexe: 'M', groupe_sanguin: 'A+' 
});

const fetchPatients = async () => {
  try {
    // MODIFICATION ICI : utilisez /api/patients/
    const response = await fetch('http://127.0.0.1:8000/api/patients/');
    
    if (response.ok) {
      patients.value = await response.json();
      globalStats.value.patientCount = patients.value.length;
    } else {
      console.error("Erreur HTTP:", response.status);
    }
  } catch (error) {
    console.error("Erreur chargement patients:", error);
  }
};
const openModal = (type, patient = null) => {
  modalType.value = type;
  if (type === 'edit' && patient) {
    currentPatient.value = { ...patient };
  } else {
    currentPatient.value = { nom: '', prenom: '', telephone: '', password: '', date_naissance: '', email: '', adresse: '', sexe: 'M', groupe_sanguin: 'A+' };
  }
  showModal.value = true;
};

const openInfoModal = (patient) => {
  currentPatient.value = { ...patient };
  showInfoModal.value = true;
};

const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

const savePatient = async () => {
  // 1. Validation locale : on vérifie que les champs obligatoires ne sont pas vides
  if (!currentPatient.value.nom.trim() || !currentPatient.value.telephone.trim()) {
    alert("Le nom et le téléphone sont obligatoires.");
    return;
  }

  // 2. Préparation des données
  const payload = { ...currentPatient.value };

  // Nettoyage : si date_naissance est vide, on l'enlève pour éviter l'erreur de format
  if (!payload.date_naissance || payload.date_naissance === "") {
    delete payload.date_naissance;
  }

  // Suppression du mot de passe s'il est vide (pour ne pas écraser l'existant bêtement)
  if (!payload.password || payload.password === "") {
    delete payload.password;
  }

  const method = modalType.value === 'add' ? 'POST' : 'PUT';
  const url = modalType.value === 'add' 
    ? 'http://127.0.0.1:8000/clinical/rest/patients/' 
    : `http://127.0.0.1:8000/clinical/rest/patients/${currentPatient.value.id}/`;

  try {
    const response = await fetch(url, {
      method: method,
      headers: { 
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      showModal.value = false;
      await fetchPatients();
    } else {
      const errorData = await response.json();
      // Affiche l'erreur détaillée pour comprendre ce qui bloque côté Django
      console.error("Erreur serveur :", errorData);
      alert("Erreur serveur : " + JSON.stringify(errorData));
    }
  } catch (error) {
    console.error("Erreur de connexion :", error);
  }
};

  // Note: Si votre input type="date" est bien utilisé, il envoie déjà du YYYY-MM-DD.
  // Si le champ est vide, on envoie null pour éviter les erreurs de format.
  const payload = { ...currentPatient.value };
  if (!payload.date_naissance) delete payload.date_naissance;

  const method = modalType.value === 'add' ? 'POST' : 'PUT';
  const url = modalType.value === 'add' 
    ? 'http://127.0.0.1:8000/clinical/rest/patients/' 
    : `http://127.0.0.1:8000/clinical/rest/patients/${currentPatient.value.id}/`;

  try {
    const response = await fetch(url, {
      method: method,
      headers: { 
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      showModal.value = false;
      await fetchPatients();
    } else {
      const errorData = await response.json();
      console.error("Erreur serveur :", errorData);
      alert("Erreur : " + JSON.stringify(errorData));
    }
  } catch (error) {
    console.error("Erreur de connexion :", error);
  }
};

const deletePatient = async (id) => {
  if (confirm("Supprimer ce patient ?")) {
    await fetch(`http://127.0.0.1:8000/clinical/rest/patients/${id}/`, { method: 'DELETE', headers: { 'X-CSRFToken': getCookie('csrftoken') } });
    fetchPatients();
  }
};

onMounted(fetchPatients);
</script>

<template>
  <div class="patients-manager">
    <!-- Le reste de votre template reste identique -->
    <div class="header-section">
      <h3>Liste des patients</h3>
      <button class="btn-add" @click="openModal('add')">+ Ajouter nouveau</button>
    </div>

    <table class="patient-table">
      <thead>
        <tr>
          <th>Nom / Prénom</th>
          <th>Téléphone</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in patients" :key="p.id">
          <td>{{ p.nom }} {{ p.prenom }}</td>
          <td>{{ p.telephone }}</td>
          <td class="options-cell">
            <button class="btn-info" @click="openInfoModal(p)">Info</button>
            <button class="btn-modify-list" @click="openModal('edit', p)">Modifier</button>
            <button class="btn-delete-list" @click="deletePatient(p.id)">Effacer</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content-large">
        <h3>{{ modalType === 'add' ? 'Ajouter' : 'Modifier' }} le patient</h3>
        <div class="form-grid">
          <div class="form-column">
            <label>Nom *</label>
            <input v-model="currentPatient.nom" class="sghl-input" />
            <label>Prénom *</label>
            <input v-model="currentPatient.prenom" class="sghl-input" />
            <label>Mot de passe</label>
            <input v-model="currentPatient.password" type="password" class="sghl-input" />
            <label>Téléphone *</label>
            <input v-model="currentPatient.telephone" class="sghl-input" />
            <label>Date de naissance</label>
            <input v-model="currentPatient.date_naissance" type="date" class="sghl-input" />
          </div>
          <div class="form-column">
            <label>Email *</label>
            <input v-model="currentPatient.email" class="sghl-input" />
            <label>Adresse *</label>
            <input v-model="currentPatient.adresse" class="sghl-input" />
            <label>Sexe</label>
            <select v-model="currentPatient.sexe" class="sghl-input">
              <option value="M">Male</option>
              <option value="F">Female</option>
            </select>
            <label>Groupe sanguin</label>
            <select v-model="currentPatient.groupe_sanguin" class="sghl-input">
              <option v-for="g in groupesSanguins" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="showModal = false" class="btn-cancel">Annuler</button>
          <button @click="savePatient" class="btn-save">Enregistrer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Vos styles existants */
.patients-manager { background: white; padding: 20px; border-radius: 8px; }
.header-section { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.patient-table { width: 100%; border-collapse: collapse; }
.patient-table th, .patient-table td { padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: left; }
.options-cell { display: flex; gap: 8px; }
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content-large { background: white; padding: 30px; border-radius: 8px; width: 600px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px; }
.form-column { display: flex; flex-direction: column; }
label { font-size: 0.85rem; font-weight: bold; margin-top: 10px; color: #475569; }
.modal-actions { margin-top: 20px; display: flex; justify-content: flex-end; gap: 10px; }
.sghl-input { width: 100%; padding: 8px; margin-top: 5px; border-radius: 4px; border: 1px solid #ccc; box-sizing: border-box; }
button { cursor: pointer; border: none; border-radius: 4px; font-size: 12px; padding: 5px 10px; }
.btn-add { background: #059669; color: white; padding: 10px 15px; font-weight: bold; }
.btn-save { background: #3b82f6; color: white; padding: 8px 15px; }
.btn-cancel { background: #e5e7eb; padding: 8px 15px; }
.btn-modify-list { background: #10b981; color: white; }
.btn-delete-list { background: #ef4444; color: white; }
.btn-info { background: #6366f1; color: white; }
</style>