
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CheckEc
# Create your views here.



#@login_required(login_url = 'login')
def contracts(request):

    issues = CheckEc.objects.all().values()
    print(issues)
    return render(request, "pao/contracts.html")
