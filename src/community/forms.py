from django import forms
from django.forms import ModelForm

from . import models


class RegulatorForm(ModelForm):
    user = forms.CharField(disabled=True)

    class Meta:
        model = models.RegulatorCommunity
        fields = '__all__'


class GeneForm(ModelForm):
    user = forms.CharField(disabled=True)

    class Meta:
        model = models.GeneCommunity
        fields = '__all__'
