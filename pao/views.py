
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from .models import CheckEc, Concat, Appeals
from django.db.models import Sum
from django.views.generic import ListView, CreateView, FormView
from .forms import ConcatForm
from .files import files1C
from .studyload import StudyLoad
from .forms import Proccess1CFileForm, StudyLoadForm

from .tasks import send_spam_email
# Create your views here.



#@login_required(login_url = 'login')
class ContractsListView(ListView):

    
    template_name = "pao/contracts.html"
    queryset = CheckEc.objects.all().select_related("contractName__expertEC__department").order_by("contractName")
    print(queryset[0].createdTime)
    context_object_name = "issues"
    login_required = True

    
    def get_context_data(self, **kwargs):

        sum_requests = CheckEc.objects.all().aggregate(Sum("verified"), Sum("declared"))
        all_persent = round(sum_requests["verified__sum"]/sum_requests["declared__sum"]*100)

        appeals = Appeals.objects.all()

        context = super().get_context_data(**kwargs)
        context["sum_requests"] = sum_requests
        context["all_persent"] = all_persent
        context["createdTime"] = self.queryset[0].createdTime
        context["appeals"] = appeals[0].count

        return context

class ConcatView(CreateView):

    model = Concat
    form_class = ConcatForm
    success_url = "/"
    template_name = "pao/mail.html"

    def form_valid(self, form ) :
        form.save()
        #send(form.instance.email)
        send_spam_email.delay(form.instance.email)
        return super().form_valid(form)

def file(request):

   form = Proccess1CFileForm()
   
   if request.method == "POST":

      form = Proccess1CFileForm(request.POST, request.FILES)
      if form.is_valid():

         
         file = form.cleaned_data["file"]
         response = files1C().getInfo(file, type)
         
         if response:
            return response
         else:
            messages.info(request, "Запрос отклонен. Проверьте файл на соответствие шаблону 1С!")
      else:
            messages.info(request, "Запрос отклонен. Загрузите файл формата .xlsx!")

   return render(request,"pao/file.html", {"form":form})


class StudyLoadView(FormView):

   form_class = StudyLoadForm
   template_name = "pao/nagruzka.html"
   success_url = "sudyload"
   
   def form_valid(self, form) -> HttpResponse:

      file = self.get_form_kwargs().get("files").get("file")
      response = StudyLoad(file).makeLoad()

      if response:
         return  response
      else:
      
         messages.info(self.request, "Запрос отклонен. Файлы в архиве не соответствуют файлам нагрузки")
         return super().form_valid(form)

   def form_invalid(self, form):
      
      messages.info(self.request, "Запрос отклонен. Можно загружать только архив формата .zip")

      return super().form_invalid(form)

      

   