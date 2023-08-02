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
        {",V.enrOrderNumber 'Номер приказа'" if self.request.get("checkboxOrderDate") else ""}
        {",convert(char, V.enrOrderDate, 104) 'Дата приказа'" if self.request.get("checkboxOrderDate") else "" }
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

        where CONVERT(date,SC.DURATIONBEGIN_P) BETWEEN '{self.request.get("start_date")}' AND '{self.request.get("end_date")}'
        """
        return data 
    
    def reg_exam(self):

        data = self.prepare_data()
        data = self.make_query(data)
        data = self.clear_data(data)

        return data
    

class ExamWrite(ReportDataOperation):

    def __init__(self, request) -> None:
        self.request = request


    def prepare_data(self):

        if self.request.get("group") == "Да":
            group = """
            ,case
            
            when D.TITLE_P = 'История' then 'общеобразовательный 1'
            when D.TITLE_P = 'История  (профильность: Юридические науки)' then 'юридические 1'
            when D.TITLE_P = 'История  (профильность: Гуманитарные науки)' then 'гуманитарные 1'
            
            when D.TITLE_P = 'Английский язык' then 'английский язык 1'
            when D.TITLE_P = 'Немецкий язык' then 'немецкий язык 1'
            when D.TITLE_P = 'Французский язык' then 'французский язык 1'
            
            when D.TITLE_P = 'Биология' then 'общеобразовательный'
            when D.TITLE_P = 'Биология (профильность: Гуманитарные науки)' then 'гуманитарные науки'
            
            when D.TITLE_P = 'География' then 'общеобразовательный'
            when D.TITLE_P = 'География (профильность:Технические науки)' then 'технические науки'
        
            end  as 'group1'
            """
            group_where = """
            case
            
            when D.TITLE_P = 'История' then 'общеобразовательный 1'
            when D.TITLE_P = 'История  (профильность: Юридические науки)' then 'юридические 1'
            when D.TITLE_P = 'История  (профильность: Гуманитарные науки)' then 'гуманитарные 1'
            
            when D.TITLE_P = 'Английский язык' then 'английский язык 1'
            when D.TITLE_P = 'Немецкий язык' then 'немецкий язык 1'
            when D.TITLE_P = 'Французский язык' then 'французский язык 1'
            
            when D.TITLE_P = 'Биология' then 'общеобразовательный'
            when D.TITLE_P = 'Биология (профильность: Гуманитарные науки)' then 'гуманитарные науки'
            
            when D.TITLE_P = 'География' then 'общеобразовательный'
            when D.TITLE_P = 'География (профильность:Технические науки)' then 'технические науки'
        
            end
            """
        else:
            group = ""
        
        if self.request.get("exam"):
            exam = ", ".join(str(f"'{x}'") for x in self.request.get("exam"))
       
        data = f"""
            select distinct

        case -- Сопоставление текстового названия экзамена в Тандеме с Уникальным названием курса в Мудле

            -- Бакалавриат / Специалитет
            when D.TITLE_P = 'Английский язык' then 'Иностранный язык ВИ'
            when D.TITLE_P = 'Немецкий язык' then 'Иностранный язык ВИ'
            when D.TITLE_P = 'Французский язык' then 'Иностранный язык ВИ'
            when D.TITLE_P in('Биология','Биология (профильность: Гуманитарные науки)') then 'Биология ВИ'
            when D.TITLE_P in ('География', 'География (профильность:Технические науки)') then 'География ВИ'
            when D.TITLE_P in ('Информатика и ИКТ', 'Информатика и ИКТ (профильность: Технические науки)') then 'Информатика и ИКТ ВИ'
            when D.TITLE_P in ('История', 'История  (профильность: Гуманитарные науки)', 'История  (профильность: Юридические науки)')  then 'История ВИ'
            when D.TITLE_P in ('Математика')   then 'Математика ВИ'
            when D.TITLE_P in ('Математика  (профильность: Гуманитарные науки)')   then 'Математика ВИ (Гуманитарные науки)'
            when D.TITLE_P in ('Математика (профильность: Технические науки)')   then 'Математика ВИ (Технические науки)'
            when D.TITLE_P in ('Математика (профильность: Экономика и управление)')   then 'Математика ВИ (Экономика и управление)'
            when D.TITLE_P in ('Обществознание  (профильность: Гуманитарные науки)')  then 'Обществознание ВИ (Гуманитарные науки)'
            when D.TITLE_P in ('Обществознание')  then 'Обществознание ВИ'
            when D.TITLE_P in ('Обществознание  (профильность: Экономика и управление)')  then 'Обществознание ВИ (Экономика и управление)'
            when D.TITLE_P in ('Обществознание  (профильность: Юридические науки)')  then 'Обществознание ВИ (Юридические науки)'
            when D.TITLE_P = 'Русский язык' then 'Русский язык ВИ'
            when D.TITLE_P = 'Физика' then 'Физика ВИ'
            
            -- Магистратура
            when D.TITLE_P = 'маг. МЭ Зарубежное регионоведение' then 'Международные отношения ВИ'
            when D.TITLE_P = 'маг. МЭ Инноватика' then 'Инноватика ВИ'
            when D.TITLE_P = 'маг. МЭ Информационные системы и технологии' then 'Информационные системы и технологии ВИ'
            when D.TITLE_P = 'маг. МЭ Международные отношения' then 'Международные отношения ВИ'
            when D.TITLE_P = 'маг. МЭ Прикладная информатика' then 'Прикладная информатика ВИ'
            when D.TITLE_P = 'маг. МЭ Психология' then 'Психология ВИ'
            when D.TITLE_P = 'маг. МЭ Реклама и связи с общественностью' then 'Реклама и связи с общественностью ВИ'
            when D.TITLE_P = 'маг. МЭ Социология' then 'Социология ВИ'
            when D.TITLE_P = 'маг. МЭ Статистика' then 'Статистика ВИ'
            when D.TITLE_P = 'маг. МЭ Экономика и Управление' then 'Экономика ВИ'
            when D.TITLE_P = 'маг. МЭ Юриспруденция' then 'Юриспруденция ВИ'
            when D.TITLE_P = 'маг. Экономика' then 'Экономика ВИ'
            when D.TITLE_P = 'маг. Управление персоналом' then 'Управление персоналом ВИ'
            when D.TITLE_P = 'маг. Бизнес-информатика' then 'Бизнес-информатика ВИ'
            when D.TITLE_P = 'маг. Государственное и муниципальное управление' then 'Государственное и муниципальное управление ВИ'
            when D.TITLE_P = 'маг. Менеджмент' then 'Менеджмент ВИ'
            when D.TITLE_P = 'маг. Финансы и кредит' then 'маг. Финансы и кредит'
            when d.TITLE_P = 'маг. МЭ Жилищное хозяйство и коммунальная инфраструктура' then 'Жилищное хозяйство и коммунальная инфраструктура ВИ'

        --Аспирантура

            when D.TITLE_P = 'асп. Частно-правовые (цивилистические) науки' then 'Юриспруденция (аспирантура) ВИ'
        when D.TITLE_P = 'асп. Социология управления' then 'Социология управления ВИ'
        end as 'course1'
        
        -- ,D.TITLE_P 
        ,V.personalNumber 'username' -- Логин студента = Код абитуриента

        {group}

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

        where  CONVERT(date,SC.DURATIONBEGIN_P) BETWEEN '{self.request.get("start_date")}' AND '{self.request.get("end_date")}'
        and  V.enrollmentCampaign = '{self.request.get("compony")}'
        {f"AND D.TITLE_P in ({exam})" if self.request.get("exam") else ""}
        {f"AND {group} is not null" if self.request.get("group") == "Да" else ""}
 
        """
        
        return data 
    
    def write_exam(self):

        data = self.prepare_data()
        data = self.make_query(data)
        data = self.clear_data(data)

        return data
    

class ExamMail(ReportDataOperation):

    def __init__(self, request) -> None:
        self.request = request


    def prepare_data(self):

        data = f"""
        select distinct

        EG.TITLE_P '№ ЭГ' -- Номер экзаменационной группы (потока ВИ) для идентификации человека в ведомостях
        ,D.TITLE_P 'Вступительное испытание'
        ,CONVERT(varchar, SC.DURATIONBEGIN_P, 104) 'Начало' -- Дата проведения экзамена
        ,V.personalNumber 'Личный номер'
        ,'1' + REVERSE(V.personalNumber * 4) 'password' -- Еще раз генерируется пароль для рассылки 
        ,ISNULL(V.firstName, '') + ' ' + ISNULL(V.middleName, '') 'Обращение' -- Только Имя и Отчество для того, чтобы в письме написать "Добрый день, ..."
        ,V.fullFio 'ФИО Абитуриента' -- Для идентификации, отметке об участии 
        ,ISNULL(PContact.EMAIL_P, '') 'Почта' -- Почта абитуриента, на которую будет направлено письмо с инструкцией + логином + паролем

        -- Создаются пустые столбцы с заголовками, чтобы в них в Экселе вставить значения из вспомогательных файлов
        ,'' 'Тест Moodle' -- Ссылка на Курс в Мудле (мы вставляли вручную в этот файл, но можно дополнить в скрипте, чтобы выводилось автоматически)
        ,'' 'ZOOM URL' -- Ссылка на подключение к Зуму (включая токен, чтобы при переходе не надо было вводить пароль)
        ,'' 'ZOOM ID' -- Только Идентификатор конференции
        ,'' 'ZOOM PWD' -- Пароль для подключения к Зуму по Идентификатору

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

        where CONVERT(date,SC.DURATIONBEGIN_P) BETWEEN '{self.request.get("start_date")}' AND '{self.request.get("end_date")}'

        ORDER BY D.TITLE_P, V.fullFio
        """

        return data
        
        
    
    def write_exam(self):

        data = self.prepare_data()
        data = self.make_query(data)
        data = self.clear_data(data)

        return data
        
        



