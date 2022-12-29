
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CheckEc
from django.db.models import Sum
# Create your views here.



#@login_required(login_url = 'login')
def contracts(request):

    issues = CheckEc.objects.all().select_related("contractName__expertEC__department")
    sum_requests = CheckEc.objects.all().aggregate(Sum("verified"), Sum("declared"))
    all_persent = round(sum_requests["verified__sum"]/sum_requests["declared__sum"]*100)
 
   
    return render(request, "pao/contracts.html", {"issues": issues, "sum_requests": sum_requests, "all_persent": all_persent})
