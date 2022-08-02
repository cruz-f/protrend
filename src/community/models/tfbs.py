from django.contrib.auth import get_user_model
from django.db import models

from constants import help_text, choices

User = get_user_model()


class TFBSCommunity(models.Model):
    # properties
    protrend_id = models.CharField(blank=True, max_length=100, help_text=help_text.protrend_id)
    sequence = models.TextField(blank=False, help_text=help_text.tfbs_sequence)
    strand = models.CharField(blank=True, max_length=50, choices=list(choices.strand.items()),
                              help_text=help_text.strand)
    start = models.IntegerField(blank=True, null=True, help_text=help_text.start)
    stop = models.IntegerField(blank=True, null=True, help_text=help_text.stop)

    # evidences and others
    evidence = models.CharField(blank=True, max_length=250, help_text=help_text.evidence_name)
    pmid = models.IntegerField(blank=True, null=True, help_text=help_text.pmid)

    # connections
    user = models.ForeignKey(User, related_name='tfbss', verbose_name='User', on_delete=models.CASCADE)

    def __str__(self):
        return self.sequence

    class Meta:
        verbose_name = 'TFBS'
        verbose_name_plural = 'TFBSs'
