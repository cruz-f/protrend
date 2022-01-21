from rest_framework import serializers

# stands for protrend api
import domain.database as papi
from constants import help_text, choices


# --------------------------------------
# Base Serializer
# --------------------------------------
class BaseSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    created = serializers.DateTimeField(read_only=True, help_text=help_text.created)
    updated = serializers.DateTimeField(required=False, help_text=help_text.updated)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


# --------------------------------------
# MixIn Serializers
# --------------------------------------
class NameMixInSerializer(serializers.Serializer):
    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class SequenceMixInSerializer(serializers.Serializer):
    # properties
    sequence = serializers.CharField(required=False, help_text=help_text.sequence)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PositionMixInSerializer(serializers.Serializer):
    # properties
    strand = serializers.ChoiceField(required=False, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(required=False, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, help_text=help_text.stop)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class GeneMixInSerializer(serializers.Serializer):
    # properties
    locus_tag = serializers.CharField(required=True, max_length=50, help_text=help_text.locus_tag)
    uniprot_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.uniprot_accession)
    name = serializers.CharField(required=False, max_length=50, help_text=help_text.gene_name)
    synonyms = serializers.ListField(required=False, child=serializers.CharField(required=False),
                                     help_text=help_text.synonyms)
    function = serializers.CharField(required=False, help_text=help_text.function)
    description = serializers.CharField(required=False, help_text=help_text.description)
    ncbi_gene = serializers.IntegerField(required=False, help_text=help_text.ncbi_gene)
    ncbi_protein = serializers.IntegerField(required=False, help_text=help_text.ncbi_protein)
    genbank_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.genbank_accession)
    refseq_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.refseq_accession)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


