from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import datetime

# ==========================================
# 1. MODULE AUTHENTIFICATION
# ==========================================
class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('BIOLOGISTE', 'Biologiste / Technicien Labo'),
        ('ADMINISTRATIF', 'Personnel Administratif'),
        ('PATIENT', 'Patient'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PATIENT')
    telephone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# ==========================================
# 2. MODULE CLINIQUE & LABORATOIRE
# ==========================================
class Patient(models.Model):
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ipp = models.CharField(max_length=20, unique=True, blank=True)  
    code_sghl = models.CharField(max_length=20, unique=True, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, default='M')
    telephone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    groupe_sanguin = models.CharField(max_length=5, blank=True, null=True)
    service_assigne = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code_sghl:
            annee = datetime.datetime.now().year
            self.code_sghl = f"PAT-{annee}-{uuid.uuid4().hex[:6].upper()}"
        if not self.ipp:
            self.ipp = f"IPP-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom.upper()} {self.prenom} ({self.code_sghl})"

class Doctor(models.Model):
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, default='M')
    date_naissance = models.DateField(null=True, blank=True)
    salaire = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    horaire = models.CharField(max_length=100, null=True, blank=True)
    jours_travail = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.specialite})"

# models.py
class Historique(models.Model):
    action = models.CharField(max_length=255) # Ex: "Vente de Paracétamol", "Rendez-vous Dr. X"
    categorie = models.CharField(max_length=50) # Ex: "Vente", "Achat", "RDV"
    date_creation = models.DateTimeField(auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['-date_creation']

# ==========================================
# 3. MODULE RENDEZ-VOUS
# ==========================================
class RendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="rendezvous")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="rendezvous")
    date_heure = models.DateTimeField()
    motif = models.TextField()
    est_valide = models.BooleanField(default=True)

# ==========================================
# 4. MODULE GESTION DES LITS
# ==========================================
class Batiment(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    adresse = models.TextField(blank=True, null=True)

class Service(models.Model):
    nom = models.CharField(max_length=100)
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name="services")

class Chambre(models.Model):
    numero = models.CharField(max_length=10)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="chambres")

class Lit(models.Model):
    numero = models.CharField(max_length=10, default="001")
    service = models.CharField(max_length=100, default="Non défini")
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name="lits", null=True, blank=True)
    est_occupe = models.BooleanField(default=False)

class Hospitalisation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="hospitalisations")
    medecin_referent = models.ForeignKey(User, on_delete=models.PROTECT, related_name="patients_references")
    lit = models.OneToOneField(Lit, on_delete=models.PROTECT, related_name="hospitalisation_active")
    date_entree = models.DateTimeField(auto_now_add=True)
    date_sortie_prevue = models.DateTimeField()
    est_active = models.BooleanField(default=True)

# ==========================================
# 5. MODULE RAPPORTS (Nouveaux modèles)
# ==========================================
class Medicament(models.Model):
    nom = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom

class Ordonnance(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"Ordonnance du {self.date_creation}"

class TypeTest(models.Model):
    """Ex: Hémogramme, Glycémie, Groupe Sanguin..."""
    nom = models.CharField(max_length=100)
    unite_mesure = models.CharField(max_length=20, blank=True)
    valeur_reference_min = models.FloatField(null=True, blank=True)
    valeur_reference_max = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nom

class ExamenLabo(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
        ('VALIDE', 'Validé par le biologiste'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test = models.ForeignKey(TypeTest, on_delete=models.CASCADE)
    medecin_prescripteur = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    date_prescription = models.DateTimeField(auto_now_add=True)
    date_resultat = models.DateTimeField(null=True, blank=True)
    resultat_valeur = models.FloatField(null=True, blank=True)
    commentaire = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')

    def __str__(self):
        return f"{self.test.nom} - {self.patient.nom}"