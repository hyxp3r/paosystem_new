from django.shortcuts import render
from .models import EduLevelProgram, Program, DevelopeForm, PriemType, GoogleReport, Status, ExamesTite
from django.http import JsonResponse
from .tasks import make_report_xlsx, make_report_google, register_entrant, write_exames, make_mail_exam

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.views.generic import  View
from django.core.paginator import Paginator

from .google import GoogleConnection, DeleteData



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
        status = Status.objects.all().order_by("name")
        
        context = {}

        context['eduLevel'] = eduLevel
        context['programs'] = program
        context['forms'] = form
        context['typePriem'] = finance
        context['status'] = status

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
 
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

            self.postData = request.POST.dict()
           
            self.postData.update({"program":request.POST.getlist("program")})
            self.postData.update({"form":request.POST.getlist("form")})
            self.postData.update({"competitionType":request.POST.getlist("competitionType")})
            self.postData.update({"abiturstatus":request.POST.getlist("abiturstatus")})
            self.postData.update({"user":request.user.id})
            

         
            if self.postData.get("radioReportType") == "google":
                task = make_report_google.delay(self.postData)
                operation_type = "google"
            else:
                
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


#фильтр для формы запросов
class MyAjaxFilterView(View):

    def get(self, request, *args, **kwargs):

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # Получение значений выбранных полей формы
            filter_value = request.GET.get('filter_field1')
            
            # Фильтрация данных на основе значений выбранных полей
            filtered_data = Program.objects.filter(eduLevel__name = filter_value)
            # Пример формирования данных для отправки в JSON-формате
            data = {'filtered_data': list(filtered_data.values())}

            return JsonResponse(data)
        
#Вывод данных в отчетную таблицу
class ReportTable(View):

     template_name = 'oopk/report_table.html'


     def get(self, request, *args, **kwargs):

        report = GoogleReport.objects.select_related("user").order_by("-created_time")

        paginator = Paginator(report, 10) # 10 элементов на страницу
        page = request.GET.get('page')
        items = paginator.get_page(page)

        context = {}

        context['reports'] = items


        return render(request, self.template_name, context)

#Удаление отчета google
@csrf_exempt
def delete_sheet_view(request):

   
    result = {"success": True, "error": None}

    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

    
        services = GoogleConnection(request.user.pk).build_services()
    
        if services["error"]:
            result.update({"success": False,"error": services["error"]})

        spreadsheet_id = GoogleReport.objects.get(pk = request.POST.get("itemId")).spreadsheet_id
      

        delete_result = DeleteData(drive_service = services["drive_service"], spreadsheet_id=spreadsheet_id).delete()
        GoogleReport.objects.get(pk = request.POST.get("itemId")).delete()

        
        return JsonResponse(result)

#------------------------------------------
#Exames

class ExamRegistration(View):
    template_name = 'oopk/exam_registration.html'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = {
            "success": True,
            "errors": None
        }

        self.postData = {}
    
    def get(self, request, *args, **kwargs):
     

        return render(request, self.template_name)  
    
    def post(self, request, *args, **kwargs):

        self.postData = request.POST.dict()

        task = register_entrant.delay(self.postData)
 
        return JsonResponse({'task_id': task.id})
    

@csrf_exempt
def download_reg_file_view(request):

    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
     
        task_id = request.POST.get('task_id')
        
        result = register_entrant.AsyncResult(task_id)
      
        if result.ready():

            result = result.result
            
            return JsonResponse({'status': 'SUCCESS', 'file': result["file"], 'file_name': result["file_name"], 'type': result["type"] } )
           
        else:
            
            return JsonResponse({'status': 'in_progress'})
    else:
       
        return HttpResponse("Error: Invalid request method.")

class ExamWrite(View):
    template_name = 'oopk/exam_write.html'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = {
            "success": True,
            "errors": None
        }

        self.postData = {}
    
    def get(self, request, *args, **kwargs):

        eduLevel = ExamesTite.objects.select_related('edulevel').values_list('edulevel__name', flat=True).distinct()
        exames_title = ExamesTite.objects.values_list('name', flat=True).order_by("name")
        
        
        context = {}

        context['eduLevel'] = eduLevel
        context["exames"] = exames_title
     

        return render(request, self.template_name, context)  
    
    def post(self, request, *args, **kwargs):

        self.postData = request.POST.dict()

        self.postData.update({"exam":request.POST.getlist("exam")})

        task = write_exames.delay(self.postData)
 
        return JsonResponse({'task_id': task.id})
 

#фильтр для записи экзаменов
class ExameAjaxFilterView(View):

    def get(self, request, *args, **kwargs):

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # Получение значений выбранных полей формы
            group = True if request.GET.get('group') == "Да" else False
    
            eduLevel = request.GET.get('eduLevel')
      
            # Фильтрация данных на основе значений выбранных полей
            filtered_data = ExamesTite.objects.select_related("edulevel").filter(edulevel__name = eduLevel, group = group)
        
            # Пример формирования данных для отправки в JSON-формате
            data = {'filtered_data': list(filtered_data.values())}

            return JsonResponse(data)
        
@csrf_exempt
def download_write_file_view(request):

    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
     
        task_id = request.POST.get('task_id')
        
        result = write_exames.AsyncResult(task_id)
      
        if result.ready():

            result = result.result
            
            return JsonResponse({'status': 'SUCCESS', 'file': result["file"], 'file_name': result["file_name"], 'type': result["type"] } )
           
        else:
            
            return JsonResponse({'status': 'in_progress'})
    else:
       
        return HttpResponse("Error: Invalid request method.")


class ExamMail(View):
    template_name = 'oopk/exam_mail.html'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.data = {
            "success": True,
            "errors": None
        }

        self.postData = {}
    
    def get(self, request, *args, **kwargs):
     

        return render(request, self.template_name)  
    
    def post(self, request, *args, **kwargs):

        self.postData = request.POST.dict()

        task = make_mail_exam.delay(self.postData)
 
        return JsonResponse({'task_id': task.id})
    

@csrf_exempt
def download_mail_file_view(request):

    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
     
        task_id = request.POST.get('task_id')
        
        result = make_mail_exam.AsyncResult(task_id)
      
        if result.ready():

            result = result.result
            
            return JsonResponse({'status': 'SUCCESS', 'file': result["file"], 'file_name': result["file_name"], 'type': result["type"] } )
           
        else:
            
            return JsonResponse({'status': 'in_progress'})
    else:
       
        return HttpResponse("Error: Invalid request method.")