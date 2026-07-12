<template>
  <div class="pharmacie-dashboard">
    <div class="header">
      <h2><i class="fas fa-mortar-pestle"></i> Pharmacie Hospitalière</h2>
      <!-- Bouton avec l'événement @click lié -->
      <button class="btn-add" @click="ajouterMedicament">
        <i class="fas fa-plus"></i> Ajouter Médicament
      </button>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Médicament</th>
            <th>Stock</th>
            <th>Prix Unitaire</th>
            <th>État</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="med in medicaments" :key="med.id">
            <td class="med-name">{{ med.nom }}</td>
            <td>{{ med.stock }} unités</td>
            <td>{{ med.prix }} FCFA</td>
            <td>
              <span :class="['badge', med.stock < 10 ? 'critique' : 'ok']">
                {{ med.stock < 10 ? 'Stock Critique' : 'En stock' }}
              </span>
            </td>
            <td>
              <button 
                class="btn-delivrer" 
                :disabled="med.stock <= 0"
                @click="delivrer(med.id)"
              >
                Délivrer
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const medicaments = ref([
  { id: 1, nom: 'Paracétamol', stock: 100, prix: 500 },
  { id: 2, nom: 'Amoxicilline', stock: 5, prix: 1200 },
  { id: 3, nom: 'Ibuprofène', stock: 25, prix: 800 }
]);

// Fonction pour ajouter un nouveau médicament
const ajouterMedicament = () => {
  const nom = prompt("Nom du médicament :");
  const stock = prompt("Quantité en stock :");
  const prix = prompt("Prix unitaire :");
  
  if (nom && stock && prix) {
    medicaments.value.push({
      id: Date.now(),
      nom: nom,
      stock: parseInt(stock),
      prix: parseInt(prix)
    });
  }
};

// Fonction pour délivrer un médicament
const delivrer = (id) => {
  const med = medicaments.value.find(m => m.id === id);
  if (med && med.stock > 0) {
    med.stock -= 1;
    alert(`${med.nom} délivré avec succès !`);
  }
};
</script>

<style scoped>
.pharmacie-dashboard { padding: 20px; background: #ffffff; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.header h2 { color: #1e293b; display: flex; align-items: center; gap: 10px; }

.table-container { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; margin-top: 10px; }
th { text-align: left; background: #f8fafc; padding: 15px; color: #64748b; font-size: 0.9rem; }
td { padding: 15px; border-bottom: 1px solid #f1f5f9; }

.med-name { font-weight: bold; color: #334155; }
.badge { padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; }
.critique { background: #fee2e2; color: #dc2626; }
.ok { background: #dcfce7; color: #166534; }

.btn-add { background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; transition: 0.3s; }
.btn-add:hover { background: #2563eb; }
.btn-delivrer { background: #64748b; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; }
.btn-delivrer:disabled { background: #e2e8f0; cursor: not-allowed; }
.btn-delivrer:hover:not(:disabled) { background: #475569; }
</style>