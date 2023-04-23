from django.urls import path
from .views import Report, MyAjaxFilterView, download_report_view
from django.contrib.auth.decorators import login_required




urlpatterns = [
    path("oopk/report", login_required(Report.as_view()), name = "report"),
    path("oopk/report/filter", login_required(MyAjaxFilterView.as_view()), name = "filter"),
    path("oopk/report/getreport", download_report_view, name = "getreport"),
    
] 
    