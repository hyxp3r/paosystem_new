from django import forms
from .models import Concat
from django.core.validators import FileExtensionValidator


class ConcatForm(forms.ModelForm):

    class Meta:

        model = Concat
        fields = "__all__"


CHOICES = [('Admin','АУП'), ('Teacher','ППС'),('All','Все')]

class Proccess1CFileForm(forms.Form):
    
    types = forms.ChoiceField(widget=forms.RadioSelect(attrs = {"class":"form-check-input",
     "type":"radio", "name":"flexRadioDefault"}), choices = CHOICES, )
    file = forms.FileField(widget=forms.FileInput(attrs = {"class":"form-control", "type":"file", 
    "id":"formFile", "onchange":"deleteWarning()", 'accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel'}),
    validators=[FileExtensionValidator(allowed_extensions=["xlsx"])])