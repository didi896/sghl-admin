import { ref } from 'vue'

// Cet objet sera partagé entre tous tes composants
export const globalStats = ref({
  doctorCount: 0,
  patientCount: 0
})