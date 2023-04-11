from django.urls import path
from .views import Report
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path("pao/contracts", login_required(Report.as_view()), name = "report"),
    
] 
    