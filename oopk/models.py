from django.db import models
from main.models import User

# Create your models here.

#Уровень образования
class EduLevelProgram(models.Model):

    name = models.CharField("Наименование", max_length = 50)
    tandem_name = models.CharField("Наименование в Tandem", max_length = 50)

    def __str__(self) -> str:
        return self.name

    class Meta:

        verbose_name = "Уровень подготовки направления"
        verbose_name_plural = "Уровень подготовки направления"

#Направление подготовки
class Program(models.Model):

    code = models.CharField("Код" ,max_length= 8)
    name = models.CharField("Наименование", max_length=100)
    eduLevel = models.ForeignKey(EduLevelProgram, verbose_name = "Уровень образования", on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.code + " " + self.name

    class Meta:
        
        verbose_name = "Направление подготовки"
        verbose_name_plural = "Направления подготовки"

    def makeProgram(self):

        program = self.code + " " + self.name

        return program
    

#Вид приема
class PriemType(models.Model):

    name = models.CharField("Наименование", max_length=100)


    def __str__(self) -> str:
        return self.name

    class Meta:
        
        verbose_name = "Вид приема"
        verbose_name_plural = "Вид приема"


#Форма
class DevelopeForm(models.Model):

    name = models.CharField("Наименование", max_length=100)
    sort = models.SmallIntegerField("Индекс для сортировки")


    def __str__(self) -> str:
        return self.name

    class Meta:
        
        verbose_name = "Форма"
        verbose_name_plural = "Форма"

#Статус
class Status(models.Model):

    name = models.CharField("Наименование", max_length=100)


    def __str__(self) -> str:
        return self.name

    class Meta:
        
        verbose_name = "Статус"
        verbose_name_plural = "Статус"


class GoogleReport(models.Model):

    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = "Пользователь")
    url = models.URLField("Ссылка на отчет", null = True, blank = True)
    spreadsheet_id = models.CharField("ID документа", max_length= 155 ,null=True, blank=True)
    name = models.CharField("Наименование отчета", max_length = 50, null = False, blank = True )
    comment = models.TextField("Комментарий к отчету", max_length = 200, null = True, blank = True)

    def __str__(self) -> str:
        return self.name
    

    class Meta:

        verbose_name = "Отчеты Google"
        verbose_name_plural = "Отчеты Google"
    
