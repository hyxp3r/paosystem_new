from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .models import  GoogleReport
from system.models import Google
import json
from main.models import User
from django.db import transaction


class GoogleErrors:

    def __init__(self) -> None:

        self.result = {"error": None}


        
class GoogleConnection(GoogleErrors):

    SCOPES =  ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']

    def __init__(self, user: int) -> None:
        super().__init__()
        self.user = user
        self.creds = Credentials.from_authorized_user_info(Google.objects.get(user = self.user).json, self.SCOPES)

        

    
    def update_creds(self):

        creds_json = self.creds.to_json()
        creds_json = json.loads(creds_json)
        

        Google.objects.filter(user=self.user).update(json = creds_json)

    def check_creds(self):

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
           
                self.creds.refresh(Request())
                self.update_creds()
        
              
    
    def build_services(self):
        try:
            self.check_creds()
        except:
            self.result.update({"error": "Ошибка при при формировании Google Key"})
            return self.result

        try:
            service = build('sheets', 'v4', credentials = self.creds)
            drive_service = build('drive', 'v3', credentials = self.creds)
            self.result.update({"service": service, "drive_service": drive_service})
            return self.result
        except:
            self.result.update({"error": "Ошибка при при создании сервисов"})

    
 
class Create_Sheet(GoogleErrors):

    def __init__(self, user: int, service, name , comment) -> None:

        super().__init__()
    
        self.user_inst = User.objects.get(pk = user)
        self.comment = comment
        self.name = name
        self.report = GoogleReport.objects.create(user = self.user_inst)
        self.service = service

        self.spreadsheet = {
                    'properties': {
                        'title': self.name
                    },
                    'sheets': [
                        {
                            'properties': {
                                'title': 'Отчет'
                            }
                        }
                    ]
                }

    def create(self):

        try:
            spreadsheet = self.service.spreadsheets().create(body=self.spreadsheet).execute()
            spreadsheet_id = spreadsheet['spreadsheetId']
            sheet_id = spreadsheet['sheets'][0]['properties']['sheetId']
            
            url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
            self.report.url = url
            self.report.spreadsheet_id = spreadsheet_id
            if self.comment:
                self.report.comment = self.comment
            self.report.name = self.name
            self.report.save()
            self.result.update({"sheet_id": sheet_id, "spreadsheet_id": spreadsheet_id, "url": url})
        except:
            last_obj = GoogleReport.objects.latest('id')
            last_obj.delete()
            self.result.update({"error":"Ошибка при создании файла"})
        
        return self.result


class InsertData(GoogleErrors):

    def __init__(self, data, service, spreadsheet_id, range_name = "Отчет") -> None:
        super().__init__()
        self.data = data
        self.service = service
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name



    def insert(self):


        try:
            values = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId= self.spreadsheet_id,
            body=
            {
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"{self.range_name}!A1",
                        "majorDimension": "ROWS",
                        "values": self.data.T.reset_index().T.values.tolist()}]
            }
            ).execute()
        except:
            self.result.update({"error":"Ошибка при добавлении данных"})

        return self.result

class Permissions(GoogleErrors):

    def __init__(self, drive_service, spreadsheet_id ) -> None:
        super().__init__()
       
        self.drive_service = drive_service
        self.spreadsheet_id = spreadsheet_id

    def add_editor(self):

        permission = {
        'role': 'writer',
        'type': 'anyone',
        'allowFileDiscovery': False,
        }

        try:
            self.drive_service.permissions().create(fileId=self.spreadsheet_id, body=permission).execute()
       
        except:
            self.result.update({"error":"Ошибка при добавлении прав"})

        return self.result
        


class Clear:

    def __init__(self, service, spreadsheet_id, range_name) -> None:

        self.service = service
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name

    def clear_data(self):
        
        self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheet_id, range=f'{self.range_name}!A1:Z').execute()
        
    
class Custom(GoogleErrors):


    def __init__(self, service, spreadsheet_id, sheet_id, columns) -> None:
        super().__init__()
        self.service = service
        self.spreadsheet_id = spreadsheet_id
        self.sheet_id = sheet_id
        self.columns = columns

        self.requests = []

        self.custom_variants = {
            "column_resize": self.column_resize,
            "froze_row": self.froze_row,
            "center_data": self.center_data

        }

    def column_resize(self):

        self.requests.append( {
        'autoResizeDimensions': {
            'dimensions': {
                'sheetId': self.sheet_id,
                'dimension': 'COLUMNS',
                'startIndex': 0,
                'endIndex': self.columns
            }
        }
    })
        
    
    def froze_row(self):
        
        self.requests.append({
        'updateSheetProperties': {
            'properties': {
                'sheetId': self.sheet_id,
                'gridProperties': {
                    'frozenRowCount': 1
                }
            },
            'fields': 'gridProperties.frozenRowCount'
        }
    })
    
    def center_data(self):

        self.requests.append({
        'repeatCell': {
            'range': {
                'sheetId': self.sheet_id,
                'startRowIndex': 0,
                'endRowIndex': 1,
                'startColumnIndex': 0,
                'endColumnIndex': self.columns
            },
            'cell': {
                'userEnteredFormat': {
                    'textFormat': {
                        'bold': True
                    },
                    'horizontalAlignment': 'CENTER'
                }
            },
            'fields': 'userEnteredFormat(textFormat,horizontalAlignment)'
        }
    })
        
    def make_custom(self, *args):

        for user_variant in args:
            for k, variant in self.custom_variants.items():
                if user_variant == k:
                    variant()
        try:
            batch_update_request = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id, body={'requests': self.requests})
            batch_update_response = batch_update_request.execute()
        except:
             self.result.update({"error":"Ошибка при добавлении кастомизации"})
             
        return self.result
       

           
class DeleteData(GoogleErrors):

    def __init__(self, drive_service, spreadsheet_id) -> None:
        super().__init__()
        self.drive_service = drive_service
        self.spreadsheet_id = spreadsheet_id

    
    def delete(self):

        try:
            self.drive_service.files().delete(fileId=self.spreadsheet_id).execute()
        except:
            self.result.update({"error":"Ошибка при удалении файла!"})
     
        
        return self.result


