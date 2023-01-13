from multiprocessing import reduction
import pandas as pd
from django.http import HttpResponse

class files1C():

    def __init__(self) -> None:
        self.response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.response['Content-Disposition'] = 'attachment; filename=1C_itog.xlsx'

    def Admin(self, df):

        self.df = df.loc[(df['Должность.Категория статистического учета'].isin(['АУП', 'АУПО', ' МОП','ПП', 
        'Руководители','Специалисты','УВП']))]
        
        return self.df

    def Teacher (self,df):

        self.df = df.loc[(df['Должность.Категория статистического учета'].isin(['Научные и научно-педагогические работники', 'НС',
        'ППС','Преподаватели СПО']))]

        return self.df

    def getInfo(self, file, type):

        try:
            self.data = pd.read_excel(file, skiprows=[0,1], header=1)
            self.data = self.data[['Сотрудник.Физическое лицо', 'Должность.Категория статистического учета']]
            self.df = pd.DataFrame(data=self.data)
            self.df = self.df.drop_duplicates(subset=['Сотрудник.Физическое лицо'])
            
            self.df = self.df.sort_values(by=['Сотрудник.Физическое лицо'])
        except: 
            self.response = False
            return self.response

        if type == "Admin":
            self.df = self.Admin(self.df)
        elif type == "Teacher":
            self.df = self.Teacher(self.df)
        elif type == "All":
            pass
        
        self.df.to_excel(self.response,index=False)
       
        return self.response