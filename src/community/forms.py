from django.forms import ModelForm

from . import models


class EffectorForm(ModelForm):

    class Meta:
        model = models.EffectorCommunity
        fields = '__all__'
        exclude = ('user', )


class GeneForm(ModelForm):

    class Meta:
        model = models.GeneCommunity
        fields = '__all__'
        exclude = ('user', )


class InteractionForm(ModelForm):

    class Meta:
        model = models.InteractionCommunity
        fields = '__all__'
        exclude = ('user', )


class OrganismForm(ModelForm):

    class Meta:
        model = models.OrganismCommunity
        fields = '__all__'
        exclude = ('user', )


class RegulatorForm(ModelForm):

    class Meta:
        model = models.RegulatorCommunity
        fields = '__all__'
        exclude = ('user', )


class TFBSForm(ModelForm):

    class Meta:
        model = models.TFBSCommunity
        fields = '__all__'
        exclude = ('user', )
