from django.contrib.auth import get_user_model
from django.db import models

from constants import help_text


User = get_user_model()


class EffectorCommunity(models.Model):
    # properties
    protrend_id = models.CharField(blank=True, max_length=100, help_text=help_text.protrend_id)
    name = models.CharField(blank=False, max_length=250, help_text=help_text.required_name)
    kegg_compounds = models.CharField(blank=True, max_length=50, help_text=help_text.kegg_compounds)

    # evidences and others
    evidence = models.CharField(blank=True, max_length=250, help_text=help_text.required_name)
    pmid = models.IntegerField(blank=True, help_text=help_text.pmid)

    # connections
    user = models.ForeignKey(User, related_name='effectors', verbose_name='User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Effector'
        verbose_name_plural = 'Effectors'
