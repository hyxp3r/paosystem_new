from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class Report(TemplateView):
    template_name = 'oopk/report.html'