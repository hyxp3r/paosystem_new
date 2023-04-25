import pyodbc
from django.conf import settings
import pandas as pd
from .xlsxResponse import ResponseXlsx



class Connection:

    server = settings.TANDEM_HOST
    database = settings.TANDEM_DB
    username = settings.TANDEM_USERNAME
    password = settings.TANDEM_PASSWORD

    def connect(self):

        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)

class ReportOne(Connection):

    def get(self, request):
        
        self.connect()

        programs = request.get("program")
        forms = request.get("form")


        with self.conn:

            #print(request.get("checkboxLanguageMain"))
            print(request)

            data = pd.read_sql_query(f"""SELECT DISTINCT
            V.personalNumber as 'Личный номер ПК'
            ,V.fullFio as 'ФИО'
            ,V.developForm as 'Форма'
            ,V.programSetTitle as 'Направление'
            {",Replace(ISNULL(PContact.PHONEMOBILE_P, ''), '+', '') 'Телефон'" if request.get("checkboxPhone") else ""}
            {",ISNULL(PContact.EMAIL_P, '') as 'E-mail'" if request.get("checkboxEmail") else ""}
            {",CAST(V.rating as int) as 'Сумма баллов'" if request.get("checkboxRating") else ""}
            {",V.eduDocumentAverageMark as 'Средний балл ДОО'" if request.get("checkboxDocumentRating") else ""}
            {",FL.TITLE_P as 'Язык'" if request.get("radioLanguage") else ""} 
            {",EP.COMMENT_P as 'Профиль'" if request.get("checkboxProfile") else ""} 
          
            FROM Tandem_prod.dbo.enr_req_competition_ext_view AS V
           
            JOIN Tandem_prod.dbo.ENR14_REQUEST_T R ON R.ENTRANT_ID = V.entrantId
            JOIN enr14_request_t ER on EN.ID = ER.ENTRANT_ID
            JOIN identitycard_t IC on IC.ID = ER.identitycard_id
            
            JOIN Tandem_prod.dbo.PERSON_T P on P.ID = IC.PERSON_ID 
            JOIN Tandem_prod.dbo.personcontactdata_t PContact ON P.CONTACTDATA_ID = PContact.ID

            {"JOIN personforeignlanguage_t L on P.ID = L.PERSON_ID JOIN foreignlanguage_t FL on L.LANGUAGE_ID = FL.ID" if request.get("radioLanguage") else ""} 
            {"JOIN enr14_requested_comp_t EP on EP.REQUEST_ID = V.entrantRequestId" if request.get("checkboxProfile") else ""} 

            WHERE V.enrollmentCampaignYear = 2022
            AND V.developForm in ({", ".join(str(f"'{x}'") for x in forms)})
            AND V.programSetTitle in ({", ".join(str(f"'{x}'") for x in programs)})
            {"AND L.MAIN_P = 1" if request.get("radioLanguage") == "main" else ""} 
            {"AND L.MAIN_P <> 1" if request.get("radioLanguage") == "second" else ""} 
            """, self.conn)
         
            return data


        

        
        
    


