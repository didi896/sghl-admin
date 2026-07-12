from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, 
    DoctorViewSet, 
    OrdonnanceViewSet, 
    TypeTestViewSet, 
    ExamenLaboViewSet, 
    RendezVousViewSet,   # <--- Importez votre nouveau ViewSet
    get_rapport_stats,
    login_view,
    send_email_api
)

# Configuration du router pour les ViewSets automatiques
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'type-tests', TypeTestViewSet, basename='type-test')
router.register(r'examens-labo', ExamenLaboViewSet, basename='examen-labo')
router.register(r'rendez-vous', RendezVousViewSet, basename='rendez-vous') # <--- Enregistré ici

urlpatterns = [
    # Cette ligne "capture" l'URL que votre frontend demande et la redirige vers le router
    path('rest/', include(router.urls)), 
    
    # Mettez les chemins spécifiques EN PREMIER
    path('rapport-stats/', get_rapport_stats, name='rapport-stats'),
    path('auth/', login_view, name='login'),
    path('send-email/', send_email_api, name='send-email'),
    
    # Mettez le router (qui contient tous les ViewSets) EN DERNIER
    path('', include(router.urls)),
]