from django.contrib.auth import get_user_model
from django.db import models

from constants import help_text


User = get_user_model()


class OrganismCommunity(models.Model):
    # properties
    protrend_id = models.CharField(blank=True, max_length=100, help_text=help_text.protrend_id)
    name = models.CharField(blank=False, max_length=250, help_text=help_text.organism_name)

    ncbi_taxonomy = models.IntegerField(blank=False, help_text=help_text.ncbi_taxonomy)
    species = models.CharField(blank=True, max_length=150, help_text=help_text.species)
    strain = models.CharField(blank=True, max_length=150, help_text=help_text.strain)
    refseq_accession = models.CharField(blank=True, max_length=50, help_text=help_text.refseq_accession)
    genbank_accession = models.CharField(blank=True, max_length=50, help_text=help_text.genbank_accession)
    ncbi_assembly = models.IntegerField(blank=True, null=True, help_text=help_text.ncbi_assembly)
    assembly_accession = models.CharField(blank=True, max_length=50, help_text=help_text.assembly_accession)

    # connections
    user = models.ForeignKey(User, related_name='organisms', verbose_name='User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Organism'
        verbose_name_plural = 'Organisms'
