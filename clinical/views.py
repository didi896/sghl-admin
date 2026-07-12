from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json

# Importation des modèles
from .models import (
    TypeTest, ExamenLabo, Patient, Doctor, 
    Ordonnance, Medicament, RendezVous, Historique
)

# Importation des Serializers
from .serializers import (
    TypeTestSerializer, ExamenLaboSerializer, 
    PatientSerializer, DoctorSerializer, 
    OrdonnanceSerializer, RendezVousSerializer,
    HistoriqueSerializer
)

# --- ViewSets ---

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class OrdonnanceViewSet(viewsets.ModelViewSet):
    queryset = Ordonnance.objects.all()
    serializer_class = OrdonnanceSerializer

class HistoriqueViewSet(viewsets.ModelViewSet):
    queryset = Historique.objects.all()
    serializer_class = HistoriqueSerializer

class TypeTestViewSet(viewsets.ModelViewSet):
    queryset = TypeTest.objects.all()
    serializer_class = TypeTestSerializer

class ExamenLaboViewSet(viewsets.ModelViewSet):
    queryset = ExamenLabo.objects.all()
    serializer_class = ExamenLaboSerializer
    
    def get_queryset(self):
        queryset = ExamenLabo.objects.all()
        statut = self.request.query_params.get('statut', None)
        if statut:
            queryset = queryset.filter(statut=statut)
        return queryset

class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all().order_by('-date_heure')
    serializer_class = RendezVousSerializer

    def get_queryset(self):
        queryset = RendezVous.objects.all()
        docteur_id = self.request.query_params.get('docteur', None)
        if docteur_id:
            queryset = queryset.filter(docteur_id=docteur_id)
        return queryset

# --- Vues API ---

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        return Response({"message": "Connexion réussie"}, status=200)
    return Response({"error": "Identifiants invalides"}, status=401)

@api_view(['POST'])
def send_email_api(request):
    try:
        to = request.data.get('to')
        subject = request.data.get('subject')
        body = request.data.get('body')
        send_mail(subject, body, 'noreply@sghl.com', [to], fail_silently=False)
        return Response({"status": "Email envoyé avec succès"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

def get_rapport_stats(request):
    data = {
        'patients': Patient.objects.count(),
        'ordonnances': Ordonnance.objects.count(),
        'stocksCritiques': Medicament.objects.filter(stock__lt=10).count()
    }
    return JsonResponse(data)

@csrf_exempt
def creer_rapport(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return JsonResponse({"status": "Rapport généré", "data": data})
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)