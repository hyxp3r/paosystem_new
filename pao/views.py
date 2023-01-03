
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CheckEc
from django.db.models import Sum
from django.views.generic import ListView
# Create your views here.



#@login_required(login_url = 'login')
class ContractsListView(ListView):

    
    template_name = "pao/contracts.html"
    queryset = CheckEc.objects.all().select_related("contractName__expertEC__department")
    context_object_name = "issues"
    login_required = True

    
    def get_context_data(self, **kwargs) -> dict[str]:

        sum_requests = CheckEc.objects.all().aggregate(Sum("verified"), Sum("declared"))
        all_persent = round(sum_requests["verified__sum"]/sum_requests["declared__sum"]*100)

        context = super().get_context_data(**kwargs)
        context["sum_requests"] = sum_requests
        context["all_persent"] = all_persent

        return context

   


