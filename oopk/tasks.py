from celery import shared_task
from .reports import ReportOne, ExamRegistration
from .xlsxIO import XLSX_IO, CSV_IO
from .google import GoogleConnection, Create_Sheet, InsertData, Permissions, Custom




@shared_task
def make_report_xlsx(request):

    data = ReportOne(request = request).make_report()
    response = XLSX_IO(data).makeIO()
    return response

@shared_task
def make_report_google(request):

    result = {"url": "", "error": None}

    data = ReportOne(request = request).make_report()
    
    services = GoogleConnection(request.get("user")).build_services()


    if services["error"]:
        result.update({"error": services["error"]})
        return result
    
    sheet_data = Create_Sheet(user =request.get("user"),service = services["service"], name = request.get("report_name"), comment = request.get("comment") ).create()

    if sheet_data["error"]:
        result.update({"error": sheet_data["error"]})
        return result
   
    result.update({"url": sheet_data["url"]})


    create = InsertData(data = data, service = services["service"], spreadsheet_id = sheet_data["spreadsheet_id"] ).insert()

    if create["error"]:
        result.update({"error": create["error"]})
        return result
    
    permissions = Permissions(drive_service = services["drive_service"], spreadsheet_id = sheet_data["spreadsheet_id"]).add_editor()
    
    if permissions["error"]:
        result.update({"error": permissions["error"]})
        return result

    custom = Custom(service = services["service"], spreadsheet_id = sheet_data["spreadsheet_id"], sheet_id = sheet_data["sheet_id"], columns = 
                    data.shape[0]).make_custom("column_resize", "froze_row", "center_data" )

    return result

    
   
@shared_task
def register_entrant(request):

    data = ExamRegistration(request = request).reg_exam()

    response = CSV_IO(data = data).makeIO()

    return response
