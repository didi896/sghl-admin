<script setup>
import { ref, computed, onMounted } from 'vue';

// État global
const searchQuery = ref('');
const showModal = ref(false);
const selectedService = ref('');
const currentTab = ref('patients');
const allPatients = ref([]);
const allLits = ref([]);
const targetService = ref('');
const litToAssign = ref(null);
const selectedPatientForLit = ref('');

// État Chefs
const chefCHU = ref(null);
const chefAmbulance = ref(null);
const chefCuisine = ref(null);
const chefGardien = ref(null);
const chefAgentSanitaire = ref(null); 

// État Ambulance
const vehicules = ref([]);
const nomVehicule = ref('');

// État Gardiennage
const historiqueAcces = ref([]);
const nouveauVisiteur = ref({ nom: '' });

// État Agent Sanitaire
const medicamentsDisponibles = [
  { id: 1, nom: 'Anti-rétroviraux (VIH)', type: 'VIH' },
  { id: 2, nom: 'Anti-tuberculeux', type: 'Tuberculose' }
];

const ajouterVisiteur = () => {
  if (nouveauVisiteur.value.nom.trim() !== '') {
    const now = new Date();
    historiqueAcces.value.push({
      id: Date.now(),
      nom: nouveauVisiteur.value.nom,
      type: 'Entrée',
      heure: now.toLocaleTimeString()
    });
    nouveauVisiteur.value.nom = '';
  }
};

const enregistrerSortie = (log) => {
  const now = new Date();
  log.type = 'Sortie';
  log.heure = now.toLocaleTimeString();
};

const nettoyerHistorique = () => {
  if (confirm("Voulez-vous vraiment effacer tout l'historique des visites ?")) {
    historiqueAcces.value = [];
  }
};

const alerteActive = ref(false);

// État Cuisine & Facturation
const panier = ref([]);
const prixTotal = computed(() => panier.value.reduce((sum, item) => sum + (item.prix * item.quantite), 0));

const plats = ref([
  { id: 1, nom: 'Riz au saka', prix: 2500, disponible: true },
  { id: 2, nom: 'Riz à l\'haricot', prix: 2000, disponible: true },
  { id: 3, nom: 'Poulet rôti', prix: 5000, disponible: true },
  { id: 4, nom: 'Poisson frit', prix: 4500, disponible: true },
  { id: 5, nom: 'Manioc', prix: 1500, disponible: true }
]);

const ajouterAuPanier = (plat, patientId) => {
  const patient = allPatients.value.find(p => p.id === patientId);
  if (!patient) return alert("Veuillez sélectionner un patient");
  panier.value.push({ ...plat, patientNom: patient.nom, quantite: 1 });
  alert("Commander avec succès !");
};

// Fonctions Chefs
const setChefGardien = () => { const nom = prompt("Entrez le nom du chef des gardiens :"); if (nom) chefGardien.value = nom; };
const setChefCHU = () => { const nom = prompt("Entrez le nom du chef du CHU :"); if (nom) chefCHU.value = nom; };
const setChefAmbulance = () => { const nom = prompt("Entrez le nom du chef d'ambulance :"); if (nom) chefAmbulance.value = nom; };
const setChefCuisine = () => { const nom = prompt("Entrez le nom du chef de cuisine :"); if (nom) chefCuisine.value = nom; };
const setChefAgentSanitaire = () => { const nom = prompt("Nom du chef des agents sanitaires :"); if (nom) chefAgentSanitaire.value = nom; };

// Fonctions Agent Sanitaire
const distribuerTraitement = (patient, med) => {
  alert(`Traitement ${med.nom} administré avec succès au patient ${patient.nom} (Rapport médical mis à jour).`);
};

const declencherUrgence = () => {
  if (confirm("ATTENTION : Déclencher l'alerte d'urgence pour intrusion/agression ?")) {
    alerteActive.value = true;
    alert("ALERTE : Les services de sécurité ont été informés !");
  }
};

const ajouterVehicule = () => {
  if (nomVehicule.value.trim() !== '') {
    vehicules.value.push({
      id: Date.now(),
      nom: nomVehicule.value,
      equipements: { defib: false, oxygene: false, brancard: false, trauma: false }
    });
    nomVehicule.value = '';
  }
};

