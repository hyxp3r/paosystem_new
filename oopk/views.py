from django.shortcuts import render
from .models import EduLevelProgram, Program, DevelopeForm

# Create your views here.
from django.views.generic import TemplateView, View


class Report(TemplateView):
    template_name = 'oopk/report.html'

    def get_context_data(self, **kwargs):
                
        context = super().get_context_data(**kwargs)

        eduLevel = EduLevelProgram.objects.all().order_by("name")
        program = Program.objects.all().order_by("code")
        form = DevelopeForm.objects.all().order_by("sort")

        context['eduLevel'] = eduLevel
        context['programs'] = program
        context['forms'] = form

        return  context
    
"""
class Report(View):

    pass
"""