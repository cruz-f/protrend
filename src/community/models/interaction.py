from django.contrib.auth import get_user_model
from django.db import models

from constants import help_text, choices


User = get_user_model()


class InteractionCommunity(models.Model):
    # properties
    protrend_id = models.CharField(blank=True, null=True, max_length=100, help_text=help_text.protrend_id)
    regulatory_effect = models.CharField(blank=False, max_length=50, choices=list(choices.regulatory_effect.items()),
                                         help_text=help_text.regulatory_effect)

    # evidences and others
    evidence = models.CharField(blank=True, null=True, max_length=250, help_text=help_text.required_name)
    pmid = models.IntegerField(blank=True, null=True, help_text=help_text.pmid)

    # connections
    user = models.ForeignKey(User, related_name='interactions', verbose_name='User', on_delete=models.CASCADE)
    organism = models.ForeignKey('community.OrganismCommunity', related_name='interactions', verbose_name='Organism',
                                 on_delete=models.CASCADE)
    regulator = models.ForeignKey('community.RegulatorCommunity', related_name='interactions', verbose_name='Regulator',
                                  on_delete=models.CASCADE)
    gene = models.ForeignKey('community.GeneCommunity', related_name='interactions', verbose_name='Gene',
                             on_delete=models.CASCADE)
    tfbs = models.ForeignKey('community.TFBSCommunity', related_name='interactions', verbose_name='TFBS',
                             on_delete=models.CASCADE, blank=True, null=True)
    effector = models.ForeignKey('community.EffectorCommunity', related_name='interactions', verbose_name='Effector',
                                 on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.regulatory_effect

    class Meta:
        verbose_name = 'Interaction'
        verbose_name_plural = 'Interactions'
