from django.urls import path
from .views import Report, MyAjaxFilterView, download_report_view, ReportTable, delete_sheet_view, ExamRegistration, download_reg_file_view, ExamWrite, ExameAjaxFilterView, download_write_file_view, ExamMail, download_mail_file_view
from django.contrib.auth.decorators import login_required




urlpatterns = [
    path("oopk/report", login_required(Report.as_view()), name = "report"),
    path("oopk/report/filter", login_required(MyAjaxFilterView.as_view()), name = "filter"),
    path("oopk/report/getreport", download_report_view, name = "getreport"),
    path("oopk/report/gettableone", login_required(ReportTable.as_view()), name = "report_table"),
    path("oopk/report/gettableone/delete-item", delete_sheet_view, name = "delete-item"),
    
    path("oopk/exam/registration", login_required(ExamRegistration.as_view()), name = "exam_registration"),
    path("oopk/exam/registration/getreg", download_reg_file_view , name = "get_reg_file"),

    path("oopk/exam/write", login_required(ExamWrite.as_view()), name = "exam_write"),
    path("oopk/exam/write/filter", login_required(ExameAjaxFilterView.as_view()), name = "filter_write"),
    path("oopk/exam/write/getwrite", download_write_file_view , name = "get_write_file"),

    path("oopk/exam/mail", login_required(ExamMail.as_view()), name = "exam_mail"),
    path("oopk/exam/mail/getmail", download_mail_file_view , name = "get_mail_file"),
    
] 
    