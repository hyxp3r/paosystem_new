from django.db import models


# Create your models here.
class Post(models.Model):

    name = models.CharField(max_length = 100, verbose_name = "Наименование должности")

    class Meta:

        verbose_name = 'Должность'
        verbose_name_plural = 'Должность'
        ordering = ('name',)

    def __str__(self) -> str:

        return (self.name)

class Department(models.Model):

    name = models.CharField(max_length = 100, verbose_name = "Название")
    shortName = models.CharField(max_length=50, null=True, blank=True, verbose_name= "Сокращенное название")

    class Meta:

        verbose_name = 'Отдел'
        verbose_name_plural = 'Отдел'
        ordering = ('name',)
    def __str__(self) -> str:

        return (self.name)

class Expert(models.Model):

    fioExpert = models.CharField(max_length=50, verbose_name = "ФИО эксперта")
    department = models.ForeignKey(Department,  null=True, blank=True, verbose_name = "Название отдела", on_delete=models.SET_NULL)


    class Meta:

        verbose_name = 'Эксперт'
        verbose_name_plural = 'Эксперт'

    def __str__(self) -> str:
        return (self.fioExpert)

    def calculateShortFio(self):

        short_fio = self.fioExpert.split(' ')
        short_fio = f'{short_fio[0]} {short_fio[1][0:1]}.{short_fio[2][0:1]}.'
        return short_fio



class ContractNames(models.Model):

    sectionEC = models.CharField(max_length=10, verbose_name = "Номер пункта")
    descriptionEC  = models.TextField(verbose_name = "Описание")
    url = models.URLField(verbose_name="Ссылка", null = True, blank=True)
    expertEC = models.ForeignKey(Expert, null=True, blank=True, verbose_name = "Эксперт", on_delete= models.SET_NULL)

    class Meta:

        verbose_name = 'Разделы ЭК'
        verbose_name_plural = 'Разделы ЭК'
    
    def __str__(self) -> str:
        return (self.sectionEC)


class CheckEc(models.Model):

    createdTime = models.DateTimeField(auto_now_add=True)
    declared = models.IntegerField(verbose_name = 'Заявлено')
    verified = models.IntegerField(verbose_name = 'Проверено')
    contractName = models.ForeignKey(ContractNames, verbose_name="Номер пункта", on_delete = models.CASCADE)

    class Meta:

        verbose_name = 'Ход ЭК'
        verbose_name_plural = 'Ход ЭК'

    def __str__(self) -> str:
        return (self.contractName.sectionEC)

    def calculateProgress(self):

        percent = 0 if self.declared == 0 else round(self.verified/self.declared*100)
        
        return percent

class Concat(models.Model):

    name = models.CharField(max_length=50, verbose_name="Имя", blank=False, null=False)
    email = models.EmailField(max_length=50)

    class Meta:

        verbose_name = "Контанкт"
        verbose_name_plural = "Контакт"

class Appeals(models.Model):

    count = models.IntegerField(verbose_name="Аппеляции")

    class Meta:

        verbose_name = "Аппеляции"
        verbose_name_plural = "Аппеляции"

