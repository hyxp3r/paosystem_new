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
        
        if self.request.get("program"):
            programs = ", ".join(str(f"'{x}'") for x in self.request.get("program"))

        if self.request.get("form"):
            forms = ", ".join(str(f"'{x}'") for x in self.request.get("form"))
            

        if self.request.get("competitionType"):
            competitionType = ", ".join(str(f"'{x}'") for x in self.request.get("competitionType"))
        
        if self.request.get("abiturstatus"):
            abiturstatus = ", ".join(str(f"'{x}'") for x in self.request.get("abiturstatus"))

        if self.request.get("checkboxMinRating"):
            minRating = self.request.get("minrating")

        data = f"""SELECT DISTINCT
        V.personalNumber as 'Личный номер ПК'
        ,V.fullFio as 'ФИО'
        ,V.developForm as 'Форма'
        ,V.programSetTitle as 'Направление'
        ,V.priority as 'Приоритет'
        {",V.competitionType as 'Тип конкурса'" if self.request.get("checkboxCompetition") else ""}
        {",V.state as 'Статус абитуриента'" if self.request.get("checkboxStatus") else ""}
        {",Replace(ISNULL(PContact.PHONEMOBILE_P, ''), '+', '') 'Телефон'" if self.request.get("checkboxPhone") else ""}
        {",ISNULL(PContact.EMAIL_P, '') as 'E-mail'" if self.request.get("checkboxEmail") else ""}
        {",CAST(V.rating as int) as 'Сумма баллов'" if self.request.get("checkboxRating") else ""}
        {",V.eduDocumentAverageMark as 'Средний балл ДОО'" if self.request.get("checkboxDocumentRating") else ""}
        {",FL.TITLE_P as 'Язык'" if self.request.get("radioLanguage") else ""} 
        {",EP.COMMENT_P as 'Профиль'" if self.request.get("checkboxProfile") else ""} 
        {",CASE WHEN V.originalDocumentHandedIn = 1 then 'Оригинал' ELSE 'Копия' end as 'Оригинал / Копия'" if self.request.get("checkboxOriginalHandIn") else ""}
        {",DK.Title_p 'Документ об образовании'" if self.request.get("checkboxDocumentKind") else ""}
        {",EL.SHORTTITLE_P as 'Уровень образования в ДОО'" if self.request.get("checkboxDocumentEduLevel") else ""}
        {",CASE WHEN V.needDormitory = 1 then 'Да' ELSE 'Нет' end as 'Необходимость в общежитии'" if self.request.get("checkboxNeedDormitory") else ""}
        {",PRelative.LASTNAME_P + ' ' + PRelative.FIRSTNAME_P + ' ' + ISNULL(PRelative.MIDDLENAME_P, '') as 'ФИО родственника'" if self.request.get("checkboxRelativeFio") else "" }
        {",PRelative.PHONES_P as 'Контактный телефон родственника'" if self.request.get("checkboxRelativePhone") else "" }
        {",PRelative.EMAIL_P as 'E-mail родственника'" if self.request.get("checkboxRelativeEmail") else ""  }
        {",RelativeDegree.TITLE_P as 'Степень родства'" if self.request.get("checkboxRelativeDegree") else "" }
        FROM Tandem_prod.dbo.enr_req_competition_ext_view AS V
        
        JOIN Tandem_prod.dbo.ENR14_REQUEST_T R ON R.ENTRANT_ID = V.entrantId
        JOIN identitycard_t IC on IC.ID = R.identitycard_id
        
        JOIN Tandem_prod.dbo.PERSON_T P on P.ID = IC.PERSON_ID 
        JOIN Tandem_prod.dbo.personcontactdata_t PContact ON P.CONTACTDATA_ID = PContact.ID

        {"JOIN personforeignlanguage_t L on P.ID = L.PERSON_ID JOIN foreignlanguage_t FL on L.LANGUAGE_ID = FL.ID" if self.request.get("radioLanguage") else ""} 
        {"JOIN enr14_requested_comp_t EP on EP.REQUEST_ID = V.entrantRequestId" if self.request.get("checkboxProfile") else ""} 
        {"JOIN person_edu_doc_t PD on P.MAINEDUDOCUMENT_ID = PD.ID JOIN c_edu_doc_kind_t DK on DK.ID = PD.EDUDOCUMENTKIND_ID JOIN c_edu_level_t EL on PD.EDULEVEL_ID = EL.ID" if self.request.get("checkboxDocumentKind") or self.request.get("checkboxDocumentEduLevel")  else ""}
        {"LEFT JOIN personnextofkin_t PRelative ON P.ID = PRelative.PERSON_ID LEFT JOIN relationdegree_t RelativeDegree ON PRelative.RELATIONDEGREE_ID = RelativeDegree.ID" if self.request.get("checkboxRelativeFio") or self.request.get("checkboxRelativePhone") or self.request.get("checkboxRelativeEmail") or self.request.get("checkboxRelativeDegree") else ""}

        WHERE V.enrollmentCampaign = '{self.request.get("compony")}'
        {f"AND V.developForm in ({forms})" if self.request.get("form") else ""}
        {f"AND V.competitionType in ({competitionType})" if self.request.get("competitionType") else ""}
        {f"AND V.programSetTitle in ({programs})"  if self.request.get("program") else ""}
        {f"AND V.state in ({abiturstatus})"  if self.request.get("abiturstatus") else ""}
        {"AND L.MAIN_P = 1" if self.request.get("radioLanguage") == "main" else ""} 
        {"AND L.MAIN_P <> 1" if self.request.get("radioLanguage") == "second" else ""} 
        {"AND V.enrOrderNumber is not null AND V.enrExtractCancelled = 0" if self.request.get("checkboxOrder") else ""}

        {f"AND CAST(V.rating as int) >= {minRating}" if self.request.get("checkboxMinRating")  else ""} 
        """
        return data
         
    def make_report(self):

        data = self.prepare_data()
        data = self.make_query(data)
        data = self.clear_data(data)

        return data


        
