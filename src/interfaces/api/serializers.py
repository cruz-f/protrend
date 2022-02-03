from rest_framework import serializers, status

# stands for protrend api
import domain.database as papi
import domain.model_api as mapi
from constants import help_text, choices
from exceptions import ProtrendException
from interfaces.api.validation import validate_dna_sequence, validate_protein_sequence


# --------------------------------------
# Base Serializer
# --------------------------------------
class BaseSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    created = serializers.DateTimeField(read_only=True, help_text=help_text.created)
    updated = serializers.DateTimeField(read_only=True, help_text=help_text.updated)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


# --------------------------------------
# Nested Object Serializers
# --------------------------------------
class ManyRelatedSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_attribute(self, instance):
        return mapi.get_related_objects(instance, self.field_name)


class SourceListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_attribute(self, instance):
        sources = mapi.get_related_objects(instance, 'data_source')
        relationships = []
        for source in sources:
            source_relationships = mapi.get_relationships(source_obj=instance, target='data_source', target_obj=source)
            for source_rel in source_relationships:
                source_rel.name = source.name
                relationships.append(source_rel)
        return relationships


class SourceHighlightSerializer(serializers.Serializer):
    # properties
    name = serializers.CharField(read_only=True, max_length=100, help_text=help_text.required_name)
    url = serializers.CharField(read_only=True, help_text=help_text.url)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class OrganismHighlightSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(read_only=True, max_length=200, help_text=help_text.organism_name)
    ncbi_taxonomy = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.ncbi_taxonomy)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_attribute(self, instance):
        organism = papi.get_organism_by_id(instance.organism)
        if organism is None:
            raise ProtrendException(detail=f'Organism with protrend id {instance.organism} not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)

        return organism


class RegulatorHighlightSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    locus_tag = serializers.CharField(read_only=True, max_length=50, help_text=help_text.locus_tag)
    uniprot_accession = serializers.CharField(read_only=True, max_length=50, help_text=help_text.uniprot_accession)
    name = serializers.CharField(read_only=True, max_length=50, help_text=help_text.gene_name)
    mechanism = serializers.ChoiceField(read_only=True, choices=choices.mechanism,
                                        help_text=help_text.mechanism)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_attribute(self, instance):
        regulator = papi.get_regulator_by_id(instance.regulator)
        if regulator is None:
            raise ProtrendException(detail=f'Regulator with protrend id {instance.regulator} not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)

        return regulator


class GeneListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_attribute(self, instance):
        genes = []
        for gene_id in instance.genes:

            gene = papi.get_gene_by_id(gene_id)
            if gene is None:
                raise ProtrendException(detail=f'Gene with protrend id {gene_id} not found',
                                        code='get error',
                                        status=status.HTTP_404_NOT_FOUND)

            genes.append(gene)

        return genes


class GeneHighlightSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    locus_tag = serializers.CharField(read_only=True, max_length=50, help_text=help_text.locus_tag)
    uniprot_accession = serializers.CharField(read_only=True, max_length=50, help_text=help_text.uniprot_accession)
    name = serializers.CharField(read_only=True, max_length=50, help_text=help_text.gene_name)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_attribute(self, instance):
        gene = papi.get_gene_by_id(instance.gene)
        if gene is None:
            raise ProtrendException(detail=f'Gene with protrend id {instance.gene} not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)

        return gene


class TFBSHighlightSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    sequence = serializers.CharField(read_only=True, help_text=help_text.tfbs_sequence)
    strand = serializers.ChoiceField(read_only=True, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(read_only=True, min_value=0, help_text=help_text.stop)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_attribute(self, instance):
        tfbs = papi.get_binding_site_by_id(instance.tfbs)
        if tfbs is None:
            raise ProtrendException(detail=f'TFBS with protrend id {instance.tfbs} not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)

        return tfbs


class EffectorHighlightSerializer(serializers.Serializer):
    # properties
    protrend_id = serializers.CharField(read_only=True, help_text=help_text.protrend_id)
    name = serializers.CharField(read_only=True, max_length=250, help_text=help_text.required_name)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_attribute(self, instance):
        effector = papi.get_effector_by_id(instance.effector)
        if effector is None:
            raise ProtrendException(detail=f'Effector with protrend id {instance.effector} not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)

        return effector


# --------------------------------------
# Concrete Serializers
# --------------------------------------
class EffectorSerializer(BaseSerializer):
    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)
    kegg_compounds = serializers.ListField(child=serializers.CharField(required=False),
                                           required=False,
                                           help_text=help_text.kegg_compounds)

    # url
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='effectors-detail',
                                               lookup_field='protrend_id',
                                               lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        return papi.create_effector(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_effector(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_effector(instance)


class EffectorDetailSerializer(EffectorSerializer):
    url = None
    # relationships
    data_source = SourceListSerializer(read_only=True,
                                       child=SourceHighlightSerializer(read_only=True))
    regulator = ManyRelatedSerializer(read_only=True,
                                      child=serializers.HyperlinkedRelatedField(
                                          read_only=True,
                                          view_name='regulators-detail',
                                          lookup_field='protrend_id',
                                          lookup_url_kwarg='protrend_id'))
    regulatory_interaction = ManyRelatedSerializer(read_only=True,
                                                   child=serializers.HyperlinkedRelatedField(
                                                       read_only=True,
                                                       view_name='interactions-detail',
                                                       lookup_field='protrend_id',
                                                       lookup_url_kwarg='protrend_id'))


class EvidenceSerializer(BaseSerializer):
    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)
    description = serializers.CharField(required=False, help_text=help_text.generic_description)

    # url
    url = serializers.HyperlinkedIdentityField(view_name='evidences-detail',
                                               lookup_field='protrend_id', lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        return papi.create_evidence(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_evidence(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_evidence(instance)


class EvidenceDetailSerializer(EvidenceSerializer):
    url = None

    # relationships
    tfbs = ManyRelatedSerializer(read_only=True,
                                 child=serializers.HyperlinkedRelatedField(
                                     read_only=True,
                                     view_name='binding-sites-detail',
                                     lookup_field='protrend_id',
                                     lookup_url_kwarg='protrend_id'))
    regulatory_interaction = ManyRelatedSerializer(read_only=True,
                                                   child=serializers.HyperlinkedRelatedField(
                                                       read_only=True,
                                                       view_name='interactions-detail',
                                                       lookup_field='protrend_id',
                                                       lookup_url_kwarg='protrend_id'))


class GeneSerializer(BaseSerializer):
    # properties
    locus_tag = serializers.CharField(required=True, max_length=50, help_text=help_text.locus_tag)
    uniprot_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.uniprot_accession)
    name = serializers.CharField(required=False, max_length=50, help_text=help_text.gene_name)
    synonyms = serializers.ListField(required=False, child=serializers.CharField(required=False),
                                     help_text=help_text.synonyms)
    function = serializers.CharField(required=False, write_only=True, help_text=help_text.function)
    description = serializers.CharField(required=False, write_only=True, help_text=help_text.description)
    ncbi_gene = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.ncbi_gene)
    ncbi_protein = serializers.IntegerField(required=False, min_value=0, write_only=True,
                                            help_text=help_text.ncbi_protein)
    genbank_accession = serializers.CharField(required=False, write_only=True, max_length=50,
                                              help_text=help_text.genbank_accession)
    refseq_accession = serializers.CharField(required=False, write_only=True, max_length=50,
                                             help_text=help_text.refseq_accession)
    sequence = serializers.CharField(required=False, write_only=True, help_text=help_text.sequence)
    strand = serializers.ChoiceField(required=False, write_only=True, choices=choices.strand,
                                     help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.stop)

    # url
    url = serializers.HyperlinkedIdentityField(view_name='genes-detail',
                                               lookup_field='protrend_id', lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        validated_data = validate_protein_sequence(validated_data)
        return papi.create_gene(**validated_data)

    def update(self, instance, validated_data):
        validated_data = validate_protein_sequence(validated_data, instance)
        return papi.update_gene(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_gene(instance)


class GeneDetailSerializer(GeneSerializer):
    url = None
    function = serializers.CharField(required=False, help_text=help_text.function)
    description = serializers.CharField(required=False, help_text=help_text.description)
    ncbi_gene = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_gene)
    ncbi_protein = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_protein)
    genbank_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.genbank_accession)
    refseq_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.refseq_accession)
    sequence = serializers.CharField(required=False, help_text=help_text.sequence)
    strand = serializers.ChoiceField(required=False, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, help_text=help_text.stop)

    # relationships
    data_source = SourceListSerializer(read_only=True,
                                       child=SourceHighlightSerializer(read_only=True))
    organism = ManyRelatedSerializer(read_only=True,
                                     child=serializers.HyperlinkedRelatedField(
                                         read_only=True,
                                         view_name='organisms-detail',
                                         lookup_field='protrend_id',
                                         lookup_url_kwarg='protrend_id'))
    operon = ManyRelatedSerializer(read_only=True,
                                   child=serializers.HyperlinkedRelatedField(
                                       read_only=True,
                                       view_name='operons-detail',
                                       lookup_field='protrend_id',
                                       lookup_url_kwarg='protrend_id'))
    regulator = ManyRelatedSerializer(read_only=True,
                                      child=serializers.HyperlinkedRelatedField(
                                          read_only=True,
                                          view_name='regulators-detail',
                                          lookup_field='protrend_id',
                                          lookup_url_kwarg='protrend_id'))
    tfbs = ManyRelatedSerializer(read_only=True,
                                 child=serializers.HyperlinkedRelatedField(
                                     read_only=True,
                                     view_name='binding-sites-detail',
                                     lookup_field='protrend_id',
                                     lookup_url_kwarg='protrend_id'))
    regulatory_interaction = ManyRelatedSerializer(read_only=True,
                                                   child=serializers.HyperlinkedRelatedField(
                                                       read_only=True,
                                                       view_name='interactions-detail',
                                                       lookup_field='protrend_id',
                                                       lookup_url_kwarg='protrend_id'))


class OperonSerializer(BaseSerializer):
    # properties inherited from PositionMixInSerializer

    # properties
    operon_db_id = serializers.CharField(required=True, max_length=50, help_text=help_text.operon_db_id)
    name = serializers.CharField(required=False, max_length=50, help_text=help_text.operon_name)
    function = serializers.CharField(required=False, max_length=250, help_text=help_text.operon_function)
    genes = serializers.ListField(required=True, child=serializers.CharField(required=True),
                                  help_text=help_text.operon_genes)
    strand = serializers.ChoiceField(required=False, write_only=True, choices=choices.strand,
                                     help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.stop)

    # url
    url = serializers.HyperlinkedIdentityField(view_name='operons-detail',
                                               lookup_field='protrend_id', lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        for gene_id in validated_data['genes']:
            gene = papi.get_gene_by_id(gene_id)
            if gene is None:
                raise ProtrendException(detail=f'Gene with protrend id {gene_id} not found',
                                        code='get error',
                                        status=status.HTTP_404_NOT_FOUND)
        return papi.create_operon(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_operon(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_operon(instance)


class OperonDetailSerializer(OperonSerializer):
    url = None
    genes = GeneListSerializer(read_only=True, child=GeneHighlightSerializer(read_only=True),
                               help_text=help_text.operon_genes)
    strand = serializers.ChoiceField(required=False, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, help_text=help_text.stop)

    # relationships
    data_source = SourceListSerializer(read_only=True,
                                       child=SourceHighlightSerializer(read_only=True))
    organism = ManyRelatedSerializer(read_only=True,
                                     child=serializers.HyperlinkedRelatedField(
                                         read_only=True,
                                         view_name='organisms-detail',
                                         lookup_field='protrend_id',
                                         lookup_url_kwarg='protrend_id'))
    gene = ManyRelatedSerializer(read_only=True,
                                 child=serializers.HyperlinkedRelatedField(
                                     read_only=True,
                                     view_name='genes-detail',
                                     lookup_field='protrend_id',
                                     lookup_url_kwarg='protrend_id'))


class OrganismSerializer(BaseSerializer):
    # properties
    name = serializers.CharField(required=True, max_length=200, help_text=help_text.organism_name)
    ncbi_taxonomy = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_taxonomy)
    species = serializers.CharField(required=False, max_length=150, help_text=help_text.species)
    strain = serializers.CharField(required=False, max_length=150, help_text=help_text.strain)
    refseq_accession = serializers.CharField(required=False, write_only=True, max_length=50,
                                             help_text=help_text.refseq_accession)
    refseq_ftp = serializers.CharField(required=False, write_only=True, max_length=250,
                                       help_text=help_text.refseq_ftp)
    genbank_accession = serializers.CharField(required=False, write_only=True, max_length=50,
                                              help_text=help_text.genbank_accession)
    genbank_ftp = serializers.CharField(required=False, write_only=True, max_length=250,
                                        help_text=help_text.genbank_ftp)
    ncbi_assembly = serializers.IntegerField(required=False, min_value=0, write_only=True,
                                             help_text=help_text.ncbi_assembly)
    assembly_accession = serializers.CharField(required=False, write_only=True, max_length=50,
                                               help_text=help_text.assembly_accession)

    # url
    url = serializers.HyperlinkedIdentityField(view_name='organisms-detail',
                                               lookup_field='protrend_id', lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        return papi.create_organism(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_organism(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_organism(instance)


class OrganismDetailSerializer(OrganismSerializer):
    url = None
    refseq_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.refseq_accession)
    refseq_ftp = serializers.CharField(required=False, max_length=250, help_text=help_text.refseq_ftp)
    genbank_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.genbank_accession)
    genbank_ftp = serializers.CharField(required=False, max_length=250, help_text=help_text.genbank_ftp)
    ncbi_assembly = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_assembly)
    assembly_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.assembly_accession)

    # relationships
    data_source = SourceListSerializer(read_only=True,
                                       child=SourceHighlightSerializer(read_only=True))
    regulator = ManyRelatedSerializer(read_only=True,
                                      child=serializers.HyperlinkedRelatedField(
                                          read_only=True,
                                          view_name='regulators-detail',
                                          lookup_field='protrend_id',
                                          lookup_url_kwarg='protrend_id'))
    gene = ManyRelatedSerializer(read_only=True,
                                 child=serializers.HyperlinkedRelatedField(
                                     read_only=True,
                                     view_name='genes-detail',
                                     lookup_field='protrend_id',
                                     lookup_url_kwarg='protrend_id'))
    tfbs = ManyRelatedSerializer(read_only=True,
                                 child=serializers.HyperlinkedRelatedField(
                                     read_only=True,
                                     view_name='binding-sites-detail',
                                     lookup_field='protrend_id',
                                     lookup_url_kwarg='protrend_id'))
    regulatory_interaction = ManyRelatedSerializer(read_only=True,
                                                   child=serializers.HyperlinkedRelatedField(
                                                       read_only=True,
                                                       view_name='interactions-detail',
                                                       lookup_field='protrend_id',
                                                       lookup_url_kwarg='protrend_id'))


class PathwaySerializer(BaseSerializer):
    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)
    kegg_pathways = serializers.ListField(required=False, child=serializers.CharField(required=False), allow_empty=True,
                                          help_text=help_text.kegg_pathways)

    # url
    url = serializers.HyperlinkedIdentityField(view_name='pathways-detail',
                                               lookup_field='protrend_id', lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        return papi.create_pathway(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_pathway(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_pathway(instance)


class PathwayDetailSerializer(PathwaySerializer):
    url = None

    # relationships
    data_source = SourceListSerializer(read_only=True,
                                       child=SourceHighlightSerializer(read_only=True))
    regulator = ManyRelatedSerializer(read_only=True,
                                      child=serializers.HyperlinkedRelatedField(
                                          read_only=True,
                                          view_name='regulators-detail',
                                          lookup_field='protrend_id',
                                          lookup_url_kwarg='protrend_id'))
    gene = ManyRelatedSerializer(read_only=True,
                                 child=serializers.HyperlinkedRelatedField(
                                     read_only=True,
                                     view_name='genes-detail',
                                     lookup_field='protrend_id',
                                     lookup_url_kwarg='protrend_id'))


class PublicationSerializer(BaseSerializer):
    # properties
    pmid = serializers.IntegerField(required=True, min_value=0, help_text=help_text.pmid)
    doi = serializers.CharField(required=False, max_length=250, help_text=help_text.doi)
    title = serializers.CharField(required=False, max_length=500, help_text=help_text.title)
    author = serializers.CharField(required=False, max_length=250, help_text=help_text.author)
    year = serializers.IntegerField(required=False, min_value=0, help_text=help_text.year)

    # url
    url = serializers.HyperlinkedIdentityField(view_name='publications-detail',
                                               lookup_field='protrend_id', lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        return papi.create_publication(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_publication(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_publication(instance)


class PublicationDetailSerializer(PublicationSerializer):
    url = None

    # relationships
    tfbs = ManyRelatedSerializer(read_only=True,
                                 child=serializers.HyperlinkedRelatedField(
                                     read_only=True,
                                     view_name='binding-sites-detail',
                                     lookup_field='protrend_id',
                                     lookup_url_kwarg='protrend_id'))
    regulatory_interaction = ManyRelatedSerializer(read_only=True,
                                                   child=serializers.HyperlinkedRelatedField(
                                                       read_only=True,
                                                       view_name='interactions-detail',
                                                       lookup_field='protrend_id',
                                                       lookup_url_kwarg='protrend_id'))


class RegulatorSerializer(BaseSerializer):
    # properties
    locus_tag = serializers.CharField(required=True, max_length=50, help_text=help_text.locus_tag)
    uniprot_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.uniprot_accession)
    name = serializers.CharField(required=False, max_length=50, help_text=help_text.gene_name)
    synonyms = serializers.ListField(required=False, child=serializers.CharField(required=False),
                                     help_text=help_text.synonyms)
    mechanism = serializers.ChoiceField(required=False, choices=choices.mechanism,
                                        help_text=help_text.mechanism)
    function = serializers.CharField(required=False, write_only=True, help_text=help_text.function)
    description = serializers.CharField(required=False, write_only=True, help_text=help_text.description)
    ncbi_gene = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.ncbi_gene)
    ncbi_protein = serializers.IntegerField(required=False, min_value=0, write_only=True,
                                            help_text=help_text.ncbi_protein)
    genbank_accession = serializers.CharField(required=False, write_only=True, max_length=50,
                                              help_text=help_text.genbank_accession)
    refseq_accession = serializers.CharField(required=False, write_only=True, max_length=50,
                                             help_text=help_text.refseq_accession)
    sequence = serializers.CharField(required=False, write_only=True, help_text=help_text.sequence)
    strand = serializers.ChoiceField(required=False, write_only=True, choices=choices.strand,
                                     help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, write_only=True, help_text=help_text.stop)

    # url
    url = serializers.HyperlinkedIdentityField(view_name='regulators-detail',
                                               lookup_field='protrend_id', lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        validated_data = validate_protein_sequence(validated_data)
        return papi.create_regulator(**validated_data)

    def update(self, instance, validated_data):
        validated_data = validate_protein_sequence(validated_data, instance)
        return papi.update_regulator(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_regulator(instance)


class RegulatorDetailSerializer(RegulatorSerializer):
    url = None
    function = serializers.CharField(required=False, help_text=help_text.function)
    description = serializers.CharField(required=False, help_text=help_text.description)
    mechanism = serializers.ChoiceField(required=False, choices=choices.mechanism,
                                        help_text=help_text.mechanism)
    ncbi_gene = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_gene)
    ncbi_protein = serializers.IntegerField(required=False, min_value=0, help_text=help_text.ncbi_protein)
    genbank_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.genbank_accession)
    refseq_accession = serializers.CharField(required=False, max_length=50, help_text=help_text.refseq_accession)
    sequence = serializers.CharField(required=False, help_text=help_text.sequence)
    strand = serializers.ChoiceField(required=False, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, help_text=help_text.stop)

    # relationships
    data_source = SourceListSerializer(read_only=True,
                                       child=SourceHighlightSerializer(read_only=True))
    organism = ManyRelatedSerializer(read_only=True,
                                     child=serializers.HyperlinkedRelatedField(
                                         read_only=True,
                                         view_name='organisms-detail',
                                         lookup_field='protrend_id',
                                         lookup_url_kwarg='protrend_id'))
    effector = ManyRelatedSerializer(read_only=True,
                                     child=serializers.HyperlinkedRelatedField(
                                         read_only=True,
                                         view_name='effectors-detail',
                                         lookup_field='protrend_id',
                                         lookup_url_kwarg='protrend_id'))
    gene = ManyRelatedSerializer(read_only=True,
                                 child=serializers.HyperlinkedRelatedField(
                                     read_only=True,
                                     view_name='genes-detail',
                                     lookup_field='protrend_id',
                                     lookup_url_kwarg='protrend_id'))
    tfbs = ManyRelatedSerializer(read_only=True,
                                 child=serializers.HyperlinkedRelatedField(
                                     read_only=True,
                                     view_name='binding-sites-detail',
                                     lookup_field='protrend_id',
                                     lookup_url_kwarg='protrend_id'))
    regulatory_interaction = ManyRelatedSerializer(read_only=True,
                                                   child=serializers.HyperlinkedRelatedField(
                                                       read_only=True,
                                                       view_name='interactions-detail',
                                                       lookup_field='protrend_id',
                                                       lookup_url_kwarg='protrend_id'))


class RegulatoryFamilySerializer(BaseSerializer):
    # properties
    name = serializers.CharField(required=True, max_length=250, help_text=help_text.required_name)
    mechanism = serializers.ChoiceField(required=False, choices=choices.mechanism,
                                        help_text=help_text.mechanism)
    rfam = serializers.CharField(required=False, write_only=True, max_length=100, help_text=help_text.rfam)
    description = serializers.CharField(required=False, write_only=True, help_text=help_text.generic_description)

    # url
    url = serializers.HyperlinkedIdentityField(view_name='rfams-detail',
                                               lookup_field='protrend_id', lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        return papi.create_rfam(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_rfam(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_rfam(instance)


class RegulatoryFamilyDetailSerializer(RegulatoryFamilySerializer):
    url = None
    rfam = serializers.CharField(required=False, max_length=100, help_text=help_text.rfam)
    description = serializers.CharField(required=False, help_text=help_text.generic_description)

    # relationships
    data_source = SourceListSerializer(read_only=True,
                                       child=SourceHighlightSerializer(read_only=True))
    regulator = ManyRelatedSerializer(read_only=True,
                                      child=serializers.HyperlinkedRelatedField(
                                          read_only=True,
                                          view_name='regulators-detail',
                                          lookup_field='protrend_id',
                                          lookup_url_kwarg='protrend_id'))


class RegulatoryInteractionSerializer(BaseSerializer):
    # properties
    organism = serializers.CharField(required=True, max_length=100, help_text=help_text.organism_id)
    regulator = serializers.CharField(required=True, max_length=100, help_text=help_text.regulator_id)
    gene = serializers.CharField(required=True, max_length=100, help_text=help_text.gene_id)
    tfbs = serializers.CharField(required=False, max_length=100, help_text=help_text.tfbs_id)
    effector = serializers.CharField(required=False, max_length=100, help_text=help_text.effector_id)
    regulatory_effect = serializers.ChoiceField(required=True, choices=choices.regulatory_effect,
                                                help_text=help_text.regulatory_effect)

    # url
    url = serializers.HyperlinkedIdentityField(view_name='interactions-detail',
                                               lookup_field='protrend_id', lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        return papi.create_interaction(**validated_data)

    def update(self, instance, validated_data):
        return papi.update_interaction(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_interaction(instance)


class RegulatoryInteractionDetailSerializer(RegulatoryInteractionSerializer):
    url = None
    organism = OrganismHighlightSerializer(read_only=True)
    regulator = RegulatorHighlightSerializer(read_only=True)
    gene = GeneHighlightSerializer(read_only=True)
    tfbs = TFBSHighlightSerializer(read_only=True)
    effector = EffectorHighlightSerializer(read_only=True)

    # relationships
    data_source = SourceListSerializer(read_only=True,
                                       child=SourceHighlightSerializer(read_only=True))
    evidence = ManyRelatedSerializer(read_only=True,
                                     child=serializers.HyperlinkedRelatedField(
                                         read_only=True,
                                         view_name='evidences-detail',
                                         lookup_field='protrend_id',
                                         lookup_url_kwarg='protrend_id'))
    publication = ManyRelatedSerializer(read_only=True,
                                        child=serializers.HyperlinkedRelatedField(
                                            read_only=True,
                                            view_name='publications-detail',
                                            lookup_field='protrend_id',
                                            lookup_url_kwarg='protrend_id'))
    data_organism = ManyRelatedSerializer(read_only=True,
                                          child=serializers.HyperlinkedRelatedField(
                                              read_only=True,
                                              view_name='organisms-detail',
                                              lookup_field='protrend_id',
                                              lookup_url_kwarg='protrend_id'))
    data_effector = ManyRelatedSerializer(read_only=True,
                                          child=serializers.HyperlinkedRelatedField(
                                              read_only=True,
                                              view_name='effectors-detail',
                                              lookup_field='protrend_id',
                                              lookup_url_kwarg='protrend_id'))
    data_regulator = ManyRelatedSerializer(read_only=True,
                                           child=serializers.HyperlinkedRelatedField(
                                               read_only=True,
                                               view_name='regulators-detail',
                                               lookup_field='protrend_id',
                                               lookup_url_kwarg='protrend_id'))
    data_gene = ManyRelatedSerializer(read_only=True,
                                      child=serializers.HyperlinkedRelatedField(
                                          read_only=True,
                                          view_name='genes-detail',
                                          lookup_field='protrend_id',
                                          lookup_url_kwarg='protrend_id'))
    data_tfbs = ManyRelatedSerializer(read_only=True,
                                      child=serializers.HyperlinkedRelatedField(
                                          read_only=True,
                                          view_name='binding-sites-detail',
                                          lookup_field='protrend_id',
                                          lookup_url_kwarg='protrend_id'))


class TFBSSerializer(BaseSerializer):
    # properties
    organism = serializers.CharField(required=True, max_length=100, help_text=help_text.organism_id)
    sequence = serializers.CharField(required=True, help_text=help_text.tfbs_sequence)
    strand = serializers.ChoiceField(required=True, choices=choices.strand, help_text=help_text.strand)
    start = serializers.IntegerField(required=False, min_value=0, help_text=help_text.start)
    stop = serializers.IntegerField(required=False, min_value=0, help_text=help_text.stop)
    length = serializers.IntegerField(required=True, min_value=0, help_text=help_text.length)

    # url
    url = serializers.HyperlinkedIdentityField(view_name='binding-sites-detail',
                                               lookup_field='protrend_id', lookup_url_kwarg='protrend_id')

    def create(self, validated_data):
        validated_data = validate_dna_sequence(validated_data)
        return papi.create_binding_site(**validated_data)

    def update(self, instance, validated_data):
        validated_data = validate_dna_sequence(validated_data, instance)
        return papi.update_binding_site(instance, **validated_data)

    @staticmethod
    def delete(instance):
        return papi.delete_binding_site(instance)


class TFBSDetailSerializer(TFBSSerializer):
    url = None
    organism = OrganismHighlightSerializer(read_only=True)

    # relationships
    data_source = SourceListSerializer(read_only=True,
                                       child=SourceHighlightSerializer(read_only=True))
    evidence = ManyRelatedSerializer(read_only=True,
                                     child=serializers.HyperlinkedRelatedField(
                                         read_only=True,
                                         view_name='evidences-detail',
                                         lookup_field='protrend_id',
                                         lookup_url_kwarg='protrend_id'))
    publication = ManyRelatedSerializer(read_only=True,
                                        child=serializers.HyperlinkedRelatedField(
                                            read_only=True,
                                            view_name='publications-detail',
                                            lookup_field='protrend_id',
                                            lookup_url_kwarg='protrend_id'))
    data_organism = ManyRelatedSerializer(read_only=True,
                                          child=serializers.HyperlinkedRelatedField(
                                              read_only=True,
                                              view_name='organisms-detail',
                                              lookup_field='protrend_id',
                                              lookup_url_kwarg='protrend_id'))
    regulator = ManyRelatedSerializer(read_only=True,
                                      child=serializers.HyperlinkedRelatedField(
                                          read_only=True,
                                          view_name='regulators-detail',
                                          lookup_field='protrend_id',
                                          lookup_url_kwarg='protrend_id'))
    gene = ManyRelatedSerializer(read_only=True,
                                 child=serializers.HyperlinkedRelatedField(
                                     read_only=True,
                                     view_name='genes-detail',
                                     lookup_field='protrend_id',
                                     lookup_url_kwarg='protrend_id'))
    regulatory_interaction = ManyRelatedSerializer(read_only=True,
                                                   child=serializers.HyperlinkedRelatedField(
                                                       read_only=True,
                                                       view_name='interactions-detail',
                                                       lookup_field='protrend_id',
                                                       lookup_url_kwarg='protrend_id'))
