
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.



#@login_required(login_url = 'login')
def contracts(request):
    return render(request, "pao/contracts.html")
