from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Patient, Batiment, Service, Chambre, Lit, Hospitalisation

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'role', 'email', 'is_staff')
    list_filter = ('role', 'is_staff')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('code_sghl', 'nom', 'prenom', 'telephone', 'date_naissance')
    search_fields = ('nom', 'prenom', 'code_sghl')

@admin.register(Batiment)
class BatimentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'batiment')

@admin.register(Chambre)
class ChambreAdmin(admin.ModelAdmin):
    list_display = ('numero', 'service') 

@admin.register(Lit)
class LitAdmin(admin.ModelAdmin):
    # Mis à jour : 'code' est devenu 'numero'
    list_display = ('numero', 'service', 'chambre', 'est_occupe') 
    list_filter = ('est_occupe', 'service')

@admin.register(Hospitalisation)
class HospitalisationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'lit', 'date_entree', 'est_active')