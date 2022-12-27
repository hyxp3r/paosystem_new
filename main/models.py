from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
 
class User(AbstractUser):
    department = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Отдел")
    post = models.CharField(max_length = 50, blank = True, null = True, verbose_name = "Должность")
    dateBith = models.DateField(default = timezone.now, verbose_name = "Дата рождения")

    def getAge (self):

        today = date.today()
        age = today.year - self.dateBith.year - ((today.month, today.day) < ( self.dateBith.month,  self.dateBith.day))
        return age
