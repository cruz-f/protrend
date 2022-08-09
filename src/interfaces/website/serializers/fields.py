from rest_framework import serializers

from constants import help_text, choices
from interfaces.serializers.fields import NestedField


# ----------------------------------------------------------
# Objects Field
# ----------------------------------------------------------
class OrganismField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(read_only=True, max_length=200, help_text=help_text.organism_name)
    ncbi_taxonomy = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.ncbi_taxonomy)
    species = serializers.CharField(required=False, max_length=150, help_text=help_text.species)
    strain = serializers.CharField(required=False, max_length=150, help_text=help_text.strain)


class EffectorField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(read_only=True, max_length=250, help_text=help_text.effector_name)
    kegg_compounds = serializers.ListField(read_only=True, required=False, child=serializers.CharField(required=False),
                                           help_text=help_text.kegg_compounds)


class PathwayField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(read_only=True, max_length=250, help_text=help_text.pathway_name)
    kegg_pathways = serializers.ListField(required=False, child=serializers.CharField(required=False),
                                          help_text=help_text.kegg_pathways)


class RegulatorField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    locus_tag = serializers.CharField(read_only=True, max_length=50, help_text=help_text.locus_tag)
    name = serializers.CharField(read_only=True, max_length=50, help_text=help_text.gene_name)
    uniprot_accession = serializers.CharField(read_only=True, max_length=50, help_text=help_text.uniprot_accession)
    ncbi_gene = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_gene)
    mechanism = serializers.ChoiceField(required=False, choices=choices.mechanism,
                                        help_text=help_text.mechanism)


class GeneField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    locus_tag = serializers.CharField(read_only=True, max_length=50, help_text=help_text.locus_tag)
    name = serializers.CharField(read_only=True, max_length=50, help_text=help_text.gene_name)
    uniprot_accession = serializers.CharField(read_only=True, max_length=50, help_text=help_text.uniprot_accession)
    ncbi_gene = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_gene)


class TFBSField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    sequence = serializers.CharField(read_only=True, help_text=help_text.tfbs_sequence)
    start = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.stop)
    strand = serializers.ChoiceField(read_only=True, choices=choices.strand, help_text=help_text.strand)


class RegulatoryInteractionField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    organism = serializers.CharField(required=True, max_length=100, help_text=help_text.organism_id)
    regulator = serializers.CharField(required=True, max_length=100, help_text=help_text.regulator_id)
    gene = serializers.CharField(required=True, max_length=100, help_text=help_text.gene_id)
    tfbs = serializers.CharField(required=False, max_length=100, help_text=help_text.tfbs_id)
    effector = serializers.CharField(required=False, max_length=100, help_text=help_text.effector_id)
    regulatory_effect = serializers.ChoiceField(required=True, choices=choices.regulatory_effect,
                                                help_text=help_text.regulatory_effect)


class RegulatoryFamilyField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(read_only=True, max_length=250, help_text=help_text.rfam_name)
    mechanism = serializers.ChoiceField(required=False,
                                        choices=choices.mechanism,
                                        help_text=help_text.mechanism)
    rfam = serializers.CharField(required=False, max_length=100, help_text=help_text.rfam)
    description = serializers.CharField(required=False, help_text=help_text.rfam_description)


class EvidenceField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(read_only=True, max_length=250, help_text=help_text.evidence_name)
    description = serializers.CharField(read_only=True, help_text=help_text.evidence_description)


class PublicationField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    pmid = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.pmid)
    doi = serializers.CharField(required=False, max_length=250, help_text=help_text.doi)
    title = serializers.CharField(required=False, max_length=500, help_text=help_text.title)
    author = serializers.CharField(required=False, max_length=250, help_text=help_text.author)
    year = serializers.IntegerField(required=False, min_value=0, help_text=help_text.year)


class OperonField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    operon_db_id = serializers.CharField(required=True, max_length=50, help_text=help_text.operon_db_id)
    name = serializers.CharField(required=False, max_length=50, help_text=help_text.operon_name)
    function = serializers.CharField(read_only=True, help_text=help_text.operon_function)
    genes = serializers.ListField(read_only=True,
                                  child=serializers.CharField(required=False),
                                  help_text=help_text.operon_genes)
    strand = serializers.ChoiceField(required=False, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, help_text=help_text.stop)


class MotifField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    regulator = serializers.CharField(read_only=True, help_text=help_text.regulator_id)
    consensus_sequence = serializers.CharField(read_only=True, help_text=help_text.consensus_sequence)
    sequences = serializers.ListField(read_only=True,
                                      child=serializers.CharField(required=False),
                                      help_text=help_text.aligned_sequence)
