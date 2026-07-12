from ninja import NinjaAPI, Schema
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from datetime import date
from typing import List, Optional
from uuid import UUID
from django.shortcuts import get_object_or_404
# Importez votre modèle Lit ici
from clinical.models import Patient, Doctor, RendezVous, Lit 

api = NinjaAPI(title="API SGHL")

# --- SCHÉMAS ---
class LoginSchema(Schema):
    username: str
    password: str

# --- SCHÉMAS LITS (AJOUTÉS) ---
# Modifiez le schema pour inclure chambre_id
class LitSchema(Schema):
    id: Optional[int] = None
    numero: str
    service: str
    chambre_id: int  # Ajout obligatoire

@api.post("/lits/", response=LitSchema)
def create_lit(request, data: LitSchema):
    # On utilise chambre_id directement car c'est une Foreign Key
    lit = Lit.objects.create(
        numero=data.numero, 
        service=data.service, 
        chambre_id=data.chambre_id
    )
    return lit

# --- SCHÉMAS PATIENTS ---
class PatientSchema(Schema):
    id: UUID
    code_sghl: Optional[str] = None
    nom: str
    prenom: str
    date_naissance: Optional[date] = None
    sexe: str
    telephone: str
    email: Optional[str] = None
    adresse: Optional[str] = None
    groupe_sanguin: Optional[str] = None
    service_assigne: Optional[str] = None # Ajouté pour supporter votre frontend

class PatientCreateSchema(Schema):
    nom: str
    prenom: str
    date_naissance: Optional[date] = None
    sexe: str = 'M'
    telephone: str
    email: Optional[str] = None
    adresse: Optional[str] = None
    groupe_sanguin: Optional[str] = None
    service_assigne: Optional[str] = None

# --- SCHÉMAS DOCTEURS ---
class DoctorSchema(Schema):
    id: int
    nom: str
    prenom: str
    specialite: str
    telephone: str
    email: str
    sexe: str
    salaire: Optional[float] = None
    horaire: Optional[str] = None
    jours_travail: Optional[str] = None
    date_naissance: Optional[date] = None

class DoctorCreateSchema(Schema):
    nom: str
    prenom: str
    specialite: str
    telephone: str
    email: str
    sexe: str
    salaire: Optional[float] = None
    horaire: Optional[str] = None
    jours_travail: Optional[str] = None
    date_naissance: Optional[date] = None

# --- AUTHENTIFICATION ---
@api.post("/auth/")
def login_user(request, data: LoginSchema):
    user = authenticate(request, username=data.username, password=data.password)
    if user is None:
        User = get_user_model()
        try:
            user_obj = User.objects.get(email=data.username)
            user = authenticate(request, username=user_obj.username, password=data.password)
        except User.DoesNotExist:
            pass
    if user is not None:
        login(request, user)
        return {"success": True, "message": "Connexion réussie"}
    return JsonResponse({"detail": "Identifiants incorrects."}, status=401)

# --- STATISTIQUES ---
@api.get("/stats/")
def get_stats(request):
    return {
        "doctors_count": Doctor.objects.count(),
        "patients_count": Patient.objects.count(),
        "rendezvous_count": RendezVous.objects.count(),
    }

# --- ROUTES LITS (NOUVELLES) ---
@api.get("/lits/", response=List[LitSchema])
def list_lits(request):
    return list(Lit.objects.all())

@api.post("/lits/")
def create_lit(request, data: LitSchema):
    # Vérification de l'existence de la chambre
    try:
        chambre = Chambre.objects.get(id=data.chambre_id)
    except Chambre.DoesNotExist:
        # Retourne une erreur explicite au lieu d'un crash 500
        return {"error": "Cette chambre n'existe pas"}, 404
        
    lit = Lit.objects.create(
        numero=data.numero, 
        service=data.service, 
        chambre=chambre
    )
    return lit

@api.delete("/lits/{lit_id}/")
def delete_lit(request, lit_id: int):
    lit = get_object_or_404(Lit, id=lit_id)
    lit.delete()
    return {"success": True}

# --- ROUTES PATIENTS ---
@api.get("/patients/", response=List[PatientSchema])
def list_patients(request):
    return Patient.objects.all()

@api.post("/patients/", response={200: PatientSchema, 409: dict, 422: dict})
def create_patient(request, data: PatientCreateSchema):
    if Patient.objects.filter(nom=data.nom, prenom=data.prenom).exists():
        return 409, {"detail": "Un patient avec ce nom et prénom existe déjà."}
    try:
        patient = Patient.objects.create(**data.dict())
        return 200, patient
    except Exception as e:
        return 422, {"detail": str(e)}

@api.put("/patients/{patient_id}/", response=PatientSchema)
def update_patient(request, patient_id: UUID, data: PatientCreateSchema):
    patient = get_object_or_404(Patient, id=patient_id)
    update_data = data.dict(exclude_unset=True)
    for attr, value in update_data.items():
        setattr(patient, attr, value)
    patient.save()
    return patient

@api.delete("/patients/{patient_id}/")
def delete_patient(request, patient_id: UUID):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return {"success": True}

# --- ROUTES DOCTEURS ---
@api.get("/doctors/", response=List[DoctorSchema])
def list_doctors(request):
    return Doctor.objects.all()

@api.post("/doctors/", response={200: DoctorSchema, 409: dict, 422: dict})
def create_doctor(request, data: DoctorCreateSchema):
    if Doctor.objects.filter(nom=data.nom, prenom=data.prenom).exists():
        return 409, {"detail": "Un docteur avec ce nom et prénom existe déjà."}
    try:
        doctor = Doctor.objects.create(**data.dict())
        return 200, doctor
    except Exception as e:
        return 422, {"detail": str(e)}

@api.put("/doctors/{doctor_id}/", response=DoctorSchema)
def update_doctor(request, doctor_id: int, data: DoctorCreateSchema):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    update_data = data.dict(exclude_unset=True)
    for attr, value in update_data.items():
        setattr(doctor, attr, value)
    doctor.save()
    return doctor

@api.delete("/doctors/{doctor_id}/")
def delete_doctor(request, doctor_id: int):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    return {"success": True}