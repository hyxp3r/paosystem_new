from django import forms
from .models import Concat


class ConcatForm(forms.ModelForm):

    class Meta:

        model = Concat
        fields = "__all__"