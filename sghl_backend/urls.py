# sghl_backend/urls.py
from django.contrib import admin
from django.urls import path, include 
from django.views.generic.base import RedirectView
from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls), 
    
    # MODIFIEZ CETTE LIGNE :
    # Au lieu de 'clinical/', utilisez '' (vide) pour que les routes 
    # de clinical.urls soient directement accessibles comme /patients/
    # OU utilisez 'api/' si vous voulez que tout soit sous le préfixe /api/
    path('clinical/rest/', include('clinical.urls')),
    path('api/', include('clinical.urls')), 
    
    path('', RedirectView.as_view(url='/api/docs', permanent=False), name='index'),
]