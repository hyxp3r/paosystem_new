from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from pao import models as paopodels
 
class User(AbstractUser):
    department = models.ForeignKey(paopodels.Department, null = True, blank = True, verbose_name = "Отдел", on_delete=models.SET_NULL)
    post = models.ForeignKey(paopodels.Post, null = True, blank = True, verbose_name = "Должность", on_delete=models.SET_NULL)
    dateBith = models.DateField(default = timezone.now, verbose_name = "Дата рождения")

    def getAge (self):

        today = date.today()
        age = today.year - self.dateBith.year - ((today.month, today.day) < ( self.dateBith.month,  self.dateBith.day))
        return age
