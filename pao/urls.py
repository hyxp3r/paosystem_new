from django.urls import path
from . import views

urlpatterns = [
    path("pao/contracts", views.contracts, name = "paocontracts"),
    
] 