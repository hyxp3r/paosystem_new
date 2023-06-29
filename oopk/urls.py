from django.urls import path
from .views import Report, MyAjaxFilterView, download_report_view, ReportTable, delete_sheet_view
from django.contrib.auth.decorators import login_required




urlpatterns = [
    path("oopk/report", login_required(Report.as_view()), name = "report"),
    path("oopk/report/filter", login_required(MyAjaxFilterView.as_view()), name = "filter"),
    path("oopk/report/getreport", download_report_view, name = "getreport"),
    path("oopk/report/gettableone", login_required(ReportTable.as_view()), name = "report_table"),
    path("oopk/report/gettableone/delete-item", delete_sheet_view, name = "delete-item")
    
] 
    