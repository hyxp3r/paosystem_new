from django.urls import path
from .views import ContractsListView, ConcatView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(ConcatView.as_view()), name = "mail"),
    path("pao/contracts", login_required(ContractsListView.as_view()), name = "paocontracts"),
    
] 