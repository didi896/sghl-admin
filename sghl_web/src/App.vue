<script setup>
import { ref } from 'vue'
import Dashboard from './components/Dashboard.vue'
import Sidebar from './components/Sidebar.vue'
import Services from './components/Services.vue'
import Medicament from './components/Medicament.vue'
import Programme from './components/Programme.vue'
import Email from './components/Email.vue'
import Pharmacie from './components/Pharmacie.vue'
import Ordonnance from './components/Ordonnance.vue'
import Rapport from './components/Rapport.vue'
import Laboratoire from './components/Laboratoire.vue'
import Finance from './components/Finance.vue'
import Appointments from './components/Appointments.vue'
import History from './components/History.vue'
import Visit from './components/Visit.vue'

const mode = ref('login')
const username = ref('')
const password = ref('')
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const pageActive = ref('home')
const userRole = ref('') // 'admin' ou 'patient'

const medicaments = ref([
  { id: 1, nom: 'Paracétamol', stock: 100, prix: 500 },
  { id: 2, nom: 'Amoxicilline', stock: 50, prix: 1200 }
]);

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

const handleLogin = async () => {
  errorMessage.value = ''; 
  isLoading.value = true;
  try {
    const response = await fetch('http://127.0.0.1:8000/api/auth/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify({ username: username.value, password: password.value })
    })
    if (response.ok) {
      const data = await response.json()
      userRole.value = data.role || 'patient' // Défini par votre API
      mode.value = 'dashboard'
    } else {
      errorMessage.value = 'Identifiants invalides.'
    }
  } catch (e) {
    errorMessage.value = 'Serveur inaccessible.'
  } finally { 
    isLoading.value = false 
  }
}

const handleRegister = async () => {
  isLoading.value = true;
  try {
    const response = await fetch('http://127.0.0.1:8000/api/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value, first_name: firstName.value, last_name: lastName.value, email: email.value })
    });
    if (response.ok) {
      successMessage.value = "Compte créé ! Connectez-vous.";
      switchMode('login');
    } else {
      errorMessage.value = "Erreur inscription.";
    }
  } catch (e) { errorMessage.value = "Erreur réseau."; } finally { isLoading.value = false; }
}

const switchMode = (m) => { mode.value = m; errorMessage.value = ''; successMessage.value = ''; }
</script>

<template>
  <div v-if="mode === 'dashboard'" class="app-layout">
    <!-- Le Sidebar n'affiche que le nécessaire si patient -->
    <Sidebar :activeView="pageActive" @change-view="newView => pageActive = newView" />
    
    <main class="content-area">
      <!-- Restreindre l'accès si patient -->
      <template v-if="userRole === 'patient'">
        <Dashboard v-if="pageActive === 'home'" :currentView="pageActive" />
        <Email v-else-if="pageActive === 'email'" /> <!-- Pour envoyer le mail au docteur -->
        <p v-else>Accès restreint. Veuillez contacter un docteur par email.</p>
      </template>

      <!-- Accès total pour l'admin -->
      <template v-else>
        <Medicament v-if="pageActive === 'medicament'" v-model:list="medicaments" />
        <Ordonnance v-else-if="pageActive === 'ordonnance'" />
        <Finance v-else-if="pageActive === 'finance'" />
        <Services v-else-if="pageActive === 'services'" />
        <Programme v-else-if="pageActive === 'programme'" />
        <Email v-else-if="pageActive === 'email'" />
        <Pharmacie v-else-if="pageActive === 'pharmacie'" />
        <Rapport v-else-if="pageActive === 'rapport'" />
        <Laboratoire v-else-if="pageActive === 'laboratoire'" />
        <Appointments v-else-if="pageActive === 'appointments'" />
        <History v-else-if="pageActive === 'history'" />
        <Visit v-else-if="pageActive === 'visit'" />
        <Dashboard v-else :currentView="pageActive" :medicamentsCount="medicaments.length" />
      </template>
    </main>
  </div>

  <div v-else class="sghl-container">
    <div class="sghl-card">
      <h2 class="sghl-title">SGHL Portal</h2>
      <form @submit.prevent="mode === 'login' ? handleLogin() : handleRegister()" class="sghl-form">
        <input v-model="username" placeholder="Identifiant" required class="sghl-input" />
        <input v-model="password" type="password" placeholder="Mot de passe" required class="sghl-input" />
        <template v-if="mode === 'register'">
          <input v-model="firstName" placeholder="Prénom" required class="sghl-input" />
          <input v-model="lastName" placeholder="Nom" required class="sghl-input" />
          <input v-model="email" type="email" placeholder="Email" required class="sghl-input" />
        </template>
        <button :disabled="isLoading" type="submit" class="sghl-btn">
          {{ isLoading ? '...' : (mode === 'login' ? 'Se connecter' : 'S\'inscrire') }}
        </button>
      </form>
      <button @click="switchMode(mode === 'login' ? 'register' : 'login')" class="sghl-link">
        {{ mode === 'login' ? 'Créer un compte' : 'Déjà inscrit ? Connectez-vous' }}
      </button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<style>
body, html { margin: 0; padding: 0; width: 100%; height: 100%; }
</style>

<style scoped>
.app-layout { display: flex; min-height: 100vh; }
.content-area { flex: 1; padding: 20px; background: #f8fafc; }
.sghl-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; display: flex; align-items: center; justify-content: center; background: #f1f5f9; }
.sghl-card { width: 400px; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.sghl-form { display: flex; flex-direction: column; gap: 12px; }
.sghl-input { padding: 12px; border: 1px solid #cbd5e1; border-radius: 6px; width: 100%; }
.sghl-btn { background: #3b82f6; color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; }
.sghl-link { background: none; border: none; color: #3b82f6; text-decoration: underline; margin-top: 15px; cursor: pointer; width: 100%; }
.error { color: #dc2626; font-size: 13px; text-align: center; margin-top: 10px; }
.sghl-title { text-align: center; margin-bottom: 20px; }
</style>