const listeServices = [
  'Réanimation', 'Morgue', 'CHU', 'Hospitalisation', 'Consultation',
  'Maternité', 'Pédiatrie', 'Ophtalmologie', 'Cardiologie', 'Neurologie',
  'Gynécologie', 'Infirmerie', 'Ambulance', 'Cuisine', 'Gardiennage', 'Agent sanitaire'
];

const allowedServices = ['Réanimation', 'Pédiatrie', 'Maternité', 'Cardiologie', 'Gynécologie', 'Ophtalmologie', 'Infirmerie', 'Neurologie', 'Hospitalisation', 'CHU', 'Ambulance', 'Cuisine', 'Gardiennage', 'Agent sanitaire'];
const hospitalisationOptions = ['Cardiologie', 'Neurologie', 'Gynécologie', 'Ophtalmologie', 'Maternité', 'Pédiatrie', 'Infirmerie'];

onMounted(async () => {
  await refreshPatients();
  await refreshLits();
});

const refreshPatients = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/patients/');
    const data = await res.json();
    allPatients.value = data.map(p => ({ 
      ...p, 
      service_assigne: p.service_assigne ? p.service_assigne.toString() : null,
      lit_assigne: p.lit_assigne 
    }));
  } catch (error) { console.error("Erreur patients:", error); }
};

const refreshLits = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/lits/');
    allLits.value = await res.json();
  } catch (error) { console.error("Erreur lits:", error); }
};

const filteredServices = computed(() => listeServices.filter(s => s.toLowerCase().includes(searchQuery.value.toLowerCase())));
const normalize = (str) => (str ? str.toString().normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim() : "");
const availablePatients = computed(() => allPatients.value.filter(p => !p.service_assigne));

const assignedPatients = computed(() => {
  if (!selectedService.value) return [];
  const targetPrincipal = normalize(selectedService.value);
  return allPatients.value.filter(p => {
    const pService = normalize(p.service_assigne);
    if (selectedService.value === 'CHU') return pService === 'chu';
    if (selectedService.value === 'Hospitalisation') {
      if (targetService.value) return pService === normalize(targetService.value);
      return hospitalisationOptions.map(opt => normalize(opt)).includes(pService) || pService === 'hospitalisation';
    }
    return pService === targetPrincipal;
  });
});

const litsInService = computed(() => {
  const s = (selectedService.value === 'Hospitalisation') ? targetService.value : selectedService.value;
  return allLits.value.filter(l => l.service === s);
});

const openDetails = (service) => {
  selectedService.value = service;
  targetService.value = '';
  if (service === 'Ambulance') currentTab.value = 'vehicules';
  else if (service === 'Cuisine') currentTab.value = 'menu';
  else if (service === 'Gardiennage') currentTab.value = 'acces';
  else if (service === 'Agent sanitaire') currentTab.value = 'traitement';
  else currentTab.value = 'patients';
  showModal.value = true;
};

const addPatientToService = async (patient) => {
  const serviceFinal = selectedService.value === 'Hospitalisation' ? targetService.value : selectedService.value;
  await fetch(`http://localhost:8000/api/patients/${patient.id}/`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...patient, service_assigne: serviceFinal })
  });
  await refreshPatients();
};

const removePatient = async (patient) => {
  await fetch(`http://localhost:8000/api/patients/${patient.id}/`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...patient, service_assigne: null, lit_assigne: null })
  });
  await refreshPatients();
};

const transferToReanimation = async (patient) => {
  if (!confirm("Transférer vers la Réanimation ?")) return;
  await fetch(`http://localhost:8000/api/patients/${patient.id}/`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...patient, service_assigne: 'Réanimation' })
  });
  await refreshPatients();
};

const assignPatientToLit = async (lit) => {
  if (!selectedPatientForLit.value) return;
  const patient = allPatients.value.find(p => p.id === selectedPatientForLit.value);
  await fetch(`http://localhost:8000/api/patients/${patient.id}/`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...patient, lit_assigne: lit.id })
  });
  await refreshPatients();
  litToAssign.value = null;
};

const getPatientDansLit = (litId) => allPatients.value.find(p => String(p.lit_assigne) === String(litId));

