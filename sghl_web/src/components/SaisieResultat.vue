<template>
  <div class="labo-card">
    <h3>Saisie des résultats de laboratoire</h3>
    
    <div class="form-group">
      <label>Examen : {{ examen.test_nom }}</label>
      <input type="number" v-model="valeur" placeholder="Valeur numérique" class="input-field">
      <textarea v-model="commentaire" placeholder="Commentaires..." class="input-field"></textarea>
      
      <button @click="validerResultat" class="btn-save">Valider le résultat</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps(['examen'])
const valeur = ref(null)
const commentaire = ref('')

const validerResultat = async () => {
  const payload = {
    resultat_valeur: valeur.value,
    commentaire: commentaire.value,
    statut: 'TERMINE'
  }

  await fetch(`http://127.0.0.1:8000/api/examens-labo/${props.examen.id}/`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  alert('Résultat enregistré avec succès !')
}
</script>

<style scoped>
.labo-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.input-field { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; }
.btn-save { background: #3b82f6; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; }
</style>