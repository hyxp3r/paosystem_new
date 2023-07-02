import pyodbc
from django.conf import settings
import pandas as pd



class Connection:

    server = settings.TANDEM_HOST
    database = settings.TANDEM_DB
    username = settings.TANDEM_USERNAME
    password = settings.TANDEM_PASSWORD

    def connect(self):

        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)
        return self.conn

class ReportDataOperation(Connection):
    
    def make_query(self, query):
        self.connect()

        with self.conn:

            data = pd.read_sql_query(query, self.conn)
            return data
            
        
    def clear_data(self, data):

        data = data.fillna("")

        return data
    

class ReportOne(ReportDataOperation):

    def __init__(self, request:dict) -> None:
        
        self.request = request

    def prepare_data(self):
        

        programs = ", ".join(str(f"'{x}'") for x in self.request.get("program"))
        if self.request.get("form"):
            forms = ", ".join(str(f"'{x}'") for x in self.request.get("form"))
            

        if self.request.get("competitionType"):
            competitionType = ", ".join(str(f"'{x}'") for x in self.request.get("competitionType"))
        

        data = f"""SELECT DISTINCT
        V.personalNumber as 'Личный номер ПК'
        ,V.fullFio as 'ФИО'
        ,V.developForm as 'Форма'
        ,V.programSetTitle as 'Направление'
        {",V.competitionType as 'Тип конкурса'" if self.request.get("checkboxCompetition") else ""}
        {",V.state as 'Статус абитуриента'" if self.request.get("checkboxStatus") else ""}
        {",Replace(ISNULL(PContact.PHONEMOBILE_P, ''), '+', '') 'Телефон'" if self.request.get("checkboxPhone") else ""}
        {",ISNULL(PContact.EMAIL_P, '') as 'E-mail'" if self.request.get("checkboxEmail") else ""}
        {",CAST(V.rating as int) as 'Сумма баллов'" if self.request.get("checkboxRating") else ""}
        {",V.eduDocumentAverageMark as 'Средний балл ДОО'" if self.request.get("checkboxDocumentRating") else ""}
        {",FL.TITLE_P as 'Язык'" if self.request.get("radioLanguage") else ""} 
        {",EP.COMMENT_P as 'Профиль'" if self.request.get("checkboxProfile") else ""} 
        {",CASE WHEN V.originalDocumentHandedIn = 1 then 'Оригинал' ELSE 'Копия' end as 'Оригинал / Копия'" if self.request.get("checkboxOriginalHandIn") else ""}
        
        FROM Tandem_prod.dbo.enr_req_competition_ext_view AS V
        
        JOIN Tandem_prod.dbo.ENR14_REQUEST_T R ON R.ENTRANT_ID = V.entrantId
        JOIN identitycard_t IC on IC.ID = R.identitycard_id
        
        JOIN Tandem_prod.dbo.PERSON_T P on P.ID = IC.PERSON_ID 
        JOIN Tandem_prod.dbo.personcontactdata_t PContact ON P.CONTACTDATA_ID = PContact.ID

        {"JOIN personforeignlanguage_t L on P.ID = L.PERSON_ID JOIN foreignlanguage_t FL on L.LANGUAGE_ID = FL.ID" if self.request.get("radioLanguage") else ""} 
        {"JOIN enr14_requested_comp_t EP on EP.REQUEST_ID = V.entrantRequestId" if self.request.get("checkboxProfile") else ""} 

        WHERE V.enrollmentCampaignYear = 2023
        {f"AND V.developForm in ({forms})" if self.request.get("form") else ""}
        {f"AND V.competitionType in ({competitionType})" if self.request.get("competitionType") else ""}
        AND V.programSetTitle in ({programs})
        {"AND L.MAIN_P = 1" if self.request.get("radioLanguage") == "main" else ""} 
        {"AND L.MAIN_P <> 1" if self.request.get("radioLanguage") == "second" else ""} 
        """
        return data
         
    def make_report(self):

        data = self.prepare_data()
        data = self.make_query(data)
        data = self.clear_data(data)

        return data


        

        
        
    