# --------------------------------------
# Concrete Serializers
# --------------------------------------
class EffectorSerializer(BaseSerializer, NameMixInSerializer):
    # properties
    kegg_compounds = serializers.ListField(child=serializers.CharField(required=False),
                                           required=False,
                                           help_text=help_text.kegg_compounds)

    # # relationships
    # data_source = RelationshipTo('.source.Source', BASE_REL_TYPE, model=SourceRelationship)
    # regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    # regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
    #                                         model=BaseRelationship)

    def create(self, validated_data):
        return papi.create_effector(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_effector(instance, **validated_data)


class EvidenceSerializer(BaseSerializer, NameMixInSerializer):
    # properties
    description = serializers.CharField(required=False, help_text=help_text.generic_description)

    # # relationships
    # regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    # operon = RelationshipTo('.operon.Operon', BASE_REL_TYPE, model=BaseRelationship)
    # gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)
    # tfbs = RelationshipTo('.tfbs.TFBS', BASE_REL_TYPE, model=BaseRelationship)
    # regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
    #                                         model=BaseRelationship)

    def create(self, validated_data):
        return papi.create_evidence(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_evidence(instance, **validated_data)


class GeneSerializer(BaseSerializer, GeneMixInSerializer, SequenceMixInSerializer, PositionMixInSerializer):
    # properties inherited from GeneMixInSerializer, SequenceMixInSerializer, PositionMixInSerializer

    # # relationships
    # data_source = RelationshipTo('.source.Source', BASE_REL_TYPE, model=SourceRelationship)
    # evidence = RelationshipTo('.evidence.Evidence', BASE_REL_TYPE, model=BaseRelationship)
    # publication = RelationshipTo('.publication.Publication', BASE_REL_TYPE, model=BaseRelationship)
    # pathway = RelationshipTo('.pathway.Pathway', BASE_REL_TYPE, model=BaseRelationship)
    # operon = RelationshipTo('.operon.Operon', BASE_REL_TYPE, model=BaseRelationship)
    # organism = RelationshipTo('.organism.Organism', BASE_REL_TYPE, cardinality=ZeroOrOne, model=BaseRelationship)
    # regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    # tfbs = RelationshipTo('.tfbs.TFBS', BASE_REL_TYPE, model=BaseRelationship)
    # regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
    #                                         model=BaseRelationship)

    def create(self, validated_data):
        return papi.create_gene(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_gene(instance, **validated_data)


class OperonSerializer(BaseSerializer, PositionMixInSerializer):
    # properties inherited from PositionMixInSerializer

    # properties
    operon_db_id = serializers.CharField(required=True, max_length=50, help_text=help_text.operon_db_id)
    name = serializers.CharField(required=False, max_length=50, help_text=help_text.operon_name)
    function = serializers.CharField(required=False, max_length=250, help_text=help_text.operon_function)
    genes = serializers.ListField(required=True, child=serializers.CharField(required=True),
                                  help_text=help_text.operon_genes)

    # # relationships
    # data_source = RelationshipTo('.source.Source', BASE_REL_TYPE, cardinality=One, model=SourceRelationship)
    # evidence = RelationshipTo('.evidence.Evidence', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    # publication = RelationshipTo('.publication.Publication', BASE_REL_TYPE, model=BaseRelationship)
    # organism = RelationshipTo('.organism.Organism', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    # gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)

    def create(self, validated_data):
        return papi.create_operon(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_operon(instance, **validated_data)


class OrganismSerializer(BaseSerializer):
    # properties
    name = serializers.CharField(required=True, max_length=200, help_text=help_text.organism_name)
    ncbi_taxonomy = serializers.IntegerField(required=False, help_text=help_text.ncbi_taxonomy)
    species = serializers.CharField(required=False, max_length=150, help_text=help_text.species)
    strain = serializers.CharField(required=False, max_length=150, help_text=help_text.strain)
    refseq_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.refseq_accession)
    refseq_ftp = serializers.CharField(required=False, max_length=250, help_text=help_text.refseq_ftp)
    genbank_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.genbank_accession)
    genbank_ftp = serializers.CharField(required=False, max_length=250, help_text=help_text.genbank_ftp)
    ncbi_assembly = serializers.IntegerField(required=False, help_text=help_text.ncbi_assembly)
    assembly_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.assembly_accession)

    # # relationships
    # data_source = RelationshipTo('.source.Source', BASE_REL_TYPE, model=SourceRelationship)
    # operon = RelationshipTo('.operon.Operon', BASE_REL_TYPE, model=BaseRelationship)
    # regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    # gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)
    # tfbs = RelationshipTo('.tfbs.TFBS', BASE_REL_TYPE, model=BaseRelationship)
    # regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
    #                                         model=BaseRelationship)
    def create(self, validated_data):
        return papi.create_organism(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_organism(instance, **validated_data)


class PathwaySerializer(BaseSerializer, NameMixInSerializer):
    # properties
    kegg_pathways = serializers.ListField(required=False, child=serializers.CharField(required=False), allow_empty=True,
                                          help_text=help_text.kegg_pathways)

    # # relationships
    # data_source = RelationshipTo('.source.Source', BASE_REL_TYPE, model=SourceRelationship)
    # regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    # gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)
    def create(self, validated_data):
        return papi.create_pathway(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_pathway(instance, **validated_data)


class Publication(BaseSerializer):
    # properties
    pmid = serializers.IntegerField(required=True, help_text=help_text.pmid)
    doi = serializers.CharField(required=False, max_length=250, help_text=help_text.doi)
    title = serializers.CharField(required=False, max_length=500, help_text=help_text.title)
    author = serializers.CharField(required=False, max_length=250, help_text=help_text.author)
    year = serializers.IntegerField(required=False, help_text=help_text.year)

    # # relationships
    # regulatory_family = RelationshipTo('.regulatory_family.RegulatoryFamily', BASE_REL_TYPE, model=BaseRelationship)
    # regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    # operon = RelationshipTo('.operon.Operon', BASE_REL_TYPE, model=BaseRelationship)
    # gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)
    # tfbs = RelationshipTo('.tfbs.TFBS', BASE_REL_TYPE, model=BaseRelationship)
    # regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
    #                                         model=BaseRelationship)
    def create(self, validated_data):
        return papi.create_publication(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_publication(instance, **validated_data)


class RegulatorSerializer(BaseSerializer, GeneMixInSerializer, SequenceMixInSerializer, PositionMixInSerializer):
    # properties
    mechanism = serializers.ChoiceField(required=False, choices=choices.mechanism,
                                        help_text=help_text.mechanism)

    # properties inherited from GeneMixInSerializer, SequenceMixInSerializer, PositionMixInSerializer

    # # relationships
    # data_source = RelationshipTo('.source.Source', BASE_REL_TYPE, model=SourceRelationship)
    # evidence = RelationshipTo('.evidence.Evidence', BASE_REL_TYPE, model=BaseRelationship)
    # publication = RelationshipTo('.publication.Publication', BASE_REL_TYPE, model=BaseRelationship)
    # pathway = RelationshipTo('.pathway.Pathway', BASE_REL_TYPE, model=BaseRelationship)
    # effector = RelationshipTo('.effector.Effector', BASE_REL_TYPE, model=BaseRelationship)
    # regulatory_family = RelationshipTo('.regulatory_family.RegulatoryFamily', BASE_REL_TYPE, cardinality=ZeroOrOne,
    #                                    model=BaseRelationship)
    # organism = RelationshipTo('.organism.Organism', BASE_REL_TYPE, cardinality=ZeroOrOne, model=BaseRelationship)
    # gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)
    # tfbs = RelationshipTo('.tfbs.TFBS', BASE_REL_TYPE, model=BaseRelationship)
    # regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
    #                                         model=BaseRelationship)
    def create(self, validated_data):
        return papi.create_regulator(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_regulator(instance, **validated_data)


class RegulatoryFamilySerializer(BaseSerializer, NameMixInSerializer):
    # properties
    mechanism = serializers.ChoiceField(required=False, choices=choices.mechanism,
                                        help_text=help_text.mechanism)
    rfam = serializers.CharField(max_length=100, help_text=help_text.rfam)
    description = serializers.CharField(help_text=help_text.generic_description)

    # # relationships
    # data_source = RelationshipTo('.source.Source', BASE_REL_TYPE, model=SourceRelationship)
    # publication = RelationshipTo('.publication.Publication', BASE_REL_TYPE, model=BaseRelationship)
    # regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    def create(self, validated_data):
        return papi.create_rfam(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_rfam(instance, **validated_data)


class RegulatoryInteraction(BaseSerializer):
    # properties
    regulatory_interaction_hash = serializers.CharField(read_only=True, max_length=600)
    organism = serializers.CharField(required=True, max_length=100, help_text=help_text.organism_id)
    regulator = serializers.CharField(required=True, max_length=100, help_text=help_text.regulator_id)
    gene = serializers.CharField(required=True, max_length=100, help_text=help_text.gene_id)
    tfbs = serializers.CharField(required=False, max_length=100, help_text=help_text.tfbs_id)
    effector = serializers.CharField(required=False, max_length=100, help_text=help_text.effector_id)
    regulatory_effect = serializers.ChoiceField(required=True, choices=choices.regulatory_effect,
                                                help_text=help_text.regulatory_effect)

    # # relationships
    # data_source = RelationshipTo('.source.Source', BASE_REL_TYPE, model=SourceRelationship)
    # evidence = RelationshipTo('.evidence.Evidence', BASE_REL_TYPE, model=BaseRelationship)
    # publication = RelationshipTo('.publication.Publication', BASE_REL_TYPE, model=BaseRelationship)
    # data_effector = RelationshipTo('.effector.Effector', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    # data_organism = RelationshipTo('.organism.Organism', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    # data_regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    # data_gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    # data_tfbs = RelationshipTo('.tfbs.TFBS', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    def create(self, validated_data):
        return papi.create_interaction(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_interaction(instance, **validated_data)


class TFBSSerializer(BaseSerializer, SequenceMixInSerializer, PositionMixInSerializer):
    # properties
    site_hash = serializers.CharField(read_only=True, max_length=600)
    organism = serializers.CharField(required=True, max_length=100, help_text=help_text.organism_id)
    length = serializers.IntegerField(required=True, help_text=help_text.length)

    # # relationships
    # data_source = RelationshipTo('.source.Source', BASE_REL_TYPE, model=SourceRelationship)
    # evidence = RelationshipTo('.evidence.Evidence', BASE_REL_TYPE, model=BaseRelationship)
    # publication = RelationshipTo('.publication.Publication', BASE_REL_TYPE, model=BaseRelationship)
    # data_organism = RelationshipTo('.organism.Organism', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    # regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    # gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)
    # regulatory_interaction = RelationshipTo('.regulatory_interaction.RegulatoryInteraction', BASE_REL_TYPE,
    #                                         model=BaseRelationship)
    def create(self, validated_data):
        return papi.update_biding_site(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_biding_site(instance, **validated_data)
