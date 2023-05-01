from django.shortcuts import render
from .models import EduLevelProgram, Program, DevelopeForm, PriemType
from django.http import JsonResponse
from .tasks import make_report_xlsx, make_report_google

from django.http import HttpResponse
import base64
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.views.generic import  View




class Report(View):
    template_name = 'oopk/report.html'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = {
            "success": True,
            "errors": None
        }

        self.postData = {}
    
    def get(self, request, *args, **kwargs):

        eduLevel = EduLevelProgram.objects.all().order_by("name")
        program = Program.objects.all().order_by("code")
        form = DevelopeForm.objects.all().order_by("sort")
        finance = PriemType.objects.all().order_by("name")

        context = {}

        context['eduLevel'] = eduLevel
        context['programs'] = program
        context['forms'] = form
        context['typePriem'] = finance

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
 
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

            self.postData = request.POST.dict()
            self.postData.update({"program":request.POST.getlist("program")})
            self.postData.update({"form":request.POST.getlist("form")})
            self.postData.update({"user":request.user.id})
            

            #print(request.POST.dict())
            if self.postData.get("radioReportType") == "google":
                task = make_report_google.delay(self.postData)
                operation_type = "google"
            else:
                print("xlsx")
                task = make_report_xlsx.delay(self.postData)
                operation_type = "xlsx"
        
      
            return JsonResponse({'task_id': task.id, "operation_type": operation_type})
  
       
@csrf_exempt
def download_report_view(request):

    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
     
        task_id = request.POST.get('task_id')
        

        if request.POST.get("operation_type") == "xlsx":
            result = make_report_xlsx.AsyncResult(task_id)
        else:
            result = make_report_google.AsyncResult(task_id)

        if result.ready():

            result = result.result
            
            if request.POST.get("operation_type") == "xlsx":
                
                return JsonResponse({'status': 'SUCCESS', 'file': result, 'file_name': 'report.xlsx'})
            else:
                if result["error"]:
                    pass
                else:
                    return JsonResponse({'status': 'SUCCESS', 'url': result["url"]})
        else:
            
            return JsonResponse({'status': 'in_progress'})
    else:
       
        return HttpResponse("Error: Invalid request method.")



class MyAjaxFilterView(View):

    def get(self, request, *args, **kwargs):

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # Получение значений выбранных полей формы
            filter_value = request.GET.get('filter_field1')
            
            # Фильтрация данных на основе значений выбранных полей
            filtered_data = Program.objects.filter(eduLevel__tandem_name = filter_value)
            # Пример формирования данных для отправки в JSON-формате
            data = {'filtered_data': list(filtered_data.values())}

            return JsonResponse(data)
"""
class Report(View):

    pass
"""