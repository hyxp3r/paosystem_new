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


#Google sheets creds
class Google(models.Model):

    user = models.ManyToManyField(User, verbose_name = "Пользователи" , related_name = "key_users_google")
    json = models.JSONField("Ключ", null=True, blank=True)

    
    class Meta:

        verbose_name = "Ключи Google"
        verbose_name_plural = "Ключи Google"

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
    
class AirtablePersonal(models.Model):

    user = models.ManyToManyField(User, verbose_name = "Пользователи" , related_name = "key_users_air")
    key = models.CharField("API ключ", max_length = 155, null = True, blank = True)



    class Meta:

        verbose_name = "Ключи Air"
        verbose_name_plural = "Ключи Air"


class Query(models.Model):

    name = models.CharField("Наименование запроса", max_length = 150)
    body  = models.TextField("Запрос")
    comment = models.TextField("Комментарий к запросу", null = True, blank = True)

    def __str__(self) -> str:
        return self.name


    class Meta:

        verbose_name = "Запросы"
        verbose_name_plural = "Запросы"

class GoogleMonitoring(models.Model):

    name = models.CharField("Наименование листа", max_length=150)
    id_sheet = models.CharField("ID листа", max_length=150)
    query = models.ForeignKey(Query, on_delete = models.CASCADE, verbose_name = "Запрос на формирование" )
    comment = models.TextField("Комментарий к отчету", max_length = 200, null = True, blank = True)
    status = models.BooleanField("Запущено?", default=True)

    def __str__(self) -> str:
        return self.name


    class Meta:

        verbose_name = "Мониторинг"
        verbose_name_plural = "Мониторинг"

class GoogleMonitoringFiles(models.Model):

    name = models.CharField("Наименование", max_length = 150)
    spreadsheet_id = models.CharField("ID документа", max_length=255)
    monitoring = models.ManyToManyField(GoogleMonitoring, verbose_name = "Мониторинг" , related_name = "monitoring_files")

    def __str__(self) -> str:
        return self.name


    class Meta:

        verbose_name = "Мониторинг файл"
        verbose_name_plural = "Мониторинг файл"

class AirtableBases(models.Model):

    name = models.CharField("Наименование", max_length = 150)
    base_id = models.CharField("ID базы", max_length = 150)


    def __str__(self) -> str:
        return self.name


    class Meta:

        verbose_name = "Базы Airtable"
        verbose_name_plural = "Базы Airtable"

class AirtableTables(models.Model):

    name = models.CharField("Наименование", max_length = 150)
    table_id = models.CharField("ID таблицы", max_length = 150, blank = True, null = True)
    comment = models.TextField("Комментарий к таблице", max_length = 200, null = True, blank = True)
    base = models.ForeignKey(AirtableBases, verbose_name = "База Airtable", on_delete  = models.CASCADE)
    query = models.ForeignKey(Query, verbose_name="Запрос", on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.name


    class Meta:

        verbose_name = "Таблицы Airtable"
        verbose_name_plural = "Таблицы Airtable"

class LogsCron(models.Model):

    created_at = models.DateTimeField(verbose_name="Дата завершения выполнения", auto_now_add=True)
    name = models.CharField("Наименование задачи", max_length=155)
    status = models.CharField("Статус", max_length=155)

    def __str__(self) -> str:
        return self.name


    class Meta:

        verbose_name = "Логирование CRON"
        verbose_name_plural = "Логирование CRON"