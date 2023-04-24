from celery import shared_task
from .reports import ReportOne
from .xlsxResponse import ResponseXlsx

@shared_task
def make_report_one(request):

    print(request)

    data = ReportOne().get(request)
    print(data)
    response = ResponseXlsx(data).makeIO()
    return response

    
   
   
