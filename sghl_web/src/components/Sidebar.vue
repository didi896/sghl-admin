<script setup>
// Déclaration des événements pour communiquer avec le parent (App.vue)
const emit = defineEmits(['change-view'])

// Déclaration des propriétés reçues
defineProps({ 
  activeView: {
    type: String,
    default: 'home'
  }
})
</script>

<template>
  <aside class="sidebar">
    <div class="brand">
      <i class="fas fa-hospital-user"></i> SGHL Admin
    </div>
    
    <nav>
      <!-- Menu Principal -->
      <div class="menu-item" :class="{ active: activeView === 'home' }" @click="emit('change-view', 'home')">
        <i class="fas fa-home"></i> Accueil
      </div>

      <div class="menu-section">
        <div class="menu-item" :class="{ active: activeView === 'doctors' }" @click="emit('change-view', 'doctors')">
          <i class="fas fa-user-md"></i> Gestion des Docteurs
        </div>

        <div class="sub-menu">
          <div class="menu-item" :class="{ active: activeView === 'history' }" @click="emit('change-view', 'history')">
            <i class="fas fa-history"></i> Historique
          </div>
          <!-- Option Visite médicale bien intégrée -->
          <div class="menu-item" :class="{ active: activeView === 'visit' }" @click="emit('change-view', 'visit')">
            <i class="fas fa-stethoscope"></i> Visite médicale
          </div>
        </div>
      </div>

      <div class="menu-item" :class="{ active: activeView === 'patients' }" @click="emit('change-view', 'patients')">
        <i class="fas fa-users"></i> Patients
      </div>

      <div class="menu-item" :class="{ active: activeView === 'services' }" @click="emit('change-view', 'services')">
        <i class="fas fa-briefcase-medical"></i> Services
      </div>

      <div class="menu-item" :class="{ active: activeView === 'programme' }" @click="emit('change-view', 'programme')">
        <i class="fas fa-calendar-check"></i> Programme
      </div>

      <div class="menu-item" :class="{ active: activeView === 'appointments' }" @click="emit('change-view', 'appointments')">
        <i class="fas fa-calendar-alt"></i> Rendez-vous
      </div>

      <div class="menu-item" :class="{ active: activeView === 'finance' }" @click="emit('change-view', 'finance')">
        <i class="fas fa-file-invoice-dollar"></i> Activités financières
      </div>

      <div class="menu-item" :class="{ active: activeView === 'ordonnance' }" @click="emit('change-view', 'ordonnance')">
        <i class="fas fa-prescription-bottle-alt"></i> Ordonnance
      </div>

      <div class="menu-item" :class="{ active: activeView === 'laboratoire' }" @click="emit('change-view', 'laboratoire')">
        <i class="fas fa-flask"></i> Tests de laboratoire
      </div>

      <div class="menu-item" :class="{ active: activeView === 'medicament' }" @click="emit('change-view', 'medicament')">
        <i class="fas fa-pills"></i> Médicament
      </div>

      <div class="menu-item" :class="{ active: activeView === 'pharmacie' }" @click="emit('change-view', 'pharmacie')">
        <i class="fas fa-mortar-pestle"></i> Pharmacie
      </div>

      <div class="menu-item" :class="{ active: activeView === 'rapport' }" @click="emit('change-view', 'rapport')">
        <i class="fas fa-file-alt"></i> Rapport
      </div>

      <div class="menu-item" :class="{ active: activeView === 'email' }" @click="emit('change-view', 'email')">
        <i class="fas fa-envelope"></i> Email
      </div>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar { 
  width: 260px; 
  background: #1e293b; 
  color: white; 
  min-height: 100vh; 
  display: flex; 
  flex-direction: column;
}

.brand { 
  padding: 25px; 
  font-size: 1.3rem; 
  font-weight: bold; 
  border-bottom: 1px solid #334155; 
  color: #3b82f6; 
  display: flex; 
  align-items: center; 
  gap: 10px; 
}

.menu-item { 
  padding: 15px 25px; 
  cursor: pointer; 
  color: #94a3b8; 
  transition: all 0.3s ease; 
  display: flex; 
  align-items: center; 
  gap: 12px; 
}

.menu-item i { 
  width: 20px; 
  text-align: center; 
}

.menu-item:hover, .menu-item.active { 
  background: #334155; 
  color: #ffffff; 
  border-left: 4px solid #3b82f6; 
}

.sub-menu { 
  background: #0f172a; 
}

.sub-menu .menu-item { 
  padding: 10px 25px 10px 45px; 
  font-size: 0.9rem; 
}
</style>