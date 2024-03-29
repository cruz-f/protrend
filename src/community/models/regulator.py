from django.contrib.auth import get_user_model
from django.db import models

from constants import help_text, choices


User = get_user_model()


class RegulatorCommunity(models.Model):
    # properties
    protrend_id = models.CharField(blank=True, max_length=100, help_text=help_text.protrend_id)
    locus_tag = models.CharField(blank=False, max_length=100, help_text=help_text.locus_tag)
    uniprot_accession = models.CharField(blank=True, max_length=50, help_text=help_text.uniprot_accession)
    name = models.CharField(blank=True, max_length=50, help_text=help_text.gene_name)
    function = models.CharField(blank=True, max_length=250, help_text=help_text.function)
    description = models.TextField(blank=True, help_text=help_text.description)
    mechanism = models.CharField(blank=False, max_length=50, choices=list(choices.mechanism.items()),
                                 help_text=help_text.mechanism)
    ncbi_gene = models.CharField(blank=True, max_length=50, help_text=help_text.ncbi_gene)
    ncbi_protein = models.CharField(blank=True, max_length=50, help_text=help_text.ncbi_protein)
    genbank_accession = models.CharField(blank=True, max_length=50, help_text=help_text.genbank_accession)
    refseq_accession = models.CharField(blank=True, max_length=50, help_text=help_text.refseq_accession)
    gene_sequence = models.TextField(blank=True)
    gene_sequence = models.TextField(blank=True, help_text=help_text.gene_sequence)
    protein_sequence = models.TextField(blank=True, help_text=help_text.protein_sequence)
    strand = models.CharField(blank=True, max_length=50, choices=list(choices.strand.items()),
                              help_text=help_text.strand)
    start = models.IntegerField(blank=True, null=True, help_text=help_text.start)
    stop = models.IntegerField(blank=True, null=True, help_text=help_text.stop)

    # evidences and others
    evidence = models.CharField(blank=True, max_length=250, help_text=help_text.evidence_name)
    pmid = models.IntegerField(blank=True, null=True, help_text=help_text.pmid)

    # connections
    user = models.ForeignKey(User, related_name='regulators', verbose_name='User', on_delete=models.CASCADE)

    def __str__(self):
        return self.locus_tag

    class Meta:
        verbose_name = 'Regulator'
        verbose_name_plural = 'Regulators'
