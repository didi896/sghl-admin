<script setup>
import { ref, onMounted } from 'vue';

const destinataires = ref([]); // Liste fusionnée (docteurs + patients)
const loading = ref(true);
const emailForm = ref({
  to: '',
  subject: '',
  body: ''
});

// Récupération des données réelles
const chargerContacts = async () => {
  try {
    const [resDoc, resPat] = await Promise.all([
      fetch('http://127.0.0.1:8000/api/doctors/'),
      fetch('http://127.0.0.1:8000/api/patients/')
    ]);
    
    const docs = await resDoc.json();
    const pats = await resPat.json();

    // On combine les deux listes avec un type pour la lisibilité
    destinataires.value = [
      ...docs.map(d => ({ email: d.email, nom: d.nom, type: 'Docteur' })),
      ...pats.map(p => ({ email: p.email, nom: p.nom, type: 'Patient' }))
    ].filter(contact => contact.email); // On ne garde que ceux qui ont un email
  } catch (e) {
    console.error("Erreur chargement contacts:", e);
  } finally {
    loading.value = false;
  }
};

const envoyerEmail = async () => {
  if (!emailForm.value.to) return alert("Veuillez choisir un destinataire.");
  
  try {
    // Dans Email.vue (méthode envoyerEmail)
const response = await fetch('http://127.0.0.1:8000/clinical/send-email/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(emailForm.value)
});
    
    if (response.ok) {
      alert("Email envoyé avec succès !");
      emailForm.value = { to: '', subject: '', body: '' };
    }
  } catch (e) {
    alert("Erreur lors de l'envoi.");
  }
};

onMounted(chargerContacts);
</script>

<template>
  <div class="email-wrapper">
    <h3>Messagerie SGHL Admin</h3>
    
    <div class="email-grid">
      <div class="compose-box">
        <label>Destinataire :</label>
        <select v-model="emailForm.to" class="field">
          <option value="" disabled>Sélectionner un contact...</option>
          <option v-for="c in destinataires" :key="c.email" :value="c.email">
            {{ c.nom }} ({{ c.type }})
          </option>
        </select>

        <label>Sujet :</label>
        <input v-model="emailForm.subject" class="field" placeholder="Ex: Rappel de rendez-vous" />

        <label>Message :</label>
        <textarea v-model="emailForm.body" class="field textarea" rows="8"></textarea>
        
        <button @click="envoyerEmail" class="send-btn">Envoyer l'email</button>
      </div>

      <div class="info-box">
        <h4>Contacts disponibles</h4>
        <p v-if="loading">Chargement...</p>
        <ul v-else class="contact-list">
          <li v-for="c in destinataires" :key="c.email">
            <strong>{{ c.nom }}</strong> <br>
            <small>{{ c.email }} - {{ c.type }}</small>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.email-wrapper { padding: 20px; background: white; border-radius: 8px; }
.email-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; }
.field { width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #cbd5e1; border-radius: 4px; box-sizing: border-box; }
.textarea { resize: none; }
.send-btn { background: #3b82f6; color: white; padding: 12px; border: none; border-radius: 4px; cursor: pointer; width: 100%; }
.contact-list { list-style: none; padding: 0; }
.contact-list li { padding: 10px; border-bottom: 1px solid #f1f5f9; }
</style>