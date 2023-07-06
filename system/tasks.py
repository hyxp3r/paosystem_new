from .models import GoogleMonitoringFiles, LogsCron, AirtableTables
from oopk.google import Google, GoogleConnection, Clear, InsertData
from oopk.reports import ReportDataOperation
from oopk.airtable import AirtableDataOperations
from celery import shared_task

@shared_task
def update_monitoring_all():

    name_task = "Обновление мониторинга ПК2023"
    status = "Выполнено успешно"

    
    monitoring_files = GoogleMonitoringFiles.objects.prefetch_related("monitoring").all()
    services = GoogleConnection(user = 1).build_services()
    try:    
        for file in monitoring_files:

            sheets = file.monitoring.all().select_related("query").all()
            spreadsheet_id = file.spreadsheet_id

            for sheet in sheets:
                    sheet_name = sheet.name
                    query = sheet.query.body

                    dataOperation = ReportDataOperation()
                    data = dataOperation.make_query(query = query)
                    data = dataOperation.clear_data(data = data) 
                    clearData = Clear(service = services["service"], spreadsheet_id = spreadsheet_id, range_name = sheet_name).clear_data()
                    insertData = InsertData(data = data, service = services["service"], spreadsheet_id = spreadsheet_id, range_name = sheet_name).insert()

        LogsCron.objects.create(name = name_task, status = status)
        
    except:
        status = "Ошибка"
        LogsCron.objects.create(name = name_task, status = status)
                   

@shared_task
def update_air_grant():

    name_task = "Гранты 235+ (air)"
    status = "Выполнено успешно"
    data_operation = ReportDataOperation()
    try:
        table = AirtableTables.objects.select_related("query").filter(name = "Гранты_ВО_2023")[0]
    except:
        LogsCron.objects.create(name = name_task, status = "Ошибка при получении записи PostgreSQL")
        raise ConnectionError
    
    table_name = "Гранты_ВО_2023"
    base_id = table.base.base_id
    query = table.query.body
    
    airtable = AirtableDataOperations(user_id = 1, base_id = base_id, table_name = table_name)

    try:
        data = data_operation.make_query(query = query)
        data = data_operation.clear_data(data = data)
        records = data.to_dict("records")
    except:
        LogsCron.objects.create(name = name_task, status = "Ошибка Tandem")
        raise ConnectionError

    try:
        not_found = airtable.comparison(records = records, view = "python_import")
        result = airtable.insert_batch(records = not_found)
    except:
        LogsCron.objects.create(name = name_task, status = "Ошибка при работе с AirTable")
        raise ConnectionError
    
    LogsCron.objects.create(name = name_task, status = status)