class ExamRegistration(ReportDataOperation):

    def __init__(self, request) -> None:
        self.request = request


    def prepare_data(self):
        
        data = f"""
        select distinct

        'ВИ 2023' 'firstname' 
        ,V.fullFio 'lastname' 
        ,V.personalNumber + '@nsuem.ru' 'email' 
        ,V.personalNumber 'username'
        ,'1' + REVERSE(V.personalNumber * 4) 'password' 

        from enr14_exam_group_t EG
        join enr14_exam_pass_discipline_t EPD on EPD.EXAMGROUP_ID = EG.ID
        join enr14_camp_discipline_t CD on CD.ID = EG.DISCIPLINE_ID
        join enr14_c_discipline_t D on D.ID = CD.DISCIPLINE_ID

        join enr14_exam_group_sch_event_t SCHEV on SCHEV.EXAMGROUP_ID = EG.ID
        join enr14_exam_sched_event_t EVE on EVE.ID = SCHEV.EXAMSCHEDULEEVENT_ID
        join sc_event SC on SC.ID = EVE.SCHEDULEEVENT_ID

        join Tandem_prod.dbo.enr_req_competition_ext_view V on V.entrantId = EPD.ENTRANT_ID
        JOIN Tandem_prod.dbo.ENR14_REQUEST_T R ON R.ENTRANT_ID = V.entrantId
        JOIN Tandem_prod.dbo.identitycard_t IC ON IC.ID = R.IDENTITYCARD_ID
        JOIN Tandem_prod.dbo.PERSON_T P on P.ID = IC.PERSON_ID 
        JOIN Tandem_prod.dbo.personcontactdata_t PContact ON P.CONTACTDATA_ID = PContact.ID

        where V.enrollmentCampaignYear = 2023 
        and CONVERT(date,SC.DURATIONBEGIN_P) BETWEEN '{self.request.get("start_date")}' AND '{self.request.get("end_date")}'
        """
        return data 
    
    def reg_exam(self):

        data = self.prepare_data()
        data = self.make_query(data)
        data = self.clear_data(data)

        return data
            
            