const libererLit = async (litId) => {
  const patient = getPatientDansLit(litId);
  if (patient) {
    await fetch(`http://localhost:8000/api/patients/${patient.id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...patient, lit_assigne: null })
    });
    await refreshPatients();
  }
};
</script>

<template>
  <div class="services-container">
    <h3>Gestion des Services Médicaux</h3>
    <input v-model="searchQuery" placeholder="Rechercher un service..." class="search-input" />
    
    <div class="services-grid">
      <div v-for="service in filteredServices" :key="service" class="service-card">
        <i class="icon-med">🏥</i>
        <span>{{ service }}</span>
        <button class="med-btn med-btn--blue" v-if="allowedServices.includes(service)" @click="openDetails(service)">Voir détails</button>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content">
        <h3>{{ selectedService }}</h3>
        
        <div class="tabs">
          <button v-if="!['Ambulance', 'Cuisine', 'Gardiennage', 'Agent sanitaire'].includes(selectedService)" @click="currentTab = 'patients'" :class="{active: currentTab === 'patients'}">Admettre</button>
          <button v-if="!['Ambulance', 'Cuisine', 'Gardiennage', 'Agent sanitaire'].includes(selectedService)" @click="currentTab = 'assigned'" :class="{active: currentTab === 'assigned'}">Liste Patients</button>
          <button v-if="!['Ambulance', 'Cuisine', 'CHU', 'Gardiennage', 'Agent sanitaire'].includes(selectedService)" @click="currentTab = 'lits'" :class="{active: currentTab === 'lits'}">Lits</button>
          <button v-if="selectedService === 'Ambulance'" @click="currentTab = 'vehicules'" :class="{active: currentTab === 'vehicules'}">Véhicules</button>
          <button v-if="selectedService === 'Cuisine'" @click="currentTab = 'menu'" :class="{active: currentTab === 'menu'}">Menu</button>
          <button v-if="selectedService === 'Cuisine'" @click="currentTab = 'facture'" :class="{active: currentTab === 'facture'}">Factures</button>
          <button v-if="selectedService === 'Gardiennage'" @click="currentTab = 'acces'" :class="{active: currentTab === 'acces'}">Accès & Badges</button>
          <button v-if="selectedService === 'Gardiennage'" @click="currentTab = 'alerte'" :class="{active: currentTab === 'alerte'}" style="background: #ef4444; color: white;">Urgence</button>
          <button v-if="selectedService === 'Agent sanitaire'" @click="currentTab = 'traitement'" :class="{active: currentTab === 'traitement'}">Traitements</button>
        </div>

        <div class="modal-body">
          
          <!-- ONGLET : AGENT SANITAIRE -->
          <div v-if="selectedService === 'Agent sanitaire'">
            <div class="chef-section" style="background: #ecfdf5; border-color: #a7f3d0;">
              <span><strong>Chef Agent Sanitaire :</strong> {{ chefAgentSanitaire || 'Non défini' }}</span>
              <button class="med-btn med-btn--blue" @click="setChefAgentSanitaire">{{ chefAgentSanitaire ? 'Modifier' : 'Définir' }}</button>
            </div>

            <h4>Distribution de Traitements (VIH/Tuberculose)</h4>
            <div v-for="pat in allPatients" :key="pat.id" class="patient-item">
              <div>
                <strong>{{ pat.nom }} {{ pat.prenom }}</strong>
                <div style="display: flex; gap: 5px; margin-top: 5px;">
                  <button v-for="med in medicamentsDisponibles" :key="med.id" 
                          class="med-btn med-btn--green" style="font-size: 0.7em;" 
                          @click="distribuerTraitement(pat, med)">
                    {{ med.type }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- ONGLET : GARDIENNAGE -->
          <div v-if="selectedService === 'Gardiennage'">
            <div class="chef-section" style="background: #fee2e2; border-color: #fecaca;">
              <span><strong>Chef des gardiens :</strong> {{ chefGardien || 'Non défini' }}</span>
              <button class="med-btn med-btn--blue" @click="setChefGardien">{{ chefGardien ? 'Modifier' : 'Définir' }}</button>
            </div>
            
            <div v-if="currentTab === 'acces'">
              <div class="admin-section">
                <input v-model="nouveauVisiteur.nom" placeholder="Nom du visiteur" class="inline-input" />
                <button class="med-btn med-btn--green" @click="ajouterVisiteur">Enregistrer Entrée</button>
              </div>
              <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
                <h4>Historique des Entrées/Sorties</h4>
                <button v-if="historiqueAcces.length > 0" class="med-btn med-btn--red" @click="nettoyerHistorique" style="padding: 4px 8px; font-size: 0.8em;">Tout nettoyer</button>
              </div>
              <div v-for="log in historiqueAcces" :key="log.id" class="patient-item">
                <div>
                  <strong>{{ log.nom }}</strong> - {{ log.type }} 
                  <small style="color: #64748b;">(à {{ log.heure }})</small>
                </div>
                <button v-if="log.type === 'Entrée'" class="med-btn med-btn--red" @click="enregistrerSortie(log)">Sortie</button>
                <span v-else class="med-btn" style="background: #94a3b8; cursor: default; color: white;">Terminé</span>
              </div>
            </div>

            <div v-if="currentTab === 'alerte'" class="total-section" style="text-align: center;">
              <button class="med-btn med-btn--red" style="padding: 20px; font-size: 1.2em; width: 100%;" @click="declencherUrgence">
                🚨 BOUTON D'URGENCE (Intrusion/Agression)
              </button>
            </div>
          </div>

          <!-- ONGLET : CUISINE -->
          <div v-if="selectedService === 'Cuisine' && currentTab === 'menu'">
            <div class="chef-section cuisine-theme">
              <span><strong>Chef de cuisine :</strong> {{ chefCuisine || 'Non défini' }}</span>
              <button class="med-btn med-btn--blue" @click="setChefCuisine">{{ chefCuisine ? 'Modifier' : 'Définir' }}</button>
            </div>
            <div v-for="plat in plats" :key="plat.id" class="patient-item">
              <span>{{ plat.nom }} ({{ plat.prix }} FCFA)</span>
              <select v-model="selectedPatientForLit" class="inline-select">
                <option value="" disabled>Choisir patient...</option>
                <option v-for="pat in allPatients" :key="pat.id" :value="pat.id">{{ pat.nom }}</option>
              </select>
              <button class="med-btn med-btn--green" @click="ajouterAuPanier(plat, selectedPatientForLit)">Commander</button>
            </div>
          </div>

          <div v-if="selectedService === 'Cuisine' && currentTab === 'facture'">
            <div v-for="(item, index) in panier" :key="index" class="patient-item">
              <span>{{ item.patientNom }} : {{ item.nom }}</span>
              <span>{{ item.prix }} FCFA</span>
            </div>
            <div class="total-section">
              <h3>Total : {{ prixTotal }} FCFA</h3>
              <button class="med-btn med-btn--green" @click="panier = []">Valider le paiement</button>
            </div>
          </div>

          <!-- Reste des services -->
          <div v-if="currentTab === 'patients' && !['Ambulance', 'Cuisine', 'Gardiennage', 'Agent sanitaire'].includes(selectedService)">
            <div v-for="pat in availablePatients" :key="pat.id" class="patient-item">
              <span>{{ pat.nom }} {{ pat.prenom }}</span>
              <button class="med-btn med-btn--green" @click="addPatientToService(pat)">Admettre</button>
            </div>
          </div>

          <div v-if="currentTab === 'assigned' && !['Ambulance', 'Cuisine', 'Gardiennage', 'Agent sanitaire'].includes(selectedService)">
            <div v-if="selectedService === 'CHU'">
              <div class="chef-section">
                <span><strong>Chef du CHU :</strong> {{ chefCHU || 'Non défini' }}</span>
                <button class="med-btn med-btn--blue" @click="setChefCHU">{{ chefCHU ? 'Modifier' : 'Définir' }}</button>
              </div>
              <div v-for="pat in assignedPatients" :key="pat.id" class="patient-item">
                <span>{{ pat.nom }} {{ pat.prenom }}</span>
                <button class="med-btn med-btn--blue" @click="transferToReanimation(pat)">Vers Réa</button>
              </div>
            </div>
            <div v-else v-for="pat in assignedPatients" :key="pat.id" class="patient-item">
              <span>{{ pat.nom }} {{ pat.prenom }}</span>
              <button class="med-btn med-btn--red" @click="removePatient(pat)">Retirer</button>
            </div>
          </div>

          <div v-if="currentTab === 'lits' && !['Ambulance', 'Cuisine', 'Gardiennage', 'Agent sanitaire'].includes(selectedService)">
             <div class="patient-list">
              <div v-for="lit in litsInService" :key="lit.id" class="patient-item">
                <span>Lit N° {{ lit.numero }}</span>
                <div class="lit-actions">
                  <template v-if="litToAssign === lit.id">
                    <select v-model="selectedPatientForLit" class="inline-select">
                      <option v-for="pat in assignedPatients" :key="pat.id" :value="pat.id">{{ pat.nom }}</option>
                    </select>
                    <button class="med-btn med-btn--green" @click="assignPatientToLit(lit)">Valider</button>
                  </template>
                  <template v-else>
                    <button v-if="getPatientDansLit(lit.id)" class="med-btn med-btn--red" @click="libererLit(lit.id)">Libérer</button>
                    <button v-else class="med-btn med-btn--blue" @click="litToAssign = lit.id">Placer</button>
                  </template>
                </div>
              </div>
             </div>
          </div>

          <div v-if="selectedService === 'Ambulance'">
            <div class="chef-section ambulance-theme">
              <span><strong>Chef d'Ambulance :</strong> {{ chefAmbulance || 'Non défini' }}</span>
              <button class="med-btn med-btn--blue" @click="setChefAmbulance">{{ chefAmbulance ? 'Modifier' : 'Définir' }}</button>
            </div>
            <div class="admin-section">
              <input v-model="nomVehicule" placeholder="Nom ou Immatriculation" class="search-input inline-input" @keyup.enter="ajouterVehicule" />
              <button class="med-btn med-btn--green" @click="ajouterVehicule">Ajouter Véhicule</button>
            </div>
            <div class="vehicules-list">
              <div v-for="v in vehicules" :key="v.id" class="vehicule-card">
                <h4>🚑 {{ v.nom }}</h4>
                <div class="equipement-grid">
                  <label><input type="checkbox" v-model="v.equipements.defib"> Défibrillateur</label>
                  <label><input type="checkbox" v-model="v.equipements.oxygene"> Oxygène</label>
                  <label><input type="checkbox" v-model="v.equipements.brancard"> Brancard</label>
                  <label><input type="checkbox" v-model="v.equipements.trauma"> Kit Traumato</label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button class="btn-close" @click="showModal = false">Fermer</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.services-container { background: white; padding: 20px; border-radius: 8px; }
.search-input { width: 100%; padding: 12px; margin: 20px 0; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; }
.services-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }
.service-card { border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; transition: 0.2s; }
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { background: white; padding: 20px; border-radius: 8px; width: 600px; max-height: 85vh; overflow-y: auto; }
.tabs { display: flex; gap: 5px; margin-bottom: 15px; flex-wrap: wrap; }
.tabs button { padding: 8px 16px; cursor: pointer; border: 1px solid #3b82f6; background: white; border-radius: 4px; font-weight: 500; }
.tabs button.active { background: #3b82f6; color: white; }

/* Styles normalisés pour les boutons - Garantit l'absence de changement de design */
.med-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s ease;
}
.med-btn:hover { opacity: 0.9; }
.med-btn--blue { background: #3b82f6; color: white; }
.med-btn--green { background: #22c55e; color: white; }
.med-btn--red { background: #ef4444; color: white; }

.btn-close { margin-top: 20px; width: 100%; padding: 12px; background: #64748b; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
.patient-item { display: flex; justify-content: space-between; padding: 12px; border-bottom: 1px solid #f1f5f9; align-items: center; }
.chef-section { background: #f0f9ff; padding: 12px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border: 1px solid #bae6fd; }
.ambulance-theme { background: #fdf4ff; border-color: #f5d0fe; }
.cuisine-theme { background: #fff7ed; border-color: #ffedd5; }
.inline-input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
.admin-section { display: flex; gap: 10px; margin-bottom: 15px; padding: 10px; background: #f8fafc; border-radius: 6px; }
</style>