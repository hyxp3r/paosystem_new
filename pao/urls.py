from django.urls import path
from .views import ContractsListView, ConcatView, file
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(ConcatView.as_view()), name = "mail"),
    path("pao/contracts", login_required(ContractsListView.as_view()), name = "paocontracts"),
    path("pao/file1C", login_required(file), name = "file")
    
] 