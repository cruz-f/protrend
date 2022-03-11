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


class EffectorField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(read_only=True, max_length=250, help_text=help_text.required_name)


class RegulatorField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    locus_tag = serializers.CharField(read_only=True, max_length=50, help_text=help_text.locus_tag)
    uniprot_accession = serializers.CharField(read_only=True, max_length=50, help_text=help_text.uniprot_accession)
    name = serializers.CharField(read_only=True, max_length=50, help_text=help_text.gene_name)
    mechanism = serializers.ChoiceField(read_only=True, choices=choices.mechanism,
                                        help_text=help_text.mechanism)


class GeneField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    locus_tag = serializers.CharField(read_only=True, max_length=50, help_text=help_text.locus_tag)
    uniprot_accession = serializers.CharField(read_only=True, max_length=50, help_text=help_text.uniprot_accession)
    name = serializers.CharField(read_only=True, max_length=50, help_text=help_text.gene_name)


class TFBSField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    sequence = serializers.CharField(read_only=True, help_text=help_text.tfbs_sequence)
    strand = serializers.ChoiceField(read_only=True, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.stop)


class RegulatoryInteractionField(NestedField):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    regulator = serializers.CharField(required=True, max_length=100, help_text=help_text.regulator_id)
    gene = serializers.CharField(required=True, max_length=100, help_text=help_text.gene_id)
    tfbs = serializers.CharField(required=False, max_length=100, help_text=help_text.tfbs_id)
    effector = serializers.CharField(required=False, max_length=100, help_text=help_text.effector_id)
    regulatory_effect = serializers.ChoiceField(required=True, choices=choices.regulatory_effect,
                                                help_text=help_text.regulatory_effect)
