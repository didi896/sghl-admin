from rest_framework import serializers
from .models import (
    Patient, Doctor, TypeTest, ExamenLabo, 
    RendezVous, Ordonnance, Historique
)

class RendezVousSerializer(serializers.ModelSerializer):
    patient_nom = serializers.ReadOnlyField(source='patient.get_full_name')
    docteur_nom = serializers.ReadOnlyField(source='docteur.nom')

    class Meta:
        model = RendezVous
        fields = ['id', 'patient', 'docteur', 'date_heure', 'statut', 'patient_nom', 'docteur_nom']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class TypeTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeTest
        fields = '__all__'

class ExamenLaboSerializer(serializers.ModelSerializer):
    patient_nom = serializers.CharField(source='patient.nom', read_only=True)
    test_nom = serializers.CharField(source='test.nom', read_only=True)

    class Meta:
        model = ExamenLabo
        fields = '__all__'

class OrdonnanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordonnance
        fields = '__all__'

class HistoriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historique
        fields = '__all__'