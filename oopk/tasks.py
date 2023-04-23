from celery import shared_task
from .reports import ReportOne

@shared_task
def make_report_one(request):

    response = ReportOne().makeReport(request)
    return response

    
   
   
