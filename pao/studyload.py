import pandas as pd
import os
from zipfile import ZipFile
from django.http import HttpResponse
   
df_main_columns = ["Кафедра","Мероприятие реестра, норма времени", "Передано с","Лек", "Пр", "Лаб",
"тек(Консульатции)", "п/экз(Консультации)", "Экз","Зач","РГР", "Реф.", "КТР", "Кв.Э.", 
"Эссе", "Курс.раб", "Практика", "ВКР", "Рук.", "ГЭ"]

df_pps_columns = ["Кафедра","Мероприятие реестра, норма времени", "Передано с",
"Число студентов", "Академ. группа", "Курс", "Семестр",	"Часть учебного года", "НПП", "Лек", "Пр", "Лаб",
"тек(Консульатции)", "п/экз(Консультации)", "Экз","Зач","РГР", "Реф.", "КТР", "Кв.Э.",
"Эссе", "Курс.раб", "Практика", "ВКР", "Рук.", "ГЭ","Всего", "ППС",	"Ученая степень", "Ученое звание",
"Должность", "Ставка", "Итого ДО", "Итого ВО", "Итого ЗО", "На ставку",	"По часам",	"Уровень образования", "Форма обучения"]

class OpenArchive:

     def __init__(self, archive) -> None:
        
        self.archive = ZipFile(archive)

class MakeDf:

    def __init__(self) -> None:
 
        self.df_main = pd.DataFrame(columns=df_main_columns)
        self.df_pps = pd.DataFrame(columns=df_pps_columns)



class StudyLoad(OpenArchive ,MakeDf):

    def __init__(self, archive) -> None:

        super().__init__(archive)
        super(OpenArchive, self).__init__()

          
    def operation(self, file:object, sheet_name:str):

        df_1 = pd.DataFrame(pd.read_excel( self.archive.open(file.filename), sheet_name = sheet_name, decimal=","))
        df_1.columns = df_1.iloc[0]
        df_1 = df_1[1:]
        df_1["Кафедра"] = file.filename.encode('cp437').decode('CP866').replace(".xls", "")
        df_1 = df_1[(df_1["Мероприятие реестра, норма времени"] !='Всего')]
        df_1 = df_1.drop(columns = ["Всего"])

        return df_1
        

    def makePivot(self):
        
        for file in self.archive.infolist():
            
            df_1 = self.operation(file, sheet_name="Сводная")
            self.df_main = pd.concat([self.df_main, df_1], axis = 0)
            
        self.df_main = self.df_main.reindex(columns=["Кафедра","Мероприятие реестра, норма времени", "Передано с","Лек", "Пр", "Лаб",
        "тек(Консульатции)", "п/экз(Консультации)", "Экз","Зач","РГР", "Реф.", "КТР", "Кв.Э.", 
        "Эссе", "Курс.раб", "Практика", "ВКР", "Рук.", "ГЭ"])

        self.df_main = self.df_main.fillna(0)

        self.df_main = self.df_main.reset_index()
        self.df_main = self.df_main.drop(columns = ["index"])
        self.df_main.loc[:,'Всего'] = self.df_main.sum(numeric_only=True, axis=1)
       
        return self.df_main

    def make_pps(self):

        for file in self.archive.infolist():

            df_1 = self.operation(file, sheet_name="По ППС")

            self.df_pps = pd.concat([self.df_pps, df_1], axis = 0)
           
	
        self.df_pps = self.df_pps.fillna(0)
        self.df_pps["Всего"] = self.df_pps["Лек"] + self.df_pps["Пр"] + self.df_pps["Лаб"] + self.df_pps["тек(Консульатции)"] + self.df_pps["п/экз(Консультации)"] + self.df_pps["Экз"] + self.df_pps["Зач"] +  self.df_pps["РГР"] + self.df_pps["Реф."] + self.df_pps["КТР"] + self.df_pps["Кв.Э."] + self.df_pps["Эссе"] + self.df_pps["Курс.раб"] + self.df_pps["Практика"] + self.df_pps["ВКР"] + self.df_pps["Рук."] + self.df_pps["ГЭ"]	
        self.df_pps = self.df_pps.reindex(columns = ["Кафедра","Мероприятие реестра, норма времени", "Передано с",
        "Число студентов", "Академ. группа", "Курс", "Семестр",	"Часть учебного года", "НПП", "Лек", "Пр", "Лаб",
        "тек(Консульатции)", "п/экз(Консультации)", "Экз","Зач","РГР", "Реф.", "КТР", "Кв.Э.",
        "Эссе", "Курс.раб", "Практика", "ВКР", "Рук.", "ГЭ","Всего", "ППС",	"Ученая степень", "Ученое звание",
        "Должность", "Ставка", "Итого ДО", "Итого ВО", "Итого ЗО", "На ставку",	"По часам",	"Уровень образования", "Форма обучения"])
	
        self.df_pps = self.df_pps.reset_index()
        self.df_pps = self.df_pps.drop(columns = ["index"])

        return self.df_pps

    def makeLoad(self):

        try:
            df_pivot = self.makePivot()
            df_pps = self.make_pps()
            response = ResponseXlsx(filename="studyLoadReport", items= [df_pivot, df_pps], sheet_names = ["Сводная", "По ППС"]).verifyCount()
            return response
        except Exception as e:
            pass
    
class ResponseXlsx:

    def __init__(self, filename:str, **kwargs) -> None:

        self.items = kwargs
        self.response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.response['Content-Disposition'] = f"attachment; filename={filename}.xlsx"

    
    def verifyCount(self):

        if len(self.items.get("sheet_names")) == len(self.items.get("items")) and len(self.items.get("items")) > 1:

            self.response = self.makeResponseManySheets()
            return self.response

        else:

            self.response = self.makeResposnseOneSheet()
            return self.response
        
    def makeResponseManySheets(self):
           
        with pd.ExcelWriter(self.response) as writer:

            for index,item in enumerate(self.items["items"]):

                item.to_excel(writer, sheet_name = self.items["sheet_names"][index])
            
        return self.response

    def makeResposnseOneSheet(self):

        self.items["items"].to_excel(self.response, index = False)

        return self.response
                
                
         
