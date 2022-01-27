from neomodel import StringProperty, ArrayProperty, RelationshipTo, One, IntegerProperty

from .base import BaseNode
from .relationships import BASE_REL_TYPE, SourceRelationship, BaseRelationship, SOURCE_REL_TYPE
from constants import help_text, choices


class Operon(BaseNode):
    # properties
    operon_db_id = StringProperty(required=True, unique_index=True, max_length=50, help_text=help_text.operon_db_id)
    operon_db_id_factor = StringProperty(required=True, unique_index=True, max_length=50,
                                         help_text=help_text.operon_db_id)
    name = StringProperty(max_length=50, help_text=help_text.operon_name)
    function = StringProperty(max_length=250, help_text=help_text.operon_function)
    genes = ArrayProperty(StringProperty(), required=True, help_text=help_text.operon_genes)
    strand = StringProperty(choices=choices.strand, help_text=help_text.strand)
    start = IntegerProperty(help_text=help_text.start)
    stop = IntegerProperty(help_text=help_text.stop)

    # relationships
    data_source = RelationshipTo('.source.Source', SOURCE_REL_TYPE, cardinality=One, model=SourceRelationship)
    evidence = RelationshipTo('.evidence.Evidence', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    publication = RelationshipTo('.publication.Publication', BASE_REL_TYPE, model=BaseRelationship)
    organism = RelationshipTo('.organism.Organism', BASE_REL_TYPE, cardinality=One, model=BaseRelationship)
    gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)
