from django.urls import path
from .views import Report, MyAjaxFilterView, download_report_view, ReportTable, delete_sheet_view, ExamRegistration, download_reg_file_view, ExamWrite, ExameAjaxFilterView, download_write_file_view
from django.contrib.auth.decorators import login_required




urlpatterns = [
    path("oopk/report", login_required(Report.as_view()), name = "report"),
    path("oopk/report/filter", login_required(MyAjaxFilterView.as_view()), name = "filter"),
    path("oopk/report/getreport", download_report_view, name = "getreport"),
    path("oopk/report/gettableone", login_required(ReportTable.as_view()), name = "report_table"),
    path("oopk/report/gettableone/delete-item", delete_sheet_view, name = "delete-item"),
    
    path("oopk/exame/registration", login_required(ExamRegistration.as_view()), name = "exame_registration"),
    path("oopk/exame/registration/getreg", download_reg_file_view , name = "get_reg_file"),

    path("oopk/exame/write", login_required(ExamWrite.as_view()), name = "exame_write"),
    path("oopk/exame/write/filter", login_required(ExameAjaxFilterView.as_view()), name = "filter_write"),
    path("oopk/exame/write/getwrite", download_write_file_view , name = "get_write_file"),
    
] 
    