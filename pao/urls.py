from django.urls import path
from .views import ContractsListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("pao/contracts", login_required(ContractsListView.as_view()), name = "paocontracts"),
    
] 